import { GoogleGenAI, ApiError } from "@google/genai";
import fs from "node:fs";
import path from "node:path";

// Overridable without a code change, since which models the free tier serves moves.
const MODEL = process.env.GEMINI_MODEL ?? "gemini-2.5-flash";
const MAX_TOKENS = 700;
const MAX_QUESTION_CHARS = 500;
const MAX_HISTORY_TURNS = 12;
const KNOWLEDGE_CHAR_CAP = 18000;
const RATE_WINDOW_MS = 60_000;
const RATE_MAX_PER_WINDOW = 6;

const SYSTEM_RULES = [
  "너는 김유신의 포트폴리오 페이지에 있는 안내 에이전트다. 아래 포트폴리오 전문만을 근거로 답한다.",
  "규칙:",
  '(1) 본문에 없는 사실은 만들지 않고 "포트폴리오에 없는 내용"이라고 말한다.',
  "(2) 수치는 기록 대조 전 초안 기준임을 필요할 때 밝힌다.",
  "(3) CorePress는 교육용 POC이며 상용 구축 경험이 아니다.",
  "(4) 계약 완료 고객사와 미팅 단계(삼성·현대·SK)를 섞지 않는다.",
  "(5) 과장 없이 담담하게, 존댓말로, 3~5문장 이내로 답한다.",
  "(6) 포트폴리오와 무관한 요청(번역, 코드 작성, 일반 질문 등)은 거절하고 커리어 질문으로 안내한다.",
  "",
  "=== 포트폴리오 전문 ===",
].join("\n");

// The page is the single source of truth for what the agent knows, so the text is
// read back out of it rather than kept as a second copy that drifts.
let knowledgeCache: string | null = null;

function knowledge(): string {
  if (knowledgeCache !== null) return knowledgeCache;

  // Resolve from this module: Vercel may run with the repository root as cwd.
  const html = fs.readFileSync(path.join(__dirname, "..", "index.html"), "utf8");
  const body = html
    .replace(/<script[\s\S]*?<\/script>/gi, " ")
    .replace(/<style[\s\S]*?<\/style>/gi, " ");

  const blocks: string[] = [];
  for (const match of body.matchAll(/<(section|footer)\b[\s\S]*?<\/\1>/gi)) {
    const text = match[0]
      .replace(/<[^>]+>/g, " ")
      .replace(/&(nbsp|ensp|emsp|thinsp);/g, " ")
      .replace(/&amp;/g, "&")
      .replace(/&lt;/g, "<")
      .replace(/&gt;/g, ">")
      .replace(/&quot;/g, '"')
      .replace(/&#(\d+);/g, (_, d: string) => String.fromCharCode(Number(d)))
      .replace(/\s+/g, " ")
      .trim();
    if (text) blocks.push(text);
  }

  knowledgeCache = blocks.join("\n\n").slice(0, KNOWLEDGE_CHAR_CAP);
  return knowledgeCache;
}

// Best-effort only: serverless instances each hold their own counter, so this slows
// casual abuse rather than preventing it. The free tier's own quota is the real bound.
const hits = new Map<string, number[]>();

function rateLimited(ip: string): boolean {
  const now = Date.now();
  const recent = (hits.get(ip) ?? []).filter((t) => now - t < RATE_WINDOW_MS);
  recent.push(now);
  hits.set(ip, recent);
  if (hits.size > 5000) hits.clear();
  return recent.length > RATE_MAX_PER_WINDOW;
}

function allowedOrigin(origin: string | undefined): boolean {
  const allowList = (process.env.ALLOWED_ORIGINS ?? "")
    .split(",")
    .map((s: string) => s.trim())
    .filter(Boolean);
  if (allowList.length === 0) return true;
  return !!origin && allowList.includes(origin);
}

const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY });

export default async function handler(req: any, res: any) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "method_not_allowed" });
  }
  if (!allowedOrigin(req.headers.origin)) {
    return res.status(403).json({ error: "forbidden_origin" });
  }

  const ip =
    (req.headers["x-forwarded-for"] ?? "").toString().split(",")[0].trim() ||
    "unknown";
  if (rateLimited(ip)) {
    return res.status(429).json({ error: "rate_limited" });
  }

  const body = typeof req.body === "string" ? JSON.parse(req.body) : req.body;
  const incoming = Array.isArray(body?.messages) ? body.messages : [];

  // Only role and text survive from the client. The system prompt and the knowledge
  // base are assembled here so a crafted request cannot repurpose the endpoint.
  const contents = incoming
    .slice(-MAX_HISTORY_TURNS)
    .filter(
      (m: any) =>
        (m?.role === "user" || m?.role === "assistant") &&
        typeof m?.content === "string" &&
        m.content.trim(),
    )
    .map((m: any) => ({
      role: m.role === "assistant" ? "model" : "user",
      parts: [{ text: m.content.slice(0, MAX_QUESTION_CHARS) }],
    }));

  if (!contents.length || contents[contents.length - 1].role !== "user") {
    return res.status(400).json({ error: "bad_request" });
  }

  try {
    const response = await ai.models.generateContent({
      model: MODEL,
      contents,
      config: {
        systemInstruction: SYSTEM_RULES + "\n" + knowledge(),
        maxOutputTokens: MAX_TOKENS,
      },
    });

    const text = response.text?.trim();
    return res.status(200).json({ text: text || "답변을 생성하지 못했습니다." });
  } catch (error) {
    if (error instanceof ApiError) {
      // 429 is the free tier's own quota, which the visitor cannot do anything about
      // beyond waiting — surface it as rate limiting rather than a generic failure.
      if (error.status === 429) {
        return res.status(429).json({ error: "rate_limited" });
      }
      console.error(`Gemini API error ${error.status}: ${error.message}`);
      return res.status(502).json({ error: "upstream_error" });
    }
    console.error(error);
    return res.status(500).json({ error: "server_error" });
  }
}

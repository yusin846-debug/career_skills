#!/usr/bin/env python3
"""Render the resume body of each lane file to PDF.

The lane files carry working notes alongside the resume — per-company tailoring,
risk handling, submission gates, inline reviewer comments. Only the part between
the name heading and the first following section is the resume; everything after
it must never reach a recruiter.
"""

import html
import re
import subprocess
import sys
from pathlib import Path

import markdown

HERE = Path(__file__).parent
OUT = HERE / "pdf"

LANES = [
    ("05-resume-gtm.md", "김유신_이력서_GTM_토스플레이스", "ko"),
    ("01-resume-customer-success.md", "KimYushin_Resume_CustomerSuccess", "en"),
    ("02-resume-sales-ops.md", "KimYushin_Resume_SalesOps", "en"),
    ("03-resume-sdr.md", "KimYushin_Resume_SDR", "en"),
]

NAME_HEADING = re.compile(r"^## (KIM YUSHIN|김유신)\s*$", re.M)
NEXT_SECTION = re.compile(r"^## ", re.M)


def resume_body(path: Path) -> str:
    text = path.read_text(encoding="utf-8")

    start = NAME_HEADING.search(text)
    if not start:
        sys.exit(f"{path.name}: no name heading found")

    after = NEXT_SECTION.search(text, start.end())
    body = text[start.start(): after.start() if after else len(text)]

    # Reviewer notes are written as HTML comments, which would otherwise survive
    # into the rendered document as invisible-but-present text.
    body = re.sub(r"<!--.*?-->", "", body, flags=re.S)

    leftover = re.findall(r"\[\[[^\]]+\]\]", body)
    if leftover:
        sys.exit(f"{path.name}: unfilled placeholder in resume body: {leftover[0]}")

    return body.strip()


CSS = """
@page { size: A4; margin: 11mm 13mm; }
* { box-sizing: border-box; }
body {
  font-family: "Noto Sans CJK KR", "Noto Sans", sans-serif;
  font-size: 9.1pt; line-height: 1.5; color: #16181a; margin: 0;
  word-break: keep-all;
}
h2 {
  font-size: 20pt; font-weight: 700; letter-spacing: -0.03em;
  margin: 0 0 2mm; padding: 0;
}
.contact {
  font-size: 8.6pt; color: #4e5359; margin: 0 0 4mm;
  padding-bottom: 3mm; border-bottom: 1.2pt solid #16181a;
}
.contact a { color: #125a63; text-decoration: none; }
h3 {
  font-size: 8.6pt; font-weight: 700; letter-spacing: 0.14em;
  text-transform: uppercase; color: #125a63;
  margin: 3.8mm 0 1.8mm; padding-bottom: 1mm;
  border-bottom: 0.5pt solid #d6d1c7;
}
h3:first-of-type { margin-top: 3mm; }
p { margin: 0 0 1.5mm; }
strong { font-weight: 700; color: #000; }
em { color: #4e5359; font-style: normal; font-size: 8.4pt; }
ul { margin: 0 0 2.2mm; padding-left: 3.8mm; }
li { margin-bottom: 1.3mm; }
li::marker { color: #8b9095; }
code {
  font-family: "Noto Sans Mono CJK KR", monospace;
  font-size: 8.6pt; background: #f1eee8; padding: 0 1mm; border-radius: 1mm;
}
/* Company / role lines run as consecutive bold-then-italic paragraphs. */
p > strong:only-child { font-size: 10.4pt; }
hr { border: none; border-top: 0.5pt solid #e7e3db; margin: 4mm 0; }
a { color: #125a63; }
"""


def build(md_name: str, out_stem: str, lang: str) -> Path:
    body_md = resume_body(HERE / md_name)

    # The name heading becomes the document title; the lines under it are contact
    # details and need to render as one block rather than a paragraph of prose.
    lines = body_md.split("\n")
    name = lines[0].replace("## ", "").strip()
    rest = "\n".join(lines[1:]).strip()

    contact_md, _, remainder = rest.partition("\n---\n")
    contact_html = markdown.markdown(contact_md.strip()).replace("<p>", "").replace("</p>", "")
    body_html = markdown.markdown(remainder.strip(), extensions=["tables", "sane_lists"])

    doc = f"""<!doctype html><html lang="{lang}"><head><meta charset="utf-8">
<title>{html.escape(out_stem)}</title><style>{CSS}</style></head><body>
<h2>{html.escape(name)}</h2>
<div class="contact">{contact_html}</div>
{body_html}
</body></html>"""

    OUT.mkdir(exist_ok=True)
    src = OUT / f"{out_stem}.html"
    pdf = OUT / f"{out_stem}.pdf"
    src.write_text(doc, encoding="utf-8")

    subprocess.run(
        ["/opt/pw-browsers/chromium", "--headless",
         "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
         f"--print-to-pdf={pdf}", src.as_uri()],
        check=True, capture_output=True,
    )
    src.unlink()
    return pdf


if __name__ == "__main__":
    for md_name, stem, lang in LANES:
        out = build(md_name, stem, lang)
        print(f"{out.name}  ({out.stat().st_size // 1024} KB)")

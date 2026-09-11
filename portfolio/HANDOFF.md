# 인계 노트 — 김유신 포트폴리오

## 프로젝트 개요
- 소스: GitHub `yusin846-debug/career_skills`, 브랜치 `claude/portfolio-planning-riuefd`
- 원본: `portfolio.html` + `portfolio-review-brief.md` (작성 지침·검증 원칙 담긴 브리프)
- 이 프로젝트의 `portfolio.html`이 수정본. **저장소에는 아직 커밋 안 함** — 사용자가 확인 후 직접 반영 예정
- 사용자: 김유신. Planz Coffee Sales Director(2016–2026, 창업자) → 글로벌 B2B SaaS·CRM·데이터·클라우드로 전직 준비 중 (Salesforce/Agentforce AE, Snowflake, AWS 관심 — 특정 회사명은 페이지에 박지 않기로 함)

## 브랜드 무드
- 레퍼런스: IREN(iren.com) + 사용자 링크드인 배너 — 그린→틸→네이비 그라디언트, 세리프 강조
- 라이트 테마 고정, 글래스모피즘(카드·툴·인덱스·챗 패널 반투명+blur, body::before 앰비언트 글로우)
- 히어로: 힉스필드(Higgsfield MCP) 생성 에셋 사용
  - 스틸(배경/포스터): hf_20260910_110655_49ec0a60-...png (CloudFront URL, hero CSS에)
  - 대안 스틸: hf_20260910_110654_122ed747-...png (hero CSS 주석에)
  - 물결 영상(5s 루프, kling3_0): hf_20260910_112325_6b0606b6-...mp4 — 루프 경계는 페이드아웃/인으로 마스킹(timeupdate 리스너)
  - ⚠ 전부 외부 URL — 아티팩트 게시 시 CSP에 막힐 수 있음. 이미지들은 data URI로 인라인 필요, mp4는 용량상 불가(스틸+CSS 애니메이션 폴백으로 동작)

## 주요 구조
- 히어로: 목표 한 줄("데이터와 시스템 위에서… B2B SaaS·CRM·데이터·클라우드 조직") + 영상 배경 + heroDrift CSS 광원
- 좌측 고정 인덱스(01 Archive ~ 05 Now), 스크롤스파이, <900px 숨김
- 아카이브: 카테고리 필터(전체/Sales/GTM/Product/BM/AX/Fun & Creativity/Life), 스태거 entryIn 애니메이션. 시간순 정렬 토글은 제거함(연도 근거 부족)
- 카드 일부에 Method 01~04 참조 태그(.mref)
- 우측 하단 "Ask me anything" 챗봇: window.claude.complete 연동, 근거는 페이지 전체 텍스트(section/footer 추출, 18000자 캡). 시스템 프롬프트에 브리프 원칙(과장 금지, CorePress=교육용 POC, 계약/미팅 분리, 페이지에 없는 건 없다고 답변) 포함

## 콘텐츠 원칙 (브리프 유래 — 위반 금지)
- 수치는 기억 기준 초안, 상단 notice 유지 중(검증 후 제거 예정)
- 계약 성사처와 미팅 단계(삼성·현대·SK)를 섞지 않기 — 단, 이건 표기 지침이지 본문에 쓰는 문장 아님
- CorePress는 교육용 POC(MVP 사유: 팀 커뮤니케이션), 상용 아님
- 고른햇살 "21억→30억"은 카드 메타에서 제거됨, 본문 맥락에만 존재
- 사용자가 준 텍스트는 임의 수정 금지, 수치·명단은 사용자 확인 없이 못 고침

## 미완 / 다음 작업
1. **AX 카테고리 카드 0개** — 사용자가 글 써오기로 함(어제 기준 "내일"=오늘). 카드 추가 시 `data-cat="ax"` + 버튼 카운트 갱신 (전체 카운트 17도)
2. "음료 매출 4위" 분모 미확인 — 사용자 수치 필요
3. 카드 요약(en-s) 압축, 헤드라인 "~했습니다" 종결 다양화 — 리뷰에서 지적했으나 미착수
4. 깃 evidence-ledger를 챗봇 지식으로 넣으려면 페이지에 숨김 데이터로 임베드 필요
5. 게시 시 이미지 data URI 인라인 작업

## 편집 주의
- `.en` 카드 스타일은 `.entries > .en`으로 스코프됨(히어로의 .en 텍스트와 충돌 방지)
- 사용자 직접 편집 이력 있음 — `__om-edit-overrides` 스타일 블록 확인 후 편집
- 사용자 톤: 반말, 빠른 반복 수정 선호, 간결한 응답 선호

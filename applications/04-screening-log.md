# 지원 목록 요건 스크리닝 로그

**실행일**: 2026-09-10
**계기**: 학력이 **수료(학위 없음)** 로 확정되면서 지원 자격 자체를 재검증할 필요 발생

---

## 검증 제약 — 먼저 밝힘

이 세션의 네트워크 프록시가 **대부분의 채용 도메인을 차단**한다. 직접 열지 못한 곳은
검색 결과(2차 출처)로만 확인했으며, 아래에 `[검색]`으로 표시한다.

**차단 확인된 도메인**: `careers.adobe.com`, `adobe.wd5.myworkdayjobs.com`,
`www.careers.philips.com`, `www.amazon.jobs`, `toss.im`

> 따라서 **"전수 검증 완료"가 아니다.** 확실한 탈락 사유가 확인된 건만 삭제했고,
> 나머지는 확인 상태를 그대로 남긴다.

---

## 삭제 (3건) — 확실한 탈락 사유

### 1. Siemens Digital Industries — Genesis Program, Associate Sales Rep `[검색]`
**삭제 사유 3중 결격:**
- **한국 채용이 아님.** 실제 근무지는 Blue Ash·Mason(OH), Oakville(ON). 20주 교육도 Milford, OH.
- `recent college graduates with a bachelor's degree` — 학위 요구 + 신규 졸업자 대상.
  10년 경력자는 대상 자체가 아니다.
- `authorization to work in the US without sponsorship` + 최소 2회 재배치 요구.

> 애초에 "서울"로 기록된 것이 오류였다. Selective 판정 70점도 근거가 없었다.

### 2. Amazon — AWS Sales Operations Business Analyst (Job ID 10507624)
**삭제 사유:** 이벤트 설명에 이미 `학사 학위 증빙 여부 확인: Basic Qualification 명시`라고
적혀 있었다. 아마존의 **Basic Qualifications는 하드 스크리닝 기준**이며 통과 못 하면
서류가 열리지 않는다. 수료로는 충족 불가.

### 3. Amazon — Account Manager, Global Selling Korea (Job ID 10402171) `[검색]`
**삭제 사유:** Basic Qualifications에 `Bachelor's degree` 명시. 위와 동일 구조.

> **★ 패턴:** 아마존·AWS는 직무·지역과 무관하게 Basic Qualifications에 학사를 넣는다.
> 앞으로 아마존 계열 공고는 **기본적으로 제외**하고, 개별 공고에 `or equivalent experience`가
> 명시된 경우에만 예외로 넣는다.

---

## 유지 확정 — 학위 요건 통과

| 회사 | 직무 | 근거 | 상태 |
|---|---|---|---|
| Microsoft | Customer Success Account Manager | `Bachelor's ... OR equivalent experience` 확인 | `[검색]` 통과 |
| ServiceNow | Sr Manager, Sales Operations | 공고에 학위 요건 없음. 경력 요건만 명시 | `[검색]` 통과 |
| Datadog | Customer Success Manager | 학위 요건 없음. `5+ years customer account-facing`. 공고에 "모든 요건을 첫날부터 갖추지 않아도 된다"는 문구 존재 | `[검색]` 통과 |

---

## 확인 실패 — 도메인 차단으로 미검증

| 회사 | 직무 | 필요한 확인 |
|---|---|---|
| Adobe | Manager, ICX Sales & CS (R166234) | 학위 요건 유무 |
| Adobe | Sr Manager, CS & TAM Korea (R157816) | 학위 요건, 팀 관리 요건 |
| Philips | Sales Excellence Manager Korea (540845) | 학위 요건 |

> **유신님이 직접 열어서 Qualifications 부분만 붙여주시면** 즉시 판정 가능합니다.

---

## ★ 신규 추가 — 토스플레이스 Enterprise Marketing Manager (83점, 전체 1위)

공고 본문을 사용자가 직접 전달받아 판정 완료. **현재 목록 전체에서 가장 높은 점수**이며,
2위 Microsoft(74)와 9점 차이다.

### 자격 요건 — 전부 통과
- **학력 요건 없음.** 수료 여부가 문제되지 않는다. 아마존·Siemens를 탈락시킨 사유가 여기선 무관.
- 연차 요건 명시 없음. 과잉스펙 리스크도 낮다.
- 한국 기업 → 영어 리스크 없음.

### 점수 산출 (6개 축)

| 축 | 가중 | 평가 | 근거 |
|---|---|---|---|
| 직무 적합성 | 25% | 85 | JD가 요구하는 7개 항목 중 7개 모두 실제 케이스로 대응 |
| 증거 강도 | 20% | 95 | 항목마다 실명 딜이 붙는다. 목록 중 최고 |
| 전환 마찰 | 15% | 85 | 오프라인 설치형 B2B, 바이어가 총무·시설·인사 → 무인카페와 동일 구조 |
| 조직 학습 | 15% | 75 | 방법론 강한 조직이나 글로벌 매트릭스는 아님 |
| 장기 교환가치 | 15% | 70 | 브랜드 강함. 단 핀테크/결제는 CRM/AX 방향과 살짝 다름 |
| 지원 현실성 | 10% | 85 | 요건 장벽 없음 + 집중채용 |

**가중 합계 ≈ 83**

### JD ↔ 증거 대응 (1:1)

| JD 요구 | 대응 증거 |
|---|---|
| 고객 선정과 문제 정의 과정 | 자이·CJ·두산테스나 — 전부 "표면 요청 ≠ 실제 문제" |
| 가설 수정 → 비즈니스 결과 변화 | 현대차 ESG 패배 → 제품 수정 → 아모레퍼시픽·LG전자 수주 |
| PoC·계약 단계 변화 추적 | 두산테스나 1년 POC → 평택·안성 전면 대체 |
| 캠페인 기획→실행→성과 전 과정 주도 | 6개 채널 단독 운영. 리드→미팅 30%, 리드→매출 10–20% |
| **효과적 방식을 확장 가능하게 구조화** | **자이 법적 근거 → SK D&D 경쟁 장벽 재사용** ← 원장의 핵심 패턴 |
| 세일즈 머티리얼 직접 기획·작성 | 제안서 + 디자인 직접 수행(Figma/Adobe) |
| 복잡한 이해관계자 공략 | CJ 멀티스레딩 → 경제적 구매자(재무) 겨냥 |

> **디자인 역량이 처음으로 리드 자산이 되는 공고다.** 원장은 B2B 세일즈 지원에서
> 디자인을 앞세우지 말라고 규정했으나, 이 JD는 세일즈 머티리얼 직접 작성을
> 필수 요건으로 명시한다. 이 건에 한해 예외 적용.

### ⏰ 날짜 — 성격 구분 주의
`9/14까지 지원 시 특별 베네핏` — **공고 마감일이 아니라 혜택 기한이다.**
(이력서 가이드 제공 + 인터뷰 완료자 전원 피드백)
이 프로젝트의 "가짜 마감일" 전례가 있으므로 마감으로 표기하지 않는다.
다만 실재하는 날짜이므로 9/11 최우선 슬롯에 배치했다.

### ⚠️ 필요 작업
타이틀이 Marketing이라 **기존 이력서 3종이 모두 맞지 않는다.**
`applications/05-resume-gtm.md` (BD/GTM 레인) 신규 작성 필요.
단 JD 내용은 캠페인 마케팅이 아니라 GTM·제안 설계이므로 실제 업무는 유신님이 해온 일이다.

### 일정 반영
- 토스플레이스 → **9/11 09:00** (최우선 슬롯, 90분 배정)
- 기존 Slack AE(72) → 9/11 17:00으로 이동

---

## 삭제 (13건) — 55~58점 Stretch 구간 전수 정리

**사용자 결정.** 결격이 아니라 **확률 판단**이다. 이 구간은 대부분
`7~10년 엔터프라이즈 SaaS 세일즈` 직접 경력을 요구하는데, 유신님의 6년은
미드마켓·자체 브랜드 영업이라 성격이 다르다. 2주 집중 캠페인에서 상위 점수 건에
시간을 몰아주기 위해 정리한다.

| 날짜 | 회사 · 직무 | 점수 |
|---|---|---|
| 9/21 | Cloudflare Sr Territory AE | 58 |
| 9/21 | Elastic Sr Named AE Korea | 58 |
| 9/22 | NetApp Google Cloud Sales Specialist | 58 |
| 9/22 | Microsoft Strategic AE (Samsung) | 55 |
| 9/22 | GE Vernova Sr Sales Mgr, Grid Software | 58 |
| 9/22 | Akamai Sr Security Sales Specialist | 57 |
| 9/22 | Thermo Fisher Commercial Leader Korea | 56 |
| 9/22 | Autodesk Named Account Sales Exec | 58 |
| 9/23 | Nutanix Sr Services Sales Mgr | 56 |
| 9/23 | GitLab Sr Strategic Enterprise AE | 58 |
| 9/23 | Okta Account Executive Korea | 57 |
| 9/23 | NVIDIA AM, Automotive | 55 |
| 9/23 | NVIDIA Sr AM, Consumer Sales | 56 |

**유지한 경계선 (59~60점)** — 삭제 기준 밖이라 남김:
Nutanix Sr Commercial AM(59) · Workday AE(60) · Veeva Enterprise AE(60) ·
Workato Enterprise AE(60) · Autodesk Manufacturing Sales Exec(60) · Dyson Sales AM(60)

> ⚠️ **일정 공백 발생:** 9/22는 2건, 9/23은 1건만 남았다. 마지막 이틀이 사실상 비었으므로
> 앞 구간을 뒤로 분산하거나 캠페인을 9/21에 종료하는 편이 낫다.

---

## 삭제 총계: 16건

| 구분 | 건수 |
|---|---|
| 학위·자격 결격 | 3 |
| 55~58점 Stretch 정리 | 13 |

---

## 남은 작업

- [ ] Adobe 2건 · Philips 1건 · Toss 1건 — 공고 본문 확보 후 학위 요건 판정
- [ ] 지원서 학력란 작성 표준 문구 확정 (`Biology, 2013–2018, coursework completed`)
- [ ] 9/22–9/23 공백 처리 — 앞 구간 재배치 또는 캠페인 조기 종료
- [ ] 남은 Stretch 중 점수 미표기 건(Apple Channel Sales, Notion Consultant,
      Palo Alto, Google Cloud Partner, Snowflake Partner Dev, Atlassian) 점수 부여 후 재판정

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
| Toss | (job_id 7971642003) | 전체 요건 — 유신님이 내용 전달 필요 |

> **유신님이 직접 열어서 Qualifications 부분만 붙여주시면** 즉시 판정 가능합니다.
> 참고로 토스는 통상 학력 요건을 두지 않는 편이나, 확인 없이 단정하지 않는다.

---

## 별도 쟁점 — 학위가 아니라 **경력 연차** 미달군

삭제하지 않았으나, 다수 공고가 **7~10년의 "엔터프라이즈 SaaS 세일즈"** 직접 경력을
요구한다. 유신님의 6년은 미드마켓·자체 브랜드 영업이라 성격이 다르다.

| 공고 | 요구 | 점수 |
|---|---|---|
| GitLab Strategic AE | 7년+ 엔터프라이즈 SaaS | 58 |
| Okta AE Korea | 7년+ 엔터프라이즈 SaaS + C-Level | 57 |
| Nutanix Sr Services Sales Mgr | 7–10년+ 엔터프라이즈 서비스 세일즈 | 56 |
| Google Cloud Partner Sales Mgr | 8년 채널 세일즈/파트너 관리 | Stretch |
| ServiceNow Sr Mgr Sales Ops | 8년+ Sales Ops | 72 |
| Microsoft Strategic AE (Samsung) | 최고 레벨 | 55 |
| Elastic Sr Named AE | Senior Named | 58 |

> 이건 **결격이 아니라 확률 문제**다. 점수 55~58 구간은 이미 Stretch로 분류돼 있으므로
> 판정 체계는 정상 작동했다. 다만 2주 집중 캠페인에서 이 구간에 시간을 쓸 것인지는
> 별도 판단이 필요하다.

---

## 남은 작업

- [ ] Adobe 2건 · Philips 1건 · Toss 1건 — 공고 본문 확보 후 학위 요건 판정
- [ ] 지원서 학력란 작성 표준 문구 확정 (`Biology, 2013–2018, coursework completed`)
- [ ] 55~58점 Stretch 구간 유지 여부 결정

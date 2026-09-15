# Portfolio session handoff — 2026-09-15
Repository: yusin846-debug/career_skills. Vercel root: portfolio. Main deploys automatically.
Live: https://yushin-portfolio.vercel.app/
CorePress article: https://yushin-portfolio.vercel.app/corepress.html
Read latest remote files before modifying; local older clones have uncommitted older changes.

## Positioning and content
User wants design-savvy, AI-fluent integrated B2B marketing/sales positioning. Keep factual, precise personal contributions and collaboration.
Hero: B2B MARKETING · SALES · CRM; 고객을 이해하고, 디자인과 AI로 마케팅부터 세일즈까지 연결합니다.
Six teal/porcelain 3D tool icons; four small glass social marks at hero upper-right and footer. Y-glass favicon set.
CJ before/after cafe photos, Tesna co-installation/interior photos, SK D&D AI-brightened image with explicit AI caption and Brunch /35 lead-source link, DM/inbound/ad correspondence/exhibition materials, residential lounge photo added.
Product stories rewritten around revenue opportunity, voluntary learning/R&D and hygiene validation/SOP planning, specialist vendor development coordination and final review.
CorePress: fictional educational POC; user made Experience Cloud portal, led requirements coordination with PM/PL, processes and presentation. Four projects, first place, Grand Prize. Program MVP is separate student vote, not project award.
Portal account is blocked: user confirmed. Do not attempt login/access verification. Public portal CTAs removed; mark account restricted.
CorePress article covers customer journey (SEO, lead, Opportunity, RFP shortlist, RFQ, Quote, Contract/Order), Asset-centered service/replacement, Sales/Service/Field Service/Agentforce, standard/extension boundaries, personal role and award.
SEO and conversion improvements are goals, not verified commercial outcomes. Team implementation not solo work.
PDF original: portfolio/assets/corepress/CorePress_ValueEngineering_v3.12.pdf, 30 pages, exact original verified. Three award photos and four slide excerpts in same folder.

## Fixed defects
Residential image previously broken inline data: replaced by real file portfolio/assets/cases/residential-lounge.webp; browser confirmed displayed. Cropped via CSS for emphasis with full-image link. Added deployment/use narrative.
Current commit moves CorePress links and award image INSIDE expandable .body; previously outside, flush against card edges and visible while collapsed. Dedicated responsive classes align text/buttons/image. User requested this fix, then new session.
CorePress article and assets remain available; existing article body preserved.

## Engineering
Main HTML is around 1 MB with legacy inline image data. Prefer separate assets for future additions. Do not transmit enormous base64 content in model-visible messages.
GitHub create_blob supports base64 binary, then create_tree(base tree), create_commit(parent), update_ref(force=false). Verify returned blob SHA against local git blob hash. For reading large source, git fetch/show works; fetch_file may return empty content for >1 MB.
Do not replace live file from stale local source. Non-forced updates protect concurrent changes.
Browser QA must actually scroll lazy images into view and check naturalWidth > 0; PIL verify alone wasn't sufficient.
Use existing browser skill/client, not alternate automation.
Next work only as user requests; no outstanding portfolio redesign authorized beyond session tasks. User wants new session because this thread is slow.

"""Editorial eight-page GTM portfolio. Review summaries when grounding changes.
Dependencies: reportlab, beautifulsoup4, Pillow. Public HTML supplies social URLs
and the original hero image; this script contains the selected case summaries.
"""
import argparse, html, urllib.request
from pathlib import Path
from bs4 import BeautifulSoup
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.utils import ImageReader
from reportlab.graphics.barcode import qr
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
a=argparse.ArgumentParser()
a.add_argument('--input',type=Path,default=ROOT/'index.html')
a.add_argument('--output',type=Path,default=ROOT/'output/pdf/Kim_Yushin_Portfolio.pdf')
a.add_argument('--font-dir',type=Path,default=Path.home()/'.cache/portfolio-pdf-fonts')
a.add_argument('--hero',type=Path)
args=a.parse_args();args.font_dir.mkdir(parents=True,exist_ok=True)
for weight in ['Regular','Bold']:
 f=args.font_dir/f'NanumGothic-{weight}.ttf'
 if not f.exists():urllib.request.urlretrieve('https://raw.githubusercontent.com/google/fonts/main/ofl/nanumgothic/'+f.name,f)
 pdfmetrics.registerFont(TTFont('KR'+('B' if weight=='Bold' else ''),str(f)))
pdfmetrics.registerFontFamily('KR',normal='KR',bold='KRB',italic='KR',boldItalic='KRB')
soup=BeautifulSoup(args.input.read_text(),'html.parser')
hero=args.hero or args.font_dir/'portfolio-hero.png'
if not hero.exists():urllib.request.urlretrieve(soup.select_one('.hero-vid')['poster'],hero)
W,H=landscape(A4);M=42;CW=W-2*M
BG='#F7F6F2';INK='#17363E';TEAL='#155D65';MUTED='#657A7E';HAIR='#D4DEDA';MINT='#E6EFE9';NAVY='#10323D';WHITE='#FFFFFF';PALE='#BCDCD2'
args.output.parent.mkdir(parents=True,exist_ok=True)
c=canvas.Canvas(str(args.output),pagesize=(W,H),pageCompression=1)
c.setTitle('김유신 포트폴리오 | B2B GTM · Sales & Operations');c.setAuthor('김유신');c.setSubject('GTM 경험을 시각적으로 정리한 포트폴리오')
TEXT=[]

def box(x,y,w,h,fill=MINT,stroke=None,r=10):
 c.setFillColor(HexColor(fill));c.setStrokeColor(HexColor(stroke or fill));c.setLineWidth(.6)
 c.roundRect(x,H-y-h,w,h,r,fill=1,stroke=bool(stroke))

def line(x1,y1,x2,y2,color=HAIR,width=1):
 c.setStrokeColor(HexColor(color));c.setLineWidth(width);c.line(x1,H-y1,x2,H-y2)

def p(t,x,y,w,size=14,color=INK,bold=False,leading=None,maxh=None):
 t=html.escape(t).replace('\n','<br/>')
 q=Paragraph(t,ParagraphStyle('text',fontName='KRB' if bold else 'KR',fontSize=size,leading=leading or size*1.5,textColor=HexColor(color),wordWrap='CJK'))
 _,h=q.wrap(w,1000)
 assert y+h<H-35, (c.getPageNumber(),t,y,h)
 if maxh is not None:assert h<=maxh+.01,(t,h,maxh)
 q.drawOn(c,x,H-y-h);TEXT.append((c.getPageNumber(),x,y,w,h,t));return y+h

def eng(t,x,y,size=10,color=MUTED,font='Helvetica'):
 c.setFillColor(HexColor(color));c.setFont(font,size);c.drawString(x,H-y-size,t)

def link(label,url,x,y,w=200,size=12,color=TEAL):
 bot=p(label,x,y,w,size,color)
 c.linkURL(url,(x,H-bot,x+w,H-y),relative=0,thickness=0);return bot

def base(n,label,dark=False):
 color=NAVY if dark else BG
 c.setFillColor(HexColor(color));c.rect(0,0,W,H,fill=1,stroke=0)
 fg=PALE if dark else TEAL
 eng('KIM YUSHIN / PORTFOLIO',M,25,8,fg)
 eng(label,W-M-175,25,8,fg)
 line(M,H-32,W-M,H-32,'#31535A' if dark else HAIR,.5)
 eng('PLANZ 2017-2026  /  B2B GTM',M,H-23,7,fg)
 eng(f'{n:02d} / 08',W-M-32,H-23,7,fg)
 c.bookmarkPage('page'+str(n))
 c.addOutlineEntry(label,'page'+str(n),0)

def title(n,label,t,sub=None,dark=False):
 base(n,label,dark);p(t,M,65,CW,27,WHITE if dark else TEAL,True,36)
 if sub:p(sub,M,145,CW,12,PALE if dark else MUTED)

def arrow(x,y,length=21,color=TEAL):
 line(x,y,x+length,y,color,1.1);line(x+length-5,y-4,x+length,y,color,1.1);line(x+length-5,y+4,x+length,y,color,1.1)

def circle(x,y,r,color=MINT):
 c.setFillColor(HexColor(color));c.circle(x,H-y,r,fill=1,stroke=0)

def detail(label,t,x,y,w=188):
 p(label,x,y,w,9,MUTED,True);return p(t,x,y+19,w,12.2,INK,False,18.3)

# 1 / A visual cover using the same owned image as the web portfolio.
base(1,'B2B GTM / SALES & OPERATIONS')
im=Image.open(hero).convert('RGB');target=(W-510)/H; iw,ih=im.size;cropw=int(ih*target);left=max(0,int(iw*.55)-cropw//2)
im=im.crop((left,0,left+cropw,ih));c.drawImage(ImageReader(im),510,0,W-510,H,mask='auto')
eng('B2B GTM',M,96,12,TEAL)
p('고객의 문제를\n사업의 실행으로.',M,139,452,35,TEAL,True,49)
p('김유신',M,283,420,26,INK,True)
eng('KIM YUSHIN',M,332,10,TEAL)
p('고객 발굴부터 제안·계약·도입과 운영까지.\n서로 다른 사정을 이해하고, 실행 가능한 방법을 찾습니다.',M,385,425,13,INK,False,22)
p('플랜즈 2017-2026 · 약 9년',M,456,420,11,MUTED)
link('웹 포트폴리오 보기  →','https://yushin-portfolio.vercel.app/',M,494,245,11)
eng('Making complex work clear,',548,345,16,WHITE,'Times-Roman')
eng('workable, and human.',548,372,20,WHITE,'Times-Italic')
eng('01 / 08',W-M-32,H-23,7,WHITE)
c.showPage()

# 2 / Scope is a flow, not an inflated job title.
title(2,'01 / GTM SCOPE','시장을 만나고,\n운영까지 연결합니다.','GTM은 직함보다, 고객이 선택하고 계속 사용할 수 있게 만드는 업무의 범위입니다.')
stages=[('고객 발굴','리드 · 수요 채널','DM·아웃바운드\n박람회·콘텐츠'),('제안 설계','문제 · 예산 구조','고객의 제약에 맞춘\n가격과 도입 방식'),('계약','조건 · 이해관계자','구매 결정이 가능한\n거래 구조'),('도입','POC · 현장 조율','작게 검증하고\n도입 범위를 확장'),('운영·개선','CRM · SOP','잘된 방식을 남기고\n다음 고객에 적용')]
cw=(CW-56)/5
for i,(name,sub,body) in enumerate(stages):
 x=M+i*(cw+14);box(x,204,cw,195,WHITE,HAIR)
 eng(f'0{i+1}',x+16,221,10,TEAL);p(name,x+16,251,cw-32,18,INK,True)
 p(sub,x+16,292,cw-32,10,TEAL);p(body,x+16,327,cw-32,11,MUTED,False,18)
 if i<4:arrow(x+cw-1,299,16)
line(M+12,462,W-M-12,462,TEAL,1.2)
for x,year,caption in [(M, '2017','플랜즈 참여·업무 시작'),(M+285,'2019','B2B 영업을 주력으로 담당'),(M+570,'2026','CRM·데이터·AI로 확장')]:
 circle(x+5,462,4,TEAL);eng(year,x,478,13,TEAL);p(caption,x,502,240,11,MUTED)
c.showPage()

# 3 / Three deals, three different buying constraints.
title(3,'02 / SALES & ADOPTION','같은 제품도,\n고객마다 다른 도입 경로가 필요합니다.')
cases=[('CJ올리브네트웍스','5대 계약','기존 계약과 여러 지사의\n카페 관리 부담','위약금 대응을 위한\n영업 예산 재구성','중단된 제안을 다시 열고\n1년 반 만에 계약'),('두산테스나','POC → 확대','기존 제품의 고장·관리 부담과\n교체 결정의 부담','기존 제품 운영관리까지\n포함하는 제안','서안성 POC 후\n평택·안성으로 도입 확대'),('SK D&D','매각 + 위탁','고객의 예산 집행 방식에\n맞는 계약 구조 필요','기기 매각과 위탁운영을\n결합한 제안','구로 생각공장\n메인 카페테리아 수주')]
cw=(CW-32)/3
for i,(org,metric,problem,change,outcome) in enumerate(cases):
 x=M+i*(cw+16);box(x,177,cw,351,WHITE,HAIR)
 p(org,x+18,195,cw-36,13,TEAL,True);p(metric,x+18,224,cw-36,23,INK,True)
 line(x+18,273,x+cw-18,273)
 detail('고객의 제약',problem,x+18,290,cw-36)
 detail('바꾼 방식',change,x+18,364,cw-36)
 detail('결과',outcome,x+18,438,cw-36)
c.showPage()

# 4 / Market entry and prioritisation, without invented matrix scores.
title(4,'03 / GO-TO-MARKET','누구에게 먼저 갈지,\n어떤 이유로 선택받을지 정합니다.')
left=356;rightx=M+380;rw=CW-380
box(M,180,left,349,TEAL)
p('자이S&D · GS건설',M+23,202,left-46,12,PALE,True)
p('커피 도입을\n주거 서비스의 차별화로.',M+23,235,left-46,22,WHITE,True,33)
for i,(num,label) in enumerate([('01','신규 단지의 차별화 요구 파악'),('02','제휴 제안과 MOU 설계'),('03','GS건설과 도입 요건 검토'),('04','지자체 영업신고')]):
 y=326+i*36;eng(num,M+23,y,10,PALE);p(label,M+57,y-2,left-80,12,WHITE)
p('검토한 판례집에서 해당 사례를 찾지 못한 상황.\n최초 신고라는 공식 확인과는 구분합니다.',M+23,484,left-46,9.3,PALE,False,14)
p('영업 우선순위',rightx,188,rw,18,INK,True)
criteria=['도입 시점','ROI','성사 가능성'];bw=(rw-16)/3
for i,t in enumerate(criteria):box(rightx+i*(bw+8),226,bw,48,MINT);p(t,rightx+10+i*(bw+8),242,bw-20,11,TEAL,True)
p('표에서 점수화',rightx,291,rw,14,INK,True);arrow(rightx+142,302,27)
p('아사나 우선순위 태그',rightx+184,290,rw-184,12,TEAL,True)
line(rightx,342,rightx+rw,342)
p('수요를 만든 여섯 채널',rightx,366,rw,18,INK,True)
for i,t in enumerate(['DM','퍼포먼스 마케팅','PR','아웃바운드','박람회','세미나']):
 x=rightx+(i%2)*(rw/2+4);y=408+(i//2)*37
 box(x,y,rw/2-8,28,WHITE,HAIR,r=5);p(t,x+12,y+6,rw/2-30,10.5,MUTED)
c.showPage()

# 5 / Product development as three concrete translations.
title(5,'04 / PRODUCT & LEARNING','고객의 신호를\n제품과 운영 기준으로 바꿉니다.')
items=[('DATA → PRODUCT','자판기 매출 데이터','고객사 데이터를 확보·분석해\n비타민C·타우린 드링크를\n기획하고 OEM으로 개발했습니다.','데이터 확보 → 분석 → OEM'),('REQUIREMENTS → PRODUCT','멸균농축크림우유','기능요구서를 표준화하고\n공급사와 약 6개월 공동 개발해\n위생·기호성·물류효율을 다뤘습니다.','요구사항 → 공동 개발'),('SCIENCE → OPERATIONS','위생 SOP','생물학 배경을 활용해\n무인 식음료 서비스의 위생 SOP와\n밸리데이션 체계를 만들었습니다.','전공 지식 → 현장 기준')]
cw=(CW-32)/3
for i,(tag,t,b,foot) in enumerate(items):
 x=M+i*(cw+16);box(x,177,cw,230,WHITE,HAIR)
 eng(tag,x+18,196,8,TEAL);p(t,x+18,228,cw-36,18,INK,True)
 p(b,x+18,280,cw-36,12,INK,False,20);p(foot,x+18,374,cw-36,9.5,TEAL,True)
box(M,430,CW,100,MINT)
p('실패를 다음 제안에 반영',M+20,449,210,13,TEAL,True)
p('현대차 양재 수주 실패',M+20,479,210,12,INK)
arrow(M+215,490,27)
p('텀블러·리유저블 구성 반영',M+259,479,235,12,INK)
arrow(M+495,490,27)
p('아모레퍼시픽·LG전자 계약에 활용',M+543,472,CW-563,11.5,INK)
c.showPage()

# 6 / People and operating systems; omit private family finances.
title(6,'05 / PEOPLE & OPERATIONS','사람과 운영이\n함께 나아가도록.')
left=356;rightx=M+380;rw=CW-380
p('직속 팀원 2명 채용·관리',M,185,left,21,INK,True)
line(M+24,265,M+300,265,TEAL);line(M+160,238,M+160,265,TEAL)
for x,t in [(M+24,'리드 확보'),(M+300,'문서 작업')]:
 circle(x,265,7,TEAL);p(t,x-24,284,130,12,TEAL,True)
p('주간 할당과 수행 결과의 성과 반영',M,339,left,14,INK,True)
p('기대에 못 미치면 업무 과정을 직접 관찰하고,\n일대일로 방법을 교정했습니다.',M,376,left,13,MUTED,False,22)
box(rightx,178,rw,246,MINT)
p('고른햇살 · 가족 사업',rightx+20,198,rw-40,12,TEAL,True)
p('인건비를 줄이지 않는 조건으로\n운영 구조를 개선했습니다.',rightx+20,230,rw-40,18,INK,True,28)
for i,t in enumerate(['원가·유통 조건 검토','전문가와 SOP 정리','ERP 도입으로 숫자가 보이는 운영']):
 p(f'0{i+1}',rightx+20,309+i*32,30,10,TEAL,True);p(t,rightx+59,307+i*32,rw-80,12,INK)
line(M,450,W-M,450)
p('파이프라인 운영',M,474,190,13,TEAL,True)
for x,label in [(M+204,'Trello'),(M+370,'Asana'),(M+536,'Relate')]:
 p(label,x,474,140,18,INK,True)
 if label!='Relate':arrow(x+106,490,30)
p('잠재고객 · 영업기회 · 운영중 단계를 구성하고, 도구를 옮겨가며 관리했습니다.',M+204,508,CW-204,11,MUTED)
c.showPage()

# 7 / A deliberately clear boundary around the education project.
title(7,'06 / COREPRESS - EDUCATIONAL POC','비즈니스 시나리오를\nSalesforce 프로세스로.',dark=True)
box(W-M-159,83,159,33,'#27535D',r=5);p('6인 팀 · 교육용 POC',W-M-147,91,135,11,WHITE,True)
p('가상의 산업장비 제조사를 상정한 설계안과 시연입니다.',M,150,CW,13,PALE)
steps=['Experience\nCloud','Opportunity','Asset','Case','Field\nService','리포팅'];sw=(CW-50)/6
for i,t in enumerate(steps):
 x=M+i*(sw+10);box(x,207,sw,92,'#214953',r=6);eng(f'0{i+1}',x+12,219,8,PALE);p(t,x+12,244,sw-24,11.5,WHITE,True,17)
 if i<5:arrow(x+sw-1,254,12,PALE)
p('개인 기여',M,329,CW,11,PALE,True)
for i,(t,b) in enumerate([('범위·역할 분담','팀이 맡을 범위와 역할을 정리'),('프로세스 설계','업무 시나리오를 시스템 흐름으로'),('발표 구성·진행','최종 발표의 구성과 전달')]):
 x=M+i*(CW/3);p(t,x,362,CW/3-20,18,WHITE,True);p(b,x,399,CW/3-24,11.5,PALE)
line(M,448,W-M,448,'#3B6068')
p('Salesforce Certified Platform Administrator',M,470,CW,13,WHITE,True)
p('616시간 과정 수료 · CorePress 최종 발표 대상 · 과정 MVP',M,501,CW,11,PALE)
p('Agentforce는 제한된 활용 시나리오 설계이며 상용 구축·운영 경험과 구분합니다.',M,531,CW,9,PALE)
c.showPage()

# 8 / A clear next action plus the four user-supplied social channels.
base(8,'07 / NEXT CONVERSATION')
p('좋은 일은,\n대화에서 시작됩니다.',M,74,455,30,TEAL,True,43)
p('시장과 사업의 성장 가능성,\n합리적인 피드백, 서로 성장할 기회.',M,199,438,18,INK,True,30)
p('CRM·데이터·AI로 관심을 넓히고 있으며,\n기회를 특정 산업으로 한정하지 않습니다.',M,281,433,13,MUTED,False,22)
p('사람마다 다른 사정을 이해하고,\n함께 더 나은 방법을 찾는 사람이고 싶습니다.',M,355,429,15,TEAL,True,25)
p('경희대학교 생물학 수료 · 2013.03-2018.02\n학위 미취득',M,476,429,10,MUTED,False,16)
x=M+469;rw=CW-469
box(x,71,rw,459,WHITE,HAIR)
p('유신과 커피챗',x+20,95,rw-40,20,TEAL,True)
link('yusin846@gmail.com','mailto:yusin846@gmail.com',x+20,137,rw-40,13)
for i,a in enumerate(soup.select('.social-links a')):
 label=a.get_text(' ',strip=True).replace('↗','').strip()
 link(label+'  →',a['href'],x+20,184+i*33,rw-40,12)
line(x+20,325,x+rw-20,325)
p('자세한 사례와 언론 기록',x+20,343,rw-40,12,INK,True)
link('웹 포트폴리오에서 보기  →','https://yushin-portfolio.vercel.app/',x+20,371,rw-40,11)
code=qr.QrCodeWidget('https://yushin-portfolio.vercel.app/');bounds=code.getBounds();qw=bounds[2]-bounds[0];qh=bounds[3]-bounds[1]
d=Drawing(85,85,transform=[85/qw,0,0,85/qh,0,0]);d.add(code);renderPDF.draw(d,c,x+14,H-505)
p('17개 사례·상세 설명\n커리어 에이전트',x+111,434,rw-125,10,MUTED,False,17)
c.showPage();c.save()
print(args.output)
print('Pages: 8 / text blocks:',len(TEXT))

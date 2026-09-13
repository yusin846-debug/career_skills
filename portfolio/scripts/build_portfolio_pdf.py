"""Build a selectable, linked A4 edition from the public portfolio HTML.

Requires reportlab and beautifulsoup4. Nanum Gothic TTFs are downloaded from
Google Fonts if --font-dir does not contain them. No browser or private data.
"""
import argparse
import html
import re
import urllib.request
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--input', type=Path, default=ROOT / 'index.html')
parser.add_argument('--output', type=Path, default=ROOT / 'output/pdf/Kim_Yushin_Portfolio.pdf')
parser.add_argument('--font-dir', type=Path, default=Path.home() / '.cache/portfolio-pdf-fonts')
args = parser.parse_args()
args.font_dir.mkdir(parents=True, exist_ok=True)
for weight in ('Regular', 'Bold'):
    file = args.font_dir / f'NanumGothic-{weight}.ttf'
    if not file.exists():
        urllib.request.urlretrieve('https://raw.githubusercontent.com/google/fonts/main/ofl/nanumgothic/' + file.name, file)
    pdfmetrics.registerFont(TTFont('KR' + ('B' if weight == 'Bold' else ''), str(file)))
pdfmetrics.registerFontFamily('KR', normal='KR', bold='KRB', italic='KR', boldItalic='KRB')

soup = BeautifulSoup(args.input.read_text(), 'html.parser')
articles = soup.select('.entries > .en')
assert len(articles) == 17, 'Review pagination when the archive changes.'
W, H = A4
M = 48
CW = W - M * 2
INK, TEAL, MUTED, BG, HAIR = map(HexColor, ['#183238', '#135B63', '#607176', '#F7F6F2', '#D5DDDA'])
args.output.parent.mkdir(parents=True, exist_ok=True)
c = canvas.Canvas(str(args.output), pagesize=A4, pageCompression=1)
c.setTitle('김유신 포트폴리오 | Kim Yushin Portfolio')
c.setAuthor('김유신')
c.setSubject('Planz 2017-2026 · B2B Sales · Customer Operations · CRM')

def clean(text):
    return re.sub(r'\s+', ' ', text).strip().replace('—', '-').replace('–', '-').replace('\u2011', '-')

def rich(node):
    if isinstance(node, NavigableString):
        return html.escape(re.sub(r'\s+', ' ', str(node)).replace('—', '-').replace('–', '-'))
    if node.name == 'br':
        return '<br/>'
    inner = ''.join(rich(x) for x in node.children)
    if node.name in ('b', 'strong'):
        return '<b>' + inner + '</b>'
    if node.name == 'a' and node.get('href', '').startswith(('https://', 'mailto:')):
        return f'<link href="{html.escape(node["href"], quote=True)}" color="#135B63">{inner}</link>'
    return inner

def text(selector, node=None):
    return clean((node or soup).select_one(selector).get_text(' ', strip=True))

def para(value, size=11, color=INK, bold=False, leading=None):
    return Paragraph(value, ParagraphStyle('p', fontName='KRB' if bold else 'KR', fontSize=size,
        leading=leading or size * 1.62, textColor=color, wordWrap='CJK', splitLongWords=True))

def draw(value, x, y, width=CW, size=11, color=INK, bold=False, leading=None):
    p = para(value, size, color, bold, leading)
    _, height = p.wrap(width, 2000)
    p.drawOn(c, x, y - height)
    return y - height

def base(number, label):
    c.setFillColor(BG); c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setStrokeColor(HAIR); c.setLineWidth(.5); c.line(M, H-51, W-M, H-51)
    c.setFillColor(TEAL); c.setFont('Helvetica', 8)
    c.drawString(M, H-36, 'KIM YUSHIN  /  PORTFOLIO')
    c.drawRightString(W-M, H-36, label)
    c.line(M, 40, W-M, 40)
    c.setFillColor(MUTED); c.setFont('Helvetica', 7.5)
    c.drawString(M, 26, 'PLANZ 2017-2026  /  B2B SALES SINCE 2019')
    c.drawRightString(W-M, 26, f'{number:02d} / 12')
    c.bookmarkPage('page' + str(number))

def heading(number, label, title, subtitle=None):
    base(number, label)
    c.addOutlineEntry(title, 'page'+str(number), level=0)
    y = draw(html.escape(title).replace('\n', '<br/>'), M, H-76, size=23, color=TEAL, bold=True, leading=31)
    if subtitle:
        y = draw(subtitle, M, y-13, size=10, color=MUTED)
    return y-23

def article_blocks(index, compact=False):
    a = articles[index]
    meta = clean(a.select_one('.en-meta').get_text(' · ', strip=True))
    out = [('meta', html.escape(meta)), ('title', rich(a.select_one('.en-t'))), ('summary', rich(a.select_one('.en-s')))]
    clients = a.select('.client-logo span')
    if clients:
        out += [('beat', '주요 계약 고객사'), ('body', ' · '.join(html.escape(x.get_text()) for x in clients))]
    art = a.select_one('.art')
    if art:
        for item in art.children:
            if isinstance(item, NavigableString) or not item.get_text(strip=True):
                continue
            cls = item.get('class', [])
            kind = 'quote' if 'pull' in cls else ('beat' if 'beat' in cls else 'body')
            value = ' · '.join(x.get_text() for x in item.select('span')) if 'logos' in cls else rich(item)
            out.append((kind, value))
    return out + [('space', '')]

def layout(blocks, y, minimum=10.2, initial=11.3):
    # Size is selected from actual paragraph heights, never by character count.
    def specs(kind, size):
        return {
            'meta': (8.2, TEAL, False, 5),
            'title': (size+3.7, INK, True, 9),
            'summary': (size, TEAL, False, 13),
            'body': (size, INK, False, 7),
            'beat': (size, INK, True, 7),
            'quote': (size, TEAL, True, 12),
            'small': (size-1.7, MUTED, False, 9),
            'space': (0, INK, False, 15),
        }[kind]
    size = initial
    while size >= minimum - .001:
        total = 0
        for kind, value in blocks:
            n, col, bold, gap = specs(kind, size)
            total += gap + (para(value, n, col, bold).wrap(CW, 2000)[1] if n else 0)
        if total <= y-60:
            break
        size = round(size-.2, 2)
    assert size >= minimum-.001, f'Page overflow: {c.getPageNumber()}, {total:.1f} > {y-60:.1f}'
    for kind, value in blocks:
        n, col, bold, gap = specs(kind, size)
        if n:
            y = draw(value, M, y, size=n, color=col, bold=bold)
        y -= gap
    print(f'page {c.getPageNumber():02d}: body {size:.1f}pt, bottom {y:.1f}pt')
    return y

def process_panel(top, title, nodes, columns=4):
    rows = (len(nodes)+columns-1)//columns
    panelh = 58 + rows*56
    c.setFillColor(HexColor('#EAF0EC')); c.roundRect(M,top-panelh,CW,panelh,7,fill=1,stroke=0)
    draw(title,M+16,top-15,CW-32,9,TEAL,True)
    cellw=(CW-40)/columns
    for i,label in enumerate(nodes):
        x=M+16+(i%columns)*cellw; y=top-42-(i//columns)*56
        draw(f'{i+1:02d}',x,y,cellw-12,8,MUTED)
        draw(html.escape(label),x,y-15,cellw-14,9.2,INK,True,13)

def archive(number, indices, title):
    y = heading(number, '01 / ARCHIVE', title)
    blocks=[]
    for idx in indices: blocks += article_blocks(idx)
    bottom=layout(blocks,y)
    if number == 2:
        process_panel(224,'2023 가을 - 2025.05  /  제안을 다시 움직인 과정',['고객 문제 인터뷰','8대 구성 제안','영업 예산 재구성','5대 계약'])
    elif number == 5:
        process_panel(208,'주거시설 도입을 위한 과정',['차별화 제휴 제안','MOU 설계','도입 요건 검토','지자체 영업신고'])
    elif number == 7:
        process_panel(282,'DESIGNED FLOW  /  교육용 POC 설계 흐름',['Experience Cloud','Opportunity','Asset','Case','Field Service','리포팅'],columns=3)
    c.showPage()

# Cover: large typography and restrained translucent color fields from the web.
base(1, '2017 - 2026')
c.saveState(); c.setFillColor(TEAL); c.setFillAlpha(.08)
c.circle(W-35, H-190, 175, fill=1, stroke=0)
c.setFillColor(HexColor('#81BCA6')); c.setFillAlpha(.16); c.circle(W-105, H-155, 135, fill=1, stroke=0); c.restoreState()
c.setFillColor(TEAL); c.setFont('Times-Roman', 32)
c.drawString(M, H-118, 'Making complex work clear,')
c.setFont('Times-Italic', 34); c.drawString(M, H-161, 'workable, and human.')
draw('김유신', M, H-219, size=43, color=TEAL, bold=True, leading=56)
c.setFillColor(TEAL); c.setFont('Helvetica',11);c.drawString(M, H-290, 'KIM YUSHIN')
y = draw('막힌 곳을 먼저 찾고,<br/>상대에게 도움이 되는 쪽으로 풀고,<br/>그 과정에서 서로 남는 게 있게 만듭니다.',M,H-336,size=17,color=INK,bold=True,leading=28)
y = draw(html.escape(text('.tail')), M,y-22,size=10,color=MUTED)
y = draw(rich(soup.select_one('.goal')),M,y-18,size=10.8)
c.setStrokeColor(HAIR);c.line(M,185,W-M,185)
contents=[('02 - 08','Archive','page2'),('09','Method','page9'),('10','Tools & interests','page10'),('11','Now','page11'),('12','Press & contact','page12')]
for i,(n,label,dest) in enumerate(contents):
    yy=165-i*18;c.setFillColor(MUTED);c.setFont('Helvetica',9);c.drawString(M,yy,n)
    c.setFillColor(TEAL);c.drawString(M+67,yy,label);c.linkRect('',dest,(M,yy-3,M+260,yy+12),relative=0,thickness=0)
c.linkURL('https://yushin-portfolio.vercel.app/',(M,45,W-M,65),relative=0)
draw('yushin-portfolio.vercel.app',M,64,size=9,color=TEAL)
c.showPage()
archive(2,[0],'멈춘 제안을 계약으로 연결합니다')
archive(3,[1,4],'고객의 도입 부담과 예산을 읽습니다')
archive(4,[2,3],'실패에서 배우고, 다른 고객으로 이어갑니다')
archive(5,[5],'전례가 불분명한 도입 요건을 풀어갑니다')
archive(6,[6,7,8,9,11,12],'수요·제품·운영을 함께 설계합니다')
archive(7,[10],'현장의 문제를 시스템으로 옮깁니다')
archive(8,[13],'지켜야 할 것을 먼저 정하고 시작합니다')

y=heading(9,'02 / METHOD',text('#method h2').replace('익혀서, ', '익혀서,\n'),rich(soup.select_one('#method .dek')))
blocks=[]
for row in soup.select('.meth-row'):
    blocks += [('meta',text('.meth-n',row)),('title',rich(row.select_one('.meth-t'))),('body',rich(row.select_one('.meth-d'))),('space','')]
layout(blocks,y,initial=11.8);c.showPage()

y=heading(10,'03 / TOOLS & INTERESTS','배워서 일에 쓰고, 경험을 기록합니다')
# Tools in two balanced columns.
tools=soup.select('.tool'); colw=(CW-28)/2; bottoms=[]
for col in range(2):
    yy=y;xx=M+col*(colw+28)
    for t in tools[col*3:col*3+3]:
        yy=draw(html.escape(text('.tool-k',t)),xx,yy,colw,8.2,TEAL)
        yy=draw(rich(t.select_one('.tool-title')),xx,yy-5,colw,12,INK,True)
        yy=draw(rich(t.select_one('.tool-v')),xx,yy-7,colw,10,MUTED)-22
    bottoms.append(yy)
y=min(bottoms)-8;c.setStrokeColor(HAIR);c.line(M,y,W-M,y);y-=18
blocks=[]
for idx in [14,15,16]:blocks += [(kind, value) for kind, value in article_blocks(idx) if kind not in ('meta', 'space')]
layout(blocks,y,minimum=10,initial=10.6);c.showPage()

y=heading(11,'04 / NOW',text('#now h2'),rich(soup.select_one('#now .dek')))
for a in soup.select('.arc-c'):
    y=draw(html.escape(text('.arc-n',a)),M,y,90,8.5,TEAL)
    # Draw next to the date, preserving one shared baseline.
    top=y+13.77
    yy=draw(rich(a.select_one('.arc-t')),M+106,top,CW-106,12,INK,True)
    yy=draw(rich(a.select_one('.arc-d')),M+106,yy-6,CW-106,10,MUTED)
    y=yy-21
y=draw('자격 · 수상 · 학력',M,y-1,size=13,color=TEAL,bold=True)-14
for a in soup.select('.cred'):
    y=draw(rich(a.select_one('.cred-t')),M,y,size=10.5,bold=True)
    y=draw(rich(a.select_one('.cred-d')),M,y-3,size=9,color=MUTED)-11
y=draw(rich(soup.select_one('.closer')),M,y-10,size=13.2,color=TEAL,bold=True,leading=22)
assert y>58, y
c.showPage()

y=heading(12,'05 / PRESS & CONTACT','기록을 읽고, 대화를 이어갑니다')
y=draw(rich(soup.select_one('#press .dek')),M,y,size=9.5,color=MUTED)-16
for a in soup.select('#press .press a'):
    title=''.join(str(x) for x in a.contents if not getattr(x,'name',None)=='span').strip()
    title=html.escape(clean(BeautifulSoup(title,'html.parser').get_text()))
    src=rich(a.select_one('.src')); url=html.escape(a['href'],quote=True)
    y=draw(f'<link href="{url}" color="#135B63">{title}</link>',M,y,size=9.5,bold=True,leading=13.5)
    y=draw(src,M,y-2,size=7.9,color=MUTED,leading=11)-7
y-=4;c.setStrokeColor(HAIR);c.line(M,y,W-M,y);y-=15
y=draw('유신과 커피챗 어떠세요?',M,y,size=16,color=TEAL,bold=True)-5
y=draw('채용 이야기 · 협업 제안 · 가벼운 인사',M,y,size=9.5,color=MUTED)-9
y=draw('<link href="mailto:yusin846@gmail.com" color="#135B63">yusin846@gmail.com</link>',M,y,size=11)-8
social=[]
for a in soup.select('.social-links a'):
    label=a.get_text(' ',strip=True).replace('↗','').strip()
    social.append(f'<link href="{html.escape(a["href"],quote=True)}" color="#135B63">{label}</link>')
y=draw('  ·  '.join(social),M,y,size=10)-7
y=draw('<link href="https://yushin-portfolio.vercel.app/" color="#135B63">웹 포트폴리오와 커리어 에이전트 방문하기</link>',M,y,size=9.5)
assert y>52, y
c.showPage();c.save()
print(args.output)

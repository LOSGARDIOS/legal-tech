# -*- coding: utf-8 -*-
"""Render AGREEMENT_v2_HE.md as an A4, RTL, print-ready document that keeps
the visual language of the original Los Gardios PDF."""
import io, re, html

src = io.open("AGREEMENT_v2_HE.md", encoding="utf-8").read()
lines = src.split("\n")

def inline(t):
    t = html.escape(t)
    t = re.sub(r'`([^`]+)`', r'<code>\1</code>', t)
    t = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<em>\1</em>', t)
    return t

out, i = [], 0
in_tbl = False

def close_tbl():
    global in_tbl
    if in_tbl:
        out.append("</tbody></table>")
        in_tbl = False

while i < len(lines):
    ln = lines[i].rstrip()
    s = ln.strip()

    if not s:
        close_tbl(); i += 1; continue

    # table
    if s.startswith("|") and i + 1 < len(lines) and re.match(r'^\|[\s:|-]+\|$', lines[i+1].strip()):
        close_tbl()
        hdr = [c.strip() for c in s.strip("|").split("|")]
        aln = [c.strip() for c in lines[i+1].strip().strip("|").split("|")]
        def al(a): return "center" if a.startswith(":") and a.endswith(":") else "right"
        out.append("<table><thead><tr>" + "".join(
            f'<th style="text-align:{al(a)}">{inline(c)}</th>' for c, a in zip(hdr, aln)) + "</tr></thead><tbody>")
        in_tbl = True; i += 2
        while i < len(lines) and lines[i].strip().startswith("|"):
            cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
            out.append("<tr>" + "".join(
                f'<td style="text-align:{al(aln[j]) if j<len(aln) else "right"}">{inline(c)}</td>'
                for j, c in enumerate(cells)) + "</tr>")
            i += 1
        close_tbl(); continue

    close_tbl()

    if s == "---":
        out.append('<div class="pagebreak"></div>'); i += 1; continue

    m = re.match(r'^(#{1,4})\s+(.*)$', s)
    if m:
        lvl, txt = len(m.group(1)), m.group(2)
        out.append(f'<h{lvl}>{inline(txt)}</h{lvl}>'); i += 1; continue

    if s.startswith("> "):
        blk = []
        while i < len(lines) and lines[i].strip().startswith(">"):
            blk.append(lines[i].strip().lstrip(">").strip()); i += 1
        out.append('<div class="note">' + "<br>".join(inline(b) for b in blk if b) + "</div>")
        continue

    if re.match(r'^[-*]\s+', s) or re.match(r'^\d+\.\s+', s):
        ordered = bool(re.match(r'^\d+\.\s+', s))
        tag = "ol" if ordered else "ul"
        out.append(f"<{tag}>")
        while i < len(lines):
            c = lines[i].strip()
            if re.match(r'^[-*]\s+', c) or re.match(r'^\d+\.\s+', c):
                out.append("<li>" + inline(re.sub(r'^([-*]|\d+\.)\s+', '', c)) + "</li>"); i += 1
            else:
                break
        out.append(f"</{tag}>"); continue

    out.append("<p>" + inline(s) + "</p>"); i += 1

close_tbl()
body = "\n".join(out)

# the masthead already carries the wordmark: fold the leading title block into a title sheet
body = body.replace('<h1>LOS GARDIOS</h1>\n<h2>הסכם התקשרות עם לקוח</h2>',
                    '<div class="doctitle">הסכם התקשרות עם לקוח</div>', 1)

# annex cover pages, matching the original's A / B / C divider sheets
for L, title, sub in [
    ("A", "פרוטוקול Genesis",
     "איך מתחילים לעבוד יחד: מחקר Genesis הראשוני שהארגון מבצע ומממן ברובו, ההשתתפות העצמית של הלקוח, מה קורה אם בסוף המחקר מחליטים שלא להמשיך, ואופציית הרכישה (Buyout)."),
    ("B", "תנאים מסחריים ותשומות",
     "התקציב החודשי, גבולות הגזרה ורמת הסובלנות שהלקוח קובע, מנגנון עצירת ההפסד (Stop-Loss), וטבלת מילוי אחת שמרכזת את כל הפרמטרים המסחריים."),
    ("C", "נתונים, פרטיות ותקשורת מוקלטת",
     "שלוש שכבות המידע ומה נעשה בכל שכבה, איך שומרים על פרטיות הלקוח, ואיך ומתי מוקלטות שיחות ופגישות."),
]:
    cover = (f'<section class="annex-cover"><div class="ac-letter">{L}</div>'
             f'<div class="ac-brand">LOS GARDIOS<span>· הסכם התקשרות עם לקוח</span></div>'
             f'<div class="ac-tag">נספח {L}</div><div class="ac-title">{title}</div>'
             f'<p class="ac-sub">{sub}</p>'
             f'<div class="ac-foot">מהווה חלק בלתי-נפרד מההסכם (סעיף 15(א)) · נכנס לתוקף עם החתימה בסוף מסמך זה</div></section>')
    body = body.replace(f"<h1>נספח {L} — ", cover + f'<h1 class="annex-h">נספח {L} — ', 1)

CSS = """
:root{--ink:#14181f;--muted:#5b6472;--rule:#d9dee6;--accent:#8a6a2f;--soft:#f7f8fa;--band:#101418}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:#e9ebef;color:var(--ink);direction:rtl;
 font-family:"Frank Ruhl Libre","David Libre","Times New Roman",Georgia,serif;
 font-size:10.4pt;line-height:1.72}
.sheet{max-width:820px;margin:0 auto;background:#fff;padding:34px 46px 46px;
 box-shadow:0 1px 3px rgba(0,0,0,.10)}
.masthead{border-bottom:2.5px solid var(--band);padding-bottom:14px;margin-bottom:26px;
 display:flex;justify-content:space-between;align-items:flex-end;gap:16px;flex-wrap:wrap}
.mh-brand{font-family:Helvetica,Arial,sans-serif;font-weight:700;font-size:19pt;
 letter-spacing:.30em;color:var(--band)}
.mh-meta{font-family:Helvetica,Arial,sans-serif;font-size:7.4pt;letter-spacing:.16em;
 color:var(--muted);text-align:left;line-height:1.9;direction:ltr}
.conf{display:inline-block;border:1px solid var(--accent);color:var(--accent);
 font-family:Helvetica,Arial,sans-serif;font-size:7pt;letter-spacing:.24em;
 padding:2px 9px;border-radius:2px}
h1{font-size:16pt;margin:26px 0 12px;padding-bottom:8px;border-bottom:2px solid var(--band);
 letter-spacing:.01em}
h1.annex-h{border-bottom-color:var(--accent)}
h2{font-size:12.4pt;margin:22px 0 8px;color:var(--band)}
h3{font-size:10.9pt;margin:16px 0 6px;color:#2a3444}
h4{font-size:10pt;margin:13px 0 5px;color:var(--muted)}
p{margin:0 0 9px;text-align:justify}
strong{font-weight:700}
code{font-family:"SF Mono",Menlo,Consolas,monospace;font-size:.87em;background:var(--soft);
 border:1px solid var(--rule);border-radius:3px;padding:.5px 4px;direction:ltr;
 display:inline-block;unicode-bidi:embed}
ul,ol{margin:0 0 10px;padding-inline-start:22px}
li{margin:0 0 4px;text-align:justify}
table{width:100%;border-collapse:collapse;margin:12px 0 16px;font-size:9.2pt;
 display:block;overflow-x:auto}
thead th{background:var(--band);color:#fff;font-weight:600;padding:7px 9px;
 border:1px solid var(--band);font-family:Helvetica,Arial,sans-serif;font-size:8.6pt}
tbody td{border:1px solid var(--rule);padding:7px 9px;vertical-align:top}
tbody tr:nth-child(even){background:var(--soft)}
.note{background:var(--soft);border-inline-start:3px solid var(--accent);
 padding:11px 14px;margin:13px 0;font-size:9.6pt;color:#333c4a}
hr{border:0;border-top:1px solid var(--rule);margin:22px 0}
.pagebreak{border-top:1px solid var(--rule);margin:26px 0}
.annex-cover{page-break-before:always;break-before:page;margin:36px -46px;padding:74px 46px;
 background:linear-gradient(160deg,#101418 0%,#1d2530 62%,#2b3542 100%);color:#fff;
 min-height:340px;position:relative}
.ac-letter{position:absolute;inset-inline-start:40px;top:26px;
 font-family:Helvetica,Arial,sans-serif;font-size:120pt;font-weight:700;
 color:rgba(255,255,255,.075);line-height:1}
.ac-brand{font-family:Helvetica,Arial,sans-serif;font-size:11pt;font-weight:700;
 letter-spacing:.26em;margin-bottom:44px}
.ac-brand span{font-weight:400;letter-spacing:.06em;font-size:8.6pt;
 color:rgba(255,255,255,.62);margin-inline-start:10px}
.ac-tag{font-family:Helvetica,Arial,sans-serif;font-size:8.4pt;letter-spacing:.24em;
 color:var(--accent);margin-bottom:8px}
.ac-title{font-size:25pt;font-weight:700;margin-bottom:16px;position:relative;z-index:1}
.ac-sub{max-width:560px;color:rgba(255,255,255,.80);font-size:9.6pt;line-height:1.85;
 text-align:justify;position:relative;z-index:1}
.ac-foot{position:absolute;bottom:26px;inset-inline-start:46px;
 font-family:Helvetica,Arial,sans-serif;font-size:7.4pt;letter-spacing:.10em;
 color:rgba(255,255,255,.50)}
.doctitle{font-size:23pt;font-weight:700;margin:6px 0 4px;letter-spacing:.01em}
.docfoot{margin-top:34px;padding-top:12px;border-top:1px solid var(--rule);
 font-family:Helvetica,Arial,sans-serif;font-size:7.6pt;letter-spacing:.10em;
 color:var(--muted);display:flex;justify-content:space-between;flex-wrap:wrap;gap:10px}
@page{size:A4;margin:17mm 15mm}
@media print{
 body{background:#fff}
 .sheet{max-width:none;box-shadow:none;padding:0}
 .annex-cover{margin:0;padding:66px 20mm;-webkit-print-color-adjust:exact;print-color-adjust:exact}
 thead th{-webkit-print-color-adjust:exact;print-color-adjust:exact}
 h1,h2{break-after:avoid}
 table,.note{break-inside:avoid}
}
"""

doc = f"""<!doctype html>
<html lang="he" dir="rtl"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Los Gardios — הסכם התקשרות עם לקוח</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Frank+Ruhl+Libre:wght@400;500;700&family=David+Libre:wght@400;500;700&display=swap" rel="stylesheet">
<style>{CSS}</style></head>
<body><div class="sheet">
<div class="masthead">
  <div><div class="mh-brand">LOS GARDIOS</div>
    <div style="margin-top:7px"><span class="conf">סודי · CONFIDENTIAL</span></div></div>
  <div class="mh-meta">Los Gardios Holdings [ ]<br>516819257 · השדרה המרכזית 15, מודיעין<br>גרסת תבנית 2 · ערכת מסמכי התקשרות אחידה</div>
</div>
{body}
<div class="docfoot"><span>Los Gardios — הסכם התקשרות עם לקוח (סודי)</span><span>גרסת תבנית 2</span></div>
</div></body></html>"""

io.open("AGREEMENT_v2_HE.html", "w", encoding="utf-8").write(doc)
print("wrote AGREEMENT_v2_HE.html", len(doc), "bytes")

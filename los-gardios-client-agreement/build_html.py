# -*- coding: utf-8 -*-
"""Render AGREEMENT_v2_HE.md as an A4, RTL, print-ready document that keeps
the visual language of the original Los Gardios PDF."""
import io, re, html, base64, os

src = io.open("AGREEMENT_v2_HE.md", encoding="utf-8").read()
lines = src.split("\n")

# Brand assets (logo mark + official stamp), embedded as base64 so the HTML/PDF is self-contained.
_ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
def _data_uri(fname):
    with open(os.path.join(_ASSETS, fname), "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode("ascii")

LOGO_MARK = _data_uri("logo_mark_web.png")
LOGO_STAMP = _data_uri("logo_stamp_web.png")

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

# annex cover pages — matching the original PDF's own divider-page design exactly:
# white background, a per-annex accent color (sampled from the source file), a small
# top masthead line with a colored circular letter badge, a colored "annex X" tag, the
# title and body in black/gray, and a giant, pale-tinted oversized letter bottom-left.
ANNEX_COLORS = {
    "A": ("#5B2986", "#F4F0F6"),  # Genesis — purple (also the brand's primary accent)
    "B": ("#1A836E", "#EEF6F4"),  # Commercial terms — teal
    "C": ("#B3531D", "#F9F3EF"),  # Data & privacy — burnt orange
    "D": ("#2C5AA0", "#EEF3FA"),  # Personal-data DPA — blue (no original page to sample; new annex)
}
_DEFAULT_AC_FOOT = "מהווה חלק בלתי-נפרד מההסכם (סעיף 15(א)) · נכנס לתוקף עם החתימה בסוף מסמך זה"
for L, title, sub, foot in [
    ("A", "פרוטוקול Genesis",
     "איך מתחילים לעבוד יחד: מחקר Genesis הראשוני שהארגון מבצע ומממן ברובו, ההשתתפות העצמית של הלקוח, מה קורה אם בסוף המחקר מחליטים שלא להמשיך, ואופציית הרכישה (Buyout).",
     _DEFAULT_AC_FOOT),
    ("B", "תנאים מסחריים ותשומות",
     "התקציב החודשי, גבולות הגזרה ורמת הסובלנות שהלקוח קובע, מנגנון עצירת ההפסד (Stop-Loss), וטבלת מילוי אחת שמרכזת את כל הפרמטרים המסחריים.",
     _DEFAULT_AC_FOOT),
    ("C", "נתונים, פרטיות ותקשורת מוקלטת",
     "שלוש שכבות המידע ומה נעשה בכל שכבה, איך שומרים על פרטיות הלקוח, ואיך ומתי מוקלטות שיחות ופגישות.",
     _DEFAULT_AC_FOOT),
    ("D", "הגנת מידע אישי (DPA)",
     "מטרות ואופן עיבוד המידע האישי, סוגי המידע ונושאיו, מעבדי משנה, העברות בין-לאומיות, דיווח על אירועי אבטחה, וזכות ביקורת.",
     "חל על ההתקשרות רק אם סומן ככזה בטבלת התנאים המסחריים שבנספח B (סעיף 15(א))"),
]:
    accent, tint = ANNEX_COLORS[L]
    cover = (
        f'<section class="annex-cover" style="--ax:{accent};--ax-tint:{tint}">'
        f'<div class="ac-mast"><span class="ac-mast-text">הסכם התקשרות עם לקוח · LOS GARDIOS</span>'
        f'<span class="ac-badge">{L}</span></div>'
        f'<div class="ac-rule"></div>'
        f'<div class="ac-body">'
        f'<div class="ac-tag"><span class="ac-tag-dash"></span>נספח {L}</div>'
        f'<div class="ac-title">{title}</div>'
        f'<p class="ac-sub">{sub}</p>'
        f'</div>'
        f'<div class="ac-letter">{L}</div>'
        f'<div class="ac-footrule"></div>'
        f'<div class="ac-foot">{foot}</div>'
        f'</section>'
    )
    body = body.replace(f"<h1>נספח {L} — ", cover + f'<h1 class="annex-h">נספח {L} — ', 1)

# the framework agreement itself (chapters א'-ד') gets the same divider treatment as the
# three annexes, so all four parts of the document open with a matching cover page —
# using the base brand purple (the framework's own identity, not a sub-annex hue) and a
# section-mark (§) in place of an annex letter, since this part isn't "annex X".
_fw_accent, _fw_tint = ANNEX_COLORS["A"]
_fw_cover = (
    f'<section class="annex-cover" style="--ax:{_fw_accent};--ax-tint:{_fw_tint}">'
    f'<div class="ac-mast"><span class="ac-mast-text">הסכם התקשרות עם לקוח · LOS GARDIOS</span>'
    f'<span class="ac-badge">§</span></div>'
    f'<div class="ac-rule"></div>'
    f'<div class="ac-body">'
    f'<div class="ac-tag"><span class="ac-tag-dash"></span>פרקים א׳–ד׳</div>'
    f'<div class="ac-title">הסכם המסגרת</div>'
    f'<p class="ac-sub">יסודות ההתקשרות וחובות הצדדים, הגנה על נכסי הארגון וקניין רוחני, פיצוי מוסכם והגבלת אחריות, ותקופת ההתקשרות, סיומה ויישוב סכסוכים.</p>'
    f'</div>'
    f'<div class="ac-letter">§</div>'
    f'<div class="ac-footrule"></div>'
    f'<div class="ac-foot">חלק א׳ מארבעת חלקי ההסכם · ראו מפת ההסכם לעיל</div>'
    f'</section>'
)
body = body.replace('<h1>פרק א&#x27; — יסודות ההתקשרות</h1>',
                     _fw_cover + '<h1 class="annex-h">פרק א׳ — יסודות ההתקשרות</h1>', 1)

# Signature blocks: the organization's column carries the official stamp — the authorized
# signatory signs across/beside it on the printed page, in addition to filling in their
# details in the rows above (name, title, ID) which remain plain fill-in lines.
_STAMP_CELL = (
    '<div class="stampcell"><img src="' + LOGO_STAMP + '" alt="חותמת הארגון" class="stampimg">'
    '<div class="stampline"></div><div class="stampcaption">חתימת המורשה — על החותמת ולצידה</div></div>'
)
body = body.replace(
    '<tr><td style="text-align:right">חתימה וחותמת</td><td style="text-align:right">______________________</td><td style="text-align:right">______________________</td></tr>',
    '<tr><td style="text-align:right">חתימה וחותמת</td><td style="text-align:right">______________________</td><td style="text-align:right">' + _STAMP_CELL + '</td></tr>',
    1,
)
body = body.replace(
    '<tr><td style="text-align:right">חתימה</td><td style="text-align:right">______________________</td><td style="text-align:right">______________________</td></tr>',
    '<tr><td style="text-align:right">חתימה</td><td style="text-align:right">______________________</td><td style="text-align:right">' + _STAMP_CELL + '</td></tr>',
    1,
)

# Clause cards — the original wraps each סעיף's body in a pale card sitting below the
# bold heading (the heading itself stays outside/above it, on the white page). Every
# <h2> here is either "סעיף N — ..." (gets the card) or a signature sub-heading like
# "אישורי קריאה"/"חתימות" (left alone, matching the original's plain signature pages).
_parts = re.split(r'(<h[12][^>]*>.*?</h[12]>)', body)
_out2, _pending, _in_clause = [], [], False
def _flush():
    global _pending, _in_clause
    if _in_clause and _pending:
        _out2.append('<div class="clausebox">' + "".join(_pending) + '</div>')
    else:
        _out2.extend(_pending)
    _pending = []
for _tok in _parts:
    _m = re.match(r'<h([12])[^>]*>(.*?)</h\1>', _tok, re.S)
    if _m:
        _flush()
        _in_clause = _m.group(1) == "2" and _m.group(2).strip().startswith("סעיף ")
        _out2.append(_tok)
    else:
        _pending.append(_tok)
_flush()
body = "".join(_out2)

CSS = """
:root{--ink:#14181f;--muted:#5b6472;--rule:#d9dee6;--accent:#5B2986;--soft:#f7f8fa;--band:#101418;--card:#FAFAFD}
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
 letter-spacing:.30em;color:var(--band);display:flex;align-items:center;gap:10px}
.mh-mark{height:34px;width:auto;flex:none}
.mh-meta{font-family:Helvetica,Arial,sans-serif;font-size:7.4pt;letter-spacing:.16em;
 color:var(--muted);text-align:left;line-height:1.9;direction:ltr}
.conf{display:inline-block;border:1px solid var(--accent);color:var(--accent);
 font-family:Helvetica,Arial,sans-serif;font-size:7pt;letter-spacing:.24em;
 padding:2px 9px;border-radius:2px}
h1{font-size:16pt;margin:26px 0 12px;padding-bottom:8px;border-bottom:3px solid var(--accent);
 letter-spacing:.01em}
h1:not(.annex-h){page-break-before:always;break-before:page}
h2{font-size:12.4pt;margin:22px 0 8px;color:var(--band)}
.clausebox{background:var(--card);border-radius:5px;padding:14px 17px;margin:0 0 10px}
.clausebox>p:last-child,.clausebox>ul:last-child,.clausebox>ol:last-child,.clausebox>table:last-child{margin-bottom:0}
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
/* Annex divider pages — matches the original PDF's own design: white background,
   a per-annex accent color (--ax / --ax-tint, set inline per section), a thin
   colored rule under a small running-header line, a colored circular letter badge,
   a colored tag with a short dash, and a giant pale-tinted letter bottom-left. */
.annex-cover{page-break-before:always;break-before:page;margin:36px -46px 0;padding:0 46px 56px;
 background:#fff;color:var(--ink);min-height:620px;position:relative;overflow:hidden}
.ac-mast{display:flex;justify-content:space-between;align-items:center;padding-top:36px}
.ac-mast-text{font-family:Helvetica,Arial,sans-serif;font-size:7.6pt;letter-spacing:.20em;
 color:var(--muted)}
.ac-badge{width:30px;height:30px;border-radius:50%;background:var(--ax);color:#fff;
 font-family:Helvetica,Arial,sans-serif;font-weight:700;font-size:11pt;
 display:flex;align-items:center;justify-content:center;flex:none}
.ac-rule{height:2px;background:var(--ax);margin:14px 0 0}
.ac-body{padding-top:150px;position:relative;z-index:1}
.ac-tag{font-family:Helvetica,Arial,sans-serif;font-size:8.6pt;font-weight:700;
 letter-spacing:.22em;color:var(--ax);margin-bottom:12px;
 display:flex;align-items:center;gap:12px;justify-content:flex-end}
.ac-tag-dash{display:inline-block;width:34px;height:2px;background:var(--ax)}
.ac-title{font-size:24pt;font-weight:700;margin-bottom:16px;color:var(--ink);text-align:right}
.ac-sub{max-width:560px;margin-inline-start:auto;color:var(--muted);font-size:9.8pt;
 line-height:1.85;text-align:right}
.ac-letter{position:absolute;left:-18px;bottom:-40px;
 font-family:Georgia,"Times New Roman",serif;font-size:280pt;font-weight:700;
 color:var(--ax-tint);line-height:1;z-index:0;user-select:none}
.ac-footrule{border-top:1px solid var(--rule);margin-inline-start:34%;margin-top:200px;
 position:relative;z-index:1}
.ac-foot{font-family:Helvetica,Arial,sans-serif;font-size:7.4pt;letter-spacing:.06em;
 color:var(--muted);text-align:right;margin-top:8px;position:relative;z-index:1}
.stampcell{display:flex;flex-direction:column;align-items:center;gap:2px}
.stampimg{width:92px;height:92px;object-fit:contain;opacity:.9}
.stampline{width:100%;border-top:1px solid var(--ink);margin-top:2px}
.stampcaption{font-family:Helvetica,Arial,sans-serif;font-size:6.6pt;color:var(--muted);
 letter-spacing:.03em;text-align:center}
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
  <div><div class="mh-brand"><img src="{LOGO_MARK}" alt="Los Gardios" class="mh-mark">LOS GARDIOS</div>
    <div style="margin-top:7px"><span class="conf">סודי · CONFIDENTIAL</span></div></div>
  <div class="mh-meta">לוס גרדיוס בע"מ<br>516819257 · השדרה המרכזית 15, מודיעין<br>גרסת תבנית 2 · ערכת מסמכי התקשרות אחידה</div>
</div>
{body}
<div class="docfoot"><span>Los Gardios — הסכם התקשרות עם לקוח (סודי)</span><span>גרסת תבנית 2</span></div>
</div></body></html>"""

io.open("AGREEMENT_v2_HE.html", "w", encoding="utf-8").write(doc)
print("wrote AGREEMENT_v2_HE.html", len(doc), "bytes")

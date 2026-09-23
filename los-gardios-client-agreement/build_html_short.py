# -*- coding: utf-8 -*-
"""Render AGREEMENT_v2_HE.md as an A4, RTL, print-ready document that keeps
the visual language of the original Los Gardios PDF."""
import io, re, html, base64, os

src = io.open("AGREEMENT_SHORT_HE.md", encoding="utf-8").read()
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

    # explicit keep-together group (heading/intro + the table it introduces,
    # so a table that doesn't fit the remaining page takes its heading with it
    # instead of stranding the heading/intro on the previous page)
    if s == "<!--group-start-->":
        out.append('<div class="keepgroup">'); i += 1; continue
    if s == "<!--group-end-->":
        out.append('</div>'); i += 1; continue

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
# Same 4-color categorical palette as the Guide's forecast-table section
# groups (gold/gold-deep/muted/purple) — not an independent color system.
ANNEX_COLORS = {
    "A": ("#A9824F", "#F4EEE4"),  # Genesis — gold
    "B": ("#8C6A3D", "#F2EAE0"),  # Commercial terms — gold-deep
    "C": ("#7D6F5C", "#F0EEE9"),  # Data & privacy — muted
    "D": ("#5B2986", "#F4F0F6"),  # Personal-data DPA — purple
}
_DEFAULT_AC_FOOT = "מהווה חלק בלתי-נפרד מההסכם (סעיף 15(א)) · נכנס לתוקף עם החתימה בסוף מסמך זה"
for L, title, sub, foot in [
    ("A", "Genesis — תנאים כספיים",
     "שווי מחקר Genesis וחלוקת העלות, דמי ההשתתפות העצמית, מה קורה אם בסוף המחקר מחליטים שלא להמשיך, ואופציית הרכישה (Buyout). תיאור מלא של תהליך המחקר עצמו — במדריך הלקוח.",
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
    # compact per-annex banner — a colored tag + rule, no full divider page: the short
    # contract's whole point is length, and the full-page annex-cover (min-height:620px,
    # masthead, giant letter) costs nearly a full page per annex even sharing with content.
    accent, tint = ANNEX_COLORS[L]
    cover = (
        f'<div class="mini-divider" style="--ax:{accent};--ax-tint:{tint}">'
        f'<span class="mini-badge">{L}</span>'
        f'<span class="mini-sub">{sub}</span>'
        f'</div>'
    )
    body = body.replace(f"<h1>נספח {L} — ", cover + f'<h1 class="annex-h" style="border-bottom-color:{accent}">נספח {L} — ', 1)

# the framework agreement itself (chapters א'-ד') gets the same divider treatment as the
# three annexes, so all four parts of the document open with a matching cover page —
# using the base brand purple (the framework's own identity, not a sub-annex hue) and a
# section-mark (§) in place of an annex letter, since this part isn't "annex X".
_fw_accent, _fw_tint = ANNEX_COLORS["A"]
_fw_cover = (
    f'<div class="mini-divider" style="--ax:{_fw_accent};--ax-tint:{_fw_tint}">'
    f'<span class="mini-badge">§</span>'
    f'<span class="mini-sub">יסודות ההתקשרות וחובות הצדדים, הגנה על נכסי הארגון וקניין רוחני, פיצוי מוסכם והגבלת אחריות, תקופה, סיום ויישוב סכסוכים.</span>'
    f'</div>'
)
body = body.replace('<h1>פרק א&#x27; — יסודות ההתקשרות</h1>',
                     _fw_cover + f'<h1 class="annex-h" style="border-bottom-color:{_fw_accent}">פרק א׳ — יסודות ההתקשרות</h1>', 1)

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
#
# Four clauses carry materially more weight for the signer than the rest of the
# document — the non-solicit/non-circumvent restriction, the liquidated-damages
# table, the liability cap, and the Buyout/independent-implementation restriction
# — and get a visually distinct card (purple accent instead of gold) so a reader
# skimming under signing pressure gets a cue that these are not routine clauses.
_KEY_CLAUSES = (
    "סעיף 8 — הגנה על הקשרים המקצועיים",
    "סעיף 11 — סעדים, השבת ההשקעה",
    "סעיף 12 — הגבלת אחריות",
    "סעיף 3 — אופציית רכישה",
)
_parts = re.split(r'(<h[12][^>]*>.*?</h[12]>)', body)
_out2, _pending, _in_clause, _key_clause = [], [], False, False
def _flush():
    global _pending, _in_clause, _key_clause
    if _in_clause and _pending:
        _cls = "clausebox clausebox-key" if _key_clause else "clausebox"
        _out2.append(f'<div class="{_cls}">' + "".join(_pending) + '</div>')
    else:
        _out2.extend(_pending)
    _pending = []
for _tok in _parts:
    _m = re.match(r'<h([12])[^>]*>(.*?)</h\1>', _tok, re.S)
    if _m:
        _flush()
        _htxt = _m.group(2).strip()
        _in_clause = _m.group(1) == "2" and _htxt.startswith("סעיף ")
        _key_clause = any(_htxt.startswith(k) for k in _KEY_CLAUSES)
        _out2.append(_tok)
    else:
        _pending.append(_tok)
_flush()
body = "".join(_out2)

CSS = """
/* Design language deliberately lighter than CLIENT_GUIDE_HE.md's build: the
   Guide is a physical, printed, editorial piece meant to impress on arrival;
   this Agreement is a digital document signed digitally — it borrows the
   Guide's palette tokens and Heebo/Frank Ruhl Libre font pairing so the two
   read as one brand family, but stays plain and functional (white page, no
   dark cover band, no photographic/editorial treatment) rather than matching
   the Guide's own level of production. The Agreement keeps its own flowing-
   document architecture (native @page pagination, not the Guide's per-page
   divs): this is a light re-theme, not a re-architecture. */
:root{
 --ink:#2A2118; --muted:#7D6F5C; --rule:#E3D8C3; --soft:#FAF7F1;
 --gold:#A9824F; --gold-deep:#8C6A3D;
 --purple:#5B2986; --accent:#5B2986
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:#eeeae1;color:var(--ink);direction:rtl;
 font-family:"Heebo","Frank Ruhl Libre",Georgia,serif;
 font-size:10.4pt;line-height:1.78}
.sheet{max-width:820px;margin:0 auto;background:#fff;padding:34px 46px 46px}
.masthead{border-bottom:2px solid var(--gold);padding-bottom:14px;margin-bottom:26px;
 display:flex;justify-content:space-between;align-items:flex-end;gap:16px;flex-wrap:wrap}
.mh-brand{font-family:Helvetica,Arial,sans-serif;font-weight:700;font-size:17pt;
 letter-spacing:.28em;color:var(--ink);display:flex;align-items:center;gap:10px}
.mh-mark{height:30px;width:auto;flex:none}
.mh-meta{font-family:"Heebo",sans-serif;font-size:7.4pt;letter-spacing:.16em;
 color:var(--muted);text-align:left;line-height:1.9;direction:ltr}
.conf{display:inline-block;border:1px solid var(--purple);color:var(--purple);
 font-family:"Heebo",sans-serif;font-size:7pt;letter-spacing:.24em;
 padding:2px 9px;border-radius:2px}
h1{font-family:"Frank Ruhl Libre",serif;font-weight:600;font-size:17pt;margin:26px 0 12px;
 padding-bottom:8px;border-bottom:3px solid var(--gold);letter-spacing:.01em;color:var(--ink)}
h2{font-family:"Frank Ruhl Libre",serif;font-weight:600;font-size:12.8pt;margin:22px 0 8px;
 color:var(--ink);break-after:avoid;page-break-after:avoid}
.clausebox{background:var(--soft);border-inline-start:3px solid var(--gold);
 padding:14px 17px;margin:0 0 10px;break-inside:avoid;page-break-inside:avoid}
.clausebox-key{border-inline-start:5px solid var(--purple);position:relative;padding-top:28px}
.clausebox-key::before{content:"מנגנון הגנה מרכזי — קראו בעיון";position:absolute;
 top:10px;inset-inline-start:17px;font-family:"Heebo",sans-serif;font-weight:700;
 font-size:7.4pt;letter-spacing:.14em;color:var(--purple)}
.keepgroup{break-inside:avoid;page-break-inside:avoid}
.clausebox>p:last-child,.clausebox>ul:last-child,.clausebox>ol:last-child,.clausebox>table:last-child{margin-bottom:0}
h3{font-family:"Frank Ruhl Libre",serif;font-size:11.2pt;margin:16px 0 6px;color:var(--gold-deep)}
h4{font-size:10pt;margin:13px 0 5px;color:var(--muted)}
p{margin:0 0 9px;text-align:justify}
strong{font-weight:700;color:var(--ink)}
code{font-family:"SF Mono",Menlo,Consolas,monospace;font-size:.87em;background:var(--soft);
 border:1px solid var(--rule);border-radius:3px;padding:.5px 4px;direction:ltr;
 display:inline-block;unicode-bidi:embed}
ul,ol{margin:0 0 10px;padding-inline-start:22px}
li{margin:0 0 4px;text-align:justify}
table{width:100%;border-collapse:collapse;margin:12px 0 16px;font-size:9.2pt;
 display:block;overflow-x:auto}
thead th{background:transparent;color:var(--gold-deep);font-weight:700;padding:7px 9px;
 border-bottom:2px solid var(--gold);font-family:"Heebo",sans-serif;font-size:8.6pt;letter-spacing:.02em}
tbody td{border-bottom:1px solid var(--rule);padding:7px 9px;vertical-align:top}
.note{background:var(--soft);border-inline-start:3px solid var(--gold-deep);
 padding:11px 14px;margin:13px 0;font-size:9.6pt;color:#382c1f}
hr{border:0;border-top:1px solid var(--rule);margin:22px 0}
.pagebreak{border-top:1px solid var(--rule);margin:26px 0}
/* Compact per-section banner — a colored badge letter and a one-line
   description above the heading, in the same eyebrow language as the
   Guide's chapter dividers, sized to cost no extra page per section. */
.mini-divider{display:flex;align-items:center;gap:12px;margin:30px 0 -4px;padding-top:16px;
 border-top:2px solid var(--ax)}
.mini-badge{width:26px;height:26px;border-radius:50%;background:var(--ax);color:#fff;
 font-family:"Frank Ruhl Libre",serif;font-weight:700;font-size:11pt;flex:none;
 display:flex;align-items:center;justify-content:center}
.mini-sub{font-family:"Heebo",sans-serif;font-size:8.8pt;color:var(--muted);line-height:1.6}
.stampcell{display:flex;flex-direction:column;align-items:center;gap:2px}
.stampimg{width:92px;height:92px;object-fit:contain;opacity:.9}
.stampline{width:100%;border-top:1px solid var(--ink);margin-top:2px}
.stampcaption{font-family:"Heebo",sans-serif;font-size:6.6pt;color:var(--muted);
 letter-spacing:.03em;text-align:center}
.doctitle{font-family:"Frank Ruhl Libre",serif;font-weight:600;font-size:23pt;margin:6px 0 4px;letter-spacing:.01em}
.docfoot{margin-top:34px;padding-top:12px;border-top:1px solid var(--rule);
 font-family:"Heebo",sans-serif;font-size:7.6pt;letter-spacing:.10em;
 color:var(--muted);display:flex;justify-content:space-between;flex-wrap:wrap;gap:10px}
@page{size:A4;margin:22mm 15mm 17mm}
@media print{
 body{background:#fff}
 .sheet{max-width:none;padding:0}
 .masthead{margin:0 0 26px}
 thead th{-webkit-print-color-adjust:exact;print-color-adjust:exact}
 .clausebox,.mini-badge{-webkit-print-color-adjust:exact;print-color-adjust:exact}
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
<link href="https://fonts.googleapis.com/css2?family=Heebo:wght@300;400;600;700&family=Frank+Ruhl+Libre:wght@600;700&display=swap" rel="stylesheet">
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

io.open("AGREEMENT_SHORT_HE.html", "w", encoding="utf-8").write(doc)
print("wrote AGREEMENT_SHORT_HE.html", len(doc), "bytes")

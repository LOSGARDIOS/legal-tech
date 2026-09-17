# -*- coding: utf-8 -*-
"""Render CLIENT_GUIDE_HE.md as a premium, editorial-feeling A4 RTL PDF.

Design language: dark espresso section dividers with ghost numerals, a
cream content-page body, a brass/gold accent system (rules, eyebrows,
stat tiles, key-insight callouts), and Los Gardios' own Velvet Purple
used sparingly as the brand-identity touch (logo mark, one accent line
on the cover, a single narrative accent inside two of the new diagrams)
rather than as the dominant hue — the warm gold/espresso palette is the
editorial atmosphere; purple is the brand anchor.

The underlying Hebrew CONTENT is copied verbatim from CLIENT_GUIDE_HE.md
(source of truth); this build script is presentation-only — page
grouping, diagram composition and the Intake Form's field grouping/order
are the only structural decisions made here, and they never introduce a
sentence that isn't in the .md. New concepts (the operating-model flow,
the sustainability principle, the Genesis specialist-lens system, the
oversight/reporting mechanics) are all authored in CLIENT_GUIDE_HE.md
first and merely visualized here.
"""
import io, os, base64

_HERE = os.path.dirname(os.path.abspath(__file__))
_ASSETS = os.path.join(_HERE, "assets")

def _data_uri(fname):
    with open(os.path.join(_ASSETS, fname), "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode("ascii")

# Full-resolution, tight-cropped source (see assets/ note) — replaces the
# low-res logo_mark_web.png that caused visible blur when placed small in
# headers/cover/closing. Same artwork, no redesign, just more real pixels.
LOGO_MARK = _data_uri("logo_mark_crisp.png")

CSS = """
:root{
  --espresso:#241A12; --espresso2:#2C2015; --espresso-line:#3d2f20;
  --cream:#FAF5EB; --cream2:#F2E9D8; --cream3:#EDE2CC;
  --ink:#2A2118; --muted:#7D6F5C; --rule:#E3D8C3;
  --gold:#A9824F; --gold-deep:#8C6A3D; --gold-pale:rgba(169,130,79,.09);
  --purple:#5B2986;
  --warn-bg:#F7EBE8; --warn-border:#8C3B32; --warn-label:#8C3B32;
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:#ded6c6;color:var(--ink);direction:rtl;
 font-family:"Heebo","Frank Ruhl Libre",Georgia,serif;font-size:10.4pt;line-height:1.82}
.sheet{max-width:820px;margin:0 auto;background:var(--cream)}
.page{position:relative;padding:16mm 20mm 20mm;min-height:257mm;background:var(--cream)}
.page.dark{background:var(--espresso)}
.page + .page{break-before:page;page-break-before:always}
em,i{font-style:italic}

/* ---------- running header (breadcrumb style) ---------- */
.pagehead{display:flex;justify-content:space-between;align-items:flex-end;
 font-family:"Heebo",sans-serif;font-size:7.4pt;letter-spacing:.16em;color:var(--muted);
 border-bottom:1px solid var(--rule);padding-bottom:10px;margin-bottom:8mm}
.pagehead.on-dark{color:#9c8f7a;border-bottom-color:var(--espresso-line)}
.pagehead .brand{display:flex;align-items:center;gap:8px;text-transform:uppercase;color:var(--ink);font-weight:700}
.pagehead.on-dark .brand{color:#EDE6D8}
.pagehead .brand img{height:15px}
.pagehead .brand .lat{unicode-bidi:isolate}
.pagehead .crumb{color:var(--gold-deep);font-weight:700}
.pagehead.on-dark .crumb{color:var(--gold)}
.pagehead .crumb .num{unicode-bidi:isolate}
.pagehead .org{color:var(--purple);opacity:.72}
.pagehead.on-dark .org{color:#b9a4d6;opacity:.8}

/* ---------- in-flow footer (repeats only where placed; Playwright's own
   footer_template supplies the reliable per-physical-page numbering) ---------- */
.pagefoot{margin-top:16mm;padding-top:10px;border-top:1px solid var(--rule);
 display:flex;justify-content:space-between;font-family:"Heebo",sans-serif;
 font-size:7.2pt;letter-spacing:.1em;color:var(--muted)}
.page.dark .pagefoot{border-top-color:var(--espresso-line);color:#8a7d68}

/* ---------- COVER ---------- */
.cover{min-height:297mm;padding:0;display:flex;flex-direction:column;
 align-items:center;justify-content:center;text-align:center;position:relative}
.cover-mark{width:60px;height:auto;margin-bottom:34px;filter:brightness(0) invert(1);opacity:.95}
.cover-eyebrow{font-family:"Heebo",sans-serif;font-weight:700;font-size:10.5pt;
 letter-spacing:.4em;margin:0 0 24px;color:var(--gold);unicode-bidi:isolate}
.cover-title{font-family:"Frank Ruhl Libre",serif;font-weight:600;font-size:32pt;
 letter-spacing:.01em;margin:0 0 14px;color:#F7F1E4}
.cover-rule{width:56px;height:2px;background:linear-gradient(to left,var(--gold),var(--purple));margin:22px 0}
.cover-sub{font-family:"Heebo",sans-serif;font-weight:300;font-size:10.2pt;
 letter-spacing:.06em;color:#c9bda5;max-width:320px;line-height:1.95}
.cover-tags{position:absolute;bottom:60mm;display:flex;gap:10px}
.cover-tag{border:1px solid var(--espresso-line);color:#a99a7d;font-family:"Heebo",sans-serif;
 font-size:7.4pt;letter-spacing:.14em;padding:4px 12px;border-radius:1px}
.cover-foot{position:absolute;bottom:20mm;font-family:"Heebo",sans-serif;font-size:7.4pt;
 letter-spacing:.16em;color:#7c6f5a;unicode-bidi:isolate}

/* ---------- SECTION DIVIDER (dark, bottom-anchored, ghost numeral) ---------- */
.divider{min-height:257mm;display:flex;flex-direction:column;justify-content:flex-end;
 position:relative;overflow:hidden}
.divider-ghost{position:absolute;inset-inline-end:-6mm;bottom:8mm;font-family:"Frank Ruhl Libre",serif;
 font-weight:700;font-size:230pt;line-height:1;color:var(--gold-pale);z-index:0;user-select:none;unicode-bidi:isolate}
.divider-inner{position:relative;z-index:1;padding-bottom:8mm}
.divider-eyebrow{display:flex;align-items:center;gap:12px;font-family:"Heebo",sans-serif;
 font-size:8.2pt;letter-spacing:.16em;color:var(--gold);margin-bottom:16px}
.divider-eyebrow .dash{width:30px;height:1px;background:var(--gold)}
.divider-title{font-family:"Frank Ruhl Libre",serif;font-size:27pt;font-weight:600;
 max-width:520px;line-height:1.45;margin:0 0 16px;color:#F7F1E4}
.divider-sub{font-family:"Heebo",sans-serif;font-size:9.6pt;color:#b9ac93;
 max-width:420px;line-height:1.9;margin-bottom:18px}
.divider-endrule{width:36px;height:1px;background:var(--espresso-line)}

/* ---------- SECTION HEADING on content pages ---------- */
.eyebrow{font-family:"Heebo",sans-serif;font-size:8pt;letter-spacing:.15em;
 color:var(--gold-deep);font-weight:700;margin-bottom:6px}
h1.sec{font-family:"Frank Ruhl Libre",serif;font-size:20pt;font-weight:600;
 line-height:1.35;margin:0 0 10px}
.secrule{height:1px;background:linear-gradient(to left,var(--gold),transparent);margin:0 0 16px}
h2.sub{display:flex;align-items:center;gap:10px;font-family:"Frank Ruhl Libre",serif;
 font-size:13pt;font-weight:600;color:var(--ink);margin:24px 0 10px}
h2.sub::before{content:"";width:20px;height:1px;background:var(--gold);flex:none}
.body-copy{font-family:"Heebo",sans-serif;font-size:9.8pt;line-height:1.95;
 color:#382c1f;margin:0 0 14px}
strong{font-weight:700;color:var(--ink)}

/* ---------- CARDS (two-up profile style) ---------- */
.cardgrid{display:flex;gap:14px;margin:16px 0}
.cardgrid.stack{flex-direction:column}
.cardgrid.grid2{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.cardgrid.grid3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px}
.cardgrid.grid3 .card{padding:13px 14px}
.cardgrid.grid3 .card-title{font-size:11pt;margin:0 0 6px}
.cardgrid.grid3 .card p{font-size:8.6pt;line-height:1.75}
.card{flex:1;background:var(--cream2);border:1px solid var(--rule);border-top:3px solid var(--gold);
 border-radius:2px;padding:16px 18px;break-inside:avoid-page;page-break-inside:avoid}
.card-label{font-family:"Heebo",sans-serif;font-size:7.6pt;letter-spacing:.13em;
 color:var(--gold-deep);margin-bottom:8px;font-weight:700}
.card-title{font-family:"Frank Ruhl Libre",serif;font-size:12.5pt;font-weight:600;margin:0 0 8px}
.card p{font-family:"Heebo",sans-serif;font-size:9.5pt;color:#4a3d2c;line-height:1.85;margin:0}

/* ---------- KEY-INSIGHT / WARNING callouts ---------- */
.callout{border-inline-start:3px solid var(--gold-deep);background:var(--cream2);
 padding:13px 18px;margin:16px 0;font-family:"Heebo",sans-serif;font-size:9.3pt;
 color:#3d3222;line-height:1.85;break-inside:avoid-page;page-break-inside:avoid}
.callout b{color:var(--ink)}
.callout.warn{border-inline-start-color:var(--warn-border);background:var(--warn-bg);color:#5c2c26}
.callout.warn b{color:var(--warn-label)}
.callout-label{font-style:italic;font-weight:700}

/* ---------- STAT TILE ROW ---------- */
.stats{display:flex;gap:10px;margin:18px 0;break-inside:avoid-page;page-break-inside:avoid}
.stat{flex:1;background:var(--cream2);border:1px solid var(--rule);border-radius:2px;
 padding:14px 8px;text-align:center;break-inside:avoid-page}
.stat-num{font-family:"Frank Ruhl Libre",serif;font-size:16pt;font-weight:700;color:var(--gold-deep);unicode-bidi:isolate}
.stat-cap{font-family:"Heebo",sans-serif;font-size:7.6pt;color:var(--muted);
 margin-top:5px;line-height:1.5}

/* ---------- PROMPT / REFLECTION BOX ---------- */
.prompt{background:var(--cream2);border-radius:2px;padding:14px 18px;margin:14px 0;
 border-inline-start:2px solid var(--gold);break-inside:avoid-page;page-break-inside:avoid}
.prompt-label{font-family:"Heebo",sans-serif;font-size:7.6pt;letter-spacing:.13em;
 color:var(--gold-deep);font-weight:700;margin-bottom:6px}
.prompt-q{font-family:"Heebo",sans-serif;font-size:9.6pt;color:#382c1f;line-height:1.85}
.fine{font-family:"Heebo",sans-serif;font-size:8.5pt;color:var(--muted);
 line-height:1.8;border-inline-start:2px solid var(--rule);padding-inline-start:12px;margin:12px 0;
 break-inside:avoid-page;page-break-inside:avoid}

/* ---------- PROCESS DIAGRAM ---------- */
.process{margin:20px 0}
.pstep{display:flex;gap:16px;align-items:flex-start;padding:13px 0;
 border-bottom:1px solid var(--rule);break-inside:avoid-page;page-break-inside:avoid}
.pstep:last-child{border-bottom:none}
.pnum{flex:none;width:28px;height:28px;border-radius:50%;background:var(--espresso);color:var(--gold);
 font-family:"Frank Ruhl Libre",serif;font-weight:700;font-size:11.5pt;
 display:flex;align-items:center;justify-content:center;unicode-bidi:isolate}
.ptxt{font-family:"Heebo",sans-serif;font-size:9.5pt;color:#382c1f;line-height:1.85;padding-top:3px}

/* ---------- FLOW (operating-model diagram) ---------- */
.flow{display:flex;align-items:center;gap:8px;margin:22px 0 8px}
.flow-stage{flex:1;text-align:center}
.flow-eyebrow{font-family:"Heebo",sans-serif;font-size:7.6pt;letter-spacing:.13em;
 color:var(--gold-deep);font-weight:700;margin-bottom:8px}
.flow-card{background:var(--cream2);border:1px solid var(--rule);border-radius:2px;
 padding:14px 8px;font-family:"Frank Ruhl Libre",serif;font-size:10.5pt;font-weight:600;color:var(--ink)}
.flow-node{width:60px;height:60px;border-radius:50%;background:var(--espresso);color:var(--gold);
 display:flex;align-items:center;justify-content:center;margin:0 auto 8px}
.flow-connector{flex:0 0 22px;height:1px;background:var(--gold);align-self:center;margin-top:20px}
.flow-loop{margin-top:14px;font-family:"Heebo",sans-serif;font-size:8.6pt;color:var(--muted);
 text-align:center;line-height:1.8;padding:0 20px}

/* ---------- CONTRAST ROW (not-vs-is) ---------- */
.contrast{border-radius:2px;padding:11px 16px;margin:10px 0;font-family:"Heebo",sans-serif;
 font-size:9.3pt;break-inside:avoid-page;page-break-inside:avoid}
.contrast.dim{background:var(--cream3);color:var(--muted);border:1px dashed var(--rule)}
.contrast.affirm{background:var(--cream2);border-inline-start:3px solid var(--gold);
 color:var(--gold-deep);font-weight:700;padding:15px 18px;font-size:9.8pt}

/* ---------- PERMISSION PAGE (quiet, typographic) ---------- */
.permission-quote{font-family:"Frank Ruhl Libre",serif;font-style:italic;font-weight:600;
 font-size:19pt;text-align:center;line-height:1.55;color:var(--ink);max-width:520px;margin:34px auto 24px}
.permission-dots{display:flex;justify-content:center;gap:11px;margin:8px 0 10px}
.permission-dot{width:10px;height:10px;border-radius:50%;background:var(--gold)}
.permission-dot.you{background:transparent;border:2px solid var(--purple)}
.permission-cap{text-align:center;font-family:"Heebo",sans-serif;font-size:7.8pt;
 color:var(--muted);letter-spacing:.08em;margin-bottom:28px}

/* ---------- HORIZON (sustainability rings) ---------- */
.horizon-wrap{position:relative;min-height:96mm;display:flex;align-items:center;justify-content:center;overflow:hidden}
.horizon-svg{position:absolute;inset-inline-end:-10mm;top:50%;transform:translateY(-50%);z-index:0;opacity:.9}
.horizon-cap{position:relative;z-index:1;text-align:center;font-family:"Heebo",sans-serif;
 font-size:9.6pt;color:var(--muted);max-width:360px;line-height:1.9}

/* ---------- GENESIS LENSES ---------- */
.lenses{display:flex;gap:10px;margin:20px 0 4px}
.lens{flex:1;border-top:3px solid var(--gold);background:var(--cream2);padding:12px 8px;text-align:center}
.lens.c2{border-top-color:var(--gold-deep)}
.lens.c3{border-top-color:var(--muted)}
.lens.c4{border-top-color:var(--purple)}
.lens-icon{margin:0 auto 8px;width:26px;height:26px}
.lens-label{font-family:"Heebo",sans-serif;font-size:8pt;font-weight:700;color:var(--ink);line-height:1.4}
.lens-converge{display:flex;flex-direction:column;align-items:center;margin:14px 0 6px}
.lens-line{width:1px;height:20px;background:var(--gold)}
.lens-node{width:52px;height:52px;border-radius:50%;background:var(--espresso);color:var(--gold);
 display:flex;align-items:center;justify-content:center;font-family:"Frank Ruhl Libre",serif;
 font-size:8.6pt;font-weight:700;text-align:center;line-height:1.15}

/* ---------- MICRO TABLE (break-even defaults) ---------- */
table.micro{width:100%;border-collapse:collapse;margin:14px 0;font-family:"Heebo",sans-serif;
 font-size:9.2pt;break-inside:avoid-page;page-break-inside:avoid}
table.micro th{text-align:start;font-size:7.6pt;letter-spacing:.1em;color:var(--gold-deep);
 font-weight:700;padding:0 0 8px;border-bottom:1px solid var(--rule)}
table.micro td{padding:10px 0;border-bottom:1px solid var(--rule);vertical-align:top;color:#382c1f}
table.micro td:first-child{color:var(--ink);font-weight:600;width:38%}

/* ---------- DATA TABLE (illustrative forecast example) ---------- */
table.data{width:100%;border-collapse:collapse;margin:3px 0;font-family:"Heebo",sans-serif;
 font-size:8.2pt;break-inside:avoid-page;page-break-inside:avoid}
table.data th{text-align:center;font-size:7pt;letter-spacing:.05em;color:var(--gold-deep);
 font-weight:700;padding:0 5px 6px;border-bottom:1px solid var(--rule)}
table.data td{padding:6px 5px;border-bottom:1px solid var(--rule);text-align:center;color:#382c1f}
table.data td:first-child{color:var(--ink);font-weight:600}
table.data th:last-child,table.data td:last-child{text-align:start}
.tbl-label{font-family:"Heebo",sans-serif;font-size:8pt;letter-spacing:.08em;
 color:var(--gold-deep);font-weight:700;margin:6px 0 1px}

/* ---------- WIDE DATA TABLE (illustrative 12-month forecast, many columns) ---------- */
table.data-full{width:100%;border-collapse:collapse;margin:6px 0;font-family:"Heebo",sans-serif;
 font-size:6.6pt;break-inside:avoid-page;page-break-inside:avoid}
table.data-full th{text-align:center;font-size:6pt;letter-spacing:.01em;color:var(--gold-deep);
 font-weight:700;padding:2px 1px 5px;border-bottom:1px solid var(--rule);white-space:nowrap}
table.data-full td{padding:4.5px 1px;border-bottom:1px solid var(--rule);text-align:center;
 color:#382c1f;white-space:nowrap}
table.data-full td:first-child{color:var(--ink);font-weight:600}
table.data-full th:last-child,table.data-full td:last-child{text-align:start}
table.data-full th.sec-mkt,table.data-full td.sec-mkt{background:rgba(169,130,79,.08)}
table.data-full th.sec-com,table.data-full td.sec-com{background:rgba(140,106,61,.08)}
table.data-full th.sec-ret,table.data-full td.sec-ret{background:rgba(125,111,92,.09)}
table.data-full th.sec-fin,table.data-full td.sec-fin{background:rgba(91,41,134,.06)}
table.data-full th.sec-mkt{border-top:3px solid var(--gold)}
table.data-full th.sec-com{border-top:3px solid var(--gold-deep)}
table.data-full th.sec-ret{border-top:3px solid var(--muted)}
table.data-full th.sec-fin{border-top:3px solid var(--purple)}
.tbl-legend{display:flex;gap:16px;margin:2px 0 6px;font-family:"Heebo",sans-serif;
 font-size:7.4pt;color:var(--muted)}
.tbl-legend .dot{display:inline-block;width:7px;height:7px;border-radius:50%;margin-inline-end:5px}

/* ---------- INTAKE FORM ---------- */
.intake-intro{font-family:"Heebo",sans-serif;font-size:9.6pt;color:var(--muted);
 line-height:1.9;max-width:560px;margin-bottom:6px}
.igroup{margin:20px 0;break-inside:avoid-page;page-break-inside:avoid}
.igroup-head{display:flex;align-items:center;gap:12px;margin-bottom:8px}
.igroup-num{font-family:"Frank Ruhl Libre",serif;background:var(--espresso);color:var(--gold);
 width:26px;height:26px;border-radius:50%;display:flex;align-items:center;justify-content:center;
 font-weight:700;font-size:10pt;flex:none;unicode-bidi:isolate}
.igroup-title{font-family:"Frank Ruhl Libre",serif;font-size:12pt;font-weight:600}
.igroup-note{font-family:"Heebo",sans-serif;font-size:8.2pt;color:var(--gold-deep);
 margin-bottom:6px;margin-inline-start:38px}
.ifields{margin-inline-start:38px;font-family:"Heebo",sans-serif;font-size:9.3pt;
 color:#382c1f;line-height:2.2}
.ifields .f{display:flex;align-items:baseline;gap:8px;border-bottom:1px dotted var(--rule);
 padding:4px 0}
.ifields .f .flabel{flex:none;color:#4a3d2c}
.ifields .f .fline{flex:1;border-bottom:1px solid var(--rule);min-height:13px}

/* ---------- CLOSING (sign-off style) ---------- */
.closing{min-height:257mm;display:flex;flex-direction:column;justify-content:flex-end;
 position:relative;overflow:hidden}
.closing-ghost{position:absolute;inset-inline-end:0mm;bottom:-8mm;font-family:"Frank Ruhl Libre",serif;
 font-weight:700;font-size:210pt;line-height:1;color:var(--gold-pale);z-index:0;user-select:none}
.closing-inner{position:relative;z-index:1;padding-bottom:8mm}
.closing-eyebrow{display:flex;align-items:center;gap:12px;font-family:"Heebo",sans-serif;
 font-size:8.2pt;letter-spacing:.16em;color:var(--gold);margin-bottom:16px}
.closing-eyebrow .dash{width:30px;height:1px;background:var(--gold)}
.closing-title{font-family:"Frank Ruhl Libre",serif;font-size:25pt;font-weight:600;
 line-height:1.4;margin:0 0 16px;color:#F7F1E4}
.closing p{font-family:"Heebo",sans-serif;font-size:9.8pt;color:#c9bda5;line-height:1.95;
 max-width:480px;margin:0 0 22px}
.closing-brand{display:flex;align-items:center;gap:10px;margin-top:10px}
.closing-brand img{height:26px;filter:brightness(0) invert(1);opacity:.9}
.closing-brand .tx{font-family:"Heebo",sans-serif}
.closing-brand .tx .n{font-weight:700;letter-spacing:.14em;font-size:9.5pt;color:#F7F1E4}
.closing-brand .tx .t{font-style:italic;font-size:8.2pt;color:#a99a7d;margin-top:2px}

@page{size:A4;margin:0}
@media print{
 body{background:#fff}
 .sheet{max-width:none}
 .card,.prompt,.callout,.stat,.stats,.pstep,.fine,table.micro{break-inside:avoid}
 h1.sec,h2.sub,.igroup-head,.divider-title,.eyebrow{break-after:avoid}
}
"""

def pagehead(num, title, dark=False):
    cls = "pagehead on-dark" if dark else "pagehead"
    return (f'<div class="{cls}"><span class="brand"><img src="{LOGO_MARK}">'
            f'<span class="lat">LOS GARDIOS</span> · מדריך הלקוח</span>'
            f'<span class="crumb"><span class="num">{num}</span> · {title}</span>'
            f'<span class="org">לוס גרדיוס בע"מ</span></div>')

def pagefoot():
    return '<div class="pagefoot"><span>סודי · חלק ממכלול ההתקשרות</span><span>© לוס גרדיוס בע"מ</span></div>'

PAGES = []

# ==================================================================
# COVER
# ==================================================================
PAGES.append(f'''<div class="page dark cover">
  <img src="{LOGO_MARK}" class="cover-mark">
  <div class="cover-eyebrow">L O S &nbsp; G A R D I O S</div>
  <div class="cover-title">מדריך הלקוח</div>
  <div class="cover-rule"></div>
  <div class="cover-sub">תקציב · מסגרת השקעה · טווח זמן<br>קריאה לפני תחילת הדרך המשותפת</div>
  <div class="cover-tags"><span class="cover-tag">סודי</span><span class="cover-tag">גרסת מדריך 2</span></div>
  <div class="cover-foot">CONFIDENTIAL · LOS GARDIOS GROUP</div>
</div>''')

# ==================================================================
# DIVIDER 01 — How Los Gardios Works
# ==================================================================
PAGES.append('''<div class="page dark divider">
  <div class="divider-ghost">01</div>
  <div class="divider-inner">
    <div class="divider-eyebrow"><span class="dash"></span>פרק 01</div>
    <div class="divider-title">איך לוס גרדיוס עובד</div>
    <div class="divider-sub">מי אנחנו, אילו נכסים ומערכות עומדים מאחורי העבודה, ואיך מורכבת מעטפת המומחים סביב הפרויקט שלכם.</div>
    <div class="divider-endrule"></div>
  </div>
</div>''')

# ==================================================================
# 1.1 — Who we are + the client-controlled principle
# ==================================================================
PAGES.append(f'''<div class="page">
{pagehead("01", "מי אנחנו")}
<div class="eyebrow">זהות</div>
<h1 class="sec">מי אנחנו</h1>
<div class="secrule"></div>
<p class="body-copy">לוס גרדיוס היא קבוצת שירותים מקצועית הפועלת בתחומי המיתוג, השיווק, הפיתוח והמסחר, המעמידה ללקוחותיה החיצוניים צוותים, מתודולוגיות ומערכות קנייניות לצורך קידום עסקיהם. אנחנו עובדים עם כל לקוח כישות עסקית נפרדת (B2B), במסגרת פרויקט מסחרי בתשלום.</p>
<h2 class="sub">העיקרון המנחה: הלקוח קובע את המסגרת</h2>
<p class="body-copy">עיקרון התפעול המרכזי של הארגון פשוט: הלקוח מגדיר את המסגרת הכלכלית והאסטרטגית שבה הוא רוצה ויכול לפעול, והארגון בוחן מה ניתן לבנות באחריות בתוכה — ורק אז, יחד, מגיעים לתוכנית ולמודל מסחרי קונקרטיים. זהו ההפך מהמודל הנפוץ, שבו ספק קובע מראש כמה על הלקוח לשלם.</p>
<div class="callout"><span class="callout-label">בהמשך המדריך:</span> פרק 3 (תקציב, מסגרת השקעה וטווח זמן) מסביר את העיקרון הזה לעומק, כולל האופן שבו הוא בא לידי ביטוי בפועל.</div>
{pagefoot()}
</div>''')

# ==================================================================
# 1.2 — Organization's assets
# ==================================================================
PAGES.append(f'''<div class="page">
{pagehead("01", "נכסי הארגון וההשקעה שביסודם")}
<div class="eyebrow">מה עומד מאחורי העבודה</div>
<h1 class="sec">נכסי הארגון וההשקעה שביסודם</h1>
<div class="secrule"></div>
<p class="body-copy">כדי לספק שירות ברמה גבוהה ועקבית לכל לקוח, אנחנו משקיעים משאבים משמעותיים עוד לפני תחילת ההתקשרות הספציפית עמכם — בגיוס ובהכשרת אנשי מקצוע, בבניית קשרים עסקיים, בפיתוח ידע ותהליכים פנימיים, ובמערכות טכנולוגיות קנייניות (ראו העמוד הבא). ההגנה על נכסים אלה היא הבסיס שמאפשר לנו להמשיך להשקיע באותה רצינות בכל התקשרות, בלי קשר להיקפה.</p>
<div class="cardgrid grid2">
  <div class="card"><div class="card-label">הון אנושי</div><p>הארגון מונה 100+ שותפים ברחבי העולם שעוברים איתור, סינון והכשרה מקצועית מתמשכת (הנפרסת על פני כשלוש שנים), ליווי ופיקוח שוטפים של כל נציג ושותף מטעמנו.</p></div>
  <div class="card"><div class="card-label">רשת קשרים עסקיים</div><p>קשרים עם ספקים, יצרנים, מפיצים ושותפים עסקיים, המבוססים על אמון ומוניטין שנצברים לאורך זמן ולא בבת-אחת (ראו גם Atlas Network בהמשך).</p></div>
  <div class="card"><div class="card-label">מידע סודי</div><p>מבנה תמחור, תהליכים פנימיים, ומידע מצטבר על ספקים ולקוחות.</p></div>
  <div class="card"><div class="card-label">הון אינטלקטואלי ותשתית</div><p>מתודולוגיות, מודלים, תבניות עבודה, ומערכות טכנולוגיות — לרבות מערכות ומודלי בינה מלאכותית בפיתוחנו (ראו העמוד הבא).</p></div>
</div>
<div class="fine">הכלל האופרטיבי: פגיעה מכוונת באחד מהנכסים האלה — למשל שידול של נציג מטעמנו לעבוד ישירות מולכם מחוץ למסגרת הארגון, או עקיפת קשר עסקי שנחשפתם אליו באמצעותנו — מזכה אותנו בפיצוי מוסכם, ללא צורך בהוכחת נזק, לפי הסכומים והתקרות הקבועים בסעיף 11 להסכם. זה אינו חל על ההתקשרות הרגילה שלכם עמנו; זה חל רק על ניצול לרעה מכוון של מה שחשפנו לכם.</div>
{pagefoot()}
</div>''')

# ==================================================================
# 1.3 — Proprietary technology (Neuron, unified)
# ==================================================================
PAGES.append(f'''<div class="page">
{pagehead("01", "טכנולוגיה קניינית ומערכות פנימיים")}
<div class="eyebrow">תשתית תפעולית</div>
<h1 class="sec">טכנולוגיה קניינית ומערכות פנימיים</h1>
<div class="secrule"></div>
<p class="body-copy">מעבר לצוות המומחים שלנו, מפתח הארגון מערכת פנימית קניינית בשם <strong>Neuron</strong> — משלבת תיעוד, ניהול פרויקטים ותקשורת פנימית (ובהם הדוחות התקופתיים שתקבלו), יחד עם מודלים אלגוריתמיים ייעודיים המכונים נוירונים. כל נוירון בנוי לזהות את הדפוסים שמאחורי הנתונים: מיפוי הזדמנויות, חיזוי תוצאות, ותרגום אותות לכדי החלטות ברורות בזמן אמת. ברגע שמודל מגיע לרמת ביטחון ביצוע גבוהה, ניתן להפוך תהליך נתון לאוטומטי — אך המערכת עובדת כי אנשים עובדים: האלגוריתמים פועלים לצד צוות גלובלי של אסטרטגים, אנליסטים ואנשי קריאייטיב שמביאים שיקול דעת, חוש נרטיבי וטעם, וקובעים מתי ואיך תהליך עובר לאוטומציה.</p>
<div class="callout"><span class="callout-label">חשוב שתדעו:</span> המערכת בפיתוח פנימי מתקדם ומשמשת את הארגון פנימית — אינה נמכרת כמוצר תוכנה עצמאי. תפקידה להרחיב את יכולת הצוותים לצפות בדפוסים ולנתח היקפי מידע גדולים (לעיתים במונחי מיליוני עד טריליוני נתונים, כמושג של קנה-מידה — לא כמדד מובטח לכל פרויקט) — לא להחליף שיקול דעת אנושי. מומחי הארגון קובעים, מפקחים ומאשרים את הפעולה בכל שלב; היכולות בפועל תלויות בהיקף הנתונים הזמין ובבשלות המערכת באותו שלב.</div>
<p class="fine">מערכות אלה, לרבות כל שיפור בהן, הן נכס קנייני בלעדי של הארגון בכל עת (סעיף 10(ב) להסכם) — גם כשהן משמשות לתכנון או לביצוע עבורכם באופן ספציפי. אתם מקבלים רישיון שימוש בתוצרים שהופקו באמצעותן — לא בעלות או גישה למערכות עצמן. הארגון אינו חושף כאן פרטים על הארכיטקטורה הטכנית או השיטות הפנימיות של מערכות אלה — אלה סוד מסחרי שלו (סעיף 9 להסכם).</p>
<p class="fine">ייתכן שבמסגרת אספקת השירותים תיחשפו להיבטים מסוימים ממערכות אלה או מתוצרים שהופקו באמצעותן. חשיפה זו כפופה לחובת הסודיות ההדדית שבהסכם: נכסי הארגון — לרבות מערכות Neuron — מהווים "מידע סודי" כהגדרתו בסעיף 9, ואתם מחויבים לשמור עליו בסודיות באותו אופן שהארגון מחויב כלפיכם, הן במהלך ההתקשרות והן חמש שנים לאחריה (וללא הגבלת זמן ביחס לסוד מסחרי — סעיף 9(ה)). החשיפה ניתנת לכם לתועלת במסגרת ההתקשרות בלבד, ואינה מקנה זכות, בעלות או עניין בנכסים עצמם (סעיף 2(ג)).</p>
{pagefoot()}
</div>''')

# ==================================================================
# 1.4 — Atlas Network
# ==================================================================
PAGES.append(f'''<div class="page">
{pagehead("01", "Atlas Network")}
<div class="eyebrow">רשת מסחרית בינלאומית</div>
<h1 class="sec">Atlas Network</h1>
<div class="secrule"></div>
<p class="body-copy">בנוסף לצוות הפנימי, מתחזק הארגון את <strong>Atlas Network</strong> — רשת קשרים מסחריים בינלאומית הפרוסה על פני מדינות מרכזיות, ובהן סין, ארצות הברית, דובאי, פקיסטן, ערב הסעודית, אמריקה הלטינית, אירופה ואחרות.</p>
<p class="body-copy">הרשת כוללת קשרים עם יצרנים, ספקים, מפיצים וגורמי הפצה ומכירה, ומאפשרת לארגון לבחון עבור לקוחותיו אפשרויות במיקור חוץ, הפצה, הרחבה בינלאומית, אופטימיזציית עלויות ואלטרנטיבות בשרשרת אספקה — בהתאם לצרכים הספציפיים של כל פרויקט.</p>
<div class="fine">לא כל הזדמנות ברשת רלוונטית או זמינה לכל לקוח; ההתאמה נבחנת לפי אופי הפרויקט.</div>
{pagefoot()}
</div>''')

# ==================================================================
# 1.5 — Specialist capabilities
# ==================================================================
PAGES.append(f'''<div class="page">
{pagehead("01", "יכולות מומחים")}
<div class="eyebrow">הרכב הצוות לפי צורך</div>
<h1 class="sec">יכולות מומחים</h1>
<div class="secrule"></div>
<p class="body-copy">אנחנו לא בנויים סביב חבילת שירות אחידה. כל התקשרות נבנית סביב הצרכים בפועל של העסק — שילוב שונה של אסטרטגיה, מחקר, שיווק, קריאייטיב, פיתוח ותפעול, בהתאם למה שהפרויקט דורש. הביטוי המובנה ביותר לעיקרון הזה הוא הרכב מעטפת המומחים במחקר Genesis — ראו פרק 3.</p>
{pagefoot()}
</div>''')

# ==================================================================
# DIVIDER 02 — Engagement Models
# ==================================================================
PAGES.append('''<div class="page dark divider">
  <div class="divider-ghost">02</div>
  <div class="divider-inner">
    <div class="divider-eyebrow"><span class="dash"></span>פרק 02</div>
    <div class="divider-title">מודלי ההתקשרות</div>
    <div class="divider-sub">ארבעת המסלולים שההסכם תומך בהם, ולמה גמישות מסחרית היא ארכיטקטורה — לא הנחה.</div>
    <div class="divider-endrule"></div>
  </div>
</div>''')

# ==================================================================
# 2.1 — The four tracks
# ==================================================================
_track_badge = lambda t: f'<div class="igroup-num" style="width:32px;height:32px;font-size:12pt">{t}</div>'
PAGES.append(f'''<div class="page">
{pagehead("02", "ארבעת המסלולים")}
<div class="eyebrow">מסגרות מסחריות נתמכות</div>
<h1 class="sec">ארבעת המסלולים</h1>
<div class="secrule"></div>
<p class="body-copy">התמורה הכלכלית הסופית של כל התקשרות ספציפית נקבעת ונחתמת ב"הצעה" נפרדת, לאחר השלמת מחקר Genesis (פרק 3) — אבל כדאי להכיר כבר עכשיו את מסגרות המודל המסחרי שההסכם תומך בהן.</p>
<div class="cardgrid grid2">
  <div class="card"><div class="card-label">{_track_badge("0")} מסלול 0</div><div class="card-title">מחקר ואסטרטגיה, ללא תקציב שוטף</div><p>תשלום חד-פעמי במחיר בסיס של 10,000$ בתוספת מע"מ (נספח A סעיף 2) — אותו מחקר ואותו שווי כמו במסלולים מבוססי-התקציב; ההבדל הוא באופן המימון בלבד.</p></div>
  <div class="card"><div class="card-label">{_track_badge("A")} מסלול A</div><div class="card-title">ריטיינר קבוע</div><p>תמורה חודשית קבועה ומוסכמת מראש עבור היקף עבודה ומשאבים מוגדרים. מתאים כשאתם מעדיפים ודאות תקציבית מלאה.</p></div>
  <div class="card"><div class="card-label">{_track_badge("B")} מסלול B</div><div class="card-title">מודל משולב</div><p>ריטיינר מופחת + חלוקת ערך (רכיב מבוסס-תוצאות). מתאים כשרוצים לחלוק סיכון והזדמנות, בלי לוותר לגמרי על ודאות תשלום בסיסית.</p></div>
  <div class="card"><div class="card-label">{_track_badge("C")} מסלול C</div><div class="card-title">מודל תוצאות</div><p>התמורה מבוססת בעיקרה על חלוקת ערך/אחוזים, בכפוף למנגנון שייקבע בהצעה. מתאים כשההשתתפות הכלכלית שלנו קשורה ישירות לתוצאה.</p></div>
</div>
<div class="fine">בכל מסלול מבוסס-אחוזים או משולב: פרטי המנגנון המדויק — על מה חל האחוז, מה מפעיל אותו, מהי תקופת ההתחשבנות — ייקבעו ויירשמו ב"הצעה" החתומה עצמה; טבלת התנאים המסחריים שבנספח B קובעת רק את פרמטרי הקלט (תקציב, גבולות גזרה, סובלנות ו-Stop-Loss), לא את מבנה התמורה הסופי.</div>
<div class="callout"><span class="callout-label">לא בטוחים איזה מסלול מתאים?</span> אפשר לסמן "ייקבע בהצעה" ולבקש את המלצתנו (ראו "שני נתיבים אפשריים", פרק 3) — מחקר Genesis מתבצע באותו אופן ובאותו מחיר קבוע, שאינו תלוי במסלול, והמסלול הסופי נקבע עם חתימת ההצעה.</div>
{pagefoot()}
</div>''')

# ==================================================================
# 2.2 — Flexibility + shared growth
# ==================================================================
PAGES.append(f'''<div class="page">
{pagehead("02", "גמישות מסחרית וצמיחה משותפת")}
<div class="eyebrow">ארכיטקטורה, לא הנחה</div>
<h1 class="sec">גמישות מסחרית — ארכיטקטורה, לא הנחה</h1>
<div class="secrule"></div>
<p class="body-copy">כשההזדמנות, ההתאמה האסטרטגית והערך הצפוי לטווח ארוך מצדיקים זאת, אנחנו עשויים לבנות את השתתפותנו בהתקשרות באופן שונה — למשל היקף התחלתי מצומצם שגדל בהדרגה, או שלביות בהתקשרות. אלה מבני התקשרות שהמסמכים המשפטיים תומכים בהם, לא הנחות ולא צעד של רצון טוב — זו ארכיטקטורה מסחרית, שנועדה להתאים את ההתקשרות למציאות של העסק.</p>
<h2 class="sub">צמיחה משותפת — עד כמה שהמבנה המסחרי מאפשר זאת</h2>
<p class="body-copy">כאשר המבנה המסחרי כולל רכיב תלוי-ערך (מסלול B או C), האינטרס הכלכלי שלנו מתואם באופן חלקי עם האינטרס שלכם — ככל שהפרויקט מצליח יותר, כך גדלה גם ההשתתפות הכלכלית שלנו בו. זו הסיבה שאנחנו עשויים להעדיף מבנה כזה כשיש לנו אמון גבוה בפוטנציאל הפרויקט.</p>
<div class="fine">זהו תיאור של תמריץ מבני — לא הבטחה לתוצאה או להצלחה משותפת; הביצועים בפועל תלויים בגורמים רבים, כמפורט בפרק 3.</div>
{pagefoot()}
</div>''')

# ==================================================================
# DIVIDER 03 — Budget / investment / timeline
# ==================================================================
PAGES.append('''<div class="page dark divider">
  <div class="divider-ghost">03</div>
  <div class="divider-inner">
    <div class="divider-eyebrow"><span class="dash"></span>פרק 03</div>
    <div class="divider-title">תקציב, מסגרת השקעה וטווח זמן</div>
    <div class="divider-sub">איך אנחנו חושבים על תקציב, מדוע אנחנו שואלים עליו, ואיך זה מתורגם לתוכנית אמיתית.</div>
    <div class="divider-endrule"></div>
  </div>
</div>''')

# ==================================================================
# 3 — Opening hook (trimmed)
# ==================================================================
PAGES.append(f'''<div class="page">
{pagehead("03", "למה אנחנו שואלים")}
<div class="eyebrow">פתיח</div>
<h1 class="sec">אנחנו לא מתחילים מ"הנה החבילה שלנו והמחיר שלה"</h1>
<div class="secrule"></div>
<p class="body-copy">אנחנו מתחילים מ: ספרו לנו מה אתם מנסים להשיג, כמה אתם באמת מוכנים ויכולים להשקיע, אילו אילוצים קיימים, ומה אתם מאמינים שאפשר. אנחנו נקבע מה ניתן לבנות באחריות בתוך המסגרת הזו.</p>
<p class="body-copy">לפני שאנחנו בונים תוכנית עסקית, שיווקית ופיננסית עבורכם, אנחנו צריכים להבין את המציאות הכלכלית שבתוכה אתם רוצים ויכולים לפעול. המידע הזה לא נועד לקבוע כמה אפשר לגבות מכם — הוא נועד לקבוע מה אפשר לבנות באחריות, בהיקף, בקצב ובמודל שמתאימים לעסק שלכם.</p>
<div class="callout"><span class="callout-label">העיקרון:</span> תקציב גדול יותר עשוי לאפשר היקף רחב יותר — אבל לא תוצאה טובה יותר מאליה. הקשר בין תקציב להיקף העבודה הוא שאלה של תכנון, לא הבטחה.</div>
<p class="body-copy"><strong>רמת תשומת הלב, המקצועיות וההשקעה שלנו בפרויקט שלכם אינה תלויה בגודל התקציב — היא זהה, בכל היקף עבודה.</strong></p>
{pagefoot()}
</div>''')

# ==================================================================
# 4 — NEW: operating-model flow + contrast
# ==================================================================
_flow_icon = '''<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.5">
<circle cx="10.5" cy="10.5" r="6.5"/><line x1="15.3" y1="15.3" x2="21" y2="21"/></svg>'''
PAGES.append(f'''<div class="page">
{pagehead("03", "המודל שלנו")}
<div class="eyebrow">הגישה שלנו</div>
<h1 class="sec">אתם קובעים את המסגרת. אנחנו בוחנים מה אפשר לבנות בתוכה</h1>
<div class="secrule"></div>
<div class="flow">
  <div class="flow-stage"><div class="flow-eyebrow">שלב 1</div><div class="flow-card">אתם<br><span style="font-weight:400;font-size:8.6pt;color:var(--muted)">תקציב · מסגרת · חזון</span></div></div>
  <div class="flow-connector"></div>
  <div class="flow-stage"><div class="flow-eyebrow">שלב 2</div><div class="flow-node">{_flow_icon}</div><div style="font-family:'Heebo',sans-serif;font-size:9pt;font-weight:700">אנחנו בוחנים</div></div>
  <div class="flow-connector"></div>
  <div class="flow-stage"><div class="flow-eyebrow">שלב 3</div><div class="flow-card">יחד<br><span style="font-weight:400;font-size:8.6pt;color:var(--muted)">תוכנית + הצעה</span></div></div>
</div>
<div class="flow-loop">אם המסגרת שהגדרתם אינה תואמת את היקף הפרויקט המבוקש — ננהל איתכם שיחה בתום-לב לפני כל החלטה על המשך התהליך, ולא נבנה עבורכם הצעה שאיננו מאמינים שהיא בת-קיימא.</div>
<h2 class="sub">לא ככה, אלא ככה</h2>
<div class="contrast dim">✕ אנחנו קובעים כמה עליכם לשלם, ואתם מתאימים את עצמכם לזה</div>
<div class="contrast affirm">✓ אתם קובעים את המסגרת הכלכלית. אנחנו בוחנים מה ניתן לבנות באחריות בתוכה — ורק אז מגיעים יחד לתוכנית ולמודל מסחרי קונקרטיים.</div>
<p class="body-copy" style="margin-top:14px">המטרה שלנו היא התקשרות שאתם יכולים לקיים לאורך זמן — לא התקשרות שדוחקת אתכם מעבר ליכולת שלכם.</p>
{pagefoot()}
</div>''')

# ==================================================================
# 5 — NEW: trust + permission
# ==================================================================
PAGES.append(f'''<div class="page">
{pagehead("03", "האמון שלנו מתחיל בכנות")}
<div class="permission-quote">"תנו לנו את המספר האמיתי —<br>לא את המספר שאתם חושבים שאנחנו רוצים לשמוע."</div>
<div class="permission-dots">
  <span class="permission-dot"></span><span class="permission-dot"></span><span class="permission-dot you"></span><span class="permission-dot"></span><span class="permission-dot"></span>
</div>
<div class="permission-cap">אותה תשומת לב. בכל היקף.</div>
<p class="body-copy">מרבית הלקוחות חוששים משתי טעויות הפוכות: להגיד מספר קטן מדי ולהיראות לא רציניים, או להגיד מספר גדול מדי כדי להצדיק את החזון. שתי הטעויות מובילות לאותה תוצאה — תוכנית שלא מתאימה לכם באמת. יש לכך גם השלכה מעשית: לאחר החתימה, התקציב שתקבעו הופך למחויבות תפעולית לשלושה חודשים לפחות — כך שמספר מנופח לא הופך את הפרויקט שלכם למרשים יותר; הוא הופך למחויבות אמיתית שתצטרכו לעמוד בה. <strong>אין כאן מספר "קטן מדי" — יש רק מספר לא מדויק.</strong></p>
<h2 class="sub">חזון גדול, תקציב קטן כרגע</h2>
<p class="body-copy">זה בדיוק המצב שיש לנו מבנה בשבילו. תקציב הוא שאלה של איפה העסק נמצא היום; הזדמנות היא שאלה של לאן הוא יכול להגיע — אלה שני צירים נפרדים, לא אחד. עסק עם פוטנציאל יוצא דופן, נזילות מוגבלת כרגע, הזדמנות שוק ייחודית או חזון מייסד חזק עשוי להצדיק מבנה מסחרי מותאם באותה מידה שעסק עם תקציב גדול יכול שלא להתאים לנו כלל. כשהפער הזה קיים, יש לנו מבנים מסחריים שנבנו בדיוק בשבילו — היקף התחלתי מצומצם, מבנה מבוסס-אחוזים, או שלביות (ראו "שני נתיבים אפשריים" בעמוד הבא). אלה לא הנחות שבות-לב — הן ארכיטקטורה מסחרית. אבל כדי שנוכל להשתמש בהן, אנחנו צריכים את התקציב הנוכחי האמיתי.</p>
<div class="fine">המידע שתמסרו בפרק הזה משמש לתכנון, להערכה ולבניית ה"הצעה" בלבד — ואינו מהווה התחייבות לרכישת שירותים, לתשלום סכום מסוים או להשגת תוצאה עסקית. שום מספר שתרשמו אינו סופי ואינו "נועל" אתכם. הערה זו חלה על כל הלקוחות, ללא תלות במסלול.</div>
{pagefoot()}
</div>''')

# ==================================================================
# 6 — Two paths (trimmed)
# ==================================================================
PAGES.append(f'''<div class="page">
{pagehead("03", "שני נתיבים אפשריים")}
<div class="eyebrow">בחירה</div>
<h1 class="sec">שני נתיבים אפשריים</h1>
<div class="secrule"></div>
<p class="body-copy">יש שתי דרכים לגיטימיות להתחיל את השיחה המסחרית, ואתם בוחרים — שתיהן תקפות באותה מידה:</p>
<div class="cardgrid stack">
  <div class="card"><div class="card-label">נתיב א׳</div>
    <div class="card-title">אתם מגדירים את מסגרת ההשקעה</div>
    <p>למשל: "אנחנו רוצים להשקיע כ-X בחודש למשך כ-Y חודשים" — ואנחנו בונים את התוכנית בתוכה.</p></div>
  <div class="card"><div class="card-label">נתיב ב׳</div>
    <div class="card-title">אתם מבקשים שנציע מודל מסחרי</div>
    <p>אנחנו מציגים מבנה תמחור, ריטיינר או מודל אחר שלדעתנו המקצועית מתאים לפרויקט, ואתם שוקלים אותו. אפשר להשיב על השאלות הבאות בטווחים כלליים, לציין אילוצים בלבד, או להשאיר אותן לשיקול דעתנו המקצועי — אין צורך לנחש מספר.</p></div>
</div>
<p class="body-copy"><strong>גמישות מסחרית — לא הנחה.</strong> כשההזדמנות, ההתאמה האסטרטגית והערך הצפוי לטווח ארוך מצדיקים זאת, הארגון עשוי לבנות את השתתפותו בהתקשרות באופן שונה — למשל מבנה מבוסס-אחוזים, מבנה משולב, היקף התחלתי מצומצם, או שלביות בהתקשרות. אלה מבני התקשרות שהמסמכים המשפטיים תומכים בהם, לא הנחות ולא צעד של רצון טוב — זו ארכיטקטורה מסחרית, שנועדה להתאים את ההתקשרות למציאות של העסק.</p>
{pagefoot()}
</div>''')

# ==================================================================
# 7 — Goals reflection
# ==================================================================
PAGES.append(f'''<div class="page">
{pagehead("03", "היעד והציפיות שלכם")}
<div class="eyebrow">לפני המספרים</div>
<h1 class="sec">היעד והציפיות שלכם</h1>
<div class="secrule"></div>
<p class="body-copy">לפני המספרים, נשמח להבין מה אתם מנסים להשיג.</p>
<div class="prompt"><div class="prompt-label">שאלות למחשבה</div>
<div class="prompt-q">מהי התוצאה העסקית שאתם שואפים אליה?<br>איך תגדירו התקדמות עבור הפרויקט?<br>מהם הדברים החשובים לכם ביותר בו?</div></div>
<p class="fine">התשובות כאן מכוונות אותנו בעדיפויות ובטון של התוכנית שנבנה — הן אינן יעד מדיד או הבטחה להשגת תוצאה; היעדים המדידים בפועל, ככל שייקבעו, ייקבעו בהסכם ובטבלת התנאים המסחריים בלבד.</p>
{pagefoot()}
</div>''')

# ==================================================================
# 8 — Investment framework
# ==================================================================
PAGES.append(f'''<div class="page">
{pagehead("03", "מסגרת ההשקעה שלכם")}
<div class="eyebrow">תשומת הקלט המרכזית</div>
<h1 class="sec">מסגרת ההשקעה שלכם</h1>
<div class="secrule"></div>
<p class="body-copy">השדה החשוב ביותר עבורנו כדי להתחיל לתכנן הוא <strong>התקציב החודשי</strong>; שאר השאלות כאן עוזרות לנו לדייק את התוכנית, וניתן לחדד אותן יחד איתנו בהמשך.</p>
<div class="prompt"><div class="prompt-label">ספרו לנו</div>
<div class="prompt-q">מהו התקציב החודשי המועדף עליכם?<br>האם יש היקף השקעה כולל שאתם מתכננים אליו?<br>מהו טווח הגמישות שלכם — תקציב קבוע, או מרחב תמרון בכפוף לאישורכם?<br>התקציב שאתם מוסרים כולל או לא כולל עלויות חיצוניות מסוימות (כגון תקציבי מדיה המועברים ישירות לפלטפורמות)?</div></div>
<p class="body-copy">המספר שתמסרו הוא נקודת פתיחה לתכנון בלבד — לא הצעת מחיר ולא רצפה מחייבת. <strong>תזכורת לפני שאתם עונים: אין כאן "תשובה גדולה יותר שנכון לתת". מספר קטן ואמיתי מאפשר לנו לבנות תוכנית שמדויקת לגודל הזה; מספר מנופח רק מרחיק את התוכנית מהמציאות שלכם.</strong></p>
<div class="eyebrow" style="margin-top:22px">מסגרת A/B/C — מה שכדאי לדעת כבר עכשיו</div>
<div class="stats">
  <div class="stat"><div class="stat-num">3</div><div class="stat-cap">חודשים · התחייבות תקציב מינימלית</div></div>
  <div class="stat"><div class="stat-num">30</div><div class="stat-cap">יום · הודעה מראש להפחתת תקציב</div></div>
</div>
<p class="fine">זה קיים כדי ששנינו נוכל לתכנן — לא כדי לגרום לכם להרגיש נעולים. זהו תנאי מההסכם עצמו (נספח B), לא תנאי מהפרק הזה — אך כדאי שתכירו אותו כבר עכשיו.</p>
<div class="callout"><span class="callout-label">מסלול 0 בלבד:</span> אם בחרתם ברכישת מחקר Genesis חד-פעמית בלבד, ללא תקציב שוטף (נספח A סעיף 2) — פרקי המשנה מכאן ועד "נקודת האיזון" (כולל) אינם חלים עליכם, ואינכם נדרשים למלא את השדות הנוגעים אליהם. גם דמי ההשתתפות העצמית שיוזכרו בהמשך שייכים למסלולים A/B/C בלבד. אפשר לדלג ישירות לתהליך שבסוף הפרק.</div>
{pagefoot()}
</div>''')

# ==================================================================
# 9 — Timeline
# ==================================================================
PAGES.append(f'''<div class="page">
{pagehead("03", "טווח הזמן שלכם")}
<div class="eyebrow">תכנון</div>
<h1 class="sec">טווח הזמן שלכם</h1>
<div class="secrule"></div>
<p class="body-copy">פרויקט עסקי רציני כולל בדרך כלל שלבי מחקר, בדיקה, פיתוח, כניסה לשוק, איסוף נתונים ואופטימיזציה — לפני שאפשר למדוד את האפקט המסחרי שלו בבירור.</p>
<div class="prompt"><div class="prompt-label">ספרו לנו</div>
<div class="prompt-q">מהי התקופה שאתם מתכננים לפעול בה?<br>האם יש מועדים עסקיים משמעותיים שכדאי שנכיר?</div></div>
<p class="fine">זהו שיח תכנוני כללי בלבד. המספר המדויק שישמש בפועל למדידת ביצועים הוא <strong>תקופת הסובלנות</strong> שתקבעו בעמוד הבא, ותירשם בטבלת התנאים המסחריים.</p>
{pagefoot()}
</div>''')

# ==================================================================
# 10 — NEW: sustainability principle (horizon rings)
# ==================================================================
_rings = []
_radii = [14, 24, 35, 47, 60]
for i, r in enumerate(_radii):
    t = i / (len(_radii) - 1)
    # gold -> purple stroke gradient across rings
    color = f"rgb({int(169+(91-169)*t)},{int(130+(41-130)*t)},{int(79+(134-79)*t)})"
    _rings.append(f'<circle cx="70" cy="70" r="{r}" fill="none" stroke="{color}" stroke-opacity="{0.55-0.07*i:.2f}" stroke-width="1"/>')
_horizon_svg = f'<svg class="horizon-svg" width="140" height="140" viewBox="0 0 140 140">{"".join(_rings)}<circle cx="70" cy="70" r="4" fill="var(--gold)"/></svg>'
PAGES.append(f'''<div class="page">
{pagehead("03", "העיקרון שמנחה אותנו")}
<div class="eyebrow">עמדה שקופה</div>
<h1 class="sec">לא למצות עד הסוף</h1>
<div class="secrule"></div>
<div class="horizon-wrap">{_horizon_svg}
<div class="horizon-cap">נאמר את זה בגלוי: יש לנו אינטרס ברור לא לדחוף אתכם למצות את התקציב החודשי. לקוח שמיצה את תזרים המזומנים שלו לא ממשיך להשקיע ברבעון הבא — מיצוי מלא היום עולה לנו בלקוח לטווח ארוך, בשביל חשבונית גדולה יותר לטווח קצר.</div></div>
<p class="body-copy">זו לא רק עמדה ערכית מצידנו — זה ההיגיון הכלכלי שמניע אותנו לשמר את יכולתו של העסק להמשיך להשקיע, לפעול ולצמוח. וזו גם הסיבה שברירת המחדל התפעולית שלנו, בכל התקשרות, היא לפעול <strong>בנקודת איזון</strong> ולא במיצוי תקציב מלא — לא רק כמשפט כאן, אלא כתוב במנגנון עצמו (ראו "נקודת האיזון" בהמשך).</p>
{pagefoot()}
</div>''')

# ==================================================================
# 11 — Tolerance (redesigned, plain-language first, neutral deficit callout)
# ==================================================================
PAGES.append(f'''<div class="page">
{pagehead("03", "רמת ותקופת הסובלנות שלכם")}
<div class="eyebrow">גמישות סביב רווחיות</div>
<h1 class="sec">רמת ותקופת הסובלנות שלכם</h1>
<div class="secrule"></div>
<p class="body-copy"><strong>במילים פשוטות:</strong> יש לכם תקופה מוסכמת מראש שבה מותר לנו לבנות ולבחון בלי לרדוף אחרי רווח מיידי — אבל יש לזה שני בלמים מובנים שמגנים עליכם. הבלם הראשון: גם בתקופה הזו, ברירת המחדל היא שאנחנו פועלים בנקודת איזון — לא גורמים לכם הפסד בכוונה, גם אם עוד אין רווח. הבלם השני: אם תבחרו במפורש לרדת מתחת לאיזון כדי להאיץ בנייה, תמיד תיקבע תקרה מוסכמת מראש (Stop-Loss) שאסור לחרוג ממנה. במילים אחרות: אתם קובעים כמה "מרחב נשימה" לתת למודל, ואנחנו לא יכולים לעבור את התקרה שקבעתם — לא משנה מה.</p>
<p class="fine">לדוגמה: תקציב של 20,000 ₪ לחודש ותקופת סובלנות של חמישה חודשים אומרים שבמהלך התקופה הזו, אנחנו רשאים להשתמש בתקציב הזמין כדי לבנות, לבחון ולהרחיב את הפעילות — גם אם היא עדיין לא מניבה רווח, ותמיד בתוך הבלמים שלמעלה.</p>
<div class="callout"><span class="callout-label">ברירת המחדל: נקודת איזון, לא הפסד.</span> גם בתוך תקופת הסובלנות, היעד השוטף הוא לפעול בנקודת האיזון — לא לייצר רווח מלאכותי ולא לייצר הפסד במתכוון. הסובלנות מקנה גמישות סביב ציפיית הרווחיות; היא אינה אישור להפסיד כסף.</div>
<div class="callout"><span class="callout-label">גירעון זמני — רק אם תבחרו זאת במפורש, ותמיד עם תקרה.</span> לקוחות מסוימים מעדיפים להטות את מלוא התקציב לבנייה והרחבה בתקופה הראשונה, גם אם זה אומר גירעון תפעולי זמני ולא רק היעדר רווח. זו העדפה עסקית לגיטימית — אך שונה מברירת המחדל, ותצוין במפורש עם מסגרת ותקרה מוסכמות מראש. התקרה שתיקבע היא רף ה-Stop-Loss התפעולי לאותה תקופה — לא מנגנון נוסף עליו.</div>
<div class="prompt"><div class="prompt-label">ספרו לנו</div>
<div class="prompt-q">כמה זמן אתם מוכנים לתת למודל להתפתח (תקופת סובלנות)?<br>אתם מעדיפים שנתמקד בהגעה מהירה לרווחיות, או בבנייה והרחבה תוך הישארות בנקודת האיזון (רמת סובלנות: שמרנית / מאוזנת / אגרסיבית / הרחבה מרבית)?<br>אם רלוונטי — האם אתם מוכנים לגירעון זמני בפועל, ובאיזו תקרה?</div></div>
<p class="fine">חשוב שתדעו: זה לא אומר שאתם מוותרים על זכות כלשהי. בכל עת, גם בתוך תקופת הסובלנות, תוכלו לעצור פעילות, לבחון תוצאות ולסיים את ההתקשרות בהתאם לתנאי ההסכם וההצעה. רמת ותקופת הסובלנות, וגירעון זמני מוסכם אם הוסכם, יירשמו בטבלת התנאים המסחריים (נספח B); אף אחד מהם אינו יוצר מנגנון משפטי חדש מעבר לקבוע שם.</p>
{pagefoot()}
</div>''')

# ==================================================================
# 12 — Financial boundaries
# ==================================================================
PAGES.append(f'''<div class="page">
{pagehead("03", "גבולות פיננסיים")}
<div class="eyebrow">הגנה עליכם</div>
<h1 class="sec">גבולות פיננסיים</h1>
<div class="secrule"></div>
<p class="body-copy">זהו שדה אופציונלי, שתפקידו להגן עליכם.</p>
<div class="prompt"><div class="prompt-label">ספרו לנו</div>
<div class="prompt-q">מהו הסכום שאתם לא רוצים לחרוג ממנו?<br>האם יש שינויים בתקציב שדורשים אישור מפורש שלכם מראש, גם אם לדעתנו המקצועית הם משרתים את הפרויקט?</div></div>
<p class="body-copy">לא חובה לנקוב בתקרה — גם השארת השדה פתוח היא תשובה לגיטימית.</p>
<div class="eyebrow" style="margin-top:18px">ברירות המחדל, אם לא תיקבע תקרה</div>
<div class="stats">
  <div class="stat"><div class="stat-num">30</div><div class="stat-cap">יום · תקופת מדידת Stop-Loss</div></div>
  <div class="stat"><div class="stat-num">10%</div><div class="stat-cap">חריגה מותרת מהתקציב החודשי</div></div>
</div>
<p class="fine">הגבולות שתגדירו כאן ישמשו לקביעת רף ה-Stop-Loss ותקופת המדידה שלו, ויחייבו את הארגון לעצור או לצמצם פעילות בהתאם.</p>
{pagefoot()}
</div>''')

# ==================================================================
# 13 — NEW: oversight & reporting
# ==================================================================
PAGES.append(f'''<div class="page">
{pagehead("03", "בקרה ודיווח שוטף")}
<div class="eyebrow">מה קורה אחרי החתימה</div>
<h1 class="sec">בקרה ודיווח שוטף</h1>
<div class="secrule"></div>
<p class="body-copy">כדי שתוכלו לעקוב אחרי הפרויקט בלי להיות מעורבים בכל החלטה תפעולית יומיומית, ההסכם קובע כמה מנגנוני בקרה קבועים — כדאי שתכירו אותם כבר בשלב הזה:</p>
<div class="cardgrid grid2">
  <div class="card"><div class="card-label">דיווח שוטף</div><p>דוח ביצועים חודשי תמציתי אחד לפחות, וסקירה אסטרטגית רבעונית אחת לפחות — הוצאה בפועל, תוצאות ומדדי רווחיות/נקודת איזון מול התוכנית. הדוחות מועברים בכתב, באמצעות מערכת Neuron (פרק 1) ו/או בדוא"ל לנציג המוסמך שלכם.</p></div>
  <div class="card"><div class="card-label">כניסה לערוץ חדש</div><p>גם בתוך התקציב שאושר, כניסה לערוץ שיווקי או מסחרי חדש שלא נכלל בתוכנית שאושרה טעונה אישור מפורש שלכם מראש ובכתב.</p></div>
  <div class="card"><div class="card-label">אם נחצה רף ה-Stop-Loss</div><p>הפעילות בתשלום תיעצר או תצומצם תוך יום עסקים אחד, ותקבלו הודעה בכתב המפרטת את הגורם וחלופה להמשך; חידוש הפעילות טעון אישורכם.</p></div>
  <div class="card"><div class="card-label">אתם יכולים לעצור בכל עת</div><p>עצירה יזומה מצדכם מתבצעת תוך יום עסקים אחד מבקשתכם; עד חמישה ימי עסקים בחודש אינה נחשבת הפחתת תקציב ואינה הפרה מצדכם.</p></div>
</div>
{pagefoot()}
</div>''')

# ==================================================================
# 14 — Break-even (tightened, micro-table)
# ==================================================================
PAGES.append(f'''<div class="page">
{pagehead("03", "נקודת האיזון (Break-Even)")}
<div class="eyebrow">כלי תכנון, לא הבטחה</div>
<h1 class="sec">נקודת האיזון (Break-Even)</h1>
<div class="secrule"></div>
<p class="body-copy"><strong>מה זה אומר עבורכם בפועל:</strong> תחשבו על נקודת האיזון כמו מד דלק, לא כמו יעד רווח. כל עוד עלות הרכישה של לקוח לא עוברת את מה שהלקוח הזה שווה לכם בממוצע — אנחנו בטווח הבטוח. זה לא אומר שיש רווח נקי גדול; זה אומר שאנחנו לא שורפים כסף כדי להביא לקוחות. זהו כלי תכנון, <strong>לא הבטחה לרווחיות ולא תחזית מובטחת</strong>.</p>
<p class="body-copy">ובמונחים מדויקים: נקודת האיזון היא נקודת ייחוס תכנונית — כל עוד עלות הרכישה בפועל אינה עולה על שווי העסקה הממוצע כפול שיעור הרווח הגולמי שלכם, הפעילות נחשבת בנקודת האיזון או מעליה.</p>
<table class="micro">
  <tr><th>שדה</th><th>ברירת מחדל אם לא יימסר</th></tr>
  <tr><td>שיעור הרווח הגולמי (לפני הוצאות קבועות)</td><td><strong>אין ברירת מחדל.</strong> מנגנון נקודת האיזון כולו לא יופעל</td></tr>
  <tr><td>שווי עסקה ממוצע (AOV)</td><td><strong>יש</strong> — השווי שייקבע במחקר Genesis שלכם</td></tr>
</table>
<div class="prompt"><div class="prompt-label">ספרו לנו, אם ידוע לכם</div>
<div class="prompt-q">מהו שיעור הרווח הגולמי שלכם?<br>מהו שווי העסקה הממוצע שלכם, או שנסתמך על מחקר Genesis?</div></div>
<p class="fine">נקודת האיזון היא רצפה, לא תקרה — אפשר וכדאי להגדיר גם יעדי רווחיות נוספים מעליה. ככל שנקודת האיזון וההגדרות הפיננסיות רשומות בהסכם ובטבלת התנאים המסחריים — הן אלה שיחייבו, לא ההסברים הכלליים כאן.</p>
{pagefoot()}
</div>''')

# ==================================================================
# 14b — NEW: Illustrative forecast example table (real methodology,
# section-color-coded: marketing / commerce / returning customers / financial)
# ==================================================================
_FORECAST_COLS = [
    ("חודש", None),
    ("תקציב", "mkt"), ("CPM", "mkt"), ("חשיפה", "mkt"), ("CTR", "mkt"), ("מבקרים", "mkt"), ("ROAS", "mkt"),
    ("יחס המרה", "com"), ("המרות", "com"), ("CPA", "com"), ("ערך מוצר", "com"), ("פריטים/עגלה", "com"), ("AOV", "com"),
    ("יחס שימור", "ret"), ("רכישות חוזרות", "ret"), ('סה"כ המרות', "ret"),
    ("הכנסות", "fin"), ("הוצ' קבועות", "fin"), ('סה"כ הוצאות', "fin"), ("רווח", "fin"), ("ROI", "fin"),
]
_FORECAST_ROWS = [
    [1, "15,000 ₪", "20 ₪", "750,000", "1.8%", "13,500", "3.00", "1.2%", "162", "93 ₪", "93 ₪", "3",
     "278 ₪", "–", "–", "162", "45,000 ₪", "4,000 ₪", "51,000 ₪", "-6,000 ₪", "-12%"],
    [2, "20,000 ₪", "20 ₪", "1,000,000", "1.7%", "17,000", "3.50", "1.4%", "238", "84 ₪", "98 ₪", "3",
     "294 ₪", "8%", "13", "251", "70,000 ₪", "4,500 ₪", "74,000 ₪", "-4,000 ₪", "-5%"],
    [3, "26,000 ₪", "19 ₪", "1,368,000", "1.5%", "20,500", "3.85", "1.6%", "328", "79 ₪", "102 ₪", "3",
     "305 ₪", "12%", "29", "357", "100,000 ₪", "5,000 ₪", "93,000 ₪", "7,000 ₪", "8%"],
    [4, "34,000 ₪", "19 ₪", "1,789,000", "1.4%", "25,000", "4.12", "1.8%", "450", "76 ₪", "104 ₪", "3",
     "311 ₪", "16%", "52", "502", "140,000 ₪", "5,500 ₪", "119,000 ₪", "21,000 ₪", "18%"],
    [5, "42,000 ₪", "18 ₪", "2,333,000", "1.2%", "28,000", "4.40", "2.0%", "560", "75 ₪", "110 ₪", "3",
     "330 ₪", "19%", "86", "646", "185,000 ₪", "6,000 ₪", "147,000 ₪", "38,000 ₪", "26%"],
    [6, "50,000 ₪", "18 ₪", "2,778,000", "1.2%", "33,000", "4.60", "2.1%", "693", "72 ₪", "111 ₪", "3",
     "332 ₪", "21%", "118", "811", "230,000 ₪", "6,500 ₪", "174,000 ₪", "56,000 ₪", "32%"],
    [7, "58,000 ₪", "17 ₪", "3,412,000", "1.1%", "37,500", "4.66", "2.2%", "825", "70 ₪", "109 ₪", "3",
     "327 ₪", "23%", "159", "984", "270,000 ₪", "7,000 ₪", "200,000 ₪", "70,000 ₪", "35%"],
    [8, "65,000 ₪", "17 ₪", "3,824,000", "1.1%", "42,000", "4.69", "2.2%", "924", "70 ₪", "110 ₪", "3",
     "330 ₪", "24%", "198", "1,122", "305,000 ₪", "7,000 ₪", "229,000 ₪", "76,000 ₪", "33%"],
    [9, "70,000 ₪", "17 ₪", "4,118,000", "1.0%", "41,200", "4.79", "2.3%", "948", "74 ₪", "118 ₪", "3",
     "353 ₪", "25%", "231", "1,179", "335,000 ₪", "7,500 ₪", "258,000 ₪", "77,000 ₪", "30%"],
    [10, "76,000 ₪", "16 ₪", "4,750,000", "1.0%", "47,500", "4.80", "2.3%", "1,093", "70 ₪", "111 ₪", "3",
     "334 ₪", "26%", "246", "1,339", "365,000 ₪", "7,500 ₪", "285,000 ₪", "80,000 ₪", "28%"],
    [11, "82,000 ₪", "16 ₪", "5,125,000", "0.9%", "46,100", "4.82", "2.3%", "1,060", "77 ₪", "124 ₪", "3",
     "373 ₪", "27%", "295", "1,355", "395,000 ₪", "8,000 ₪", "313,000 ₪", "82,000 ₪", "26%"],
    [12, "88,000 ₪", "16 ₪", "5,500,000", "0.9%", "49,500", "4.83", "2.3%", "1,139", "77 ₪", "124 ₪", "3",
     "373 ₪", "28%", "297", "1,436", "425,000 ₪", "8,000 ₪", "340,000 ₪", "85,000 ₪", "25%"],
]
_forecast_head_cells = ''.join(
    f'<th class="sec-{grp}">{label}</th>' if grp else f'<th>{label}</th>'
    for label, grp in _FORECAST_COLS
)
_forecast_body_rows = []
for _row in _FORECAST_ROWS:
    _cells = ''.join(
        f'<td class="sec-{grp}">{val}</td>' if grp else f'<td>{val}</td>'
        for (label, grp), val in zip(_FORECAST_COLS, _row)
    )
    _forecast_body_rows.append(f'<tr>{_cells}</tr>')
_FORECAST_TABLE_HTML = (
    '<table class="data-full">'
    f'<tr>{_forecast_head_cells}</tr>'
    + ''.join(_forecast_body_rows)
    + '</table>'
)

# ==================================================================
# 14b — NEW: Illustrative forecast example table
# ==================================================================
PAGES.append(f'''<div class="page">
{pagehead("03", "דוגמה להמחשה: תוכנית לאורך זמן")}
<div class="eyebrow">להמחשה בלבד — לא תחזית</div>
<h1 class="sec">כך נראית תוכנית לאורך זמן</h1>
<div class="secrule" style="margin-bottom:6px"></div>
<div class="callout" style="margin:6px 0;padding:8px 16px"><span class="callout-label">דוגמה להמחשה בלבד — לא תחזית:</span> הטבלה שלהלן בנויה לפי אותם מדדים, שמות וקטגוריות (שיווק, מסחר, לקוחות חוזרים, פיננסי) שבהם משתמש הארגון בפועל במודל התכנון הפיננסי הפנימי שלו, ומציגה 12 חודשים בצורת עקומה ריאלית — הפסד קל בהתחלה, מעבר לנקודת איזון, שיא, והתייצבות — בדיוק כפי שתוכנית עבודה אמיתית מתפתחת. עם זאת, המספרים עצמם מומצאים להמחשה בלבד: הטבלה אינה משקפת פרויקט או לקוח אמיתי, ואינה מהווה הבטחה או התחייבות לתוצאה כלשהי בפרויקט שלכם.</div>
<div class="tbl-legend">
  <span><span class="dot" style="background:var(--gold)"></span>שיווק</span>
  <span><span class="dot" style="background:var(--gold-deep)"></span>מסחר</span>
  <span><span class="dot" style="background:var(--muted)"></span>לקוחות חוזרים</span>
  <span><span class="dot" style="background:var(--purple)"></span>פיננסי</span>
</div>
{_FORECAST_TABLE_HTML}
<p class="fine">שימו לב לצורת העקומה: הפסד קל בחודשים הראשונים (שלב למידה), מעבר לנקודת איזון, ואז שיפור הדרגתי ב-ROI ככל שמצטבר יותר מידע ונבנית תשתית לקוחות חוזרים — בדיוק העיקרון שהוסבר למעלה. התוכנית שתקבלו בפועל, בסיום מחקר Genesis שלכם, תיראה באותה צורה — אבל תהיה בנויה על הנתונים האמיתיים של העסק שלכם, לא על הדוגמה הכללית שלמעלה.</p>
{pagefoot()}
</div>''')

# ==================================================================
# 15 — NEW: Genesis specialist lenses
# ==================================================================
_icon_a = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="var(--gold-deep)" stroke-width="1.5"><rect x="4" y="12" width="3" height="7"/><rect x="10.5" y="8" width="3" height="11"/><rect x="17" y="4" width="3" height="15"/></svg>'
_icon_b = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="var(--gold-deep)" stroke-width="1.5"><path d="M3 12h4l3-7 4 14 3-7h4"/></svg>'
_icon_c = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="var(--muted)" stroke-width="1.5"><circle cx="12" cy="9" r="4"/><path d="M5 20c1-3.5 4-5 7-5s6 1.5 7 5"/></svg>'
_icon_d = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="var(--purple)" stroke-width="1.5"><path d="M4 19l4-9 4 5 4-8 4 12"/></svg>'
PAGES.append(f'''<div class="page">
{pagehead("03", "מה עומד מאחורי מחקר Genesis")}
<div class="eyebrow">לא נקודת מבט אחת</div>
<h1 class="sec">כמה עדשות מקצועיות, בו-זמנית</h1>
<div class="secrule"></div>
<p class="body-copy">מחקר Genesis אינו נשען על נקודת מבט בודדת. הוא מבוצע באמצעות מעטפת מומחים רב-תחומית — ארבעה תחומים בוחנים את ההזדמנות שלכם, כל אחד דרך העדשה שלו, לפני שהתובנות מתכנסות לכדי תוכנית אחת.</p>
<div class="lenses">
  <div class="lens"><div class="lens-icon">{_icon_a}</div><div class="lens-label">אנליטיקה<br>ומחקר</div></div>
  <div class="lens c2"><div class="lens-icon">{_icon_b}</div><div class="lens-label">שיווק<br>ופרסום</div></div>
  <div class="lens c3"><div class="lens-icon">{_icon_c}</div><div class="lens-label">קריאייטיב ופסיכולוגיה צרכנית</div></div>
  <div class="lens c4"><div class="lens-icon">{_icon_d}</div><div class="lens-label">אסטרטגיה ופיתוח עסקי</div></div>
</div>
<div class="lens-converge"><div class="lens-line"></div><div class="lens-node">התוכנית</div></div>
<p class="body-copy" style="text-align:center;color:var(--muted);font-size:9pt">תוכנית עסקית, שיווקית ופיננסית אחת — לא מבט בודד וגנרי על העסק שלכם</p>
{pagefoot()}
</div>''')

# ==================================================================
# 15.1 — NEW: Genesis output rights (two-layer: explanation + operative rule)
# ==================================================================
PAGES.append(f'''<div class="page">
{pagehead("03", "מה מקבלים, ומה זה לא כולל")}
<div class="eyebrow">שקיפות מלאה</div>
<h1 class="sec">מה מקבלים, ומה זה לא כולל</h1>
<div class="secrule"></div>
<p class="body-copy"><strong>מה זה אומר עבורכם בפועל:</strong> תקבלו תוכנית עסקית, שיווקית ופיננסית מלאה — תוצר אנליטי אמיתי, לא רק שלב מקדים לקראת הצעת מחיר. תוכלו לקרוא אותה, ללמוד ממנה, ולהחליט על בסיסה אם להמשיך. גם אם תחליטו שלא להמשיך, לא יחול עליכם חיוב נוסף מעבר לדמי ההשתתפות העצמית ששילמתם (נספח A סעיף 1).</p>
<div class="callout warn"><span class="callout-label">מה זה לא אומר:</span> קבלת התוכנית אינה מקנה לכם רישיון ליישם אותה באופן עצמאי — בעצמכם, באמצעות חברה קשורה או באמצעות צד שלישי — כי אנחנו נושאים ב-95% מעלות המחקר עוד לפני שאנחנו יודעים אם תמשיכו. בחרתם שלא להמשיך לביצוע בפועל מולנו: יישום עצמאי של מחקר Genesis, האסטרטגיה או ההצעה שהוכנו עבורכם טעון אישור מוקדם ובכתב מאיתנו, או רכישת רישיון יישום עצמאי (Buyout, ראו בהמשך) — למשך <strong>עשרים וארבעה (24) חודשים</strong> ממועד מסירת המחקר, לכל מחקר בנפרד (נספח A סעיף 3(א)). מגבלה זו אינה חלה על יישום המבוסס על ידע כללי, מגמות שוק פומביות, או מידע שהיה בידיכם כדין קודם לכן.</div>
<h2 class="sub">רישיון היישום העצמאי (Buyout)</h2>
<p class="body-copy">בכל עת, ניתן לרכוש מאיתנו רישיון עולמי, בלתי-ייחודי ולצמיתות ליישום עצמאי של תוצרי מחקר מסוים, במחיר השווה לשוויו המלא (10,000$) בניכוי דמי ההשתתפות העצמית וכל תמורה ששולמה כבר בגינו — כלומר 9,500$ עבור מי שביצע Genesis בלבד (נספח A סעיף 3(ב)). <strong>לקוחות מסלול 0</strong> ששילמו את מלוא התמורה נחשבים כמי שמימשו את ה-Buyout באופן אוטומטי, ללא צורך בפעולה נוספת, והמגבלה שלעיל אינה חלה עליהם כלל. בעלותנו במודלים, באלגוריתמים ובמערכות Neuron נותרת בידינו בכל מקרה, ואינה נמכרת במסגרת ה-Buyout.</p>
<div class="fine"><strong>המשכתם אלינו לביצוע בפועל?</strong> אתם ממשיכים ליישם את התוכנית דרכנו, כך שהמגבלה שלעיל אינה רלוונטית כל עוד אותה התקשרות ספציפית נמשכת — אך זה אינו שחרור קבוע ובלתי-תלוי ממנה: הסתיימה ההתקשרות בתוך 24 החודשים ממועד מסירת המחקר, עשויה המגבלה לחול מחדש ביחס להמשך יישום עצמאי, מעבר לתוצרים שכבר נמסרו ושולמו במלואם (שבהם יש לכם רישיון קבוע לשימוש הרגיל בעסקכם, סעיף 10(ב) להסכם). <strong>סודיות:</strong> מחקר Genesis ותוצריו הם מידע סודי לכל דבר ועניין (סעיף 9 להסכם) — מיועדים לשימושכם הפנימי בלבד.</div>
<p class="fine"><strong>מתי נדרש מחקר Genesis נפרד:</strong> לכל פרויקט, מותג או יחידה עסקית הדורש מיצוב, קהל יעד, אסטרטגיה שיווקית או מודל הכנסה נפרדים, או שוק גיאוגרפי/רגולטורי נפרד — אך לא לגיוון פנימי באותו מותג או פרויקט (נספח A סעיף 1(ה)). מספר המחקרים וזהותם ייקבעו מראש בתום-לב ויירשמו בטבלת התנאים המסחריים; מחקר נוסף שהתברר תוך כדי עבודה ייערך ויחויב אך ורק לאחר אישורכם בכתב.</p>
{pagefoot()}
</div>''')

# ==================================================================
# 16 — Process diagram
# ==================================================================
PAGES.append(f'''<div class="page">
{pagehead("03", "מהמדריך להצעה")}
<div class="eyebrow">התהליך</div>
<h1 class="sec">מהמדריך להצעה</h1>
<div class="secrule"></div>
<div class="process">
  <div class="pstep"><div class="pnum">1</div><div class="ptxt">אתם מספרים לנו את המסגרת שלכם — תקציב, מטרות, טווח זמן, סובלנות וגבולות — בטופס הקליטה שבסוף מדריך זה; הנתונים מועתקים ומאושרים בטבלת התנאים המסחריים שבנספח B להסכם.</div></div>
  <div class="pstep"><div class="pnum">2</div><div class="ptxt">עם חתימת הסכם ההתקשרות ותשלום הרלוונטי למסלולכם (דמי ההשתתפות העצמית במסלולים A/B/C, או מחיר המחקר המלא במסלול 0), אנחנו עורכים את מחקר Genesis באמצעות מעטפת המומחים הרב-תחומית, ובוחנים מה ניתן לבנות באחריות בתוך המסגרת שהגדרתם.</div></div>
  <div class="pstep"><div class="pnum">3</div><div class="ptxt">אנחנו מציגים לכם תוכנית עסקית, שיווקית ופיננסית, לצד הצעת התקשרות מסחרית — היקף, מבנה תמחור, לוח זמנים ומסגרת עבודה.</div></div>
  <div class="pstep"><div class="pnum">4</div><div class="ptxt">אתם מחליטים — לאשר, לדחות או לדון בהצעה המוצעת.</div></div>
  <div class="pstep"><div class="pnum">5</div><div class="ptxt">ה"הצעה" שתאושר ותיחתם מפעילה את ההתקשרות הספציפית הרלוונטית, לפי מסגרת ההסכם.</div></div>
</div>
<div class="callout"><span class="callout-label">לקוחות קיימים:</span> אם כבר חתמתם על הסכם ההתקשרות, והפרק הזה רלוונטי עבורכם לגבי התקשרות נוספת — התהליך חוזר על עצמו ביחס לאותה התקשרות בלבד, ואינו מצריך חתימה מחודשת; טבלת נספח B תעודכן ביחס אליה בלבד.</div>
{pagefoot()}
</div>''')

# ==================================================================
# 17 — Reminder (fixed: track-aware)
# ==================================================================
PAGES.append(f'''<div class="page">
{pagehead("03", "תזכורת")}
<div class="eyebrow">לפני שממשיכים לטופס</div>
<h1 class="sec">תזכורת</h1>
<div class="secrule"></div>
<p class="body-copy">כל המידע שתמסרו בפרק הזה — תקציב, טווח זמן, סובלנות וגבולות — משמש לתכנון ולהערכה בלבד, ואינו יוצר כשלעצמו התחייבות כלכלית.</p>
<p class="body-copy">שימו לב: חתימה על הסכם ההתקשרות עצמו כרוכה בתשלום מהמסלול שבחרתם — דמי ההשתתפות העצמית למחקר Genesis במסלולים A/B/C, או מחיר המחקר המלא במסלול 0 — אך ההתחייבות המסחרית המלאה להיקף, למחיר ולתנאי ההתקשרות הספציפית נוצרת רק ב"הצעה" חתומה בנפרד, כפי שקיבלתם הסבר עליה למעלה.</p>
{pagefoot()}
</div>''')

# ==================================================================
# 18 — Intake divider (reframed)
# ==================================================================
PAGES.append('''<div class="page dark divider">
  <div class="divider-ghost">04</div>
  <div class="divider-inner">
    <div class="divider-eyebrow"><span class="dash"></span>הצעד הבא</div>
    <div class="divider-title">טופס קליטה</div>
    <div class="divider-sub">המידע כאן משמש לתכנון בלבד ואינו קובע בעצמו היקף, מחיר או תנאים מחייבים. תמציתי במכוון, ואורך כ-5 דקות למילוי.</div>
    <div class="divider-endrule"></div>
  </div>
</div>''')

def field(label):
    return f'<div class="f"><span class="flabel">{label}</span><span class="fline"></span></div>'

INTAKE_GROUPS = [
    ("העסק והמצב הנוכחי", None, [
        "שם העסק/החברה ומספר ח.פ./עוסק", "תחום הפעילות ותיאור קצר של המוצר/השירות המרכזי",
        "מדינת הלקוח (קובעת, בין היתר, את הפורום ליישוב מחלוקות — סעיף 14 להסכם)",
        "המצב העסקי הנוכחי בקצרה (עסק קיים ופעיל / השקה חדשה / הרחבה לשוק נוסף)",
        "אילוצים חשובים שכדאי שנכיר לפני תחילת המחקר",
    ]),
    ("האנשים שמקבלים את ההחלטות", None, [
        "נציג מוסמך ראשי — שם, תפקיד, דוא\"ל", "נציג מוסמך חלופי, אם יש — שם, תפקיד, דוא\"ל",
    ]),
    ("הנתיב המועדף", "מסלולים A/B/C בלבד — ראו \"שני נתיבים אפשריים\"; שתי התשובות תקפות באותה מידה. מסלול 0: כל שדות קבוצות 3–6 אינם רלוונטיים לכם — השאירו ריק ועברו לקבוצה 7", [
        "אתם מגדירים את מסגרת ההשקעה, או מבקשים שנציע מודל מסחרי?",
    ]),
    ("מסגרת ההשקעה שלכם", None, [
        "תקציב חודשי מועדף", "היקף השקעה כולל, אם ידוע", "טווח הגמישות (תקציב קבוע / מרחב תמרון)",
    ]),
    ("סובלנות ורווחיות", None, [
        "תקופת הסובלנות המועדפת", "רמת הסובלנות (שמרנית / מאוזנת / אגרסיבית / הרחבה מרבית)",
        "העדפת רווחיות: מהר ככל האפשר, או בנייה והרחבה תוך שמירה על נקודת האיזון",
        "נכונות לגירעון תפעולי זמני בפועל, ואם כן — התקרה המבוקשת (תשמש כרף ה-Stop-Loss)",
        "שיעור הרווח הגולמי שלכם, אם ידוע", "שווי עסקה ממוצע (AOV), אם ידוע — אם לא, נסתמך על מחקר Genesis",
    ]),
    ("גבולות פיננסיים", "אופציונלי", [
        "סכום שאין לחרוג ממנו, אם יש", "שינויים בתקציב הדורשים אישור מראש, אם יש",
    ]),
    ("החזון והיעדים", None, [
        "החזון והמטרה העסקית של הפרויקט", "איך תגדירו הצלחה/התקדמות בעוד שישה חודשים?",
        "שלושת הדברים החשובים לכם ביותר בהתקשרות הזו",
    ]),
    ("טווח זמן וקווים אדומים", None, [
        "טווח הזמן שאתם מתכננים לפעול בו, ומועדים עסקיים משמעותיים",
        "גבולות או \"קווים אדומים\" אסטרטגיים (ערוצים/שווקים שלא לגעת בהם, מותג לשמור עליו בקפידה)",
    ]),
    ("מידע נוסף", "אופציונלי — קישורים וחומרי רקע פומביים/לא רגישים בלבד; אין למסור כאן פרטי גישה או סיסמאות", [
        "קישורים וחומרי רקע שיעזרו לצוות המחקר להכיר את העסק",
    ]),
]

def intake_page(num, title, groups, intro=None, outro=None):
    html = [f'<div class="page">{pagehead(num, title)}']
    if intro:
        html.append(f'<div class="eyebrow">טופס קליטה</div><h1 class="sec">טופס קליטה</h1><div class="secrule"></div><p class="intake-intro">{intro}</p>')
    for idx, title_, note, items in groups:
        grp = [f'<div class="igroup"><div class="igroup-head"><span class="igroup-num">{idx:02d}</span><span class="igroup-title">{title_}</span></div>']
        if note:
            grp.append(f'<div class="igroup-note">{note}</div>')
        grp.append('<div class="ifields">')
        for it in items:
            grp.append(field(it))
        grp.append('</div></div>')
        html.append("".join(grp))
    if outro:
        html.append(f'<p class="fine">{outro}</p>')
    html.append(pagefoot() + '</div>')
    return "".join(html)

numbered = [(i, t, n, it) for i, (t, n, it) in enumerate(INTAKE_GROUPS, start=1)]
PAGES.append(intake_page("04", "טופס קליטה", numbered[:5],
    intro='מטרת הטופס: לאסוף את המידע הדרוש לצוות המחקר והתכנון כדי לבנות עבורכם תוכנית עסקית, שיווקית ופיננסית מותאמת, ולתרגם אותה בהמשך להצעת התקשרות מסחרית ספציפית. מה שלמעלה היה ההסבר; מה שלמטה הוא רק התרגום שלו לשדות קצרים — שום דבר כאן לא אמור להפתיע אתכם.'))
PAGES.append(intake_page("04", "טופס קליטה (המשך)", numbered[5:],
    outro='הטופס תמציתי במכוון — כל שדה כאן משמש ישירות את שלב המחקר והתכנון. פרטים נוספים ומדויקים יותר ייאספו בשיחה ישירה איתכם, ואינם "נועלים" אתכם בשום מחויבות עד לחתימה על הצעה ספציפית.'))

# ==================================================================
# Closing
# ==================================================================
PAGES.append(f'''<div class="page dark closing">
  <div class="closing-ghost">LG</div>
  <div class="closing-inner">
    <div class="closing-eyebrow"><span class="dash"></span>לסיום</div>
    <div class="closing-title">כל המידע במדריך זה משמש לתכנון ולהערכה בלבד</div>
    <p>חתימה על הסכם ההתקשרות עצמו כן כרוכה בתשלום הרלוונטי למסלולכם. ההתחייבות המסחרית המלאה להיקף, למחיר ולתנאי ההתקשרות הספציפית נוצרת רק ב"הצעה" חתומה בנפרד — עד אז, כל מה שסיפרתם לנו נשאר פתוח לשינוי.<br><br>אנחנו מוכנים כשאתם מוכנים.</p>
    <div class="closing-brand"><img src="{LOGO_MARK}"><div class="tx"><div class="n">LOS GARDIOS</div><div class="t">מדריך הלקוח — סודי</div></div></div>
  </div>
</div>''')

body = "\n".join(PAGES)

doc = f"""<!doctype html>
<html lang="he" dir="rtl"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Los Gardios — מדריך הלקוח</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Heebo:wght@300;400;600;700&family=Frank+Ruhl+Libre:wght@600;700&display=swap" rel="stylesheet">
<style>{CSS}</style></head>
<body><div class="sheet">
{body}
</div></body></html>"""

io.open("CLIENT_GUIDE_HE.html", "w", encoding="utf-8").write(doc)
print("wrote CLIENT_GUIDE_HE.html", len(doc), "bytes,", len(PAGES), "page blocks")

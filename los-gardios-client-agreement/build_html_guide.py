# -*- coding: utf-8 -*-
"""Render CLIENT_GUIDE_HE.md as a premium, editorial-feeling A4 RTL PDF.

Design language: dark espresso section dividers with ghost numerals, a
cream content-page body, a brass/gold accent system (rules, eyebrows,
stat tiles, key-insight callouts), and Los Gardios' own Velvet Purple
used sparingly as the brand-identity touch (logo mark, one accent line
on the cover, a single narrative accent inside two of the new diagrams)
rather than as the dominant hue — the warm gold/espresso palette is the
editorial atmosphere; purple is the brand anchor.

The underlying Hebrew CONTENT is parsed from CLIENT_GUIDE_HE.md (source
of truth) at build time by md_guide_parser.py; this build script is
presentation-only — page grouping, diagram composition and the Intake
Form's field grouping/order are the only structural decisions made here,
and every sentence of prose it prints comes from the parsed tree, never
from a Python string literal. New concepts (the operating-model flow,
the sustainability principle, the Genesis specialist-lens system, the
oversight/reporting mechanics) are all authored in CLIENT_GUIDE_HE.md
first and merely visualized here. See md_guide_parser.py's module
docstring for the parser's conventions and the aside-classification
contract (which bold lead-ins render as .callout / .callout.warn / .fine
vs plain .body-copy).
"""
import io, os, re, base64

from md_guide_parser import load_guide, render_block, render_blocks, render_table, split_lead, inline_to_html

_HERE = os.path.dirname(os.path.abspath(__file__))
_ASSETS = os.path.join(_HERE, "assets")
G = load_guide(os.path.join(_HERE, "CLIENT_GUIDE_HE.md"))

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

/* ---------- FORECAST TABLE (months as rows, metrics as columns) ----------
   Breaks out of the normal text margins (20mm page padding) into most of
   that margin on both sides, leaving only ~2.7mm from the true page edge, to
   gain extra width so column headers never need to wrap. Column widths
   (see _FORECAST_COL_WIDTHS below) are sized per-column from measured
   header/data text widths, not equal tiers, so every header fits on one
   line without overflowing into its neighbor. */
table.fcast{width:calc(100% + 131px);margin:6px -65.5px;table-layout:fixed;
 border-collapse:collapse;font-family:"Heebo",sans-serif;font-size:7.6pt;
 break-inside:avoid-page;page-break-inside:avoid}
table.fcast th{text-align:center;font-size:7.2pt;letter-spacing:.01em;color:var(--gold-deep);
 font-weight:700;padding:3px 2px 4px;border-bottom:1px solid var(--rule);white-space:nowrap}
table.fcast td{padding:3.6px 2px;border-bottom:1px solid var(--rule);text-align:center;
 color:#382c1f;white-space:nowrap}
table.fcast td:first-child{color:var(--ink);font-weight:600}
table.fcast th.sec-mkt,table.fcast td.sec-mkt{background:rgba(169,130,79,.07)}
table.fcast th.sec-com,table.fcast td.sec-com{background:rgba(140,106,61,.07)}
table.fcast th.sec-ret,table.fcast td.sec-ret{background:rgba(125,111,92,.08)}
table.fcast th.sec-fin,table.fcast td.sec-fin{background:rgba(91,41,134,.055)}
table.fcast th.sec-mkt{border-top:3px solid var(--gold)}
table.fcast th.sec-com{border-top:3px solid var(--gold-deep)}
table.fcast th.sec-ret{border-top:3px solid var(--muted)}
table.fcast th.sec-fin{border-top:3px solid var(--purple)}
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
.ifields .f .flabel{flex:1 1 auto;min-width:0;color:#4a3d2c}
.ifields .f .fline{flex:0 0 70px;border-bottom:1px solid var(--rule);min-height:13px}

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

# ------------------------------------------------------------------
# Generic page templates. content_page() is the shared shell every page
# (bespoke or generic) is built on: pagehead + eyebrow + h1.sec + secrule
# + arbitrary body HTML + pagefoot. generic_section_page() is the
# fallback described in the module docstring for a chapter/section that
# has no bespoke layout of its own yet — it renders every block of a
# parsed section, in order, with nothing hand-authored except the short
# eyebrow caption. It is genuinely used below (not just wired up and
# left idle), for every section in this guide that doesn't need a
# cardgrid/diagram/table/stat-tile of its own.
# ------------------------------------------------------------------

def content_page(num, breadcrumb_title, eyebrow, h1, body_html, dark=False):
    return f'''<div class="page">
{pagehead(num, breadcrumb_title, dark=dark)}
<div class="eyebrow">{eyebrow}</div>
<h1 class="sec">{h1}</h1>
<div class="secrule"></div>
{body_html}
{pagefoot()}
</div>'''


def generic_section_page(num, section, eyebrow, breadcrumb_title=None):
    """The fallback template from the recommended architecture: pagehead
    + h1.sec (the section's own title) + secrule + every block of the
    section rendered in source order via the generic renderer. Used for
    every chapter-1 sub-page below that has no bespoke visual, and ready
    as-is for chapters added after this fix lands."""
    body = render_blocks(section.blocks)
    return content_page(num, breadcrumb_title or section.title, eyebrow, section.title, body)


PAGES = []

# ==================================================================
# COVER
# ==================================================================
# cover-title is the document's own title (parsed), minus the " — Los
# Gardios" tail; the version tag is the parsed version line — this is
# the "closes a related, smaller version-drift risk" fix: there is no
# second, hand-typed copy of the version/date anywhere in this script.
_cover_title = G.title.split('—')[0].strip()
PAGES.append(f'''<div class="page dark cover">
  <img src="{LOGO_MARK}" class="cover-mark">
  <div class="cover-eyebrow">L O S &nbsp; G A R D I O S</div>
  <div class="cover-title">{_cover_title}</div>
  <div class="cover-rule"></div>
  <div class="cover-sub">תקציב · מסגרת השקעה · טווח זמן<br>קריאה לפני תחילת הדרך המשותפת</div>
  <div class="cover-tags"><span class="cover-tag">סודי</span><span class="cover-tag">גרסה {G.version} · {G.updated_date}</span></div>
  <div class="cover-foot">CONFIDENTIAL · LOS GARDIOS GROUP</div>
</div>''')

# ==================================================================
# DIVIDER 01 — How Los Gardios Works
# ==================================================================
_ch1 = G.chapter("1")
PAGES.append(f'''<div class="page dark divider">
  <div class="divider-ghost">01</div>
  <div class="divider-inner">
    <div class="divider-eyebrow"><span class="dash"></span>פרק 01</div>
    <div class="divider-title">{_ch1.title}</div>
    <div class="divider-sub">מי אנחנו, אילו נכסים ומערכות עומדים מאחורי העבודה, ואיך מורכבת מעטפת המומחים סביב הפרויקט שלכם.</div>
    <div class="divider-endrule"></div>
  </div>
</div>''')

# ==================================================================
# 1.1 — Who we are + the client-controlled principle
# ==================================================================
_sec_who = _ch1.section("מי אנחנו")
_sec_principle = _ch1.section("העיקרון המנחה: הלקוח קובע את המסגרת")
PAGES.append(f'''<div class="page">
{pagehead("01", _sec_who.title)}
<div class="eyebrow">זהות</div>
<h1 class="sec">{_sec_who.title}</h1>
<div class="secrule"></div>
{render_blocks(_sec_who.blocks)}
<h2 class="sub">{_sec_principle.title}</h2>
{render_blocks(_sec_principle.blocks)}
{pagefoot()}
</div>''')

# ==================================================================
# 1.2 — Organization's assets (table -> cardgrid)
# ==================================================================
def cardgrid_from_table(table_block, grid="grid2"):
    cards = []
    for row in table_block["rows"]:
        label, body = row[0], row[1]
        cards.append(f'<div class="card"><div class="card-label">{inline_to_html(label)}</div><p>{inline_to_html(body)}</p></div>')
    return f'<div class="cardgrid {grid}">' + "".join(cards) + '</div>'

_sec_assets = _ch1.section("נכסי הארגון וההשקעה שביסודם")
_assets_blocks = _sec_assets.blocks  # [para(intro), para(list-lead-in), table, para(operative rule)]
_assets_body = "\n".join([
    render_block(_assets_blocks[0]),
    render_block(_assets_blocks[1]),
    cardgrid_from_table(_assets_blocks[2]),
    render_block(_assets_blocks[3]),
])
PAGES.append(content_page("01", _sec_assets.title, "מה עומד מאחורי העבודה", _sec_assets.title, _assets_body))

# ==================================================================
# 1.2b — Cost basis behind the protection floors (generic fallback page)
# ==================================================================
PAGES.append(generic_section_page("01", _ch1.section("יסודות עלות ההגנה על נכסי הארגון"), "עלות ההגנה"))

# ==================================================================
# 1.3 — Proprietary technology (Neuron)
# ==================================================================
PAGES.append(generic_section_page("01", _ch1.section("טכנולוגיה קניינית ומערכות פנימיות"), "תשתית תפעולית"))

# ==================================================================
# 1.4 — Atlas Network + Data/meetings/privacy. Two short sections
# combined onto one page (a page-grouping choice — both are a few short
# paragraphs on their own); the second keeps its own real section title
# as an h2.sub rather than a fabricated label.
# ==================================================================
_sec_atlas = _ch1.section("Atlas Network")
_sec_privacy = _ch1.section("נתונים, פגישות ופרטיות — בקצרה")
PAGES.append(content_page("01", _sec_atlas.title, "רשת מסחרית בינלאומית", _sec_atlas.title, "\n".join([
    render_blocks(_sec_atlas.blocks),
    f'<h2 class="sub">{_sec_privacy.title}</h2>',
    render_blocks(_sec_privacy.blocks),
])))

# ==================================================================
# 1.5 — Specialist capabilities
# ==================================================================
PAGES.append(generic_section_page("01", _ch1.section("יכולות מומחים"), "הרכב הצוות לפי צורך"))

# ==================================================================
# DIVIDER 02 — Engagement Models
# ==================================================================
_ch2 = G.chapter("2")
PAGES.append(f'''<div class="page dark divider">
  <div class="divider-ghost">02</div>
  <div class="divider-inner">
    <div class="divider-eyebrow"><span class="dash"></span>פרק 02</div>
    <div class="divider-title">{_ch2.title}</div>
    <div class="divider-sub">ארבעת המסלולים שההסכם תומך בהם, ולמה גמישות מסחרית היא ארכיטקטורה — לא הנחה.</div>
    <div class="divider-endrule"></div>
  </div>
</div>''')

# ==================================================================
# 2.1 — The four tracks. Each track is its own md paragraph, whose
# leading bold span is "מסלול <letter> — <title>." — the badge and card
# title are derived from that lead (never retyped), the card body from
# the rest of that same paragraph.
# ==================================================================
_TRACK_LEAD_RE = re.compile(r'^מסלול\s+(\S+)\s*—\s*(.+?)\.?$')

def _track_card(block):
    m = _TRACK_LEAD_RE.match(block["lead"])
    badge, title = m.group(1), m.group(2)
    _, rest_html = split_lead(block)
    return (f'<div class="card"><div class="card-label">'
            f'<div class="igroup-num" style="width:32px;height:32px;font-size:12pt;display:inline-flex;vertical-align:middle;margin-inline-end:8px">{badge}</div>'
            f'מסלול {badge}</div><div class="card-title">{title}</div><p>{rest_html}</p></div>')

_sec_tracks = _ch2.section("ארבעת המסלולים")
_tb = _sec_tracks.blocks  # [track0, trackA, trackB, trackC, mechanism-fine, unsure-callout]
# Split across two physical pages (structural, page-grouping only) — the
# full verbatim section no longer fits one page the way the old
# paraphrase did.
PAGES.append(content_page("02", _sec_tracks.title, "מסגרות מסחריות נתמכות", _sec_tracks.title, "\n".join([
    render_block(_ch2.intro_blocks()[0]),
    '<div class="cardgrid grid2">' + "".join(_track_card(b) for b in _tb[0:4]) + '</div>',
])))
PAGES.append(content_page("02", _sec_tracks.title + " (המשך)", "מסגרות מסחריות נתמכות", _sec_tracks.title + " — המשך", "\n".join([
    f'<div class="fine">{_tb[4]["html"]}</div>',
    render_block(_tb[5]),
])))

# ==================================================================
# 2.2 — Flexibility, exit schedule and shared growth. Three md sections
# combined onto one page (a structural/page-grouping choice), each kept
# under its own real section-title h2.
# ==================================================================
_sec_flex = _ch2.section("גמישות מסחרית — ארכיטקטורה, לא הנחה")
_sec_exit = _ch2.section("אם אתם מסיימים ביוזמתכם, מוקדם — לוח הנסיגה")
_sec_growth = _ch2.section("צמיחה משותפת — עד כמה שהמבנה המסחרי מאפשר זאת")
_flex_body = "\n".join([
    render_blocks(_sec_flex.blocks),
    f'<h2 class="sub">{_sec_growth.title}</h2>',
    render_blocks(_sec_growth.blocks),
    f'<h2 class="sub">{_sec_exit.title}</h2>',
    render_blocks(_sec_exit.blocks),
])
PAGES.append(content_page("02", "גמישות מסחרית וצמיחה משותפת", "ארכיטקטורה, לא הנחה", _sec_flex.title, _flex_body))

# ==================================================================
# DIVIDER 03 — Budget / investment / timeline
# ==================================================================
_ch3 = G.chapter("3")
PAGES.append(f'''<div class="page dark divider">
  <div class="divider-ghost">03</div>
  <div class="divider-inner">
    <div class="divider-eyebrow"><span class="dash"></span>פרק 03</div>
    <div class="divider-title">{_ch3.title}</div>
    <div class="divider-sub">איך אנחנו חושבים על תקציב, מדוע אנחנו שואלים עליו, ואיך זה מתורגם לתוכנית אמיתית.</div>
    <div class="divider-endrule"></div>
  </div>
</div>''')

def first_sentence_split(raw):
    """A bespoke page's h1.sec pull-quote headline: the section's own
    first sentence (split on the first '. '), never a separately typed
    headline. Returns (headline_without_period, rest_of_paragraph_html)."""
    parts = re.split(r'(?<=\.)\s+', raw, maxsplit=1)
    head = parts[0].rstrip('.')
    rest = parts[1] if len(parts) > 1 else ''
    return inline_to_html(head), inline_to_html(rest)

def qmark_lines(html):
    """Presentational line-break helper for the .prompt-q box: breaks an
    already-inline-converted string after every '?' so a paragraph that
    embeds several questions as running prose reads as stacked question
    lines, exactly as written — no word is added, removed or reordered."""
    parts = re.split(r'(?<=\?)\s+', html)
    return '<br>'.join(p for p in parts if p)

def split_ask(raw):
    """Several sections in chapter 3 are shaped, in the .md, as one
    running-prose paragraph: "<label>: <question>? <question>?
    [<trailing non-question sentence>.]" — e.g. 'ספרו לנו: מהי התקופה
    ...? האם יש מועדים ...?'. This splits that single paragraph, purely
    presentationally, onto the existing .prompt (label + stacked
    questions) design, plus an optional trailing aside — never
    rewording or reordering a single word. Returns
    (label_html, questions_html, tail_html_or_None)."""
    label, _, remainder = raw.partition(':')
    remainder = remainder.strip()
    m = re.search(r'^(.*\?)(.*)$', remainder, re.DOTALL)
    if m:
        questions, tail = m.group(1).strip(), m.group(2).strip(' —-;.')
    else:
        questions, tail = remainder, ''
    return (inline_to_html(label), qmark_lines(inline_to_html(questions)),
            inline_to_html(tail) if tail else None)

# ==================================================================
# 3 — Opening hook: the section's own first sentence as the page's
# headline (see first_sentence_split), the rest of that paragraph plus
# the section's remaining two paragraphs as body copy.
# ==================================================================
_sec_why = _ch3.section("למה אנחנו שואלים על כך")
_headline, _rest0 = first_sentence_split(_sec_why.blocks[0]["text"])
PAGES.append(content_page("03", "למה אנחנו שואלים", "פתיח", _headline, "\n".join([
    f'<p class="body-copy">{_rest0}</p>',
    render_block(_sec_why.blocks[1]),
    render_block(_sec_why.blocks[2]),
])))

# ==================================================================
# 4 — Operating-model flow. Diagram stage captions ("אתם"/"אנחנו
# בוחנים"/"יחד" + short sub-captions) are hand-authored diagram
# scaffolding (they label the graphic, they aren't sentences of prose);
# every paragraph of actual prose on this page is the section's own two
# blocks, rendered in full — including their natural inline bold on
# "אתם"/"אנחנו"/"יחד", which does the "not this, but this" contrast job
# the old hand-written contrast-row graphic used to do, without
# paraphrasing anything.
# ==================================================================
_flow_icon = '''<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.5">
<circle cx="10.5" cy="10.5" r="6.5"/><line x1="15.3" y1="15.3" x2="21" y2="21"/></svg>'''
_sec_model = _ch3.section("המודל שלנו: אתם קובעים את המסגרת")
PAGES.append(content_page("03", "המודל שלנו", "הגישה שלנו", _sec_model.title, "\n".join([
    f'''<div class="flow">
  <div class="flow-stage"><div class="flow-eyebrow">שלב 1</div><div class="flow-card">אתם<br><span style="font-weight:400;font-size:8.6pt;color:var(--muted)">תקציב · מסגרת · חזון</span></div></div>
  <div class="flow-connector"></div>
  <div class="flow-stage"><div class="flow-eyebrow">שלב 2</div><div class="flow-node">{_flow_icon}</div><div style="font-family:'Heebo',sans-serif;font-size:9pt;font-weight:700">אנחנו בוחנים</div></div>
  <div class="flow-connector"></div>
  <div class="flow-stage"><div class="flow-eyebrow">שלב 3</div><div class="flow-card">יחד<br><span style="font-weight:400;font-size:8.6pt;color:var(--muted)">תוכנית + הצעה</span></div></div>
</div>''',
    render_block(_sec_model.blocks[0]),
    f'<div class="flow-loop">{_sec_model.blocks[1]["html"]}</div>',
])))

# ==================================================================
# 5 — Trust + permission (pull-quote). The oversized quote is this
# section's own leading bold sentence (split_lead), never retyped.
# ==================================================================
_sec_trust = _ch3.section("האמון שלנו מתחיל בכנות")
_sec_before = _ch3.section("לפני שממשיכים — חשוב שתדעו")
_quote_lead, _quote_rest = split_lead(_sec_trust.blocks[0])
# "לפני שממשיכים — חשוב שתדעו" (a short before-you-continue caveat) is
# folded onto this page as fine print rather than given its own
# near-empty page — a page-grouping choice, its own text unchanged.
PAGES.append(f'''<div class="page">
{pagehead("03", _sec_trust.title)}
<div class="permission-quote">{_quote_lead}</div>
<div class="permission-dots">
  <span class="permission-dot"></span><span class="permission-dot"></span><span class="permission-dot you"></span><span class="permission-dot"></span><span class="permission-dot"></span>
</div>
<div class="permission-cap">אותה תשומת לב. בכל היקף.</div>
<p class="body-copy">{_quote_rest}</p>
{render_block(_sec_trust.blocks[1])}
<div class="fine">{_sec_before.blocks[0]["html"]}</div>
{pagefoot()}
</div>''')

# ==================================================================
# 6 — Two paths. The two bullets become the two stacked cards; card
# labels are Hebrew ordinal captions (נתיב א׳/ב׳ — a card index, not
# prose), card body is each bullet's own text.
# ==================================================================
_HEBREW_ORDINALS = ["א׳", "ב׳", "ג׳", "ד׳"]
_sec_paths = _ch3.section("שני נתיבים אפשריים")
_paths_ulist = _sec_paths.blocks[1]
_path_cards = []
for i, item_html in enumerate(_paths_ulist["items"]):
    lead, rest = None, item_html
    m = re.match(r'^<strong>(.+?)</strong>\s*(.*)$', item_html)
    title = m.group(1) if m else item_html
    body = m.group(2) if m else ''
    _path_cards.append(
        f'<div class="card"><div class="card-label">נתיב {_HEBREW_ORDINALS[i]}</div>'
        f'<div class="card-title">{title}</div><p>{body}</p></div>'
    )
_paths_body = "\n".join([
    render_block(_sec_paths.blocks[0]),
    '<div class="cardgrid stack">' + "".join(_path_cards) + '</div>',
    render_block(_sec_paths.blocks[2]),
])
PAGES.append(content_page("03", _sec_paths.title, "בחירה", _sec_paths.title, _paths_body))

# ==================================================================
# 7 — Goals reflection (prompt box; single running-prose paragraph)
# ==================================================================
_sec_goals = _ch3.section("היעד והציפיות שלכם")
_goals_label, _goals_q, _goals_tail = split_ask(_sec_goals.blocks[0]["text"])
_goals_body = f'''<p class="body-copy">{_goals_label}.</p>
<div class="prompt"><div class="prompt-label">שאלות למחשבה</div>
<div class="prompt-q">{_goals_q}</div></div>'''
if _goals_tail:
    _goals_body += f'<p class="fine">{_goals_tail}</p>'
PAGES.append(content_page("03", _sec_goals.title, "לפני המספרים", _sec_goals.title, _goals_body))

# ==================================================================
# 8 — Investment framework. "ספרו לנו:" + a REAL bullet list in the .md
# maps directly onto the existing prompt-label / prompt-q boxed design.
# ==================================================================
_sec_invest = _ch3.section("מסגרת ההשקעה שלכם")
_ib = _sec_invest.blocks  # [intro, "ספרו לנו:", ulist(4), reminder-para, terms-para, track0-callout]
_invest_body = "\n".join([
    render_block(_ib[0]),
    f'<div class="prompt"><div class="prompt-label">{_ib[1]["html"]}</div>'
    f'<div class="prompt-q">' + '<br>'.join(_ib[2]["items"]) + '</div></div>',
    render_block(_ib[3]),
    '<div class="eyebrow" style="margin-top:22px">מסגרת A/B/C — מה שכדאי לדעת כבר עכשיו</div>',
    '<div class="stats">'
    '<div class="stat"><div class="stat-num">3</div><div class="stat-cap">חודשים · התחייבות תקציב מינימלית</div></div>'
    '<div class="stat"><div class="stat-num">30</div><div class="stat-cap">יום · הודעה מראש להפחתת תקציב</div></div>'
    '</div>',
    render_block(_ib[4]),
    render_block(_ib[5]),
])
PAGES.append(content_page("03", _sec_invest.title, "תשומת הקלט המרכזית", _sec_invest.title, _invest_body))

# ==================================================================
# 9 — Timeline
# ==================================================================
_sec_timeline = _ch3.section("טווח הזמן שלכם")
_tl_label, _tl_q, _tl_tail = split_ask(_sec_timeline.blocks[0]["text"])
PAGES.append(content_page("03", _sec_timeline.title, "תכנון", _sec_timeline.title, "\n".join([
    f'<p class="body-copy">{_tl_label}.</p>',
    f'<div class="prompt"><div class="prompt-label">ספרו לנו</div><div class="prompt-q">{_tl_q}</div></div>',
    render_block(_sec_timeline.blocks[1]),
])))

# ==================================================================
# 10 — Sustainability principle (horizon rings)
# ==================================================================
_rings = []
_radii = [14, 24, 35, 47, 60]
for i, r in enumerate(_radii):
    t = i / (len(_radii) - 1)
    # gold -> purple stroke gradient across rings
    color = f"rgb({int(169+(91-169)*t)},{int(130+(41-130)*t)},{int(79+(134-79)*t)})"
    _rings.append(f'<circle cx="70" cy="70" r="{r}" fill="none" stroke="{color}" stroke-opacity="{0.55-0.07*i:.2f}" stroke-width="1"/>')
_horizon_svg = f'<svg class="horizon-svg" width="140" height="140" viewBox="0 0 140 140">{"".join(_rings)}<circle cx="70" cy="70" r="4" fill="var(--gold)"/></svg>'
_sec_sustain = _ch3.section("העיקרון שמנחה אותנו: לא למצות עד הסוף")
PAGES.append(content_page("03", "העיקרון שמנחה אותנו", "עמדה שקופה", "לא למצות עד הסוף", "\n".join([
    f'<div class="horizon-wrap">{_horizon_svg}<div class="horizon-cap">{_sec_sustain.blocks[0]["html"]}</div></div>',
    render_block(_sec_sustain.blocks[1]),
])))

# ==================================================================
# 11 — Tolerance
# ==================================================================
_sec_tol = _ch3.section("רמת ותקופת הסובלנות שלכם")
_tb2 = _sec_tol.blocks  # [plain-terms, example-fine, default-callout, deficit-callout, ask, rights-fine]
_tol_label, _tol_q, _tol_tail = split_ask(_tb2[4]["text"])
# Split across two physical pages — see the four-tracks page's comment.
PAGES.append(content_page("03", _sec_tol.title, "גמישות סביב רווחיות", _sec_tol.title, "\n".join([
    render_block(_tb2[0]),
    render_block(_tb2[1]),
    render_block(_tb2[2]),
])))
_tol_body2 = "\n".join([
    render_block(_tb2[3]),
    f'<div class="prompt"><div class="prompt-label">{_tol_label}</div><div class="prompt-q">{_tol_q}</div></div>',
] + ([f'<p class="fine">{_tol_tail}</p>'] if _tol_tail else []) + [
    render_block(_tb2[5]),
])
PAGES.append(content_page("03", _sec_tol.title + " (המשך)", "גמישות סביב רווחיות", _sec_tol.title + " — המשך", _tol_body2))

# ==================================================================
# 12 — Financial boundaries
# ==================================================================
_sec_bounds = _ch3.section("גבולות פיננסיים")
_bounds_label, _bounds_q, _bounds_tail = split_ask(_sec_bounds.blocks[0]["text"])
PAGES.append(content_page("03", _sec_bounds.title, "הגנה עליכם", _sec_bounds.title, "\n".join([
    f'<p class="body-copy">{_bounds_label}.</p>',
    f'<div class="prompt"><div class="prompt-label">ספרו לנו</div><div class="prompt-q">{_bounds_q}</div></div>',
    '<div class="eyebrow" style="margin-top:18px">ברירות המחדל, אם לא תיקבע תקרה</div>',
    '<div class="stats">'
    '<div class="stat"><div class="stat-num">30</div><div class="stat-cap">יום · תקופת מדידת Stop-Loss</div></div>'
    '<div class="stat"><div class="stat-num">10%</div><div class="stat-cap">חריגה מותרת מהתקציב החודשי</div></div>'
    '</div>',
])))

# ==================================================================
# 13 — Oversight & reporting. Each bullet's own leading bold phrase
# becomes its card title (split_lead), the rest of that bullet its card
# body.
# ==================================================================
_sec_oversight = _ch3.section("בקרה ודיווח שוטף")
_oversight_ulist = _sec_oversight.blocks[1]
_oversight_cards = []
for item_html in _oversight_ulist["items"]:
    m = re.match(r'^<strong>(.+?)</strong>\s*(.*)$', item_html)
    title = (m.group(1).rstrip('.') if m else item_html)
    body = m.group(2) if m else ''
    _oversight_cards.append(f'<div class="card"><div class="card-label">{title}</div><p>{body}</p></div>')
# 5 cards no longer fit one page under a real intro paragraph (the
# verbatim intro is longer than the old paraphrase) — 3 + 2 across two
# physical pages, same content_page shell.
PAGES.append(content_page("03", _sec_oversight.title, "מה קורה אחרי החתימה", _sec_oversight.title, "\n".join([
    render_block(_sec_oversight.blocks[0]),
    '<div class="cardgrid grid3">' + "".join(_oversight_cards[:3]) + '</div>',
])))
PAGES.append(content_page("03", _sec_oversight.title + " (המשך)", "מה קורה אחרי החתימה", _sec_oversight.title + " — המשך", "\n".join([
    '<div class="cardgrid grid2">' + "".join(_oversight_cards[3:]) + '</div>',
])))

# ==================================================================
# 14 — Break-even
# ==================================================================
_sec_breakeven = _ch3.section("נקודת האיזון (Break-Even) — במה מדובר")
_beb = _sec_breakeven.blocks  # [what-it-means, precise-terms, two-inputs-intro, table, ask, floor-note]
_be_label, _be_q, _be_tail = split_ask(_beb[4]["text"])
_be_body = "\n".join([
    render_block(_beb[0]),
    render_block(_beb[1]),
    render_block(_beb[2]),
    render_table(_beb[3]),
    f'<div class="prompt"><div class="prompt-label">{_be_label}</div><div class="prompt-q">{_be_q}</div></div>',
    render_block(_beb[5]),
])
PAGES.append(content_page("03", "נקודת האיזון (Break-Even)", "כלי תכנון, לא הבטחה", "נקודת האיזון (Break-Even)", _be_body))

# ==================================================================
# 14b — Illustrative forecast example table. Column VALUES and headers
# come straight from the .md's own table (no second, hand-typed copy of
# the same numbers to drift out of sync); only the per-column-group
# coloring and fixed pixel-measured widths — pure presentation — stay
# Python-authored, keyed by header text so they survive column
# reordering as long as the header text itself doesn't change.
# ==================================================================
_FORECAST_GROUP_BY_HEADER = {
    "תקציב": "mkt", "CPM": "mkt", "חשיפה": "mkt", "CTR": "mkt", "מבקרים": "mkt", "ROAS": "mkt",
    "יחס המרה": "com", "המרות": "com", "CPA": "com", "AOV": "com",
    "יחס שימור": "ret", "רכישות חוזרות": "ret", 'סה"כ המרות': "ret",
    "הכנסות": "fin", "הוצ' קבועות": "fin", 'סה"כ הוצאות': "fin", "רווח": "fin", "ROI": "fin",
}
# Percent widths, positional (one per column in the table's own header
# order), measured from actual Playwright header/data text widths so
# every header renders on one line without wrapping or overflowing —
# see the historical note this replaces for how they were derived.
_FORECAST_COL_WIDTHS = [
    3.625, 4.375, 3.625, 4.5, 3.625, 5.125, 4.25,
    6.375, 4.375, 3.625, 4.25,
    6.375, 9.5, 7.625,
    5.125, 7.25, 8.0, 4.375, 3.75,
]

def render_forecast_table(table_block):
    headers = table_block["headers"]
    widths = _FORECAST_COL_WIDTHS if len(_FORECAST_COL_WIDTHS) == len(headers) else [100.0 / len(headers)] * len(headers)
    colgroup = ''.join(f'<col style="width:{w}%">' for w in widths)
    def grp_cls(h):
        g = _FORECAST_GROUP_BY_HEADER.get(h)
        return f' class="sec-{g}"' if g else ''
    head_cells = ''.join(f'<th{grp_cls(h)}>{inline_to_html(h)}</th>' for h in headers)
    body_rows = []
    for row in table_block["rows"]:
        cells = ''.join(f'<td{grp_cls(h)}>{inline_to_html(v)}</td>' for h, v in zip(headers, row))
        body_rows.append(f'<tr>{cells}</tr>')
    return f'<table class="fcast"><colgroup>{colgroup}</colgroup><tr>{head_cells}</tr>{"".join(body_rows)}</table>'

_sec_forecast = _ch3.section("דוגמה להמחשה: כך נראית תוכנית לאורך זמן")
_fcb = _sec_forecast.blocks  # [illustrative-callout-lead, table, closing-note]
_forecast_table_block = next(b for b in _fcb if b["type"] == "table")
_forecast_intro = next(b for b in _fcb if b["type"] == "para" and b.get("lead"))
_forecast_closing = _fcb[-1]
PAGES.append(f'''<div class="page">
{pagehead("03", "דוגמה להמחשה: תוכנית לאורך זמן")}
<div class="eyebrow">להמחשה בלבד — לא תחזית</div>
<h1 class="sec">{_sec_forecast.title}</h1>
<div class="secrule" style="margin-bottom:6px"></div>
<div class="callout" style="margin:6px 0;padding:8px 16px">{_forecast_intro["html"]}</div>
<div class="tbl-legend">
  <span><span class="dot" style="background:var(--gold)"></span>שיווק</span>
  <span><span class="dot" style="background:var(--gold-deep)"></span>מסחר</span>
  <span><span class="dot" style="background:var(--muted)"></span>לקוחות חוזרים</span>
  <span><span class="dot" style="background:var(--purple)"></span>פיננסי</span>
</div>
{render_forecast_table(_forecast_table_block)}
{render_block(_forecast_closing)}
{pagefoot()}
</div>''')

# ==================================================================
# 15 — Genesis specialist lenses
# ==================================================================
_icon_a = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="var(--gold-deep)" stroke-width="1.5"><rect x="4" y="12" width="3" height="7"/><rect x="10.5" y="8" width="3" height="11"/><rect x="17" y="4" width="3" height="15"/></svg>'
_icon_b = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="var(--gold-deep)" stroke-width="1.5"><path d="M3 12h4l3-7 4 14 3-7h4"/></svg>'
_icon_c = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="var(--muted)" stroke-width="1.5"><circle cx="12" cy="9" r="4"/><path d="M5 20c1-3.5 4-5 7-5s6 1.5 7 5"/></svg>'
_icon_d = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="var(--purple)" stroke-width="1.5"><path d="M4 19l4-9 4 5 4-8 4 12"/></svg>'
_ch4 = G.chapter("4")
_sec_lenses = _ch4.section("מה עומד מאחורי מחקר Genesis")
PAGES.append(f'''<div class="page">
{pagehead("03", _sec_lenses.title)}
<div class="eyebrow">לא נקודת מבט אחת</div>
<h1 class="sec">{_sec_lenses.title}</h1>
<div class="secrule"></div>
{render_block(_sec_lenses.blocks[0])}
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
# 15.1 — Genesis output rights
# ==================================================================
_sec_rights = _ch4.section("מה מקבלים, ומה זה לא כולל")
_rb = _sec_rights.blocks  # [what-you-get, what-you-dont-warn, buyout, continued-fine, secrecy-fine, separate-genesis-fine]
PAGES.append(content_page("03", _sec_rights.title, "שקיפות מלאה", _sec_rights.title, render_blocks(_rb[0:2])))
PAGES.append(content_page("03", _sec_rights.title + " (המשך)", "שקיפות מלאה", _sec_rights.title + " — המשך", render_blocks(_rb[2:])))

# ==================================================================
# 16 — Process diagram. Steps are the section's own numbered list, in
# order; "לקוחות קיימים:" is that section's own leading-bold callout.
# ==================================================================
_sec_process = _ch4.section("מהמדריך להצעה")
_process_olist = next(b for b in _sec_process.blocks if b["type"] == "olist")
_process_existing_clients = next(b for b in _sec_process.blocks if b["type"] == "para")
_steps_html = "".join(
    f'<div class="pstep"><div class="pnum">{i}</div><div class="ptxt">{item}</div></div>'
    for i, item in enumerate(_process_olist["items"], start=1)
)
PAGES.append(content_page("03", _sec_process.title, "התהליך", _sec_process.title, "\n".join([
    f'<div class="process">{_steps_html}</div>',
    render_block(_process_existing_clients),
])))

# ==================================================================
# 17 — Reminder
# ==================================================================
PAGES.append(generic_section_page("03", _ch4.section("תזכורת"), "לפני שממשיכים לטופס", breadcrumb_title="תזכורת"))

# ==================================================================
# 18 — Intake divider. Every field row below is a verbatim md bullet
# (one bullet -> one field row); the 3 igroups are the .md's own "א./ב./
# ג." subsections, not a hand-split 9-group layout — a simplification
# from the previous hand-split design (documented in the build report).
# ==================================================================
_intake = G.chapter("טופס_קליטה")
PAGES.append(f'''<div class="page dark divider">
  <div class="divider-ghost">04</div>
  <div class="divider-inner">
    <div class="divider-eyebrow"><span class="dash"></span>הצעד הבא</div>
    <div class="divider-title">{_intake.title}</div>
    <div class="divider-sub">המידע כאן משמש לתכנון בלבד ואינו קובע בעצמו היקף, מחיר או תנאים מחייבים. תמציתי במכוון, ואורך כ-5 דקות למילוי.</div>
    <div class="divider-endrule"></div>
  </div>
</div>''')

def field(label_html):
    return f'<div class="f"><span class="flabel">{label_html}</span><span class="fline"></span></div>'

def igroup(num, title, note_html, items_html):
    parts = [f'<div class="igroup"><div class="igroup-head"><span class="igroup-num">{num:02d}</span><span class="igroup-title">{title}</span></div>']
    if note_html:
        parts.append(f'<div class="igroup-note">{note_html}</div>')
    parts.append('<div class="ifields">' + "".join(field(it) for it in items_html) + '</div></div>')
    return "".join(parts)

_intake_intro = _intake.intro_blocks()[0]["html"]
_sec_a = _intake.section("א. הלקוח והעסק")
_sec_b = _intake.section("ב. מסחרי")
_sec_c = _intake.section("ג. אסטרטגי")
_a_ulist = next(b for b in _sec_a.blocks if b["type"] == "ulist")
_b_ulist = next(b for b in _sec_b.blocks if b["type"] == "ulist")
_c_ulist = next(b for b in _sec_c.blocks if b["type"] == "ulist")
_c_outro = next(b for b in _sec_c.blocks if b["type"] == "para")
_b_note = "<br><br>".join(
    (f'<em>{inline_to_html(b["text"][1:-1])}</em>' if b.get("italic_whole") else b["html"])
    for b in _sec_b.blocks if b["type"] == "para"
)

PAGES.append(f'''<div class="page">
{pagehead("04", "טופס קליטה")}
<div class="eyebrow">טופס קליטה</div><h1 class="sec">טופס קליטה</h1><div class="secrule"></div>
<p class="intake-intro">{_intake_intro}</p>
{igroup(1, _sec_a.title, None, _a_ulist["items"])}
{igroup(2, _sec_b.title, _b_note, _b_ulist["items"])}
{pagefoot()}
</div>''')

PAGES.append(f'''<div class="page">
{pagehead("04", "טופס קליטה (המשך)")}
{igroup(3, _sec_c.title, None, _c_ulist["items"])}
<p class="fine">{_c_outro["html"]}</p>
{pagefoot()}
</div>''')

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

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

Chapter map (content-architecture refinement pass, v3.0): 10 numbered
chapters. Two chapter numbers are LOAD-BEARING beyond this file —
AGREEMENT_SHORT_HE.md §1 hardcodes "מדריך הלקוח, פרק 2" for the Track
A/B/C/0 definitions, and §11(a) hardcodes "מדריך הלקוח, פרק 1" for the
heading "יסודות עלות ההגנה על נכסי הארגון" — so chapter 1 (who we are +
the org's protected assets) and chapter 2 (commercial models) keep those
exact numbers even though this is otherwise a full narrative reorder.
See CLIENT_GUIDE_HE.md's own chapter order for the rest.

Content-architecture pass, v3.1: the standalone end-of-document "Intake
Form" chapter is gone. Every field it used to collect now lives inline,
right after the explanatory paragraph it belongs to, in whichever
chapter that is (1, 3, 4, 7 or 8) — see md_guide_parser.py's render_flist
for the markdown-level convention (`- [ ] label`) and CSS section for
the shared dotted-line field-row look this produces wherever it's used.
Chapter 10 closes with a short "where to find each field" index instead
of the old form.
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

/* ---------- INLINE FILL-IN FIELDS ----------
   Content-architecture pass (v3.0): fields used to live only in one
   consolidated "Intake Form" chapter at the end, laid out under a
   numbered .igroup header (a circle badge + group title) with the
   field rows indented 38px to sit clear of that badge. Fields now sit
   inline, right after the explanatory paragraph they belong to, inside
   a chapter/section that already carries its own heading — so the
   .igroup wrapper is gone and .ifields starts flush with the body copy
   around it (margin-inline-start:0) rather than indented under a badge
   that no longer exists. Same dotted-line field-row look throughout;
   see md_guide_parser.py's render_flist for the markdown convention
   (`- [ ] label`) that produces this block wherever it's used. */
.ifields{margin-inline-start:0;font-family:"Heebo",sans-serif;font-size:9.3pt;
 color:#382c1f;line-height:2.2;margin-top:4px;margin-bottom:10px}
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
 h1.sec,h2.sub,.divider-title,.eyebrow{break-after:avoid}
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
    every sub-page below that has no bespoke visual, and ready as-is for
    chapters added after this fix lands."""
    body = render_blocks(section.blocks)
    return content_page(num, breadcrumb_title or section.title, eyebrow, section.title, body)


def divider(num, chapter, sub, ghost=None):
    """Shared shell for every chapter's dark section-divider page."""
    return f'''<div class="page dark divider">
  <div class="divider-ghost">{ghost if ghost is not None else num}</div>
  <div class="divider-inner">
    <div class="divider-eyebrow"><span class="dash"></span>פרק {num}</div>
    <div class="divider-title">{chapter.title}</div>
    <div class="divider-sub">{sub}</div>
    <div class="divider-endrule"></div>
  </div>
</div>'''


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
  <div class="cover-sub">מי אנחנו · איך אנחנו עובדים · מה עומד מאחורי העבודה<br>קריאה לפני תחילת הדרך המשותפת</div>
  <div class="cover-tags"><span class="cover-tag">סודי</span><span class="cover-tag">גרסה {G.version} · {G.updated_date}</span></div>
  <div class="cover-foot">CONFIDENTIAL · LOS GARDIOS GROUP</div>
</div>''')

# ==================================================================
# DIVIDER 01 — How Los Gardios Works (identity, operating mechanics,
# who-decides-what, and the org's protected assets). Chapter number is
# load-bearing: AGREEMENT_SHORT_HE.md §11(a) cites "מדריך הלקוח, פרק 1"
# by the exact heading "יסודות עלות ההגנה על נכסי הארגון" — see module
# docstring.
# ==================================================================
_ch1 = G.chapter("1")
PAGES.append(divider("01", _ch1,
    "מי אנחנו, איך ההתקשרות מתנהלת, מי קובע מה, ואילו נכסים ומערכות עומדים מאחורי העבודה."))

# ------------------------------------------------------------------
# 1.1 — Who we are + how the relationship works
# ------------------------------------------------------------------
_sec_who = _ch1.section("מי אנחנו")
_sec_how = _ch1.section("איך ההתקשרות מתנהלת")
PAGES.append(f'''<div class="page">
{pagehead("01", _sec_who.title)}
<div class="eyebrow">זהות</div>
<h1 class="sec">{_sec_who.title}</h1>
<div class="secrule"></div>
{render_blocks(_sec_who.blocks)}
<h2 class="sub">{_sec_how.title}</h2>
{render_blocks(_sec_how.blocks)}
{pagefoot()}
</div>''')

# ------------------------------------------------------------------
# 1.2 — The client-controlled principle + who-decides-what
# ------------------------------------------------------------------
_sec_principle = _ch1.section("העיקרון המנחה: הלקוח קובע את המסגרת")
_sec_control = _ch1.section("מי קובע מה — הלקוח מול הארגון")
PAGES.append(content_page("01", _sec_principle.title, "עקרון התפעול", _sec_principle.title, "\n".join([
    render_blocks(_sec_principle.blocks),
    f'<h2 class="sub">{_sec_control.title}</h2>',
    render_blocks(_sec_control.blocks),
])))

# ------------------------------------------------------------------
# 1.3 — Organization's assets (table -> cardgrid)
# ------------------------------------------------------------------
def cardgrid_from_table(table_block, grid="grid2"):
    cards = []
    for row in table_block["rows"]:
        label, body = row[0], row[1]
        cards.append(f'<div class="card"><div class="card-label">{inline_to_html(label)}</div><p>{inline_to_html(body)}</p></div>')
    return f'<div class="cardgrid {grid}">' + "".join(cards) + '</div>'

_sec_assets = _ch1.section("נכסי הארגון וההשקעה שביסודם")
_assets_blocks = _sec_assets.blocks  # [para(intro), para(list-lead-in), table, para(operative rule)]
_sec_cost = _ch1.section("יסודות עלות ההגנה על נכסי הארגון")
_assets_body = "\n".join([
    render_block(_assets_blocks[0]),
    render_block(_assets_blocks[1]),
    cardgrid_from_table(_assets_blocks[2]),
    render_block(_assets_blocks[3]),
    f'<h2 class="sub">{_sec_cost.title}</h2>',
    render_blocks(_sec_cost.blocks),
])
PAGES.append(content_page("01", _sec_assets.title, "מה עומד מאחורי העבודה", _sec_assets.title, _assets_body))

# ------------------------------------------------------------------
# 1.4 — Cost basis behind the protection floors (Phase 2 compression:
# merged onto 1.3's page above as a sub-heading instead of its own
# page — its remaining content was the worked example only, the
# generic abstract restatement was cut as a duplicate of 1.3's own
# intro paragraph. NOT deleted: AGREEMENT_SHORT_HE.md §11(a) cites this
# exact heading text within chapter 1 (see module docstring) — the
# heading and its section() lookup both still exist, just rendered on
# 1.3's page rather than via a standalone generic_section_page call.
# ------------------------------------------------------------------

# ------------------------------------------------------------------
# 1.5 — Business identity fields (content-architecture pass, v3.1):
# these used to live in the standalone Intake Form at the end of the
# document; they're general administrative/context fields with no
# single strong topical home elsewhere in the guide, so they sit at the
# end of chapter 1 instead. Generic fallback page — plain paragraphs +
# one inline field group, nothing that needs a bespoke layout.
# ------------------------------------------------------------------
PAGES.append(generic_section_page("01", _ch1.section("כמה פרטים בסיסיים עליכם ועל העסק"), "פרטים מנהליים"))

# ==================================================================
# DIVIDER 02 — Engagement Models. Chapter number is load-bearing:
# AGREEMENT_SHORT_HE.md §1 cites "מדריך הלקוח, פרק 2" for the Track
# A/B/C/0 definitions.
# ==================================================================
_ch2 = G.chapter("2")
PAGES.append(divider("02", _ch2,
    "ארבעת המסלולים שההסכם תומך בהם, ומה קורה אם אתם מסיימים ביוזמתכם לפני הזמן."))

# ------------------------------------------------------------------
# 2.1 — The four tracks. Each track is its own md paragraph, whose
# leading bold span is "מסלול <letter> — <title>." — the badge and card
# title are derived from that lead (never retyped), the card body from
# the rest of that same paragraph.
# ------------------------------------------------------------------
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

# ------------------------------------------------------------------
# 2.2 — Exit schedule (the flexibility/staged-architecture and shared-
# growth sections that used to share this page moved to chapter 8,
# "מצבי צמיחה" — see build report point 3).
# ------------------------------------------------------------------
PAGES.append(generic_section_page("02", _ch2.section("אם אתם מסיימים ביוזמתכם, מוקדם — לוח הנסיגה"), "אם ההתקשרות מסתיימת מוקדם"))

# ==================================================================
# DIVIDER 03 — Budget / investment / timeline
# ==================================================================
_ch3 = G.chapter("3")
PAGES.append(divider("03", _ch3,
    "איך אנחנו חושבים על תקציב, מדוע אנחנו שואלים עליו, ואיך זה מתורגם לתוכנית אמיתית."))

def first_sentence_split(raw):
    """A bespoke page's h1.sec pull-quote headline: the section's own
    first sentence (split on the first '. '), never a separately typed
    headline. Returns (headline_without_period, rest_of_paragraph_html)."""
    parts = re.split(r'(?<=\.)\s+', raw, maxsplit=1)
    head = parts[0].rstrip('.')
    rest = parts[1] if len(parts) > 1 else ''
    return inline_to_html(head), inline_to_html(rest)

# NOTE: this file used to also define qmark_lines()/split_ask() here —
# a pair of helpers that split a single running-prose "ספרו לנו: Q? Q?"
# paragraph into a .prompt reflection box at render time. Content-
# architecture pass v3.1 rewrote every section that needed them so the
# .md itself now writes those questions as real field bullets
# (`- [ ] ...`, see md_guide_parser.py's render_flist) instead of prose
# for a page-time splitter to pick apart — so both helpers were removed
# as dead code rather than kept unused.

# ------------------------------------------------------------------
# 3.1 — Opening hook: the section's own first sentence as the page's
# headline (see first_sentence_split), the rest of that paragraph plus
# the section's remaining two paragraphs as body copy.
# ------------------------------------------------------------------
_sec_why = _ch3.section("למה אנחנו שואלים על כך")
_headline, _rest0 = first_sentence_split(_sec_why.blocks[0]["text"])
PAGES.append(content_page("03", "למה אנחנו שואלים", "פתיח", _headline, "\n".join([
    f'<p class="body-copy">{_rest0}</p>',
    render_block(_sec_why.blocks[1]),
    render_block(_sec_why.blocks[2]),
])))

# ------------------------------------------------------------------
# 3.2 — Operating-model flow. Diagram stage captions ("אתם"/"אנחנו
# בוחנים"/"יחד" + short sub-captions) are hand-authored diagram
# scaffolding (they label the graphic, they aren't sentences of prose);
# every paragraph of actual prose on this page is the section's own two
# blocks, rendered in full.
# ------------------------------------------------------------------
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

# ------------------------------------------------------------------
# 3.3 — Trust + permission (pull-quote). The oversized quote is this
# section's own leading bold sentence (split_lead), never retyped.
# ------------------------------------------------------------------
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

# ------------------------------------------------------------------
# 3.4 — Two paths. The two bullets become the two stacked cards; card
# labels are Hebrew ordinal captions (נתיב א׳/ב׳ — a card index, not
# prose), card body is each bullet's own text.
# ------------------------------------------------------------------
_HEBREW_ORDINALS = ["א׳", "ב׳", "ג׳", "ד׳"]
_sec_paths = _ch3.section("שני נתיבים אפשריים")
_paths_ulist = _sec_paths.blocks[1]
_path_cards = []
for i, item_html in enumerate(_paths_ulist["items"]):
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
    render_blocks(_sec_paths.blocks[2:]),
])
PAGES.append(content_page("03", _sec_paths.title, "בחירה", _sec_paths.title, _paths_body))

# ------------------------------------------------------------------
# 3.5 — Goals. Content-architecture pass, v3.1: this used to be one
# running-prose "ספרו לנו: Q? Q? Q?" paragraph split apart at render
# time by split_ask into a .prompt reflection box; the .md now writes
# the three questions as real field bullets (`- [ ] ...`), so the
# generic renderer (render_blocks) already produces the field rows —
# no bespoke splitting code needed any more.
# ------------------------------------------------------------------
PAGES.append(generic_section_page("03", _ch3.section("היעד והציפיות שלכם"), "לפני המספרים"))

# ------------------------------------------------------------------
# 3.6 — Investment framework. "ספרו לנו:" + a real field list (`- [ ]`)
# in the .md renders via the generic flist treatment (dotted-line field
# rows) — previously a bespoke prompt-label/prompt-q box; upgraded to
# actual fill-in rows now that this page is also where the reader
# answers, not just where they read the question (build report point 6
# / the "upgrade a matching ספרו לנו prompt instead of duplicating it"
# instruction).
# ------------------------------------------------------------------
_sec_invest = _ch3.section("מסגרת ההשקעה שלכם")
_ib = _sec_invest.blocks  # [intro, "ספרו לנו:", flist(4), reminder-para, terms-para, track0-fine]
_invest_body = "\n".join([
    render_block(_ib[0]),
    render_block(_ib[1]),
    render_block(_ib[2]),
    render_block(_ib[3]),
    '<div class="eyebrow" style="margin-top:8px">מסגרת A/B/C — מה שכדאי לדעת כבר עכשיו</div>',
    '<div class="stats" style="margin:6px 0">'
    '<div class="stat"><div class="stat-num">3</div><div class="stat-cap">חודשים · התחייבות תקציב מינימלית</div></div>'
    '<div class="stat"><div class="stat-num">30</div><div class="stat-cap">יום · הודעה מראש להפחתת תקציב</div></div>'
    '</div>',
    render_block(_ib[4]),
    # Compact .fine treatment (not .callout): this page is already dense
    # (field rows + stat tiles), and .callout's padding/border-on-all-
    # sides pushed the page's pagefoot onto a near-empty extra page even
    # after tightening its spacing. This note is a scoping/definitional
    # aside (which chapters don't apply to you), which is what .fine is
    # for anyway; its lighter treatment (border-inline-start only, no
    # fill) reclaims the remaining vertical space. Matches the generic
    # classification (see ASIDE_CLASS — "הערה ללקוחות מסלול 0:" -> fine).
    f'<div class="fine" style="margin:4px 0 0">{_ib[5]["html"]}</div>',
])
PAGES.append(content_page("03", _sec_invest.title, "תשומת הקלט המרכזית", _sec_invest.title, _invest_body))

# ------------------------------------------------------------------
# 3.7 — Timeline (generic; see 3.5's comment — same conversion)
# ------------------------------------------------------------------
PAGES.append(generic_section_page("03", _ch3.section("טווח הזמן שלכם"), "תכנון"))

# ------------------------------------------------------------------
# 3.8 — Financial boundaries (generic body + the existing default-value
# stat tiles, kept as hand-authored presentation since they're not a
# sentence of prose but a compact restatement of the two defaults
# already stated in the section's own closing paragraph)
# ------------------------------------------------------------------
_sec_bounds = _ch3.section("גבולות פיננסיים")
PAGES.append(content_page("03", _sec_bounds.title, "הגנה עליכם", _sec_bounds.title, "\n".join([
    render_blocks(_sec_bounds.blocks),
    '<div class="eyebrow" style="margin-top:18px">ברירות המחדל, אם לא תיקבע תקרה</div>',
    '<div class="stats">'
    '<div class="stat"><div class="stat-num">30</div><div class="stat-cap">יום · תקופת מדידת Stop-Loss</div></div>'
    '<div class="stat"><div class="stat-num">10%</div><div class="stat-cap">חריגה מותרת מהתקציב החודשי</div></div>'
    '</div>',
])))

# ------------------------------------------------------------------
# 3.9 — Strategic boundaries (new subsection — content-architecture
# pass, v3.1: strategic red lines used to live only in the end-of-
# document Intake Form; placed as a sibling of "גבולות פיננסיים" here).
# ------------------------------------------------------------------
PAGES.append(generic_section_page("03", _ch3.section("גבולות אסטרטגיים"), "הגנה עליכם"))

# ==================================================================
# DIVIDER 04 — Genesis. Previously mentioned only as the tail of the
# old chapter 3/4 split, with no divider of its own — this fixes that
# (build report point 2).
# ==================================================================
_ch4 = G.chapter("4")
PAGES.append(divider("04", _ch4,
    "מה עומד מאחורי מחקר Genesis, מה מקבלים בסופו, ומה קורה אם תבחרו ליישם אותו בעצמכם."))

# ------------------------------------------------------------------
# 4.1 — Genesis specialist lenses
# ------------------------------------------------------------------
_icon_a = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="var(--gold-deep)" stroke-width="1.5"><rect x="4" y="12" width="3" height="7"/><rect x="10.5" y="8" width="3" height="11"/><rect x="17" y="4" width="3" height="15"/></svg>'
_icon_b = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="var(--gold-deep)" stroke-width="1.5"><path d="M3 12h4l3-7 4 14 3-7h4"/></svg>'
_icon_c = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="var(--muted)" stroke-width="1.5"><circle cx="12" cy="9" r="4"/><path d="M5 20c1-3.5 4-5 7-5s6 1.5 7 5"/></svg>'
_icon_d = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="var(--purple)" stroke-width="1.5"><path d="M4 19l4-9 4 5 4-8 4 12"/></svg>'
_sec_lenses = _ch4.section("מה עומד מאחורי מחקר Genesis")
PAGES.append(f'''<div class="page">
{pagehead("04", _sec_lenses.title)}
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

# ------------------------------------------------------------------
# 4.2 — Genesis output rights
# ------------------------------------------------------------------
_sec_rights = _ch4.section("מה מקבלים, ומה זה לא כולל")
_rb = _sec_rights.blocks  # [what-you-get, what-you-dont-warn, buyout, continued-fine, secrecy-fine, separate-genesis-fine]
PAGES.append(content_page("04", _sec_rights.title, "שקיפות מלאה", _sec_rights.title, render_blocks(_rb[0:2])))
PAGES.append(content_page("04", _sec_rights.title + " (המשך)", "שקיפות מלאה", _sec_rights.title + " — המשך", render_blocks(_rb[2:])))

# ==================================================================
# DIVIDER 05 — Project Infrastructure (new chapter — build report
# point 4). Source-backed: the specialist-mix fragment already in the
# old chapter 1, plus Atlas Network, plus a short synthesis paragraph
# on the org's operational (not just advisory) capability once a
# project moves past Genesis into execution.
# ==================================================================
_ch5 = G.chapter("5")
PAGES.append(divider("05", _ch5,
    "מה עומד מאחורי הביצוע בפועל של הפרויקט, מעבר לשלב המחקר — ואיך Atlas Network מרחיב את הטווח התפעולי."))

PAGES.append(generic_section_page("05", _ch5.section("מה עומד מאחורי הביצוע בפועל"), "מייעוץ לביצוע"))
PAGES.append(generic_section_page("05", _ch5.section("Atlas Network"), "רשת מסחרית בינלאומית"))

# ==================================================================
# DIVIDER 06 — Human Capital & Proprietary Technology (new chapter —
# build report point 4: separates WHAT the org's people/tech are from
# WHY protecting them costs what it costs, which chapter 1 covers).
# ==================================================================
_ch6 = G.chapter("6")
PAGES.append(divider("06", _ch6,
    "מי מפעיל את הפרויקט שלכם בפועל, ואיזו תשתית טכנולוגית — Neuron — עומדת מאחורי הצוות."))

PAGES.append(generic_section_page("06", _ch6.section("הון אנושי"), "הרשת שמאחורי הצוות"))
PAGES.append(generic_section_page("06", _ch6.section("טכנולוגיה קניינית ומערכות פנימיות"), "תשתית תפעולית"))
PAGES.append(generic_section_page("06", _ch6.section("נתונים, פגישות ופרטיות — בקצרה"), "בקצרה"))

# ==================================================================
# DIVIDER 07 — Break-Even (its own chapter now — build report point 6:
# previously folded into the old budget chapter, now clearly separated
# from both the client's investment frame (chapter 3) and growth modes
# (chapter 8)).
# ==================================================================
_ch7 = G.chapter("7")
PAGES.append(divider("07", _ch7,
    "למה ברירת המחדל שלנו היא לפעול בנקודת איזון, ומה זה אומר בפועל — כלי תכנון, לא הבטחת רווח."))

# ------------------------------------------------------------------
# 7.1 — Sustainability principle (horizon rings)
# ------------------------------------------------------------------
_rings = []
_radii = [14, 24, 35, 47, 60]
for i, r in enumerate(_radii):
    t = i / (len(_radii) - 1)
    # gold -> purple stroke gradient across rings
    color = f"rgb({int(169+(91-169)*t)},{int(130+(41-130)*t)},{int(79+(134-79)*t)})"
    _rings.append(f'<circle cx="70" cy="70" r="{r}" fill="none" stroke="{color}" stroke-opacity="{0.55-0.07*i:.2f}" stroke-width="1"/>')
_horizon_svg = f'<svg class="horizon-svg" width="140" height="140" viewBox="0 0 140 140">{"".join(_rings)}<circle cx="70" cy="70" r="4" fill="var(--gold)"/></svg>'
_sec_sustain = _ch7.section("העיקרון שמנחה אותנו: לא למצות עד הסוף")
PAGES.append(content_page("07", "העיקרון שמנחה אותנו", "עמדה שקופה", "לא למצות עד הסוף", "\n".join([
    f'<div class="horizon-wrap">{_horizon_svg}<div class="horizon-cap">{_sec_sustain.blocks[0]["html"]}</div></div>',
    render_block(_sec_sustain.blocks[1]),
])))

# ------------------------------------------------------------------
# 7.2 — Break-even. Content-architecture pass, v3.1: the single "ספרו
# לנו, אם ידוע לכם: ...?" ask paragraph is now a real field group
# (gross margin, AOV) right after the two-inputs table, and the floor
# note gained its own field group (alternate Break-Even definition,
# extra profitability targets) — both used to live only in the
# end-of-document Intake Form. Rendered generically around the one
# genuinely bespoke element on this page (the table, still via
# render_table so its column count picks the right micro/data class);
# found positionally rather than by a fixed index so this page doesn't
# need updating again if a future edit adds or removes a field group.
# ------------------------------------------------------------------
_sec_breakeven = _ch7.section("נקודת האיזון (Break-Even) — במה מדובר")
_beb = _sec_breakeven.blocks
_be_table_i = next(i for i, b in enumerate(_beb) if b["type"] == "table")
_be_body = "\n".join([
    render_blocks(_beb[:_be_table_i]),
    render_table(_beb[_be_table_i]),
    render_blocks(_beb[_be_table_i + 1:]),
])
PAGES.append(content_page("07", "נקודת האיזון (Break-Even)", "כלי תכנון, לא הבטחה", "נקודת האיזון (Break-Even)", _be_body))

# ------------------------------------------------------------------
# 7.3 — Illustrative forecast example table. Column VALUES and headers
# come straight from the .md's own table (no second, hand-typed copy of
# the same numbers to drift out of sync); only the per-column-group
# coloring and fixed pixel-measured widths — pure presentation — stay
# Python-authored, keyed by header text so they survive column
# reordering as long as the header text itself doesn't change.
# ------------------------------------------------------------------
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

_sec_forecast = _ch7.section("דוגמה להמחשה: כך נראית תוכנית לאורך זמן")
_fcb = _sec_forecast.blocks  # [illustrative-callout-lead, table, closing-note]
_forecast_table_block = next(b for b in _fcb if b["type"] == "table")
_forecast_intro = next(b for b in _fcb if b["type"] == "para" and b.get("lead"))
_forecast_closing = _fcb[-1]
PAGES.append(f'''<div class="page">
{pagehead("07", "דוגמה להמחשה: תוכנית לאורך זמן")}
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
# DIVIDER 08 — Growth Modes (new chapter — build report point 3).
# Source-backed: the tolerance-level table already carried a "הרחבה
# מרבית (Scale)" option, the staged/graduated commercial architecture
# already existed in the old chapter 2, and Track B/C's value-sharing
# alignment already existed there too — this chapter unifies the three
# under one banner rather than inventing anything new.
# ==================================================================
_ch8 = G.chapter("8")
PAGES.append(divider("08", _ch8,
    "כמה מרחב נשימה אתם מוכנים לתת למודל כדי לצמוח מעבר לנקודת האיזון — ואילו מבנים מסחריים תומכים בכך."))

_ch8_intro = _ch8.intro_blocks()[0]

# ------------------------------------------------------------------
# 8.1 — Tolerance. Content-architecture pass, v3.1: the single running-
# prose ask ("ספרו לנו: ...?") is now a real field group (tolerance
# period, tolerance level, temporary-deficit willingness + cap, AND the
# Stop-Loss measurement period — the latter used to sit only in the
# Intake Form's commercial section, moved here since its default is
# cross-referenced from this very section's deficit paragraph) — one
# extra block vs. before, so the two-physical-page split point below is
# [0,1,2] / [3,4,5,6] rather than the old [0,1,2] / [3,4,5].
# ------------------------------------------------------------------
_sec_tol = _ch8.section("רמת ותקופת הסובלנות שלכם")
_tb2 = _sec_tol.blocks  # [plain-terms, example, default-callout, deficit-callout, ask-lead, ask-flist, rights]
# Split across two physical pages — see the four-tracks page's comment.
PAGES.append(content_page("08", _sec_tol.title, "גמישות סביב רווחיות", _sec_tol.title, "\n".join([
    render_block(_ch8_intro),
    render_block(_tb2[0]),
    render_block(_tb2[1]),
    render_block(_tb2[2]),
])))
_tol_body2 = "\n".join([
    render_block(_tb2[3]),
    render_block(_tb2[4]),
    render_block(_tb2[5]),
    render_block(_tb2[6]),
])
PAGES.append(content_page("08", _sec_tol.title + " (המשך)", "גמישות סביב רווחיות", _sec_tol.title + " — המשך", _tol_body2))

# ------------------------------------------------------------------
# 8.2 — Staged commercial architecture + shared growth. Two md sections
# combined onto one page (a page-grouping choice), the second kept
# under its own real section-title as an h2.sub.
# ------------------------------------------------------------------
_sec_flex = _ch8.section("גמישות מסחרית — ארכיטקטורה, לא הנחה")
_sec_growth = _ch8.section("צמיחה משותפת — עד כמה שהמבנה המסחרי מאפשר זאת")
_flex_body = "\n".join([
    render_blocks(_sec_flex.blocks),
    f'<h2 class="sub">{_sec_growth.title}</h2>',
    render_blocks(_sec_growth.blocks),
])
PAGES.append(content_page("08", _sec_flex.title, "ארכיטקטורה, לא הנחה", _sec_flex.title, _flex_body))

# ==================================================================
# DIVIDER 09 — Execution & Ongoing Reporting (new chapter — build
# report point 6: the oversight mechanics that used to be folded into
# the old budget chapter, now clearly the "actual deployed budget"
# control layer).
# ==================================================================
_ch9 = G.chapter("9")
PAGES.append(divider("09", _ch9,
    "מה קורה אחרי החתימה: קצב הדיווח, מה טעון אישורכם, ומה קורה אם רף ה-Stop-Loss נחצה."))

# ------------------------------------------------------------------
# 9.1 — Oversight & reporting. Each bullet's own leading bold phrase
# becomes its card title (split_lead), the rest of that bullet its card
# body.
# ------------------------------------------------------------------
_sec_oversight = _ch9.section("בקרה ודיווח שוטף")
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
PAGES.append(content_page("09", _sec_oversight.title, "מה קורה אחרי החתימה", _sec_oversight.title, "\n".join([
    render_block(_sec_oversight.blocks[0]),
    '<div class="cardgrid grid3">' + "".join(_oversight_cards[:3]) + '</div>',
])))
PAGES.append(content_page("09", _sec_oversight.title + " (המשך)", "מה קורה אחרי החתימה", _sec_oversight.title + " — המשך", "\n".join([
    '<div class="cardgrid grid2">' + "".join(_oversight_cards[3:]) + '</div>',
])))

# ==================================================================
# DIVIDER 10 — The Practical Journey: Genesis to a signed Proposal
# (new chapter — build report point 4: this used to be the tail of the
# old Genesis chapter with no divider of its own; separating it from
# Genesis's own substance keeps chapter 4 focused and gives this
# step-by-step walkthrough its own well-placed home as the guide's
# closing chapter. Content-architecture pass, v3.1: this chapter used to
# lead into the standalone Intake Form (hence the arrow ghost numeral
# instead of "10"); now that the form is gone and chapter 10 is simply
# the last numbered chapter, it gets the normal ghost numeral like every
# other chapter divider.
# ==================================================================
_ch10 = G.chapter("10")
PAGES.append(divider("10", _ch10,
    "מ-Genesis ועד להצעה חתומה — התהליך המלא שלב אחר שלב, ואיפה למצוא כל שדה שנדרש מכם."))

# ------------------------------------------------------------------
# 10.1 — Process diagram. Steps are the section's own numbered list, in
# order; "לקוחות קיימים:" is that section's own leading-bold callout.
# ------------------------------------------------------------------
_sec_process = _ch10.section("מהמדריך להצעה")
_process_olist = next(b for b in _sec_process.blocks if b["type"] == "olist")
_process_existing_clients = next(b for b in _sec_process.blocks if b["type"] == "para")
_steps_html = "".join(
    f'<div class="pstep"><div class="pnum">{i}</div><div class="ptxt">{item}</div></div>'
    for i, item in enumerate(_process_olist["items"], start=1)
)
PAGES.append(content_page("10", _sec_process.title, "התהליך", _sec_process.title, "\n".join([
    f'<div class="process">{_steps_html}</div>',
    render_block(_process_existing_clients),
])))

# ------------------------------------------------------------------
# 10.2 — Reminder
# ------------------------------------------------------------------
PAGES.append(generic_section_page("10", _ch10.section("תזכורת"), "לפני שממשיכים", breadcrumb_title="תזכורת"))

# ------------------------------------------------------------------
# 10.3 — Where to find each field. Content-architecture pass, v3.1:
# this replaces the standalone end-of-document "## טופס קליטה" chapter
# (three igroups of field rows, collected in one place away from their
# explanations) now that every field lives inline, next to the
# paragraph that explains it, in chapters 1/3/4/7/8. Chapter 10 already
# carries the "here's the process" content this guide closes on, so
# this short index absorbs the old form's closing role instead of
# giving it a divider/chapter of its own. Generic fallback page — a
# short paragraph plus the section's own bullet list, nothing bespoke.
# ------------------------------------------------------------------
PAGES.append(generic_section_page("10", _ch10.section("איפה למצוא כל שדה"), "מפת השדות"))

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

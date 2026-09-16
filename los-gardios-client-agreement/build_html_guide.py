# -*- coding: utf-8 -*-
"""Render CLIENT_GUIDE_HE.md as a premium, editorial-feeling A4 RTL PDF.

Design language: dark espresso section dividers with ghost numerals, a
cream content-page body, a brass/gold accent system (rules, eyebrows,
stat tiles, key-insight callouts), and Los Gardios' own Velvet Purple
used sparingly as the brand-identity touch (logo mark, one accent line
on the cover) rather than as the dominant hue — the warm gold/espresso
palette is the editorial atmosphere; purple is the brand anchor.

The underlying Hebrew CONTENT is copied verbatim from CLIENT_GUIDE_HE.md
(source of truth); only its visual presentation and the Intake Form's
grouping/ordering are redesigned here.
"""
import io, os, base64

_HERE = os.path.dirname(os.path.abspath(__file__))
_ASSETS = os.path.join(_HERE, "assets")

def _data_uri(fname):
    with open(os.path.join(_ASSETS, fname), "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode("ascii")

LOGO_MARK = _data_uri("logo_mark_web.png")

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
.pagehead .crumb{color:var(--gold-deep);font-weight:600}
.pagehead.on-dark .crumb{color:var(--gold)}
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
 letter-spacing:.55em;margin:0 0 24px;color:var(--gold)}
.cover-title{font-family:"Frank Ruhl Libre",serif;font-weight:600;font-size:32pt;
 letter-spacing:.01em;margin:0 0 14px;color:#F7F1E4}
.cover-rule{width:56px;height:2px;background:linear-gradient(to left,var(--gold),var(--purple));margin:22px 0}
.cover-sub{font-family:"Heebo",sans-serif;font-weight:300;font-size:10.2pt;
 letter-spacing:.06em;color:#c9bda5;max-width:320px;line-height:1.95}
.cover-tags{position:absolute;bottom:60mm;display:flex;gap:10px}
.cover-tag{border:1px solid var(--espresso-line);color:#a99a7d;font-family:"Heebo",sans-serif;
 font-size:7.4pt;letter-spacing:.14em;padding:4px 12px;border-radius:1px}
.cover-foot{position:absolute;bottom:20mm;font-family:"Heebo",sans-serif;font-size:7.4pt;
 letter-spacing:.16em;color:#7c6f5a}

/* ---------- SECTION DIVIDER (dark, bottom-anchored, ghost numeral) ---------- */
.divider{min-height:257mm;display:flex;flex-direction:column;justify-content:flex-end;
 position:relative;overflow:hidden}
.divider-ghost{position:absolute;left:-6mm;bottom:8mm;font-family:"Frank Ruhl Libre",serif;
 font-weight:700;font-size:230pt;line-height:1;color:var(--gold-pale);z-index:0;user-select:none}
.divider-inner{position:relative;z-index:1;padding-bottom:8mm}
.divider-eyebrow{display:flex;align-items:center;gap:12px;font-family:"Heebo",sans-serif;
 font-size:8.2pt;letter-spacing:.28em;color:var(--gold);margin-bottom:16px}
.divider-eyebrow .dash{width:30px;height:1px;background:var(--gold)}
.divider-title{font-family:"Frank Ruhl Libre",serif;font-size:27pt;font-weight:600;
 max-width:520px;line-height:1.35;margin:0 0 16px;color:#F7F1E4}
.divider-sub{font-family:"Heebo",sans-serif;font-size:9.6pt;color:#b9ac93;
 max-width:420px;line-height:1.9;margin-bottom:18px}
.divider-endrule{width:36px;height:1px;background:var(--espresso-line)}

/* ---------- SECTION HEADING on content pages ---------- */
.eyebrow{font-family:"Heebo",sans-serif;font-size:8pt;letter-spacing:.24em;
 color:var(--gold-deep);font-weight:700;margin-bottom:6px}
h1.sec{font-family:"Frank Ruhl Libre",serif;font-size:20pt;font-weight:600;
 margin:0 0 10px}
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
.card{flex:1;background:var(--cream2);border:1px solid var(--rule);border-top:3px solid var(--gold);
 border-radius:2px;padding:16px 18px;break-inside:avoid-page;page-break-inside:avoid}
.card-label{font-family:"Heebo",sans-serif;font-size:7.6pt;letter-spacing:.2em;
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
.stats{display:flex;gap:10px;margin:18px 0}
.stat{flex:1;background:var(--cream2);border:1px solid var(--rule);border-radius:2px;
 padding:14px 8px;text-align:center;break-inside:avoid-page}
.stat-num{font-family:"Frank Ruhl Libre",serif;font-size:16pt;font-weight:700;color:var(--gold-deep)}
.stat-cap{font-family:"Heebo",sans-serif;font-size:7.6pt;color:var(--muted);
 margin-top:5px;line-height:1.5}

/* ---------- PROMPT / REFLECTION BOX ---------- */
.prompt{background:var(--cream2);border-radius:2px;padding:14px 18px;margin:14px 0;
 border-inline-start:2px solid var(--gold);break-inside:avoid-page;page-break-inside:avoid}
.prompt-label{font-family:"Heebo",sans-serif;font-size:7.6pt;letter-spacing:.2em;
 color:var(--gold-deep);font-weight:700;margin-bottom:6px}
.prompt-q{font-family:"Heebo",sans-serif;font-size:9.6pt;color:#382c1f;line-height:1.85}
.fine{font-family:"Heebo",sans-serif;font-size:8.5pt;color:var(--muted);
 line-height:1.8;border-inline-start:2px solid var(--rule);padding-inline-start:12px;margin:12px 0}

/* ---------- PROCESS DIAGRAM ---------- */
.process{margin:20px 0}
.pstep{display:flex;gap:16px;align-items:flex-start;padding:13px 0;
 border-bottom:1px solid var(--rule);break-inside:avoid-page}
.pstep:last-child{border-bottom:none}
.pnum{flex:none;width:28px;height:28px;border-radius:50%;background:var(--espresso);color:var(--gold);
 font-family:"Frank Ruhl Libre",serif;font-weight:700;font-size:11.5pt;
 display:flex;align-items:center;justify-content:center}
.ptxt{font-family:"Heebo",sans-serif;font-size:9.5pt;color:#382c1f;line-height:1.85;padding-top:3px}

/* ---------- INTAKE FORM ---------- */
.intake-intro{font-family:"Heebo",sans-serif;font-size:9.6pt;color:var(--muted);
 line-height:1.9;max-width:560px;margin-bottom:6px}
.igroup{margin:20px 0;break-inside:avoid-page;page-break-inside:avoid}
.igroup-head{display:flex;align-items:center;gap:12px;margin-bottom:8px}
.igroup-num{font-family:"Frank Ruhl Libre",serif;background:var(--espresso);color:var(--gold);
 width:26px;height:26px;border-radius:50%;display:flex;align-items:center;justify-content:center;
 font-weight:700;font-size:10pt;flex:none}
.igroup-title{font-family:"Frank Ruhl Libre",serif;font-size:12pt;font-weight:600}
.igroup-note{font-family:"Heebo",sans-serif;font-size:8.2pt;color:var(--gold-deep);
 margin-bottom:6px;margin-right:38px}
.ifields{margin-right:38px;font-family:"Heebo",sans-serif;font-size:9.3pt;
 color:#382c1f;line-height:2.2}
.ifields .f{display:flex;align-items:baseline;gap:8px;border-bottom:1px dotted var(--rule);
 padding:4px 0}
.ifields .f .flabel{flex:none;color:#4a3d2c}
.ifields .f .fline{flex:1;border-bottom:1px solid var(--rule);min-height:13px}

/* ---------- CLOSING (sign-off style) ---------- */
.closing{min-height:257mm;display:flex;flex-direction:column;justify-content:flex-end;
 position:relative;overflow:hidden}
.closing-ghost{position:absolute;left:0mm;bottom:-8mm;font-family:"Frank Ruhl Libre",serif;
 font-weight:700;font-size:210pt;line-height:1;color:var(--gold-pale);z-index:0;user-select:none}
.closing-inner{position:relative;z-index:1;padding-bottom:8mm}
.closing-eyebrow{display:flex;align-items:center;gap:12px;font-family:"Heebo",sans-serif;
 font-size:8.2pt;letter-spacing:.28em;color:var(--gold);margin-bottom:16px}
.closing-eyebrow .dash{width:30px;height:1px;background:var(--gold)}
.closing-title{font-family:"Frank Ruhl Libre",serif;font-size:25pt;font-weight:600;
 margin:0 0 16px;color:#F7F1E4}
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
 .card,.prompt,.callout,.stat,table{break-inside:avoid}
 h1.sec,h2.sub,.igroup-head,.divider-title{break-after:avoid}
}
"""

def pagehead(eyebrow, dark=False):
    cls = "pagehead on-dark" if dark else "pagehead"
    return f'''<div class="{cls}"><span class="brand"><img src="{LOGO_MARK}">LOS GARDIOS · מדריך הלקוח</span><span class="crumb">{eyebrow}</span><span class="org">לוס גרדיוס בע"מ</span></div>'''

def pagefoot():
    return '<div class="pagefoot"><span>סודי · טיוטת עבודה פנימית</span><span>© Los Gardios Group</span></div>'

PAGES = []

# ---- Cover ----
PAGES.append(f'''<div class="page dark cover">
  <img src="{LOGO_MARK}" class="cover-mark">
  <div class="cover-eyebrow">L O S &nbsp; G A R D I O S</div>
  <div class="cover-title">מדריך הלקוח</div>
  <div class="cover-rule"></div>
  <div class="cover-sub">תקציב · מסגרת השקעה · טווח זמן<br>קריאה לפני תחילת הדרך המשותפת</div>
  <div class="cover-tags"><span class="cover-tag">סודי</span><span class="cover-tag">גרסת מדריך 1</span></div>
  <div class="cover-foot">CONFIDENTIAL · LOS GARDIOS GROUP</div>
</div>''')

# ---- Section divider 01 ----
PAGES.append('''<div class="page dark divider">
  <div class="divider-ghost">01</div>
  <div class="divider-inner">
    <div class="divider-eyebrow"><span class="dash"></span>פרק 01</div>
    <div class="divider-title">תקציב, מסגרת השקעה וטווח זמן</div>
    <div class="divider-sub">איך אנחנו חושבים על תקציב, מדוע אנחנו שואלים עליו, ואיך זה מתורגם לתוכנית אמיתית.</div>
    <div class="divider-endrule"></div>
  </div>
</div>''')

# ---- Opening philosophy statement ----
PAGES.append(f'''<div class="page">
{pagehead("01 · למה אנחנו שואלים")}
<div class="eyebrow">פתיח</div>
<h1 class="sec">אנחנו לא מתחילים מ"הנה החבילה שלנו והמחיר שלה"</h1>
<div class="secrule"></div>
<p class="body-copy">אנחנו מתחילים מ: ספרו לנו מה אתם מנסים להשיג, כמה אתם באמת מוכנים ויכולים להשקיע, אילו אילוצים קיימים, ומה אתם מאמינים שאפשר. אנחנו נקבע מה ניתן לבנות באחריות בתוך המסגרת הזו.</p>
<p class="body-copy">לפני שאנחנו בונים תוכנית עסקית, שיווקית ופיננסית עבורכם, אנחנו צריכים להבין את המציאות הכלכלית שבתוכה אתם רוצים ויכולים לפעול. המידע הזה לא נועד לקבוע כמה אפשר לגבות מכם — הוא נועד לקבוע מה אפשר לבנות באחריות, בהיקף, בקצב ובמודל שמתאימים לעסק שלכם.</p>
<div class="callout"><span class="callout-label">העיקרון:</span> תקציב גדול יותר עשוי לאפשר היקף רחב יותר — אבל לא תוצאה טובה יותר מאליה. הקשר בין תקציב להיקף העבודה הוא שאלה של תכנון, לא הבטחה.</div>
<p class="body-copy"><strong>רמת תשומת הלב, המקצועיות וההשקעה שלנו בפרויקט שלכם אינה תלויה בגודל התקציב — היא זהה, בכל היקף עבודה.</strong> עסק עם פוטנציאל יוצא דופן, נזילות מוגבלת כרגע, הזדמנות שוק ייחודית או חזון מייסד חזק עשוי להצדיק מבנה מסחרי מותאם באותה מידה שעסק עם תקציב גדול יכול שלא להתאים לנו כלל. אנחנו בוחנים פוטנציאל, מציאות, משאבים, מחויבות והתאמה אסטרטגית — לא רק את גובה התקציב.</p>
{pagefoot()}
</div>''')

PAGES.append(f'''<div class="page">
{pagehead("01 · הכלל המנחה")}
<div class="eyebrow">הגישה שלנו</div>
<h1 class="sec">אתם מגדירים את המסגרת. אנחנו בוחנים מה אפשר לבנות בתוכה</h1>
<div class="secrule"></div>
<p class="body-copy">הכלל המנחה שלנו פשוט: אתם מגדירים את המסגרת הכלכלית שבה אתם רוצים לפעול, אנחנו בוחנים מה ניתן לבנות באחריות בתוכה, ורק אז אנחנו מציעים תוכנית ומודל מסחרי קונקרטיים. המטרה שלנו היא התקשרות שאתם יכולים לקיים לאורך זמן — לא התקשרות שדוחקת אתכם מעבר ליכולת שלכם.</p>
<p class="body-copy">מטרתנו איננה למקסם הוצאה. היא לשמר את יכולתו של העסק להמשיך להשקיע, לפעול ולצמוח. עסק שמיצה את תזרים המזומנים שלו אינו יכול להמשיך לבנות, לבחון, להרחיב, להשקיע או לשלם עבור משאבים מקצועיים — ולכן המטרה היא לבנות התקשרות שבת-קיימא כלכלית לשני הצדדים.</p>
<p class="body-copy">לפעמים, אחרי שנבחן את המסגרת שהגדרתם, נגיע למסקנה שהיא אינה תואמת את היקף הפרויקט המבוקש. במקרה כזה ננהל איתכם שיחה בתום-לב לפני כל החלטה על המשך התהליך — לא נבנה עבורכם הצעה שאיננו מאמינים שהיא בת-קיימא.</p>
<h2 class="sub">בקשה הדדית</h2>
<p class="body-copy">איכות האסטרטגיה תלויה באיכות המידע שעומד לרשותנו לבנייתה. אנחנו מבקשים מכם להיות גלויים לגבינו לגבי אילוצים, בדיוק כפי שאנחנו גלויים לגביכם לגבי מה שאנחנו מאמינים שריאלי. תנו לנו את המספר האמיתי — לא את המספר שאתם חושבים שאנחנו רוצים לשמוע. תקציב נמוך כרגע יכול להתקיים לצד הזדמנות גדולה מאוד לטווח ארוך; תקציב גדול, מצדו, אינו הופך עסק אוטומטית להזדמנות אסטרטגית.</p>
{pagefoot()}
</div>''')

# ---- Track 0 callout as its own card page ----
PAGES.append(f'''<div class="page">
{pagehead("01 · הערה למסלול מסוים")}
<div class="eyebrow">לתשומת לבכם</div>
<h1 class="sec">הערה ללקוחות מסלול 0</h1>
<div class="secrule"></div>
<div class="callout"><span class="callout-label">רלוונטי רק למסלול זה:</span> אם בחרתם ברכישת מחקר Genesis חד-פעמית בלבד, ללא תקציב שוטף ("מסלול 0", נספח A סעיף 2 להסכם) — רוב הפרקים הבאים בעמודים הקרובים (מסגרת השקעה, סובלנות, Stop-Loss, נקודת האיזון — נספח B סעיפים 1–3) אינם חלים עליכם, ואינכם נדרשים למלא את השדות הנוגעים אליהם. גם דמי ההשתתפות העצמית המוזכרים בהמשך שייכים למסלולים A/B/C בלבד — תנאי התשלום במסלול 0 מפורטים בנספח A סעיף 2. אפשר לדלג ישירות לתהליך שבסוף המדריך.</div>
<h2 class="sub">לפני שממשיכים — חשוב שתדעו</h2>
<p class="body-copy">המידע שתמסרו בפרק הזה משמש אותנו לתכנון, להערכה ולבניית ה"הצעה" — ואינו מהווה כשלעצמו התחייבות לרכישת שירותים, לתשלום סכום מסוים, לקבלת הצעה מסחרית מסוימת, או להשגת תוצאה עסקית כלשהי. שום מספר, טווח או ציפייה שתרשמו כאן אינם סופיים ואינם "נועלים" אתכם — תמיד אפשר לעדכן, לדייק או לשנות כיוון בהמשך השיחה. אם חלק מהמספרים עדיין לא ברורים לכם — זה בסדר גמור; נוכל להעריך אותם יחד. התנאים המסחריים המחייבים של כל "התקשרות ספציפית" נקבעים אך ורק ב"הצעה" חתומה כהגדרתה בהסכם ההתקשרות, שתקבלו בהמשך.</p>
{pagefoot()}
</div>''')

# ---- Two paths concept page ----
PAGES.append(f'''<div class="page">
{pagehead("01 · שני נתיבים אפשריים")}
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
    <p>אנחנו מציגים מבנה תמחור, ריטיינר או מודל אחר שלדעתנו המקצועית מתאים לפרויקט, ואתם שוקלים אותו. אפשר להשיב על השאלות הבאות בטווחים כלליים, לציין אילוצים בלבד, או להשאיר אותן לשיקול דעתנו המקצועי בהצעה הראשונית — אין צורך לנחש מספר.</p></div>
</div>
<h2 class="sub">גמישות מסחרית — לא הנחה</h2>
<p class="body-copy">כשההזדמנות, ההתאמה האסטרטגית והערך הצפוי לטווח ארוך מצדיקים זאת, הארגון עשוי לבנות את השתתפותו בהתקשרות באופן שונה — למשל מבנה מבוסס-אחוזים, מבנה משולב, היקף התחלתי מצומצם, או שלביות בהתקשרות. אלה מבני התקשרות שהמסמכים המשפטיים תומכים בהם, לא הנחות ולא צעד של רצון טוב — זו ארכיטקטורה מסחרית, שנועדה להתאים את ההתקשרות למציאות של העסק.</p>
{pagefoot()}
</div>''')

# ---- Reflection page: goals ----
PAGES.append(f'''<div class="page">
{pagehead("01 · היעד והציפיות שלכם")}
<div class="eyebrow">לפני המספרים</div>
<h1 class="sec">היעד והציפיות שלכם</h1>
<div class="secrule"></div>
<p class="body-copy">לפני המספרים, נשמח להבין מה אתם מנסים להשיג.</p>
<div class="prompt"><div class="prompt-label">שאלות למחשבה</div>
<div class="prompt-q">מהי התוצאה העסקית שאתם שואפים אליה?<br>איך תגדירו התקדמות עבור הפרויקט?<br>מהם הדברים החשובים לכם ביותר בו?</div></div>
<p class="fine">התשובות כאן מכוונות אותנו בעדיפויות ובטון של התוכנית שנבנה — הן אינן יעד מדיד או הבטחה להשגת תוצאה; היעדים המדידים בפועל, ככל שייקבעו, ייקבעו בהסכם ובטבלת התנאים המסחריים בלבד.</p>
{pagefoot()}
</div>''')

# ---- Investment framework ----
PAGES.append(f'''<div class="page">
{pagehead("01 · מסגרת ההשקעה שלכם")}
<div class="eyebrow">תשומת הקלט המרכזית</div>
<h1 class="sec">מסגרת ההשקעה שלכם</h1>
<div class="secrule"></div>
<p class="body-copy">השדה החשוב ביותר עבורנו כדי להתחיל לתכנן הוא <strong>התקציב החודשי</strong>; שאר השאלות כאן עוזרות לנו לדייק את התוכנית, וניתן לחדד אותן יחד איתנו בהמשך.</p>
<div class="prompt"><div class="prompt-label">ספרו לנו</div>
<div class="prompt-q">מהו התקציב החודשי המועדף עליכם?<br>האם יש היקף השקעה כולל שאתם מתכננים אליו?<br>מהו טווח הגמישות שלכם — תקציב קבוע, או מרחב תמרון בכפוף לאישורכם?<br>התקציב שאתם מוסרים כולל או לא כולל עלויות חיצוניות מסוימות (כגון תקציבי מדיה המועברים ישירות לפלטפורמות)?</div></div>
<p class="body-copy">המספר שתמסרו הוא נקודת פתיחה לתכנון בלבד — לא הצעת מחיר ולא רצפה מחייבת. התוכנית שנציג לכם עשויה להיות שונה ממנו, בכל כיוון.</p>
<div class="eyebrow" style="margin-top:22px">מסגרת A/B/C — מה שכדאי לדעת כבר עכשיו</div>
<div class="stats">
  <div class="stat"><div class="stat-num">3</div><div class="stat-cap">חודשים · התחייבות תקציב מינימלית</div></div>
  <div class="stat"><div class="stat-num">30</div><div class="stat-cap">יום · הודעה מראש להפחתת תקציב</div></div>
</div>
<p class="fine">שימו לב: במסלולים מבוססי-תקציב (A/B/C), לאחר שהתקציב ייקבע בהצעה החתומה, ההתחייבות התפעולית היא לתקציב חודשי קבוע לשלושה חודשים לפחות; הפחתתו לאחר מכן טעונה הודעה מוקדמת בכתב של 30 יום. זהו תנאי מההסכם עצמו (נספח B), לא תנאי מהפרק הזה — אך כדאי שתכירו אותו כבר עכשיו.</p>
{pagefoot()}
</div>''')

# ---- Timeline ----
PAGES.append(f'''<div class="page">
{pagehead("01 · טווח הזמן שלכם")}
<div class="eyebrow">תכנון</div>
<h1 class="sec">טווח הזמן שלכם</h1>
<div class="secrule"></div>
<p class="body-copy">פרויקט עסקי רציני כולל בדרך כלל שלבי מחקר, בדיקה, פיתוח, כניסה לשוק, איסוף נתונים ואופטימיזציה — לפני שאפשר למדוד את האפקט המסחרי שלו בבירור.</p>
<div class="prompt"><div class="prompt-label">ספרו לנו</div>
<div class="prompt-q">מהי התקופה שאתם מתכננים לפעול בה?<br>האם יש מועדים עסקיים משמעותיים שכדאי שנכיר?</div></div>
<p class="fine">זהו שיח תכנוני כללי בלבד. המספר המדויק שישמש בפועל למדידת ביצועים הוא <strong>תקופת הסובלנות</strong> שתקבעו בעמוד הבא, ותירשם בטבלת התנאים המסחריים.</p>
{pagefoot()}
</div>''')

# ---- Tolerance ----
PAGES.append(f'''<div class="page">
{pagehead("01 · רמת ותקופת הסובלנות שלכם")}
<div class="eyebrow">גמישות סביב רווחיות</div>
<h1 class="sec">רמת ותקופת הסובלנות שלכם</h1>
<div class="secrule"></div>
<p class="body-copy">תקופת הסובלנות היא הזמן שבו אתם מאפשרים לנו גמישות לפעול בתוך מסגרת התקציב שהגדרתם, מבלי לדרוש שההתקשרות תהיה רווחית כבר מהיום הראשון. לדוגמה: תקציב של 20,000 ₪ לחודש ותקופת סובלנות של חמישה חודשים אומרים שבמהלך התקופה הזו, אנחנו רשאים להשתמש בתקציב הזמין כדי לבנות, לבחון ולהרחיב את הפעילות — גם אם היא עדיין לא מניבה רווח.</p>
<div class="callout"><span class="callout-label">ברירת המחדל: נקודת איזון, לא הפסד.</span> גם בתוך תקופת הסובלנות, היעד השוטף הוא לפעול בנקודת האיזון — לא לייצר רווח מלאכותי ולא לייצר הפסד במתכוון. הסובלנות מקנה גמישות סביב ציפיית הרווחיות; היא אינה אישור להפסיד כסף.</div>
<div class="callout warn"><span class="callout-label">גירעון זמני — רק אם תבחרו זאת במפורש, ותמיד עם תקרה.</span> לקוחות מסוימים מעדיפים להטות את מלוא התקציב לבנייה והרחבה בתקופה הראשונה, גם אם זה אומר גירעון תפעולי זמני ולא רק היעדר רווח. זו העדפה עסקית לגיטימית — אך שונה מברירת המחדל, ותצוין במפורש עם מסגרת ותקרה מוסכמות מראש. התקרה שתיקבע היא רף ה-Stop-Loss התפעולי לאותה תקופה — לא מנגנון נוסף עליו.</div>
<div class="prompt"><div class="prompt-label">ספרו לנו</div>
<div class="prompt-q">כמה זמן אתם מוכנים לתת למודל להתפתח (תקופת סובלנות)?<br>אתם מעדיפים שנתמקד בהגעה מהירה לרווחיות, או בבנייה והרחבה תוך הישארות בנקודת האיזון (רמת סובלנות: שמרנית / מאוזנת / אגרסיבית / הרחבה מרבית)?<br>אם רלוונטי — האם אתם מוכנים לגירעון זמני בפועל, ובאיזו תקרה?</div></div>
</div>
<div class="page">
{pagehead("01 · רמת ותקופת הסובלנות שלכם")}
<p class="fine">חשוב שתדעו: זה לא אומר שאתם מוותרים על זכות כלשהי. בכל עת, גם בתוך תקופת הסובלנות, תוכלו לעצור פעילות, לבחון תוצאות ולסיים את ההתקשרות בהתאם לתנאי ההסכם וההצעה — שום דבר כאן אינו משהה, מגביל או דוחה את הזכויות האלה. וכמו תמיד — גם בתום התקופה, אין בכך הבטחה לתוצאה או לרווחיות. רמת ותקופת הסובלנות, וכן גירעון זמני מוסכם אם הוסכם, יירשמו בטבלת התנאים המסחריים (נספח B); אף אחד מהם אינו יוצר מנגנון משפטי חדש מעבר לקבוע שם.</p>
{pagefoot()}
</div>''')

# ---- Financial boundaries (own page) ----
PAGES.append(f'''<div class="page">
{pagehead("01 · גבולות פיננסיים")}
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

# ---- Break-even ----
PAGES.append(f'''<div class="page">
{pagehead("01 · נקודת האיזון (Break-Even)")}
<div class="eyebrow">כלי תכנון, לא הבטחה</div>
<h1 class="sec">נקודת האיזון (Break-Even)</h1>
<div class="secrule"></div>
<p class="body-copy">נקודת האיזון היא נקודת ייחוס תכנונית: כל עוד עלות הרכישה בפועל אינה עולה על שווי העסקה הממוצע כפול שיעור הרווח הגולמי שלכם — הפעילות נחשבת בנקודת האיזון או מעליה. זהו כלי תכנון, <strong>לא הבטחה לרווחיות ולא תחזית מובטחת</strong>.</p>
<p class="body-copy">שיעור הרווח הגולמי הוא נתון שרק אתם יודעים — אין לו ברירת מחדל גנרית. אם לא תמסרו אותו, מנגנון נקודת האיזון כולו פשוט לא יופעל. שווי העסקה הממוצע (AOV) כן מקבל ברירת מחדל אם אינו ידוע לכם: השווי שייקבע במחקר Genesis שלכם.</p>
<div class="prompt"><div class="prompt-label">ספרו לנו, אם ידוע לכם</div>
<div class="prompt-q">מהו שיעור הרווח הגולמי שלכם?<br>מהו שווי העסקה הממוצע שלכם, או שנסתמך על מחקר Genesis?</div></div>
<p class="fine">נקודת האיזון היא רצפה, לא תקרה — אפשר וכדאי להגדיר גם יעדי רווחיות נוספים מעליה. ככל שנקודת האיזון וההגדרות הפיננסיות רשומות בהסכם ובטבלת התנאים המסחריים — הן אלה שיחייבו, לא ההסברים הכלליים כאן.</p>
{pagefoot()}
</div>''')

# ---- Process diagram ----
PAGES.append(f'''<div class="page">
{pagehead("01 · מהמדריך להצעה")}
<div class="eyebrow">התהליך</div>
<h1 class="sec">מהמדריך להצעה</h1>
<div class="secrule"></div>
<div class="process">
  <div class="pstep"><div class="pnum">1</div><div class="ptxt">אתם מספרים לנו את המסגרת שלכם — תקציב, מטרות, טווח זמן, סובלנות וגבולות — בטופס הקליטה שבסוף מדריך זה; הנתונים מועתקים ומאושרים בטבלת התנאים המסחריים שבנספח B להסכם.</div></div>
  <div class="pstep"><div class="pnum">2</div><div class="ptxt">עם חתימת הסכם ההתקשרות ותשלום הרלוונטי למסלולכם (דמי ההשתתפות העצמית במסלולים A/B/C, או מחיר המחקר המלא במסלול 0), אנחנו עורכים את מחקר Genesis ובוחנים מה ניתן לבנות באחריות בתוך המסגרת שהגדרתם.</div></div>
  <div class="pstep"><div class="pnum">3</div><div class="ptxt">אנחנו מציגים לכם תוכנית עסקית, שיווקית ופיננסית, לצד הצעת התקשרות מסחרית — היקף, מבנה תמחור, לוח זמנים ומסגרת עבודה.</div></div>
  <div class="pstep"><div class="pnum">4</div><div class="ptxt">אתם מחליטים — לאשר, לדחות או לדון בהצעה המוצעת.</div></div>
  <div class="pstep"><div class="pnum">5</div><div class="ptxt">ה"הצעה" שתאושר ותיחתם מפעילה את ההתקשרות הספציפית הרלוונטית, לפי מסגרת ההסכם.</div></div>
</div>
<div class="callout"><span class="callout-label">לקוחות קיימים:</span> אם כבר חתמתם עם הארגון על הסכם ההתקשרות, והפרק הזה רלוונטי עבורכם לגבי התקשרות נוספת — פרויקט, מותג או יחידה עסקית נפרדים, או מסלול שטרם הופעל — התהליך שלעיל חוזר על עצמו ביחס לאותה התקשרות ספציפית החדשה בלבד, ואינו מצריך חתימה מחודשת על הסכם ההתקשרות עצמו; טבלת נספח B תעודכן ביחס אליה בלבד, מבלי לשנות תנאים שנקבעו בהצעה חתומה אחרת שנותרה בתוקף.</div>
{pagefoot()}
</div>''')

# ---- Intake divider ----
PAGES.append('''<div class="page dark divider">
  <div class="divider-ghost">02</div>
  <div class="divider-inner">
    <div class="divider-eyebrow"><span class="dash"></span>פרק 02</div>
    <div class="divider-title">טופס קליטה</div>
    <div class="divider-sub">המידע כאן משמש לתכנון בלבד ואינו קובע בעצמו היקף, מחיר או תנאים מחייבים. תמציתי במכוון — כל שדה משמש ישירות את שלב המחקר והתכנון.</div>
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
    ("מסגרת ההשקעה שלכם", None, [
        "תקציב חודשי מועדף", "היקף השקעה כולל, אם ידוע", "טווח הגמישות (תקציב קבוע / מרחב תמרון)",
    ]),
    ("הנתיב המועדף", "ראו \"שני נתיבים אפשריים\" — שתי התשובות תקפות באותה מידה", [
        "אתם מגדירים את מסגרת ההשקעה, או מבקשים שנציע מודל מסחרי?",
    ]),
    ("סובלנות ורווחיות", "מסלול 0: השאירו ריק ועברו הלאה", [
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

# split the 9 groups across two content pages (5 + 4) to keep header/footer
# repeating naturally instead of one very long flowing section
def intake_page(eyebrow, groups, intro=None):
    html = [f'<div class="page">{pagehead(eyebrow)}']
    if intro:
        html.append(f'<div class="eyebrow">טופס קליטה</div><h1 class="sec">טופס קליטה</h1><div class="secrule"></div><p class="intake-intro">{intro}</p>')
    for idx, title, note, items in groups:
        grp = [f'<div class="igroup"><div class="igroup-head"><span class="igroup-num">{idx:02d}</span><span class="igroup-title">{title}</span></div>']
        if note:
            grp.append(f'<div class="igroup-note">{note}</div>')
        grp.append('<div class="ifields">')
        for it in items:
            grp.append(field(it))
        grp.append('</div></div>')
        html.append("".join(grp))
    html.append(pagefoot() + '</div>')
    return "".join(html)

numbered = [(i, t, n, it) for i, (t, n, it) in enumerate(INTAKE_GROUPS, start=1)]
PAGES.append(intake_page("02 · טופס קליטה", numbered[:5],
    intro='מטרת הטופס: לאסוף את המידע הדרוש לצוות המחקר והתכנון כדי לבנות עבורכם תוכנית עסקית, שיווקית ופיננסית מותאמת, ולתרגם אותה בהמשך להצעת התקשרות מסחרית ספציפית. הטופס תמציתי במכוון — כל שדה כאן משמש ישירות את שלב המחקר והתכנון; פרטים נוספים ומדויקים יותר ייאספו בשיחה ישירה איתכם, ואינם "נועלים" אתכם בשום מחויבות עד לחתימה על הצעה ספציפית.'))
PAGES.append(intake_page("02 · טופס קליטה (המשך)", numbered[5:]))

# ---- Closing ----
PAGES.append(f'''<div class="page dark closing">
  <div class="closing-ghost">LG</div>
  <div class="closing-inner">
    <div class="closing-eyebrow"><span class="dash"></span>לסיום</div>
    <div class="closing-title">כל המידע במדריך זה משמש לתכנון ולהערכה בלבד</div>
    <p>חתימה על הסכם ההתקשרות עצמו כן כרוכה בתשלום הרלוונטי למסלולכם. ההתחייבות המסחרית המלאה להיקף, למחיר ולתנאי ההתקשרות הספציפית נוצרת רק ב"הצעה" חתומה בנפרד.<br><br>אנחנו מוכנים כשאתם מוכנים.</p>
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
<link href="https://fonts.googleapis.com/css2?family=Heebo:wght@300;400;500;700&family=Frank+Ruhl+Libre:wght@500;600;700&display=swap" rel="stylesheet">
<style>{CSS}</style></head>
<body><div class="sheet">
{body}
</div></body></html>"""

io.open("CLIENT_GUIDE_HE.html", "w", encoding="utf-8").write(doc)
print("wrote CLIENT_GUIDE_HE.html", len(doc), "bytes")

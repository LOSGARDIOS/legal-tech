# -*- coding: utf-8 -*-
"""Render CLIENT_GUIDE_HE.md as a premium, editorial-feeling A4 RTL PDF.

Unlike the MSA (a sequential legal document rendered by a markdown parser),
the Client Guide needs genuinely different page archetypes — a cover, a
philosophy statement, concept cards, a numbered process diagram, and a
redesigned progressive-disclosure intake — so this script hand-composes
each section rather than parsing the .md generically. The underlying
Hebrew CONTENT is copied verbatim from CLIENT_GUIDE_HE.md (source of truth);
only its visual presentation and grouping/ordering for the intake section
are redesigned here.
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
  --ink:#1C1815; --muted:#6b6259; --rule:#e4dcd0;
  --accent:#5B2986; --accent-soft:#F4F0F6;
  --paper:#FFFFFF; --offwhite:#FBF8F3;
  --brown:#6B5A46; --taupe:#A8927A; --champagne:#EFE6D6; --stone:#F6F1E7;
  --band:#1C1815;
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:#e9e5dd;color:var(--ink);direction:rtl;
 font-family:"Heebo","Frank Ruhl Libre",Georgia,serif;font-size:10.6pt;line-height:1.85}
.sheet{max-width:820px;margin:0 auto;background:var(--paper)}
.page{position:relative;padding:26mm 20mm 32mm;min-height:257mm;background:var(--paper)}
.page + .page{break-before:page;page-break-before:always}

/* running header/footer inside each content page (not cover/dividers) */
.pagehead{display:flex;justify-content:space-between;align-items:center;
 font-family:"Heebo",sans-serif;font-size:7.6pt;letter-spacing:.18em;color:var(--taupe);
 border-bottom:1px solid var(--rule);padding-bottom:10px;margin-bottom:30px}
.pagehead .mark{display:flex;align-items:center;gap:8px}
.pagehead img{height:14px;opacity:.7}

/* ---------- COVER ---------- */
.cover{background:var(--ink);color:#fff;min-height:297mm;padding:0;
 display:flex;flex-direction:column;align-items:center;justify-content:center;
 text-align:center;position:relative}
.cover-mark{width:64px;height:auto;margin-bottom:38px;filter:brightness(0) invert(1);opacity:.92}
.cover-title{font-family:"Frank Ruhl Libre",serif;font-weight:600;font-size:30pt;
 letter-spacing:.02em;margin:0 0 10px}
.cover-brand{font-family:"Heebo",sans-serif;font-weight:700;font-size:12pt;
 letter-spacing:.5em;margin:0 0 26px;color:var(--taupe)}
.cover-sub{font-family:"Heebo",sans-serif;font-weight:300;font-size:10.5pt;
 letter-spacing:.08em;color:#cfc6b8;max-width:320px;line-height:1.9}
.cover-rule{width:52px;height:1px;background:var(--taupe);margin:30px 0}
.cover-foot{position:absolute;bottom:26mm;font-family:"Heebo",sans-serif;font-size:7.6pt;
 letter-spacing:.16em;color:#8a8072}

/* ---------- SECTION DIVIDER ---------- */
.divider{min-height:297mm;padding:26mm 20mm;background:var(--stone);
 display:flex;flex-direction:column;justify-content:center;position:relative}
.divider-num{font-family:"Frank Ruhl Libre",serif;font-size:64pt;color:var(--champagne);
 line-height:1;margin-bottom:14px}
.divider-eyebrow{font-family:"Heebo",sans-serif;font-size:8.4pt;letter-spacing:.3em;
 color:var(--accent);margin-bottom:14px}
.divider-title{font-family:"Frank Ruhl Libre",serif;font-size:23pt;font-weight:600;
 max-width:480px;line-height:1.4;margin:0 0 16px}
.divider-sub{font-family:"Heebo",sans-serif;font-size:9.6pt;color:var(--muted);
 max-width:420px;line-height:1.9}

/* ---------- PHILOSOPHY / STATEMENT PAGES ---------- */
.statement{min-height:257mm;padding:26mm 22mm;display:flex;flex-direction:column;
 justify-content:center}
.statement .lead{font-family:"Frank Ruhl Libre",serif;font-size:17pt;line-height:1.7;
 font-weight:500;max-width:560px;margin:0 0 22px}
.statement p{font-family:"Heebo",sans-serif;font-size:10.6pt;line-height:1.95;
 color:#2c2620;max-width:520px;margin:0 0 16px}
.statement strong{color:var(--ink);font-weight:700}
.pull{font-family:"Frank Ruhl Libre",serif;font-size:14.5pt;font-style:italic;
 color:var(--accent);border-right:2px solid var(--accent);padding-right:16px;
 margin:22px 0;max-width:480px;line-height:1.6}

/* ---------- CONCEPT CARDS ---------- */
.cardgrid{display:flex;flex-direction:column;gap:16px;margin-top:18px}
.card{background:var(--offwhite);border:1px solid var(--rule);border-radius:3px;
 padding:20px 22px;position:relative}
.card::before{content:"";position:absolute;top:0;right:0;bottom:0;width:3px;
 background:var(--accent);border-radius:3px 0 0 3px}
.card-label{font-family:"Heebo",sans-serif;font-size:7.8pt;letter-spacing:.22em;
 color:var(--accent);margin-bottom:8px;font-weight:700}
.card-title{font-family:"Frank Ruhl Libre",serif;font-size:13pt;font-weight:600;margin:0 0 8px}
.card p{font-family:"Heebo",sans-serif;font-size:9.8pt;color:#3a332b;line-height:1.8;margin:0}

/* glass-effect note (simulated for print: layered soft gradient, not live blur) */
.glassnote{background:linear-gradient(155deg,rgba(255,255,255,.92),rgba(239,230,214,.55));
 border:1px solid rgba(168,146,122,.35);border-radius:6px;padding:16px 20px;margin:18px 0;
 box-shadow:0 1px 2px rgba(28,24,21,.05);font-family:"Heebo",sans-serif;font-size:9.4pt;
 color:#4a4239;line-height:1.85}
.glassnote b{color:var(--ink)}

/* ---------- EXPLANATORY / INPUT PAGES ---------- */
h1.sec{font-family:"Frank Ruhl Libre",serif;font-size:19pt;font-weight:600;
 margin:0 0 6px;padding-bottom:14px;border-bottom:2px solid var(--accent)}
h2.sub{font-family:"Frank Ruhl Libre",serif;font-size:13.5pt;font-weight:600;
 color:var(--ink);margin:28px 0 10px}
.body-copy{font-family:"Heebo",sans-serif;font-size:9.9pt;line-height:1.95;
 color:#2c2620;margin:0 0 14px}
.prompt{background:var(--accent-soft);border-radius:4px;padding:14px 18px;margin:14px 0}
.prompt-label{font-family:"Heebo",sans-serif;font-size:7.8pt;letter-spacing:.2em;
 color:var(--accent);font-weight:700;margin-bottom:6px}
.prompt-q{font-family:"Heebo",sans-serif;font-size:9.8pt;color:#2c2620;line-height:1.85}
.fine{font-family:"Heebo",sans-serif;font-size:8.6pt;color:var(--muted);
 line-height:1.8;border-right:2px solid var(--rule);padding-right:12px;margin:12px 0}

/* ---------- PROCESS DIAGRAM ---------- */
.process{margin:26px 0}
.pstep{display:flex;gap:16px;align-items:flex-start;padding:14px 0;
 border-bottom:1px solid var(--rule)}
.pstep:last-child{border-bottom:none}
.pnum{flex:none;width:30px;height:30px;border-radius:50%;background:var(--ink);color:#fff;
 font-family:"Heebo",sans-serif;font-weight:700;font-size:11pt;
 display:flex;align-items:center;justify-content:center}
.ptxt{font-family:"Heebo",sans-serif;font-size:9.7pt;color:#2c2620;line-height:1.85;padding-top:4px}

/* ---------- INTAKE FORM ---------- */
.intake-intro{font-family:"Heebo",sans-serif;font-size:9.8pt;color:var(--muted);
 line-height:1.9;max-width:520px;margin-bottom:8px}
.igroup{margin:22px 0;break-inside:avoid-page;page-break-inside:avoid}
.card,.prompt,.glassnote{break-inside:avoid-page;page-break-inside:avoid}
.igroup-head{display:flex;align-items:center;gap:12px;margin-bottom:10px}
.igroup-num{font-family:"Frank Ruhl Libre",serif;font-size:16pt;color:var(--champagne);
 background:var(--ink);color:#fff;width:28px;height:28px;border-radius:50%;
 display:flex;align-items:center;justify-content:center;font-family:"Heebo",sans-serif;
 font-weight:700;font-size:10pt;flex:none}
.igroup-title{font-family:"Frank Ruhl Libre",serif;font-size:12.5pt;font-weight:600}
.igroup-note{font-family:"Heebo",sans-serif;font-size:8.4pt;color:var(--accent);
 margin-bottom:8px;margin-right:40px}
.ifields{margin-right:40px;font-family:"Heebo",sans-serif;font-size:9.5pt;
 color:#2c2620;line-height:2.3}
.ifields .f{display:flex;align-items:baseline;gap:8px;border-bottom:1px dotted var(--rule);
 padding:5px 0}
.ifields .f .flabel{flex:none;color:#3a332b}
.ifields .f .fline{flex:1;border-bottom:1px solid var(--rule);min-height:14px}

/* ---------- CLOSING ---------- */
.closing{min-height:257mm;padding:26mm 22mm;display:flex;flex-direction:column;
 justify-content:center;text-align:center;align-items:center}
.closing .mark{width:34px;margin-bottom:26px;opacity:.85}
.closing .lead{font-family:"Frank Ruhl Libre",serif;font-size:16pt;line-height:1.75;
 max-width:440px;margin:0 0 20px}
.closing .sub{font-family:"Heebo",sans-serif;font-size:9.6pt;color:var(--muted);
 max-width:400px;line-height:1.9}

@page{size:A4;margin:0}
@media print{
 body{background:#fff}
 .sheet{max-width:none}
 .card,.prompt,.glassnote,table{break-inside:avoid}
 h1.sec,h2.sub,.igroup-head{break-after:avoid}
}
"""

def pagehead(eyebrow):
    return f'''<div class="pagehead"><span class="mark"><img src="{LOGO_MARK}">LOS GARDIOS · מדריך הלקוח</span><span>{eyebrow}</span></div>'''

PAGES = []

# ---- Cover ----
PAGES.append(f'''<div class="page cover">
  <img src="{LOGO_MARK}" class="cover-mark">
  <div class="cover-brand">LOS GARDIOS</div>
  <div class="cover-title">מדריך הלקוח</div>
  <div class="cover-rule"></div>
  <div class="cover-sub">תקציב · מסגרת השקעה · טווח זמן<br>קריאה לפני תחילת הדרך המשותפת</div>
  <div class="cover-foot">סודי · CONFIDENTIAL · גרסת מדריך 1</div>
</div>''')

# ---- Opening philosophy statement ----
PAGES.append(f'''<div class="page statement">
{pagehead("למה אנחנו שואלים על כך")}
<div class="lead">אנחנו לא מתחילים מ"הנה החבילה שלנו והמחיר שלה."</div>
<p>אנחנו מתחילים מ: ספרו לנו מה אתם מנסים להשיג, כמה אתם באמת מוכנים ויכולים להשקיע, אילו אילוצים קיימים, ומה אתם מאמינים שאפשר. אנחנו נקבע מה ניתן לבנות באחריות בתוך המסגרת הזו.</p>
<p>לפני שאנחנו בונים תוכנית עסקית, שיווקית ופיננסית עבורכם, אנחנו צריכים להבין את המציאות הכלכלית שבתוכה אתם רוצים ויכולים לפעול. המידע הזה לא נועד לקבוע כמה אפשר לגבות מכם — הוא נועד לקבוע מה אפשר לבנות באחריות, בהיקף, בקצב ובמודל שמתאימים לעסק שלכם.</p>
<div class="pull">תקציב גדול יותר עשוי לאפשר היקף רחב יותר — אבל לא תוצאה טובה יותר מאליה. הקשר בין תקציב להיקף העבודה הוא שאלה של תכנון, לא הבטחה.</div>
<p><strong>רמת תשומת הלב, המקצועיות וההשקעה שלנו בפרויקט שלכם אינה תלויה בגודל התקציב — היא זהה, בכל היקף עבודה.</strong> עסק עם פוטנציאל יוצא דופן, נזילות מוגבלת כרגע, הזדמנות שוק ייחודית או חזון מייסד חזק עשוי להצדיק מבנה מסחרי מותאם באותה מידה שעסק עם תקציב גדול יכול שלא להתאים לנו כלל. אנחנו בוחנים פוטנציאל, מציאות, משאבים, מחויבות והתאמה אסטרטגית — לא רק את גובה התקציב.</p>
</div>''')

PAGES.append(f'''<div class="page statement">
{pagehead("הכלל המנחה")}
<div class="lead">אתם מגדירים את המסגרת. אנחנו בוחנים מה אפשר לבנות בתוכה.</div>
<p>הכלל המנחה שלנו פשוט: אתם מגדירים את המסגרת הכלכלית שבה אתם רוצים לפעול, אנחנו בוחנים מה ניתן לבנות באחריות בתוכה, ורק אז אנחנו מציעים תוכנית ומודל מסחרי קונקרטיים. המטרה שלנו היא התקשרות שאתם יכולים לקיים לאורך זמן — לא התקשרות שדוחקת אתכם מעבר ליכולת שלכם.</p>
<p>מטרתנו איננה למקסם הוצאה. היא לשמר את יכולתו של העסק להמשיך להשקיע, לפעול ולצמוח. עסק שמיצה את תזרים המזומנים שלו אינו יכול להמשיך לבנות, לבחון, להרחיב, להשקיע או לשלם עבור משאבים מקצועיים — ולכן המטרה היא לבנות התקשרות שבת-קיימא כלכלית לשני הצדדים.</p>
<p>לפעמים, אחרי שנבחן את המסגרת שהגדרתם, נגיע למסקנה שהיא אינה תואמת את היקף הפרויקט המבוקש. במקרה כזה ננהל איתכם שיחה בתום-לב לפני כל החלטה על המשך התהליך — לא נבנה עבורכם הצעה שאיננו מאמינים שהיא בת-קיימא.</p>
<div class="glassnote"><b>בקשה הדדית:</b> איכות האסטרטגיה תלויה באיכות המידע שעומד לרשותנו לבנייתה. אנחנו מבקשים מכם להיות גלויים לגבינו לגבי אילוצים, בדיוק כפי שאנחנו גלויים לגביכם לגבי מה שאנחנו מאמינים שריאלי. תנו לנו את המספר האמיתי — לא את המספר שאתם חושבים שאנחנו רוצים לשמוע. תקציב נמוך כרגע יכול להתקיים לצד הזדמנות גדולה מאוד לטווח ארוך; תקציב גדול, מצדו, אינו הופך עסק אוטומטית להזדמנות אסטרטגית.</div>
</div>''')

# ---- Track 0 callout as its own card page ----
PAGES.append(f'''<div class="page statement">
{pagehead("הערה למסלול מסוים")}
<h2 class="sub" style="margin-top:0">הערה ללקוחות מסלול 0</h2>
<div class="card"><div class="card-label">רלוונטי רק למסלול זה</div>
<p>אם בחרתם ברכישת מחקר Genesis חד-פעמית בלבד, ללא תקציב שוטף ("מסלול 0", נספח A סעיף 2 להסכם) — רוב הפרקים הבאים בעמודים הקרובים (מסגרת השקעה, סובלנות, Stop-Loss, נקודת האיזון — נספח B סעיפים 1–3) אינם חלים עליכם, ואינכם נדרשים למלא את השדות הנוגעים אליהם. גם דמי ההשתתפות העצמית המוזכרים בהמשך שייכים למסלולים A/B/C בלבד — תנאי התשלום במסלול 0 מפורטים בנספח A סעיף 2. אפשר לדלג ישירות לתהליך שבסוף המדריך.</p></div>
<h2 class="sub">לפני שממשיכים — חשוב שתדעו</h2>
<p class="body-copy">המידע שתמסרו בפרק הזה משמש אותנו לתכנון, להערכה ולבניית ה"הצעה" — ואינו מהווה כשלעצמו התחייבות לרכישת שירותים, לתשלום סכום מסוים, לקבלת הצעה מסחרית מסוימת, או להשגת תוצאה עסקית כלשהי. שום מספר, טווח או ציפייה שתרשמו כאן אינם סופיים ואינם "נועלים" אתכם — תמיד אפשר לעדכן, לדייק או לשנות כיוון בהמשך השיחה. אם חלק מהמספרים עדיין לא ברורים לכם — זה בסדר גמור; נוכל להעריך אותם יחד. התנאים המסחריים המחייבים של כל "התקשרות ספציפית" נקבעים אך ורק ב"הצעה" חתומה כהגדרתה בהסכם ההתקשרות, שתקבלו בהמשך.</p>
</div>''')

# ---- Two paths concept page ----
PAGES.append(f'''<div class="page statement">
{pagehead("שני נתיבים אפשריים")}
<h1 class="sec">שני נתיבים אפשריים</h1>
<p class="body-copy">יש שתי דרכים לגיטימיות להתחיל את השיחה המסחרית, ואתם בוחרים — שתיהן תקפות באותה מידה:</p>
<div class="cardgrid">
  <div class="card"><div class="card-label">נתיב א׳</div>
    <div class="card-title">אתם מגדירים את מסגרת ההשקעה</div>
    <p>למשל: "אנחנו רוצים להשקיע כ-X בחודש למשך כ-Y חודשים" — ואנחנו בונים את התוכנית בתוכה.</p></div>
  <div class="card"><div class="card-label">נתיב ב׳</div>
    <div class="card-title">אתם מבקשים שנציע מודל מסחרי</div>
    <p>אנחנו מציגים מבנה תמחור, ריטיינר או מודל אחר שלדעתנו המקצועית מתאים לפרויקט, ואתם שוקלים אותו. אפשר להשיב על השאלות הבאות בטווחים כלליים, לציין אילוצים בלבד, או להשאיר אותן לשיקול דעתנו המקצועי בהצעה הראשונית — אין צורך לנחש מספר.</p></div>
</div>
<h2 class="sub">גמישות מסחרית — לא הנחה</h2>
<p class="body-copy">כשההזדמנות, ההתאמה האסטרטגית והערך הצפוי לטווח ארוך מצדיקים זאת, הארגון עשוי לבנות את השתתפותו בהתקשרות באופן שונה — למשל מבנה מבוסס-אחוזים, מבנה משולב, היקף התחלתי מצומצם, או שלביות בהתקשרות. אלה מבני התקשרות שהמסמכים המשפטיים תומכים בהם, לא הנחות ולא צעד של רצון טוב — זו ארכיטקטורה מסחרית, שנועדה להתאים את ההתקשרות למציאות של העסק.</p>
</div>''')

# ---- Reflection page: goals ----
PAGES.append(f'''<div class="page statement">
{pagehead("היעד והציפיות שלכם")}
<h1 class="sec">היעד והציפיות שלכם</h1>
<p class="body-copy">לפני המספרים, נשמח להבין מה אתם מנסים להשיג.</p>
<div class="prompt"><div class="prompt-label">שאלות למחשבה</div>
<div class="prompt-q">מהי התוצאה העסקית שאתם שואפים אליה?<br>איך תגדירו התקדמות עבור הפרויקט?<br>מהם הדברים החשובים לכם ביותר בו?</div></div>
<p class="fine">התשובות כאן מכוונות אותנו בעדיפויות ובטון של התוכנית שנבנה — הן אינן יעד מדיד או הבטחה להשגת תוצאה; היעדים המדידים בפועל, ככל שייקבעו, ייקבעו בהסכם ובטבלת התנאים המסחריים בלבד.</p>
</div>''')

# ---- Investment framework ----
PAGES.append(f'''<div class="page statement">
{pagehead("מסגרת ההשקעה שלכם")}
<h1 class="sec">מסגרת ההשקעה שלכם</h1>
<p class="body-copy">השדה החשוב ביותר עבורנו כדי להתחיל לתכנן הוא <strong>התקציב החודשי</strong>; שאר השאלות כאן עוזרות לנו לדייק את התוכנית, וניתן לחדד אותן יחד איתנו בהמשך.</p>
<div class="prompt"><div class="prompt-label">ספרו לנו</div>
<div class="prompt-q">מהו התקציב החודשי המועדף עליכם?<br>האם יש היקף השקעה כולל שאתם מתכננים אליו?<br>מהו טווח הגמישות שלכם — תקציב קבוע, או מרחב תמרון בכפוף לאישורכם?<br>התקציב שאתם מוסרים כולל או לא כולל עלויות חיצוניות מסוימות (כגון תקציבי מדיה המועברים ישירות לפלטפורמות)?</div></div>
<p class="body-copy">המספר שתמסרו הוא נקודת פתיחה לתכנון בלבד — לא הצעת מחיר ולא רצפה מחייבת. התוכנית שנציג לכם עשויה להיות שונה ממנו, בכל כיוון.</p>
<p class="fine">שימו לב: במסלולים מבוססי-תקציב (A/B/C), לאחר שהתקציב ייקבע בהצעה החתומה, ההתחייבות התפעולית היא לתקציב חודשי קבוע לשלושה חודשים לפחות; הפחתתו לאחר מכן טעונה הודעה מוקדמת בכתב של 30 יום. זהו תנאי מההסכם עצמו (נספח B), לא תנאי מהפרק הזה — אך כדאי שתכירו אותו כבר עכשיו.</p>
</div>''')

# ---- Timeline ----
PAGES.append(f'''<div class="page statement">
{pagehead("טווח הזמן שלכם")}
<h1 class="sec">טווח הזמן שלכם</h1>
<p class="body-copy">פרויקט עסקי רציני כולל בדרך כלל שלבי מחקר, בדיקה, פיתוח, כניסה לשוק, איסוף נתונים ואופטימיזציה — לפני שאפשר למדוד את האפקט המסחרי שלו בבירור.</p>
<div class="prompt"><div class="prompt-label">ספרו לנו</div>
<div class="prompt-q">מהי התקופה שאתם מתכננים לפעול בה?<br>האם יש מועדים עסקיים משמעותיים שכדאי שנכיר?</div></div>
<p class="fine">זהו שיח תכנוני כללי בלבד. המספר המדויק שישמש בפועל למדידת ביצועים הוא <strong>תקופת הסובלנות</strong> שתקבעו בעמוד הבא, ותירשם בטבלת התנאים המסחריים.</p>
</div>''')

# ---- Tolerance ----
PAGES.append(f'''<div class="page statement">
{pagehead("רמת ותקופת הסובלנות שלכם")}
<h1 class="sec">רמת ותקופת הסובלנות שלכם</h1>
<p class="body-copy">תקופת הסובלנות היא הזמן שבו אתם מאפשרים לנו גמישות לפעול בתוך מסגרת התקציב שהגדרתם, מבלי לדרוש שההתקשרות תהיה רווחית כבר מהיום הראשון. לדוגמה: תקציב של 20,000 ₪ לחודש ותקופת סובלנות של חמישה חודשים אומרים שבמהלך התקופה הזו, אנחנו רשאים להשתמש בתקציב הזמין כדי לבנות, לבחון ולהרחיב את הפעילות — גם אם היא עדיין לא מניבה רווח.</p>
<div class="glassnote"><b>ברירת המחדל: נקודת איזון, לא הפסד.</b> גם בתוך תקופת הסובלנות, היעד השוטף הוא לפעול בנקודת האיזון — לא לייצר רווח מלאכותי ולא לייצר הפסד במתכוון. הסובלנות מקנה גמישות סביב ציפיית הרווחיות; היא אינה אישור להפסיד כסף.</div>
<div class="glassnote"><b>גירעון זמני — רק אם תבחרו זאת במפורש, ותמיד עם תקרה.</b> לקוחות מסוימים מעדיפים להטות את מלוא התקציב לבנייה והרחבה בתקופה הראשונה, גם אם זה אומר גירעון תפעולי זמני ולא רק היעדר רווח. זו העדפה עסקית לגיטימית — אך שונה מברירת המחדל, ותצוין במפורש עם מסגרת ותקרה מוסכמות מראש. התקרה שתיקבע היא רף ה-Stop-Loss התפעולי לאותה תקופה — לא מנגנון נוסף עליו.</div>
<div class="prompt"><div class="prompt-label">ספרו לנו</div>
<div class="prompt-q">כמה זמן אתם מוכנים לתת למודל להתפתח (תקופת סובלנות)?<br>אתם מעדיפים שנתמקד בהגעה מהירה לרווחיות, או בבנייה והרחבה תוך הישארות בנקודת האיזון (רמת סובלנות: שמרנית / מאוזנת / אגרסיבית / הרחבה מרבית)?<br>אם רלוונטי — האם אתם מוכנים לגירעון זמני בפועל, ובאיזו תקרה?</div></div>
<p class="fine">חשוב שתדעו: זה לא אומר שאתם מוותרים על זכות כלשהי. בכל עת, גם בתוך תקופת הסובלנות, תוכלו לעצור פעילות, לבחון תוצאות ולסיים את ההתקשרות בהתאם לתנאי ההסכם וההצעה — שום דבר כאן אינו משהה, מגביל או דוחה את הזכויות האלה. וכמו תמיד — גם בתום התקופה, אין בכך הבטחה לתוצאה או לרווחיות. רמת ותקופת הסובלנות, וכן גירעון זמני מוסכם אם הוסכם, יירשמו בטבלת התנאים המסחריים (נספח B); אף אחד מהם אינו יוצר מנגנון משפטי חדש מעבר לקבוע שם.</p>
</div>''')

# ---- Financial boundaries + break-even ----
PAGES.append(f'''<div class="page statement">
{pagehead("גבולות פיננסיים")}
<h1 class="sec">גבולות פיננסיים</h1>
<p class="body-copy">זהו שדה אופציונלי, שתפקידו להגן עליכם.</p>
<div class="prompt"><div class="prompt-label">ספרו לנו</div>
<div class="prompt-q">מהו הסכום שאתם לא רוצים לחרוג ממנו?<br>האם יש שינויים בתקציב שדורשים אישור מפורש שלכם מראש, גם אם לדעתנו המקצועית הם משרתים את הפרויקט?</div></div>
<p class="fine">לא חובה לנקוב בתקרה — גם השארת השדה פתוח היא תשובה לגיטימית. הגבולות שתגדירו כאן ישמשו לקביעת רף ה-Stop-Loss ותקופת המדידה שלו, ויחייבו את הארגון לעצור או לצמצם פעילות בהתאם. אם לא ייקבע רף מפורש, יחול רף ברירת מחדל (הפסד בגובה התקציב החודשי, על פני 30 יום); ואם לא ייקבע שיעור חריגה מותר, יחול שיעור ברירת מחדל של 10% לחודש.</p>
</div>''')

PAGES.append(f'''<div class="page statement">
{pagehead("נקודת האיזון (Break-Even)")}
<h1 class="sec">נקודת האיזון (Break-Even)</h1>
<p class="body-copy">נקודת האיזון היא נקודת ייחוס תכנונית: כל עוד עלות הרכישה בפועל אינה עולה על שווי העסקה הממוצע כפול שיעור הרווח הגולמי שלכם — הפעילות נחשבת בנקודת האיזון או מעליה. זהו כלי תכנון, <strong>לא הבטחה לרווחיות ולא תחזית מובטחת</strong>.</p>
<p class="body-copy">שיעור הרווח הגולמי הוא נתון שרק אתם יודעים — אין לו ברירת מחדל גנרית. אם לא תמסרו אותו, מנגנון נקודת האיזון כולו פשוט לא יופעל. שווי העסקה הממוצע (AOV) כן מקבל ברירת מחדל אם אינו ידוע לכם: השווי שייקבע במחקר Genesis שלכם.</p>
<div class="prompt"><div class="prompt-label">ספרו לנו, אם ידוע לכם</div>
<div class="prompt-q">מהו שיעור הרווח הגולמי שלכם?<br>מהו שווי העסקה הממוצע שלכם, או שנסתמך על מחקר Genesis?</div></div>
<p class="fine">נקודת האיזון היא רצפה, לא תקרה — אפשר וכדאי להגדיר גם יעדי רווחיות נוספים מעליה. ככל שנקודת האיזון וההגדרות הפיננסיות רשומות בהסכם ובטבלת התנאים המסחריים — הן אלה שיחייבו, לא ההסברים הכלליים כאן.</p>
</div>''')

# ---- Process diagram ----
PAGES.append(f'''<div class="page statement">
{pagehead("מהמדריך להצעה")}
<h1 class="sec">מהמדריך להצעה</h1>
<div class="process">
  <div class="pstep"><div class="pnum">1</div><div class="ptxt">אתם מספרים לנו את המסגרת שלכם — תקציב, מטרות, טווח זמן, סובלנות וגבולות — בטופס הקליטה שבסוף מדריך זה; הנתונים מועתקים ומאושרים בטבלת התנאים המסחריים שבנספח B להסכם.</div></div>
  <div class="pstep"><div class="pnum">2</div><div class="ptxt">עם חתימת הסכם ההתקשרות ותשלום הרלוונטי למסלולכם (דמי ההשתתפות העצמית במסלולים A/B/C, או מחיר המחקר המלא במסלול 0), אנחנו עורכים את מחקר Genesis ובוחנים מה ניתן לבנות באחריות בתוך המסגרת שהגדרתם.</div></div>
  <div class="pstep"><div class="pnum">3</div><div class="ptxt">אנחנו מציגים לכם תוכנית עסקית, שיווקית ופיננסית, לצד הצעת התקשרות מסחרית — היקף, מבנה תמחור, לוח זמנים ומסגרת עבודה.</div></div>
  <div class="pstep"><div class="pnum">4</div><div class="ptxt">אתם מחליטים — לאשר, לדחות או לדון בהצעה המוצעת.</div></div>
  <div class="pstep"><div class="pnum">5</div><div class="ptxt">ה"הצעה" שתאושר ותיחתם מפעילה את ההתקשרות הספציפית הרלוונטית, לפי מסגרת ההסכם.</div></div>
</div>
<div class="glassnote"><b>לקוחות קיימים:</b> אם כבר חתמתם עם הארגון על הסכם ההתקשרות, והפרק הזה רלוונטי עבורכם לגבי התקשרות נוספת — פרויקט, מותג או יחידה עסקית נפרדים, או מסלול שטרם הופעל — התהליך שלעיל חוזר על עצמו ביחס לאותה התקשרות ספציפית החדשה בלבד, ואינו מצריך חתימה מחודשת על הסכם ההתקשרות עצמו; טבלת נספח B תעודכן ביחס אליה בלבד, מבלי לשנות תנאים שנקבעו בהצעה חתומה אחרת שנותרה בתוקף.</div>
</div>''')

# ---- Intake divider ----
PAGES.append('''<div class="page divider">
  <div class="divider-eyebrow">החלק הבא</div>
  <div class="divider-num">02</div>
  <div class="divider-title">טופס קליטה</div>
  <div class="divider-sub">המידע כאן משמש לתכנון בלבד (ראו "לפני שממשיכים" למעלה) ואינו קובע בעצמו היקף, מחיר או תנאים מחייבים. הטופס תמציתי במכוון — כל שדה משמש ישירות את שלב המחקר והתכנון.</div>
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

intake_html = [f'''<div class="page statement">
{pagehead("טופס קליטה")}
<h1 class="sec">טופס קליטה</h1>
<p class="intake-intro">מטרת הטופס: לאסוף את המידע הדרוש לצוות המחקר והתכנון כדי לבנות עבורכם תוכנית עסקית, שיווקית ופיננסית מותאמת, ולתרגם אותה בהמשך להצעת התקשרות מסחרית ספציפית. הטופס תמציתי במכוון — כל שדה כאן משמש ישירות את שלב המחקר והתכנון; פרטים נוספים ומדויקים יותר ייאספו בשיחה ישירה איתכם, ואינם "נועלים" אתכם בשום מחויבות עד לחתימה על הצעה ספציפית.</p>''']

for idx, (title, note, items) in enumerate(INTAKE_GROUPS, start=1):
    grp = [f'<div class="igroup"><div class="igroup-head"><span class="igroup-num">{idx:02d}</span><span class="igroup-title">{title}</span></div>']
    if note:
        grp.append(f'<div class="igroup-note">{note}</div>')
    grp.append('<div class="ifields">')
    for it in items:
        grp.append(field(it))
    grp.append('</div></div>')
    intake_html.append("".join(grp))

intake_html.append('</div>')
PAGES.append("".join(intake_html))

# ---- Closing ----
PAGES.append(f'''<div class="page closing">
  <img src="{LOGO_MARK}" class="mark">
  <div class="lead">כל המידע במדריך זה משמש לתכנון ולהערכה בלבד.</div>
  <div class="sub">חתימה על הסכם ההתקשרות עצמו כן כרוכה בתשלום הרלוונטי למסלולכם. ההתחייבות המסחרית המלאה להיקף, למחיר ולתנאי ההתקשרות הספציפית נוצרת רק ב"הצעה" חתומה בנפרד.<br><br>אנחנו מוכנים כשאתם מוכנים.</div>
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

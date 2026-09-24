# -*- coding: utf-8 -*-
"""A small, robust Markdown parser for CLIENT_GUIDE_HE.md's specific
conventions — not a general-purpose CommonMark parser.

It turns the .md file into a structured tree (chapters -> sections ->
ordered blocks of paragraph/table/list), so build_html_guide.py can pull
every sentence of Hebrew PROSE that it renders directly from this parsed
tree, instead of retyping it as a Python string literal. Presentation
(page grouping, diagrams, card grids, stat tiles) stays hand-authored in
build_html_guide.py; this module only ever hands back content.

Conventions handled (this file's actual usage, confirmed by inspection):
  - `# Title` (document title, once, first line)
  - `**גרסה X.Y · עודכן לאחרונה: DD.MM.YYYY**` (version line, appears once
    before the first `##`)
  - `> ...` blockquote (front-matter notice; exposed but not required by
    any page today)
  - `## פרק N — Title` chapter headings
  - `### Subtitle` section headings
  - `---` horizontal rules (ignored; sections/chapters are delimited by
    heading level already)
  - paragraphs: one blank-line-separated block of text, optionally with
    inline `**bold**` spans (kept as <strong>), or a whole paragraph
    wrapped in single `*italic*`
  - bullet lists: consecutive lines starting with `- `
  - field lists: consecutive lines starting with `- [ ] ` — a fill-in
    field the reader is meant to answer, rendered as a dotted-line field
    row wherever it appears (see FLIST convention below render_flist)
  - numbered lists: consecutive lines starting with `N. `
  - GFM pipe tables: a header row, a `|---|---|` separator row, and data
    rows, all consecutive `|`-led lines

Every block also stores the ORIGINAL raw text, so a caller that needs a
word count (e.g. for the "no page has under 15 words" sanity check) or a
raw comparison can get it without re-stripping HTML.
"""
import re
from collections import OrderedDict

BOLD_RE = re.compile(r'\*\*(.+?)\*\*', re.DOTALL)
LEAD_BOLD_RE = re.compile(r'^\*\*(.+?)\*\*(.*)$', re.DOTALL)
WHOLE_ITALIC_RE = re.compile(r'^\*([^*].*[^*]|[^*])\*$', re.DOTALL)
CHAPTER_RE = re.compile(r'^##\s+(.+?)\s*$')
SECTION_RE = re.compile(r'^###\s+(.+?)\s*$')
CHAPTER_NUM_RE = re.compile(r'^פרק\s+(\d+)\s*—\s*(.+)$')
VERSION_RE = re.compile(r'^\*\*גרסה\s+([\d.]+)\s*·\s*עודכן לאחרונה:\s*([\d.]+)\*\*$')
TITLE_RE = re.compile(r'^#\s+(.+?)\s*$')


def _escape(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def inline_to_html(text):
    """Escape then convert every **bold** span to <strong>. Safe to call
    on any raw inline text (paragraph, list item, table cell)."""
    text = _escape(text)
    return BOLD_RE.sub(r'<strong>\1</strong>', text)


FIELD_ITEM_RE = re.compile(r'^-\s*\[\s*\]\s+')


def _line_kind(line):
    if line.lstrip().startswith('|'):
        return 'table'
    if FIELD_ITEM_RE.match(line):
        return 'flist'
    if re.match(r'^-\s+', line):
        return 'ul'
    if re.match(r'^\d+\.\s+', line):
        return 'ol'
    return 'p'


def _split_table_row(line):
    line = line.strip()
    if line.startswith('|'):
        line = line[1:]
    if line.endswith('|'):
        line = line[:-1]
    return [c.strip() for c in line.split('|')]


def _parse_table(lines):
    header = _split_table_row(lines[0])
    # lines[1] is the --- separator row; skip it if present.
    data_start = 2 if len(lines) > 1 and re.match(r'^\|?[\s:|-]+\|?$', lines[1].strip()) else 1
    rows = [_split_table_row(l) for l in lines[data_start:]]
    return {"type": "table", "headers": header, "rows": rows}


def _parse_paragraph(raw):
    lead = None
    italic_whole = False
    if raw.startswith('**'):
        m = LEAD_BOLD_RE.match(raw)
        if m:
            lead = m.group(1)
    elif raw.startswith('*') and not raw.startswith('**'):
        if WHOLE_ITALIC_RE.match(raw):
            italic_whole = True
    return {
        "type": "para",
        "lead": lead,
        "italic_whole": italic_whole,
        "html": inline_to_html(raw),
        "text": raw,
    }


def _parse_homogeneous_block(lines, kind):
    if kind == 'table':
        return _parse_table(lines)
    if kind == 'ul':
        items_raw = [re.sub(r'^-\s+', '', l) for l in lines]
        return {
            "type": "ulist",
            "items": [inline_to_html(it) for it in items_raw],
            "items_raw": items_raw,
        }
    if kind == 'ol':
        items_raw = [re.sub(r'^\d+\.\s+', '', l) for l in lines]
        return {
            "type": "olist",
            "items": [inline_to_html(it) for it in items_raw],
            "items_raw": items_raw,
        }
    if kind == 'flist':
        items_raw = [FIELD_ITEM_RE.sub('', l) for l in lines]
        return {
            "type": "flist",
            "items": [inline_to_html(it) for it in items_raw],
            "items_raw": items_raw,
        }
    return _parse_paragraph(' '.join(lines))


def _parse_block(lines):
    """Parse one blank-line-delimited chunk into one OR MORE blocks. A
    chunk is usually homogeneous (all table rows, all bullets, all plain
    text), but a lead-in line directly followed by a list with no blank
    line between them (e.g. "ספרו לנו:\n- ...\n- ...") is split into a
    paragraph block plus a list block, in source order."""
    kinds = [_line_kind(l) for l in lines]
    if len(set(kinds)) == 1:
        return [_parse_homogeneous_block(lines, kinds[0])]
    blocks = []
    run = [lines[0]]
    run_kind = kinds[0]
    for line, kind in zip(lines[1:], kinds[1:]):
        if kind == run_kind:
            run.append(line)
        else:
            blocks.append(_parse_homogeneous_block(run, run_kind))
            run, run_kind = [line], kind
    blocks.append(_parse_homogeneous_block(run, run_kind))
    return blocks


def _blocks_from_lines(lines):
    """Split a section/chapter-intro's raw lines into blank-line-delimited
    chunks, then classify each one (possibly into several blocks — see
    _parse_block)."""
    blocks = []
    cur = []
    for line in lines:
        if line.strip() == '':
            if cur:
                blocks.extend(_parse_block(cur))
                cur = []
            continue
        if line.strip() == '---':
            if cur:
                blocks.extend(_parse_block(cur))
                cur = []
            continue
        cur.append(line.rstrip())
    if cur:
        blocks.extend(_parse_block(cur))
    return blocks


class Section:
    def __init__(self, title, blocks):
        self.title = title
        self.blocks = blocks

    def word_count(self):
        n = 0
        for b in self.blocks:
            if b["type"] == "para":
                n += len(b["text"].split())
            elif b["type"] in ("ulist", "olist", "flist"):
                n += sum(len(it.split()) for it in b["items_raw"])
            elif b["type"] == "table":
                n += sum(len(c.split()) for row in b["rows"] for c in row)
        return n


class Chapter:
    def __init__(self, key, num, title):
        self.key = key      # "1".."4" or "intake"
        self.num = num      # int or None
        self.title = title  # chapter title without the "פרק N — " prefix
        self.sections = []  # list[Section]; a leading Section(title=None) holds chapter-intro blocks

    def section(self, title):
        for s in self.sections:
            if s.title == title:
                return s
        available = [s.title for s in self.sections]
        raise KeyError(
            f"Section {title!r} not found in chapter {self.key!r} "
            f"({self.title!r}). Available: {available}"
        )

    def intro_blocks(self):
        for s in self.sections:
            if s.title is None:
                return s.blocks
        return []


class Guide:
    def __init__(self, title, version, updated_date, chapters):
        self.title = title
        self.version = version
        self.updated_date = updated_date
        self.chapters = chapters  # list[Chapter]

    def chapter(self, key):
        key = str(key)
        for c in self.chapters:
            if c.key == key:
                return c
        available = [c.key for c in self.chapters]
        raise KeyError(f"Chapter {key!r} not found. Available: {available}")

    def section(self, chapter_key, section_title):
        return self.chapter(chapter_key).section(section_title)


def parse_guide(md_text):
    lines = md_text.split('\n')
    title = None
    version = None
    updated_date = None

    chapters = []
    cur_chapter = None
    cur_section_title = None
    cur_section_lines = []

    def flush_section():
        nonlocal cur_section_lines, cur_section_title
        if cur_chapter is None:
            cur_section_lines = []
            return
        blocks = _blocks_from_lines(cur_section_lines)
        cur_chapter.sections.append(Section(cur_section_title, blocks))
        cur_section_lines = []

    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]

        if title is None:
            m = TITLE_RE.match(line)
            if m:
                title = m.group(1)
                i += 1
                continue

        if version is None:
            m = VERSION_RE.match(line.strip())
            if m:
                version, updated_date = m.group(1), m.group(2)
                i += 1
                continue

        m = CHAPTER_RE.match(line)
        if m:
            flush_section()
            raw_title = m.group(1)
            cm = CHAPTER_NUM_RE.match(raw_title)
            if cm:
                num = int(cm.group(1))
                key = str(num)
                ch_title = cm.group(2)
            else:
                num = None
                key = re.sub(r'\s+', '_', raw_title.strip())
                ch_title = raw_title
            cur_chapter = Chapter(key, num, ch_title)
            chapters.append(cur_chapter)
            cur_section_title = None
            i += 1
            continue

        m = SECTION_RE.match(line)
        if m:
            flush_section()
            cur_section_title = m.group(1)
            i += 1
            continue

        if cur_chapter is not None and line.strip() != '>' and not line.startswith('>'):
            # skip the blockquote front-matter (only relevant before any
            # chapter exists anyway) and the top-of-file title/version
            # lines already consumed above.
            cur_section_lines.append(line)
        elif cur_chapter is None:
            pass  # front matter (title, version, blockquote) — not modeled as blocks
        i += 1

    flush_section()

    return Guide(title, version, updated_date, chapters)


def load_guide(path):
    with open(path, encoding='utf-8') as f:
        return parse_guide(f.read())


# ---------------------------------------------------------------------
# Generic renderer: turns parsed blocks into the SAME CSS-classed markup
# build_html_guide.py already defines (table.micro/.data, .callout,
# .callout.warn, .fine, .body-copy). This is the "prose in, presentation
# out" boundary described in the module docstring.
#
# Convention for asides (documented here since it's the maintenance
# contract for anyone adding new chapters):
#
#   A paragraph is classified by its LEADING bold span — the exact text
#   of a **bold lead-in** at the very start of the paragraph (`_parse_
#   paragraph`'s `lead`), looked up verbatim in ASIDE_CLASS below.
#   Unlisted lead-ins (or paragraphs with no lead-in at all) render as
#   a plain `<p class="body-copy">` — the bold lead-in still shows up
#   as inline <strong>, it just isn't pulled out into a boxed aside.
#   A whole paragraph wrapped in single `*italic*` renders as `.fine`.
#
#   This is deliberately a small, explicit, auditable TABLE keyed by the
#   short lead-in PHRASE, not a regex/keyword guess and not the full
#   sentence. Two things this buys, confirmed against how this content
#   was hand-classified before the CLIENT_GUIDE_HE.md parser existed
#   (`git show <pre-a473159 commit>:build_html_guide.py`, the ground
#   truth used to calibrate every entry below):
#     - A word like "לא" ("not") appears in the lead of both a `.callout`
#       ("לא בטוחים איזה מסלול מתאים לכם?") and a `.callout.warn`
#       ("מה זה לא אומר:") — so warn-vs-plain-callout is NOT a keyword
#       rule, it is looked up per lead-in, matching original intent.
#     - The lead-in is copied VERBATIM from the .md — never rephrased —
#       so a content edit that changes a lead-in's wording simply drops
#       back to plain `.body-copy` (safe, visible in a diff/render) and
#       is picked back up the moment the same phrase is reused, rather
#       than silently drifting.
#   A future author adds a new lead-in phrase here (one line) whenever a
#   new paragraph should render as a boxed aside, and should recognize
#   the shape: a short, colon- or period-terminated **bold phrase**
#   naming the kind of aside ("הכלל...:", "חשוב שתדעו:", "דוגמה
#   להמחשה...", "מה זה ... אומר:"), immediately followed by its
#   explanatory sentence(s) in the same paragraph.
#
#   Known limitation (not fixed here — it is a content-structure
#   question, not a rendering one, and CLIENT_GUIDE_HE.md is out of
#   scope for this fix): a few formerly-boxed asides (e.g. the exit-
#   schedule note under "אם אתם מסיימים ביוזמתכם, מוקדם", the privacy
#   summary under "נתונים, פגישות ופרטיות — בקצרה", and the pre-form
#   notice under "לפני שממשיכים — חשוב שתדעו") were promoted during a
#   later content reorg from an inline bold-led aside into their own
#   `### ` section heading with an un-led body paragraph. Since the
#   paragraph no longer carries a bold lead, this table can't catch it;
#   fixing that would mean either editing the .md (reintroducing content
#   drift risk) or collapsing a titled section into a box (a page-layout
#   decision, not a paragraph-classification one). These render as plain
#   `.body-copy` pages today — flagged for the content author, not
#   silently reinterpreted here.
# ---------------------------------------------------------------------

ASIDE_CLASS = {
    # .callout — key-insight / notable-but-positive asides: a rule, a
    # decision aid, or an orienting summary the reader benefits from
    # seeing set apart, in the warm gold-bordered box.
    "חשוב שתדעו:": "callout",
    "המסע המלא, בקצרה:": "callout",
    "ברירת המחדל: נקודת איזון, לא הפסד.": "callout",
    "גירעון זמני — רק אם תבחרו זאת במפורש, ותמיד עם תקרה.": "callout",
    "לקוחות קיימים:": "callout",
    "דוגמה להמחשה בלבד — לא תחזית.": "callout",
    "הנתיב המועדף שלכם (מסלולים A/B/C):": "callout",
    "לא בטוחים איזה מסלול מתאים לכם?": "callout",
    # .callout.warn — restriction / what-you-don't-get
    "מה זה לא אומר:": "callout warn",
    # .fine — small muted print / footnote-style asides: legal-mechanism
    # detail, worked examples and definitional cross-references that
    # support the main text without competing with it for attention.
    # "הערה ללקוחות מסלול 0:" lives here rather than .callout: it's a
    # scoping/definitional note (which parts of the Guide don't apply to
    # you), not a key-insight aside, and .callout's larger padding was
    # overflowing the page it sits on (verified: caused an orphaned
    # footer page). Semantically it fits .fine's own description better
    # anyway.
    "הערה ללקוחות מסלול 0:": "fine",
    "הכלל האופרטיבי:": "fine",
    "למה הסכומים בטבלת סעיף 11 להסכם נראים כפי שהם.": "fine",
    "דוגמה להמחשה — למה הרצפה זהה גם לתקציב קטן.": "fine",
    "סודיות.": "fine",
    "מתי נדרש מחקר Genesis נפרד.": "fine",
    "המשכתם אלינו לביצוע בפועל?": "fine",
}


def render_para(block):
    if block.get("italic_whole"):
        inner = inline_to_html(block["text"][1:-1])
        return f'<p class="fine"><em>{inner}</em></p>'
    cls = ASIDE_CLASS.get(block.get("lead"))
    if cls == "callout":
        return f'<div class="callout">{block["html"]}</div>'
    if cls == "callout warn":
        return f'<div class="callout warn">{block["html"]}</div>'
    if cls == "fine":
        return f'<div class="fine">{block["html"]}</div>'
    return f'<p class="body-copy">{block["html"]}</p>'


def render_table(block, force_class=None):
    ncols = len(block["headers"])
    cls = force_class or ("micro" if ncols <= 3 else "data")
    head = ''.join(f'<th>{inline_to_html(h)}</th>' for h in block["headers"])
    body_rows = []
    for row in block["rows"]:
        cells = ''.join(f'<td>{inline_to_html(c)}</td>' for c in row)
        body_rows.append(f'<tr>{cells}</tr>')
    return f'<table class="{cls}"><tr>{head}</tr>{"".join(body_rows)}</table>'


def render_ulist(block):
    items = ''.join(f'<li>{it}</li>' for it in block["items"])
    return f'<ul class="md-list">{items}</ul>'


def render_olist(block):
    items = ''.join(f'<li>{it}</li>' for it in block["items"])
    return f'<ol class="md-list">{items}</ol>'


# ---------------------------------------------------------------------
# FLIST — inline fill-in field groups (content-architecture pass, v3.0).
#
# Before this pass, every piece of client-supplied data lived in one
# consolidated "## טופס קליטה" chapter at the end of the document, and
# the ONLY thing that made that chapter's bullet lists render as
# dotted-line fill-in fields (the .ifields/.igroup CSS treatment) was
# build_html_guide.py reaching for that one specific chapter by name and
# hand-building the field rows for it. There was no markdown-level
# signal distinguishing "this bullet is a field to fill in" from "this
# bullet is a normal list item" — the distinction existed only in
# presentation code, tied to one heading.
#
# Per the client's request, each field now lives next to the prose that
# explains it, in whichever chapter that is — so the signal can no
# longer be "which chapter is this." Mirroring the ASIDE_CLASS design
# just above (a small, explicit, auditable markdown-level convention,
# not a structural/heading-based hook): a bullet list item written as
#   - [ ] label text
# instead of the normal
#   - label text
# is parsed as its own block type, "flist" (see _line_kind/FIELD_ITEM_RE
# and _parse_homogeneous_block above), and rendered here as one dotted-
# line field row per item — the exact same .ifields/.f/.flabel/.fline
# visual treatment the old end-of-document Intake Form used, just
# without that form's numbered .igroup wrapper (this is inline content
# now, sitting inside a chapter/section that already has its own
# heading, so it doesn't need a second, nested title of its own).
#
# The `[ ]` sigil was chosen (over, say, a special heading or an HTML
# comment) because it is visually self-explanatory in the raw .md too —
# it reads as "a blank to fill in" even before rendering — and because
# it works at the single-list-item granularity a field group needs
# (some sections mix a couple of field bullets into an otherwise normal
# explanatory list; a heading-level signal couldn't do that). A future
# author marks any new bullet as a field, in any chapter, by writing it
# as `- [ ] ...` — no code change needed unless the visual treatment
# itself should change, in which case this is the one place to change it.
# ---------------------------------------------------------------------

def render_flist(block):
    rows = ''.join(
        f'<div class="f"><span class="flabel">{it}</span><span class="fline"></span></div>'
        for it in block["items"]
    )
    return f'<div class="ifields">{rows}</div>'


def render_block(block):
    t = block["type"]
    if t == "para":
        return render_para(block)
    if t == "table":
        return render_table(block)
    if t == "ulist":
        return render_ulist(block)
    if t == "olist":
        return render_olist(block)
    if t == "flist":
        return render_flist(block)
    raise ValueError(f"unknown block type {t!r}")


def render_blocks(blocks):
    return "\n".join(render_block(b) for b in blocks)


def split_lead(block):
    """For the rare bespoke page that wants a block's leading bold phrase
    on its own (e.g. an oversized pull-quote) and the remainder
    separately — both pieces still sourced from the parsed paragraph,
    never retyped. Returns (lead_html, rest_html)."""
    if not block.get("lead"):
        return None, block["html"]
    m = LEAD_BOLD_RE.match(block["text"])
    rest_raw = m.group(2).strip()
    return inline_to_html(block["lead"]), inline_to_html(rest_raw)

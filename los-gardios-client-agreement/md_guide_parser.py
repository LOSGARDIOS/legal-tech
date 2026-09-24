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
  - `## פרק N — Title` chapter headings, and one non-numbered chapter
    (`## טופס קליטה`)
  - `### Subtitle` section headings
  - `---` horizontal rules (ignored; sections/chapters are delimited by
    heading level already)
  - paragraphs: one blank-line-separated block of text, optionally with
    inline `**bold**` spans (kept as <strong>), or a whole paragraph
    wrapped in single `*italic*`
  - bullet lists: consecutive lines starting with `- `
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


def _line_kind(line):
    if line.lstrip().startswith('|'):
        return 'table'
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
            elif b["type"] in ("ulist", "olist"):
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
#   A paragraph is classified by its LEADING bold span (the exact text of
#   a **bold lead-in** at the very start of the paragraph), looked up in
#   ASIDE_CLASS below. Unlisted lead-ins (or no lead-in at all) render as
#   a plain `<p class="body-copy">` — the bold lead-in still shows up
#   as inline <strong>, it just isn't pulled out into a boxed aside.
#   A whole paragraph wrapped in single `*italic*` renders as `.fine`.
# This keeps classification a small, explicit, auditable table instead of
# a guess — a future author adds a new lead-in phrase here (one line) if
# they want a new paragraph to render as a boxed aside.
# ---------------------------------------------------------------------

ASIDE_CLASS = {
    # .callout — key-insight / notable-but-positive asides
    "הכלל האופרטיבי:": "callout",
    "חשוב שתדעו:": "callout",
    "ברירת המחדל: נקודת איזון, לא הפסד.": "callout",
    "גירעון זמני — רק אם תבחרו זאת במפורש, ותמיד עם תקרה.": "callout",
    "לקוחות קיימים:": "callout",
    "דוגמה להמחשה בלבד — לא תחזית.": "callout",
    "הנתיב המועדף שלכם (מסלולים A/B/C):": "callout",
    "לא בטוחים איזה מסלול מתאים לכם?": "callout",
    # .callout.warn — restriction / what-you-don't-get
    "מה זה לא אומר:": "callout warn",
    # .fine — small muted print / footnote-style asides
    "למה הסכומים בטבלת סעיף 11 להסכם נראים כפי שהם.": "fine",
    "דוגמה להמחשה — למה הרצפה זהה גם לתקציב קטן.": "fine",
    "הערה ללקוחות מסלול 0:": "fine",
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

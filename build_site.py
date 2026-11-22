"""Build a static reading site from the study markdown files."""
import hashlib
import html
import html.parser
import re
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "site"
ASSET_V = "dev"

SOURCES = [
    ("開始", [
        ("strategy.html", "溫習策略", "溫習策略.md"),
        ("study-plan.html", "15 週計劃", "OCP-Java-SE-21-study-plan.md"),
    ]),
    *[
        (
            f"第 {n} 週",
            [
                (f"Week-{n:02d}-notes.html", "筆記", f"Week-{n:02d}-notes.md"),
                (f"Week-{n:02d}-glossary.html", "詞彙", f"Week-{n:02d}-glossary.md"),
            ],
        )
        for n in range(1, 9)
    ],
]


def slugify(value, separator):
    value = re.sub(r"[^\w\u4e00-\u9fff\- ]+", "", value, flags=re.UNICODE)
    value = separator.join(value.lower().split())
    return value or "section"


def rewrite_links(text):
    names = {src: dest for _, pages in SOURCES for dest, _, src in pages}

    def repl(match):
        label, target = match.group(1), match.group(2)
        dest = names.get(target)
        if dest is None:
            return match.group(0)
        return f"[{label}]({dest})"

    return re.sub(r"\[([^\]]+)\]\(([^)]+\.md)\)", repl, text)


def render_markdown(text):
    text = rewrite_links(text)
    converter = markdown.Markdown(
        extensions=["extra", "sane_lists", "toc"],
        extension_configs={"toc": {"slugify": slugify, "toc_depth": "2-3"}},
    )
    body = converter.convert(text)
    body = re.sub(
        r"<li>\s*(?:<p>)?\[ \]\s*",
        '<li class="task"><button type="button" class="box" aria-pressed="false" aria-label="完成"></button> ',
        body,
    )
    body = re.sub(
        r"<li>\s*(?:<p>)?\[[xX]\]\s*",
        '<li class="task"><button type="button" class="box on" aria-pressed="true" aria-label="完成"></button> ',
        body,
    )
    body = re.sub(
        r'(<li class="task"><button type="button" class="box(?: on)?" aria-pressed="(?:false|true)" aria-label="完成"></button>(?:(?!</li>|</p>).)*)</p>(\s*</li>)',
        r"\1\2",
        body,
    )
    body = re.sub(
        r'(<li class="task"><button type="button" class="box(?: on)?" aria-pressed="(?:false|true)" aria-label="完成"></button>)\s*(.*?)</li>',
        r'\1<span class="task-body">\2</span></li>',
        body,
        flags=re.S,
    )
    body = body.replace("<table>", '<div class="table-wrap"><table>')
    body = body.replace("</table>", "</table></div>")
    return enhance_questions(body)


class _Blocks(html.parser.HTMLParser):
    void = {"hr", "br", "img", "meta", "link", "input", "source", "col", "wbr"}

    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.blocks = []
        self.parts = []
        self.depth = 0
        self.ok = True

    def _tag(self, tag, attrs):
        bits = []
        for name, value in attrs:
            if value is None:
                bits.append(f" {name}")
            else:
                bits.append(f' {name}="{html.escape(value, quote=True)}"')
        return f"<{tag}{''.join(bits)}>"

    def handle_starttag(self, tag, attrs):
        text = self._tag(tag, attrs)
        if tag in self.void:
            if self.depth == 0:
                self.blocks.append(text)
            else:
                self.parts.append(text)
            return
        if self.depth == 0:
            self.parts = [text]
        else:
            self.parts.append(text)
        self.depth += 1

    def handle_endtag(self, tag):
        if tag in self.void:
            return
        if self.depth <= 0:
            self.ok = False
            return
        self.parts.append(f"</{tag}>")
        self.depth -= 1
        if self.depth == 0:
            self.blocks.append("".join(self.parts))
            self.parts = []

    def handle_data(self, data):
        if self.depth == 0:
            if data.strip():
                self.blocks.append(data)
            return
        self.parts.append(data)

    def handle_entityref(self, name):
        self.handle_data(f"&{name};")

    def handle_charref(self, name):
        self.handle_data(f"&#{name};")


def top_blocks(body):
    parser = _Blocks()
    parser.feed(body)
    parser.close()
    if not parser.ok or parser.depth != 0:
        return None
    return parser.blocks


_HEADING = re.compile(r"^<h([1-3]) id=\"([^\"]+)\">(.*)</h\1>$", re.S)
_QUESTION = re.compile(r"^<p><strong>((?:Q|M)\d+)\.</strong>(.*)</p>$", re.S)
_ANSWER = re.compile(
    r"^<p><strong>((?:Q|M)\d+)\s+[—–-]\s+((?:[A-H])(?:\s*,\s*[A-H])*)\.</strong>\s*(.*)</p>$",
    re.S,
)
_CHOICE = re.compile(r"(?:^|\n)\s*([A-H])\.\s*")


def heading_info(block):
    match = _HEADING.match(block.strip())
    if not match:
        return None
    return match.group(1), match.group(2), plain_text(match.group(3))


def parse_choice_block(block):
    match = re.fullmatch(r"<p>(.*)</p>", block.strip(), re.S)
    if not match:
        return None
    parts = _CHOICE.split(match.group(1).strip("\n"))
    if len(parts) < 3 or parts[0].strip():
        return None
    return [(parts[i], parts[i + 1].strip()) for i in range(1, len(parts), 2)]


def split_question_blocks(blocks):
    prefix, choices, suffix = [], [], []
    started = False
    index = 0
    while index < len(blocks):
        items = parse_choice_block(blocks[index])
        if items and ((not started and items[0][0] == "A") or started):
            started = True
            if len(items) == 1 and not items[0][1]:
                letter = items[0][0]
                index += 1
                chunks = []
                while index < len(blocks) and not parse_choice_block(blocks[index]):
                    chunks.append(blocks[index])
                    index += 1
                choices.append((letter, "".join(chunks)))
                continue
            choices.extend(items)
            index += 1
            continue
        (prefix if not started else suffix).append(blocks[index])
        index += 1
    return prefix, choices, suffix


def choice_button(letter, body):
    body = re.sub(
        r"<pre><code[^>]*>([\s\S]*?)</code></pre>",
        r'<code class="snippet">\1</code>',
        body,
    )
    return (
        f'<button type="button" class="choice" data-letter="{letter}" aria-pressed="false">'
        f'<span class="letter">{letter}</span><span class="choice-body">{body}</span></button>'
    )


def take_keys(bucket):
    keyed = {}
    leftover = []
    current = None
    parts = []

    def flush():
        nonlocal current, parts
        if current:
            keyed[current[0]] = (current[1], "".join(parts))
        current = None
        parts = []

    for block in bucket:
        match = _ANSWER.match(block.strip())
        if match:
            flush()
            letters = tuple(re.findall(r"[A-H]", match.group(2)))
            label = "、".join(letters)
            explanation = match.group(3).strip()
            current = (match.group(1), letters)
            parts = [f"<p><strong>答案：{label}。</strong> {explanation}</p>"]
        elif current:
            parts.append(block)
        else:
            leftover.append(block)
    flush()
    return keyed, leftover


def render_question(blocks, qid, answer):
    letters, answer_html = answer if answer else ((), "")
    prompt = plain_text("".join(blocks)).lower()
    multi = "1" if len(letters) > 1 or "choose all" in prompt else "0"
    prefix, choices, suffix = split_question_blocks(blocks)
    key = ",".join(letters)
    parts = [
        f'<section class="q" id="{html.escape(qid)}" data-qid="{html.escape(qid)}" data-multi="{multi}" data-key="{html.escape(key)}">'
    ]
    parts.extend(prefix)
    if choices:
        labels = "可選多項" if multi == "1" else "選一項"
        parts.append(f'<div class="choices" role="group" aria-label="{labels}">')
        parts.extend(choice_button(letter, body) for letter, body in choices)
        parts.append("</div>")
    if answer_html:
        parts.append(reveal_button())
        parts.append(f'<div class="answer" hidden>{answer_html}</div>')
    parts.extend(suffix)
    parts.append("</section>")
    return "".join(parts)


def reveal_button():
    return (
        '<button type="button" class="reveal" aria-expanded="false" aria-label="揭曉答案">'
        '<svg class="icon-show" viewBox="0 0 24 24" aria-hidden="true">'
        '<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z"/>'
        '<circle cx="12" cy="12" r="3"/></svg>'
        '<svg class="icon-hide" viewBox="0 0 24 24" aria-hidden="true">'
        '<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z"/>'
        '<circle cx="12" cy="12" r="3"/>'
        '<path d="M4 4l16 16"/></svg>'
        '<span class="reveal-label">揭曉答案</span></button>'
    )


def reveal_panel(heading, blocks, qid):
    return (
        heading
        + f'<div class="kept" data-qid="{html.escape(qid)}">'
        + reveal_button()
        + f'<div class="answer" hidden>{"".join(blocks)}</div></div>'
    )


def rebuild_section(section, section_id):
    preamble = []
    questions = []
    current = None
    answer_map = {}
    extras = []
    index = 0
    while index < len(section):
        info = heading_info(section[index])
        if info and info[0] == "3" and "answer" in info[2].lower():
            if current:
                questions.append(current)
                current = None
            heading = section[index]
            index += 1
            bucket = []
            while index < len(section):
                nxt = heading_info(section[index])
                if nxt and nxt[0] == "3":
                    break
                bucket.append(section[index])
                index += 1
            keyed, leftover = take_keys(bucket)
            answer_map.update(keyed)
            if leftover or not keyed:
                extras.append((heading, leftover or bucket, info[1]))
            continue
        if _QUESTION.match(section[index].strip()):
            if current:
                questions.append(current)
            current = [section[index]]
            index += 1
            continue
        if current is not None:
            current.append(section[index])
        else:
            preamble.append(section[index])
        index += 1
    if current:
        questions.append(current)
    rendered = list(preamble)
    for blocks in questions:
        match = _QUESTION.match(blocks[0].strip())
        qid = f"{section_id}-{match.group(1)}"
        rendered.append(render_question(blocks, qid, answer_map.get(match.group(1))))
    for heading, blocks, qid in extras:
        rendered.append(reveal_panel(heading, blocks, qid))
    return rendered


def enhance_questions(body):
    if "<strong>Q1.</strong>" not in body and "<strong>M1.</strong>" not in body:
        return body
    blocks = top_blocks(body)
    if not blocks:
        return body
    output = []
    index = 0
    while index < len(blocks):
        info = heading_info(blocks[index])
        if info and info[0] in {"1", "2"}:
            heading = blocks[index]
            index += 1
            section = []
            while index < len(blocks):
                nxt = heading_info(blocks[index])
                if nxt and nxt[0] in {"1", "2"}:
                    break
                section.append(blocks[index])
                index += 1
            if any(_QUESTION.match(block.strip()) for block in section):
                output.append(heading)
                output.extend(rebuild_section(section, info[1]))
            else:
                output.append(heading)
                output.extend(section)
            continue
        output.append(blocks[index])
        index += 1
    return "\n".join(output)


def plain_text(fragment):
    text = re.sub(r"<[^>]+>", " ", fragment)
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def toc_skip_title(title):
    text = title.strip().lower()
    if text == "what you must know":
        return True
    if text.endswith(" answers"):
        return True
    return False


def toc_label_html(title):
    day = re.match(
        r"^(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\s*[—–-]\s*(.+)$",
        title,
        flags=re.I,
    )
    if day:
        return (
            f'<span class="toc-kicker">{html.escape(day.group(1))}</span>'
            f'<span class="toc-rest">{html.escape(day.group(2))}</span>'
        )
    chapter = re.match(r"^(Chapter\s+\d+)\s*[—–-]\s*(.+)$", title, flags=re.I)
    if chapter:
        return (
            f'<span class="toc-kicker">{html.escape(chapter.group(1))}</span>'
            f'<span class="toc-rest">{html.escape(chapter.group(2))}</span>'
        )
    return f'<span class="toc-rest">{html.escape(title)}</span>'


def page_toc(body):
    heads = []
    for match in re.finditer(r"<h([123]) id=\"([^\"]+)\">(.*?)</h\1>", body, flags=re.S):
        title = plain_text(match.group(3))
        if title:
            heads.append((match.group(1), match.group(2), title))
    if heads and heads[0][0] == "1":
        heads = heads[1:]
    heads = [(level, anchor, title) for level, anchor, title in heads if not toc_skip_title(title)]
    if not heads:
        return ""
    parts = ['<ul class="toc-list">']
    open_chapter = False
    for level, anchor, title in heads:
        link = f'<a href="#{html.escape(anchor)}">{toc_label_html(title)}</a>'
        if level == "1":
            if open_chapter:
                parts.append("</ul></li>")
            parts.append(f'<li class="chapter">{link}<ul>')
            open_chapter = True
        else:
            kind = "topic" if level == "3" else "section"
            parts.append(f'<li class="{kind}">{link}</li>')
    if open_chapter:
        parts.append("</ul></li>")
    parts.append("</ul>")
    return (
        '<details class="toc" id="page-toc" open>'
        '<summary>本頁章節</summary>'
        f'{"".join(parts)}'
        "</details>"
    )


def title_of(body, fallback):
    match = re.search(r"<h1[^>]*>(.*?)</h1>", body, flags=re.S)
    return plain_text(match.group(1)) if match else fallback


FLAT = [(dest, label, src) for _, pages in SOURCES for dest, label, src in pages]


def place_name(dest):
    for name, pages in SOURCES:
        for href, label, _ in pages:
            if href == dest:
                return f"{name} · {label}"
    return ""


def shell(dest, title, body, lang):
    index = FLAT.index(next(item for item in FLAT if item[0] == dest))
    prev_link = next_link = ""
    if index > 0:
        href, _, _ = FLAT[index - 1]
        prev_link = f'<a class="prev" href="{href}"><small>上一篇</small>{html.escape(place_name(href))}</a>'
    if index < len(FLAT) - 1:
        href, _, _ = FLAT[index + 1]
        next_link = f'<a class="next" href="{href}"><small>下一篇</small>{html.escape(place_name(href))}</a>'
    place = ""
    for name, pages in SOURCES:
        for href, label, _ in pages:
            if href == dest:
                place = f'<p class="crumb">{html.escape(name)} · {html.escape(label)}</p>'
    nav = sidebar(dest)
    toc = page_toc(body)
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<script>try{{if(localStorage.getItem("ocp-nav")==="0"&&matchMedia("(min-width:861px)").matches)document.documentElement.classList.add("nav-collapsed")}}catch(e){{}}</script>
<title>{html.escape(title)} · OCP Java 21</title>
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="style.css?v={ASSET_V}">
</head>
<body>
<a class="skip" href="#content">跳到本文</a>
<div class="layout">
{nav}
<main id="content">
<div class="sheet">
{place}
{toc}
<article>
{body}
</article>
<nav class="pager" aria-label="前後篇">
{prev_link}
{next_link}
</nav>
</div>
</main>
</div>
<nav id="jump" class="jump" hidden aria-label="本頁章節"></nav>
<script src="search.js?v={ASSET_V}"></script>
</body>
</html>
"""


def sidebar(current):
    groups = []
    for name, pages in SOURCES:
        links = []
        for dest, label, _ in pages:
            current_attr = ' aria-current="page"' if dest == current else ""
            links.append(
                f'<a href="{dest}"{current_attr}>{html.escape(label)}</a>'
            )
        kind = "pair" if name.startswith("第") else "stack"
        if kind == "pair":
            groups.append(
                f'<section class="pair" data-week="{html.escape(name)}">'
                f'<div class="pair-top"><h2>{html.escape(name)}</h2>'
                f'<button type="button" class="week-done" aria-pressed="false" '
                f'aria-label="標記{html.escape(name)}完成" title="完成本週">'
                f'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12.5l4.2 4.2L19 7"/></svg>'
                f'</button></div>'
                f'<div class="links">{"".join(links)}</div></section>'
            )
        else:
            groups.append(
                f'<section class="{kind}"><h2>{html.escape(name)}</h2>'
                f'<div class="links">{"".join(links)}</div></section>'
            )
    mark = ' aria-current="page"' if current == "index.html" else ""
    return f"""<aside class="side">
<div class="side-head">
<a class="brand" href="index.html"{mark}><img src="favicon.svg" alt="" width="22" height="22">OCP Java 21</a>
<button type="button" class="fold" aria-expanded="true" aria-controls="nav" aria-label="收起目錄"><svg class="icon-open" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 5h16v14H4zM9 5v14"/><path d="M14 9l-3 3 3 3"/></svg><svg class="icon-shut" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 5h16v14H4zM9 5v14"/><path d="M13 9l3 3-3 3"/></svg></button>
</div>
<div id="week-progress" class="week-progress" hidden></div>
<div id="place" class="place" hidden></div>
<div id="nav">
<label class="find">搜尋
<input id="q" type="search" placeholder="詞、題目、規則" autocomplete="off">
</label>
<div id="results" hidden></div>
<nav aria-label="全部筆記">
{"".join(groups)}
</nav>
</div>
</aside>"""


HOME_NOTE = {
    "開始": "先看溫習方法，再對每一天",
    "第 1 週": "11月23–29日 · 型別、運算、流程",
    "第 2 週": "11月30日–12月6日 · 方法、文字、陣列",
    "第 3 週": "12月7–13日 · 類別與記憶體",
    "第 4 週": "12月14–20日 · 繼承到模式比對",
    "第 5 週": "12月21–27日 · 例外與日期",
    "第 6 週": "12月28日–1月3日 · 集合與泛型",
    "第 7 週": "1月4–10日 · lambda 與 stream",
    "第 8 週": "1月11–17日 · 輸入輸出、模組、執行緒",
}


def home():
    cards = []
    for name, pages in SOURCES:
        links = "".join(
            f'<a href="{dest}">{html.escape(label)}</a>' for dest, label, _ in pages
        )
        note = html.escape(HOME_NOTE.get(name, ""))
        cards.append(
            f"<li><h2>{html.escape(name)}</h2><p class=\"when\">{note}</p><p class=\"go\">{links}</p></li>"
        )
    body = f"""<div class="home">
<header class="hero">
<p class="kicker">1Z0-830 · 2027 年 3 月 7 日</p>
<h1>八週筆記，放在同一頁裡看</h1>
<p>11 月 23 日星期一起第 1 週。先讀溫習策略，再打開當週筆記。詞彙只在忘記一個詞的時候查。未到的星期先不要翻。</p>
<div id="place-home" class="place-home" hidden></div>
</header>
<ol class="weeks">
{"".join(cards)}
</ol>
</div>"""
    nav = sidebar("index.html")
    return f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<script>try{{if(localStorage.getItem("ocp-nav")==="0"&&matchMedia("(min-width:861px)").matches)document.documentElement.classList.add("nav-collapsed")}}catch(e){{}}</script>
<title>OCP Java 21</title>
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="style.css?v={ASSET_V}">
</head>
<body>
<a class="skip" href="#content">跳到本文</a>
<div class="layout">
{nav}
<main id="content">
{body}
</main>
</div>
<script src="search.js?v={ASSET_V}"></script>
</body>
</html>
"""


CSS = r"""
:root {
  --bg: #f3efe7;
  --paper: #fffcf7;
  --ink: #241f1c;
  --muted: #6a635c;
  --line: #e2d9cc;
  --accent: #0d4845;
  --accent-soft: #e7f4f2;
  --accent-mid: #cfe4e1;
  --code: #f3eee6;
  --code-ink: #241f1c;
  --side: 16.25rem;
  --radius: 14px;
  --shadow: 0 1px 2px rgba(36, 31, 28, 0.04), 0 8px 24px rgba(36, 31, 28, 0.05);
}
* { box-sizing: border-box; }
html {
  scroll-behavior: smooth;
  -webkit-text-size-adjust: 100%;
  text-size-adjust: 100%;
}
h1, h2, h3 { scroll-margin-top: 1.4rem; }
body {
  margin: 0;
  color: var(--ink);
  background: var(--bg);
  font-family: "Segoe UI", "Microsoft JhengHei", "PingFang TC", sans-serif;
  font-size: 17px;
  line-height: 1.65;
  min-height: 100vh;
  min-height: 100dvh;
  overflow-x: clip;
  -webkit-tap-highlight-color: rgba(14, 74, 72, 0.12);
}
:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
.skip { position: absolute; left: 1rem; top: -3rem; background: var(--ink); color: white; padding: 0.4rem 0.7rem; }
.skip:focus { top: 0.5rem; }
.layout { display: flex; min-height: 100vh; min-height: 100dvh; align-items: flex-start; }
.side {
  width: var(--side);
  flex: none;
  position: sticky;
  top: 0;
  height: 100vh;
  height: 100dvh;
  overflow: auto;
  -webkit-overflow-scrolling: touch;
  background: linear-gradient(180deg, #f8f5ef 0%, #f4f0e8 100%);
  border-right: 1px solid var(--line);
  padding: 1rem 0.8rem 2rem;
}
.side-head { display: flex; align-items: center; justify-content: space-between; gap: 0.5rem; padding: 0.1rem 0.2rem 0.35rem; }
.brand { display: inline-flex; align-items: center; gap: 0.5rem; color: var(--ink); font-weight: 750; letter-spacing: -0.01em; text-decoration: none; }
.brand img { width: 1.45rem; height: 1.45rem; display: block; border-radius: 6px; }
button, .choice, .mark, .reveal, .fold, .jump-fab, .box, .week-done { touch-action: manipulation; }
.fold {
  width: 2.1rem;
  height: 2.1rem;
  padding: 0;
  display: inline-grid;
  place-items: center;
  border: 1px solid var(--line);
  background: var(--paper);
  color: var(--ink);
  border-radius: 10px;
  cursor: pointer;
  box-shadow: 0 1px 0 rgba(36, 31, 28, 0.04);
}
.fold svg { width: 1.15rem; height: 1.15rem; fill: none; stroke: currentColor; stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round; }
.fold .icon-shut { display: none; }
.fold[aria-expanded="false"] .icon-open { display: none; }
.fold[aria-expanded="false"] .icon-shut { display: block; }
html.nav-collapsed .side { width: 3.5rem; padding: 0.85rem 0; overflow: hidden; display: flex; justify-content: center; align-items: flex-start; }
html.nav-collapsed .brand, html.nav-collapsed #nav { display: none; }
html.nav-collapsed .side-head { justify-content: center; align-items: flex-start; padding: 0; height: auto; }
html.nav-collapsed .fold { background: var(--accent); color: white; border-color: var(--accent); }
.find { display: block; margin: 0.95rem 0.1rem 0.4rem; font-size: 0.72rem; color: var(--muted); font-weight: 650; letter-spacing: 0.03em; }
.find input {
  display: block;
  width: 100%;
  margin-top: 0.3rem;
  border: 1px solid var(--line);
  background: var(--paper);
  color: var(--ink);
  border-radius: 11px;
  padding: 0.6rem 0.75rem;
  font: inherit;
  font-size: 16px;
  line-height: 1.4;
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.7);
}
.find input:focus {
  outline: none;
  border-color: #b7d0cc;
  box-shadow: 0 0 0 3px rgba(14, 74, 72, 0.12);
}
#results {
  border: 1px solid var(--line);
  border-radius: 8px;
  margin: 0.35rem 0 0.5rem;
  background: white;
  max-height: 16rem;
  overflow: auto;
}
#results a { display: block; padding: 0.5rem 0.65rem; color: inherit; text-decoration: none; border-bottom: 1px solid var(--line); }
#results a:last-child { border-bottom: 0; }
#results a:hover, #results a:focus { background: var(--accent-soft); }
#results strong { display: block; font-size: 0.86rem; line-height: 1.35; }
#results small { display: block; color: var(--muted); font-size: 0.78rem; line-height: 1.4; margin-top: 0.15rem; }
#results mark { background: #f6e3a1; color: inherit; padding: 0 0.05em; border-radius: 2px; }
#results .empty { margin: 0; padding: 0.55rem 0.65rem; color: var(--muted); font-size: 0.86rem; }
.side section { margin-top: 0.35rem; }
.side .stack { margin-top: 0.55rem; padding: 0.15rem 0.1rem 0.35rem; }
.side h2 { margin: 0.85rem 0 0.25rem; padding: 0 0.4rem; font-size: 0.7rem; letter-spacing: 0.06em; text-transform: uppercase; color: var(--muted); font-weight: 700; }
.side .stack h2 { margin-top: 0.2rem; }
.side .links a { display: block; padding: 0.4rem 0.55rem; color: var(--ink); text-decoration: none; border-radius: 9px; font-size: 0.9rem; transition: background 0.15s ease, color 0.15s ease; }
.side .links a:hover, .side .links a:focus { background: rgba(255, 253, 247, 0.9); }
.side .links a[aria-current="page"] { background: var(--accent-soft); color: var(--accent); font-weight: 700; }
.pair {
  display: flex;
  flex-direction: column;
  gap: 0.28rem;
  margin-top: 0.4rem;
  padding: 0.55rem 0.55rem 0.55rem;
  border: 1px solid transparent;
  border-radius: 12px;
  background: rgba(255, 252, 247, 0.55);
  transition: background 0.18s ease, border-color 0.18s ease, box-shadow 0.18s ease;
}
.pair:hover {
  background: var(--paper);
  border-color: #ebe3d7;
}
.pair-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.45rem;
  min-height: 1.7rem;
}
.pair h2 {
  margin: 0;
  padding: 0;
  font-size: 0.9rem;
  letter-spacing: -0.01em;
  text-transform: none;
  color: var(--ink);
  line-height: 1.25;
  font-weight: 750;
}
.pair .links { display: flex; flex-wrap: wrap; gap: 0.28rem; padding: 0; }
.pair .links a {
  background: #f1ebe2;
  border: 0;
  padding: 0.22rem 0.58rem;
  font-size: 0.74rem;
  font-weight: 650;
  color: var(--muted);
  border-radius: 999px;
  line-height: 1.3;
}
.pair .links a:hover, .pair .links a:focus {
  background: #e7e0d5;
  color: var(--ink);
}
.pair .links a[aria-current="page"] {
  background: var(--accent);
  color: white;
}
.pair:has(a[aria-current="page"]) {
  background: var(--accent-soft);
  border-color: var(--accent-mid);
  box-shadow: inset 0 0 0 1px rgba(13, 72, 69, 0.04);
}
.pair:has(a[aria-current="page"]) h2 { color: var(--accent); }
.week-done {
  flex: none;
  width: 1.75rem;
  height: 1.75rem;
  margin: 0;
  padding: 0;
  display: inline-grid;
  place-items: center;
  border: 1.5px solid #d2c8bb;
  border-radius: 999px;
  background: var(--paper);
  color: transparent;
  cursor: pointer;
  transition: background 0.18s ease, border-color 0.18s ease, color 0.18s ease, transform 0.18s ease;
}
.week-done svg {
  width: 0.9rem;
  height: 0.9rem;
  fill: none;
  stroke: currentColor;
  stroke-width: 2.4;
  stroke-linecap: round;
  stroke-linejoin: round;
}
.week-done:hover, .week-done:focus-visible {
  border-color: var(--accent);
  background: white;
  color: var(--accent);
  outline: none;
  transform: scale(1.04);
}
.week-done:focus-visible { box-shadow: 0 0 0 3px rgba(14, 74, 72, 0.14); }
.week-done[aria-pressed="true"] {
  background: var(--accent);
  border-color: var(--accent);
  color: white;
}
.pair.done {
  background: #f3f6f4;
  border-color: #d7e3df;
}
.pair.done h2 { color: #7a8581; }
.pair.done .links a { background: #e6ece9; color: #8a928e; }
.pair.done:has(a[aria-current="page"]) {
  background: #eef5f3;
  border-color: var(--accent-mid);
}
.pair.done:has(a[aria-current="page"]) h2 { color: var(--accent); }
main {
  flex: 1;
  min-width: 0;
  width: 100%;
  max-width: 100%;
  padding: clamp(0.85rem, 2vw, 1.75rem);
  display: flex;
  flex-direction: column;
  align-items: center;
  box-sizing: border-box;
}
.home { width: min(100%, 68rem); max-width: 100%; }
.sheet {
  width: 100%;
  max-width: 100%;
  min-width: 0;
  box-sizing: border-box;
  overflow-x: hidden;
  background: var(--paper);
  border: 1px solid var(--line);
  border-radius: var(--radius);
  padding: clamp(1.25rem, 3vw, 2.1rem) clamp(1.15rem, 3vw, 2.25rem);
  box-shadow: var(--shadow);
}
article { max-width: 100%; min-width: 0; overflow-wrap: break-word; }
.crumb { margin: 0 0 0.85rem; color: var(--muted); font-size: 0.85rem; }
.place, .place-home {
  background: var(--paper);
  border: 1px solid var(--accent-mid);
  border-radius: 12px;
  padding: 0.6rem 0.7rem;
  box-shadow: var(--shadow);
}
.place { margin: 0.75rem 0.1rem 0; font-size: 0.82rem; }
.place-home { margin: 1rem 0 0; max-width: 36rem; }
.place-head { display: flex; align-items: center; justify-content: space-between; gap: 0.35rem; }
.place p, .place-home p { margin: 0; color: var(--accent); font-weight: 650; font-size: 0.75rem; }
.place-list { list-style: none; margin: 0.25rem 0 0; padding: 0; display: flex; flex-direction: column; gap: 0.2rem; max-height: 11rem; overflow: auto; }
.place-item { display: flex; align-items: center; gap: 0.25rem; }
.place-item a {
  flex: 1;
  min-width: 0;
  display: block;
  font-weight: 650;
  text-decoration: none;
  color: var(--ink);
  line-height: 1.35;
  font-size: 0.84rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.place-item a:hover, .place-item a:focus { color: var(--accent); }
.place-clear, .place-item-clear {
  flex: none;
  width: 1.55rem;
  height: 1.55rem;
  margin: 0;
  padding: 0;
  display: inline-grid;
  place-items: center;
  border: 0;
  border-radius: 7px;
  background: transparent;
  color: var(--muted);
  cursor: pointer;
}
.place-clear:hover, .place-clear:focus,
.place-item-clear:hover, .place-item-clear:focus { background: white; color: var(--ink); }
.place-clear svg, .place-item-clear svg { width: 0.95rem; height: 0.95rem; fill: none; stroke: currentColor; stroke-width: 1.9; stroke-linecap: round; }
.week-progress {
  margin: 0.75rem 0.1rem 0.2rem;
  padding: 0.65rem 0.7rem 0.7rem;
  background: var(--paper);
  border: 1px solid var(--line);
  border-radius: 12px;
  box-shadow: var(--shadow);
}
.week-progress p { display: flex; justify-content: space-between; gap: 0.5rem; margin: 0; font-size: 0.78rem; font-weight: 700; }
.week-progress .pct { color: var(--accent); font-variant-numeric: tabular-nums; }
.track { margin-top: 0.45rem; height: 0.38rem; background: #efe8dc; border-radius: 999px; overflow: hidden; }
.track span { display: block; height: 100%; width: 0; background: linear-gradient(90deg, #0d4845, #1a6b66); border-radius: inherit; }
.week-progress small { display: block; margin-top: 0.38rem; color: var(--muted); font-size: 0.75rem; line-height: 1.35; }
.week-progress .where { display: block; color: var(--ink); font-weight: 650; }
html.nav-collapsed .place, html.nav-collapsed .week-progress { display: none; }
.mark {
  width: 1.7rem;
  height: 1.7rem;
  margin: 0;
  padding: 0;
  display: inline-grid;
  place-items: center;
  vertical-align: middle;
  border: 1px solid var(--line);
  background: #fffdf9;
  color: var(--muted);
  border-radius: 999px;
  cursor: pointer;
  box-shadow: none;
  transition: color 0.15s ease, background 0.15s ease, border-color 0.15s ease, opacity 0.15s ease;
}
.mark svg { width: 0.92rem; height: 0.92rem; fill: none; stroke: currentColor; stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round; }
.mark .icon-on { display: none; }
.mark:hover, .mark:focus-visible {
  color: var(--ink);
  border-color: #cfc4b4;
  background: white;
  outline: none;
}
.mark:focus-visible { box-shadow: 0 0 0 3px rgba(14, 74, 72, 0.14); }
.mark[aria-pressed="true"] { background: var(--accent); color: white; border-color: var(--accent); }
.mark[aria-pressed="true"] .icon-off { display: none; }
.mark[aria-pressed="true"] .icon-on { display: block; fill: currentColor; stroke: none; }
@media (hover: hover) and (pointer: fine) {
  article :is(h1, h2, h3) .mark { opacity: 0.42; }
  article :is(h1, h2, h3):hover .mark,
  article :is(h1, h2, h3):focus-within .mark,
  article .mark:hover,
  article .mark:focus-visible,
  article .mark[aria-pressed="true"] { opacity: 1; }
}
article :is(h1, h2, h3) {
  display: block;
  position: relative;
  max-width: 100%;
}
article :is(h1, h2, h3) .mark {
  position: static;
  margin-left: 0.4rem;
  transform: translateY(-0.06em);
}
article .q,
article > blockquote {
  position: relative;
  padding-right: 2.4rem;
}
article .q .mark,
article > blockquote .mark {
  position: absolute;
  top: 0.35rem;
  right: 0.15rem;
  left: auto;
  z-index: 2;
}
article :is(h1, h2, h3).reached {
  box-shadow: inset 3px 0 0 var(--accent);
  padding-left: 0.55rem;
}
article .q.reached,
article > blockquote.reached {
  outline: 1px solid #c5d9d5;
  background: #f7faf9;
  border-radius: 10px;
}
.hero h1, article h1 { font-size: 1.85rem; line-height: 1.25; margin: 0 0 0.7rem; font-weight: 700; }
.kicker { margin: 0 0 0.35rem; color: var(--accent); font-weight: 650; font-size: 0.92rem; }
article { font-size: 1.0625rem; line-height: 1.8; text-wrap: pretty; }
article p { margin: 1.05em 0; }
article blockquote { margin: 0.2rem 0 1.15rem; padding: 0.35rem 2.4rem 0.35rem 0.85rem; border-left: 3px solid var(--accent); border-radius: 0 8px 8px 0; background: #fbf8f3; }
article blockquote p { margin: 0.28em 0; }
article ul, article ol { margin: 0.85em 0; padding-left: 1.3rem; }
article li { margin: 0.4em 0; }
article h1 ~ h1 { font-size: 1.5rem; margin-top: 0.15rem; padding-top: 0; border-top: 0; }
hr { border: 0; height: 0; margin: 2.1rem 0 1.35rem; border-top: 1px solid var(--line); }
article h2 { margin: 1.9rem 0 0.45rem; font-size: 1.25rem; line-height: 1.4; color: inherit; }
article h1 + h2 { margin-top: 1.1rem; }
article h3 { margin: 1.35rem 0 0.3rem; font-size: 1.05rem; line-height: 1.45; }
a { color: var(--accent); }
code, pre { font-family: Consolas, "Cascadia Mono", monospace; }
:is(p, li, td, h1, h2, h3, blockquote) code {
  font-size: 0.92em;
  color: inherit;
  background: #f3eee6;
  padding: 0.04em 0.28em;
  border-radius: 4px;
  white-space: nowrap;
  overflow-wrap: normal;
  word-break: normal;
}
pre {
  background: var(--code);
  color: var(--code-ink);
  border: 1px solid #e6dfd2;
  padding: 0.8rem 1rem;
  overflow: auto;
  max-width: 100%;
  border-radius: 8px;
  line-height: 1.65;
  font-size: 0.98rem;
  margin: 0.85rem 0 1rem;
  -webkit-overflow-scrolling: touch;
  overscroll-behavior-x: contain;
}
pre code { background: transparent; color: inherit; padding: 0; font-size: inherit; }
.q {
  margin: 1.5rem 0 1.8rem;
  padding: 0.85rem 2.4rem 0.85rem 0.85rem;
  border: 1px solid var(--line);
  border-radius: 12px;
  background: #fffdf9;
}
.choices { display: flex; flex-direction: column; gap: 0.45rem; margin: 0.75rem 0 0.55rem; }
.choice { display: flex; align-items: flex-start; gap: 0.7rem; width: 100%; text-align: left; font: inherit; color: inherit; background: #fbf8f3; border: 1px solid var(--line); border-radius: 10px; padding: 0.55rem 0.75rem; cursor: pointer; line-height: 1.5; }
.choice:hover { border-color: #cfc4b4; }
.choice[aria-pressed="true"] { background: #eef4f3; border-color: #b7d0cc; }
.letter { flex: none; width: 1.65rem; height: 1.65rem; display: grid; place-items: center; border-radius: 999px; background: white; border: 1px solid var(--line); font-size: 0.8rem; font-weight: 650; }
.choice[aria-pressed="true"] .letter { background: var(--accent); color: white; border-color: var(--accent); }
.choice-body { min-width: 0; padding-top: 0.12rem; }
.choice-body code { background: transparent; padding: 0; color: inherit; }
.choice-body .snippet { display: block; white-space: pre-wrap; font-size: 0.92rem; line-height: 1.55; }
.reveal {
  display: inline-flex;
  flex-direction: row;
  flex-wrap: nowrap;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  width: fit-content;
  max-width: 100%;
  min-height: 2.45rem;
  margin: 0.35rem 0 1rem;
  padding: 0.45rem 1rem 0.45rem 0.8rem;
  border: 1px solid var(--line);
  background: white;
  color: var(--ink);
  border-radius: 999px;
  font: inherit;
  font-size: 0.9rem;
  font-weight: 650;
  line-height: 1.2;
  white-space: nowrap;
  cursor: pointer;
}
.reveal svg {
  flex: none;
  width: 1.1rem;
  height: 1.1rem;
  fill: none;
  stroke: currentColor;
  stroke-width: 1.8;
  stroke-linecap: round;
  stroke-linejoin: round;
}
.reveal .icon-hide { display: none; }
.reveal[aria-expanded="true"] {
  background: var(--accent-soft);
  border-color: #b7d0cc;
  color: var(--accent);
}
.reveal[aria-expanded="true"] .icon-show { display: none; }
.reveal[aria-expanded="true"] .icon-hide { display: inline; }
.reveal:hover, .reveal:focus-visible { background: var(--accent-soft); border-color: #b7d0cc; outline: none; }
.reveal-label { flex: none; white-space: nowrap; line-height: 1.2; }
.answer { margin-top: 0.55rem; margin-bottom: 0.35rem; padding: 0.75rem 0.9rem; background: #f6f3ec; border: 1px solid var(--line); border-radius: 10px; }
.answer > :first-child { margin-top: 0; }
.answer > :last-child { margin-bottom: 0; }
.q.shown .choice.right { background: #f3f7f6; border-color: #9bbfb8; }
.q.shown .choice.right .letter { background: var(--accent); color: white; border-color: var(--accent); }
.q.shown .choice.wrong { background: #f8f4f1; border-color: #e0d0c6; }
.q.shown .choice.wrong .letter,
.q.shown .choice.wrong[aria-pressed="true"] .letter { background: #f3e6de; color: #6b5348; border-color: #d9c2b6; }
.kept { margin: 0.35rem 0 1.2rem; }
.table-wrap { overflow-x: auto; max-width: 100%; margin: 1rem 0 1.2rem; border: 1px solid var(--line); border-radius: 8px; }
table { border-collapse: collapse; width: 100%; font-size: 0.95rem; line-height: 1.5; }
th, td { padding: 0.55rem 0.7rem; text-align: left; vertical-align: top; border-bottom: 1px solid var(--line); }
tr:last-child td { border-bottom: 0; }
th { background: #f6f1e8; font-weight: 650; }
tbody tr:nth-child(even) { background: #fbf8f3; }
article ul:has(> .task) {
  list-style: none;
  margin: 0.85em 0;
  padding: 0;
  max-width: 100%;
}
.task {
  list-style: none;
  margin: 0.45em 0;
  padding: 0.42rem 0.55rem 0.42rem 0.35rem;
  display: flex;
  align-items: flex-start;
  gap: 0.7rem;
  max-width: 100%;
  min-width: 0;
  box-sizing: border-box;
  border-radius: 10px;
  transition: background 0.18s ease;
}
.task-body {
  flex: 1;
  min-width: 0;
  overflow-wrap: break-word;
  word-break: normal;
}
.task:has(.box.on) { background: #f2f6f5; }
.task:has(.box.on) { color: #5c5854; }
.box {
  flex: none;
  width: 1.28rem;
  height: 1.28rem;
  margin: 0.18rem 0 0;
  padding: 0;
  display: inline-grid;
  place-items: center;
  border: 1.5px solid #cfc4b4;
  border-radius: 7px;
  background: white;
  color: white;
  cursor: pointer;
  transition: background 0.18s ease, border-color 0.18s ease, transform 0.18s ease, box-shadow 0.18s ease;
}
.box:hover, .box:focus-visible {
  border-color: var(--accent);
  background: var(--accent-soft);
  outline: none;
}
.box:focus-visible { box-shadow: 0 0 0 3px rgba(14, 74, 72, 0.16); }
.box.on {
  background: var(--accent);
  border-color: var(--accent);
  animation: tick-pop 0.28s ease;
}
.box.on:hover, .box.on:focus-visible { background: #0c3f3d; border-color: #0c3f3d; }
.box::after {
  content: "";
  width: 0.34rem;
  height: 0.62rem;
  border: solid currentColor;
  border-width: 0 2px 2px 0;
  transform: scale(0.4) rotate(45deg);
  opacity: 0;
  transition: transform 0.16s ease, opacity 0.16s ease;
}
.box.on::after {
  opacity: 1;
  transform: scale(1) rotate(45deg);
}
@keyframes tick-pop {
  0% { transform: scale(0.86); }
  55% { transform: scale(1.08); }
  100% { transform: scale(1); }
}
.toc {
  margin: 0 0 1.5rem;
  padding: 0.75rem 0.85rem 0.85rem;
  border: 1px solid var(--line);
  border-radius: var(--radius);
  background: #fbf8f3;
  box-shadow: var(--shadow);
}
.toc summary {
  cursor: pointer;
  list-style: none;
  font-weight: 700;
  font-size: 0.78rem;
  color: var(--muted);
  letter-spacing: 0.04em;
  padding: 0.05rem 0 0.55rem;
}
.toc summary::-webkit-details-marker { display: none; }
.toc summary::before {
  content: "";
  display: inline-block;
  width: 0.38rem;
  height: 0.38rem;
  margin-right: 0.45rem;
  border-right: 1.5px solid currentColor;
  border-bottom: 1.5px solid currentColor;
  transform: rotate(45deg) translate(-0.05rem, -0.05rem);
  vertical-align: 0.1rem;
}
.toc:not([open]) summary::before { transform: rotate(-45deg) translate(0.05rem, -0.05rem); }
.toc ul { list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 0.28rem; }
.toc li { margin: 0; line-height: 1.35; }
.toc .chapter > ul {
  margin: 0.28rem 0 0.15rem;
  padding: 0.15rem 0 0.15rem 0.55rem;
  border-left: 2px solid #e7dfd3;
  gap: 0.2rem;
}
.toc a {
  text-decoration: none;
  display: flex;
  flex-direction: column;
  gap: 0.12rem;
  padding: 0.55rem 0.65rem;
  border-radius: 11px;
  background: var(--paper);
  border: 1px solid transparent;
  color: var(--ink);
  transition: background 0.15s ease, border-color 0.15s ease, color 0.15s ease;
}
.toc a:hover, .toc a:focus {
  border-color: var(--accent-mid);
  background: var(--accent-soft);
  color: var(--accent);
}
.toc .chapter > a { font-weight: 700; }
.toc .section > a, .toc .topic > a { background: transparent; padding: 0.4rem 0.55rem; }
.toc .topic > a { color: var(--muted); font-weight: 550; }
.toc-kicker {
  display: inline-flex;
  align-self: flex-start;
  font-size: 0.68rem;
  font-weight: 750;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: var(--accent);
  background: var(--accent-soft);
  border-radius: 999px;
  padding: 0.12rem 0.45rem;
  line-height: 1.2;
}
.toc-rest { font-size: 0.92rem; font-weight: 650; line-height: 1.35; }
.toc .topic .toc-rest { font-size: 0.88rem; font-weight: 550; }
.jump {
  position: fixed;
  top: 4.5rem;
  right: 0.75rem;
  z-index: 5;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.55rem;
}
.jump-fab {
  order: 2;
  width: 3rem;
  height: 3rem;
  padding: 0;
  display: inline-grid;
  place-items: center;
  border: 1px solid var(--line);
  border-radius: 999px;
  background: var(--paper);
  color: var(--ink);
  cursor: pointer;
  box-shadow: var(--shadow);
  transition: background 0.15s ease, color 0.15s ease, border-color 0.15s ease, transform 0.15s ease;
}
.jump-fab svg { width: 1.25rem; height: 1.25rem; fill: none; stroke: currentColor; stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round; }
.jump-fab:hover, .jump-fab:focus-visible {
  background: var(--accent-soft);
  border-color: #b7d0cc;
  outline: none;
  transform: translateY(-1px);
}
.jump.open .jump-fab {
  background: var(--accent);
  color: white;
  border-color: var(--accent);
}
.jump-panel {
  order: 1;
  display: none;
  width: min(21rem, calc(100vw - 1.35rem));
  max-height: min(72dvh, calc(100vh - 8rem));
  overflow: auto;
  -webkit-overflow-scrolling: touch;
  background: rgba(255, 252, 247, 0.96);
  border: 1px solid var(--line);
  border-radius: 16px;
  padding: 0.7rem 0.7rem 0.75rem;
  box-shadow: 0 18px 40px rgba(36, 31, 28, 0.14);
  backdrop-filter: blur(10px);
}
.jump.open .jump-panel { display: block; }
.jump-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.35rem;
  margin: 0 0.15rem 0.55rem;
  padding-bottom: 0.45rem;
  border-bottom: 1px solid #efe7db;
}
.jump-head p {
  margin: 0;
  color: var(--muted);
  font-size: 0.7rem;
  font-weight: 750;
  letter-spacing: 0.06em;
  text-transform: uppercase;
}
.jump ul { list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 0.28rem; }
.jump li { margin: 0; line-height: 1.35; }
.jump .chapter > ul {
  margin: 0.28rem 0 0.2rem;
  padding: 0.1rem 0 0.1rem 0.45rem;
  border-left: 2px solid #e7dfd3;
  gap: 0.18rem;
}
.jump a {
  text-decoration: none;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 0.18rem;
  padding: 0.62rem 0.7rem;
  border-radius: 12px;
  border: 1px solid transparent;
  background: #f7f2ea;
  color: var(--ink);
  transition: background 0.15s ease, border-color 0.15s ease, color 0.15s ease, transform 0.15s ease;
}
.jump .chapter > a { font-weight: 700; }
.jump .section > a,
.jump .topic > a {
  background: transparent;
  padding: 0.45rem 0.55rem;
}
.jump .topic > a { color: var(--muted); }
.jump a:hover, .jump a:focus {
  background: var(--accent-soft);
  border-color: var(--accent-mid);
  color: var(--accent);
}
.jump a[aria-current="true"] {
  background: var(--accent-soft);
  border-color: var(--accent-mid);
  color: var(--accent);
  box-shadow: inset 3px 0 0 var(--accent);
}
.jump .toc-kicker {
  font-size: 0.64rem;
  padding: 0.1rem 0.42rem;
}
.jump .toc-rest { font-size: 0.84rem; font-weight: 650; }
.jump .topic .toc-rest { font-size: 0.78rem; font-weight: 550; }
.pager { display: flex; gap: 0.7rem; margin-top: 2rem; }
.pager a { flex: 1; display: flex; flex-direction: column; gap: 0.15rem; text-decoration: none; color: var(--ink); background: #fbf8f3; border: 1px solid var(--line); border-radius: 10px; padding: 0.7rem 0.85rem; font-weight: 650; }
.pager a.next { text-align: right; align-items: flex-end; margin-left: auto; }
.pager a:only-child { max-width: 50%; }
.pager small { color: var(--muted); font-size: 0.75rem; }
.pager a:hover, .pager a:focus { background: var(--accent-soft); }
.hero { max-width: none; }
.hero p { max-width: 46rem; }
.weeks { list-style: none; padding: 0; margin: 1.35rem 0 0; display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 16rem), 1fr)); gap: clamp(0.55rem, 1.2vw, 0.85rem); }
.weeks li {
  background: var(--paper);
  border: 1px solid var(--line);
  border-radius: var(--radius);
  padding: 1rem 1.05rem 1.05rem;
  display: flex;
  flex-direction: column;
  min-height: 8.2rem;
  box-shadow: var(--shadow);
  transition: border-color 0.18s ease, transform 0.18s ease;
}
.weeks li:hover { border-color: #b7d4cf; transform: translateY(-1px); }
.weeks h2 { margin: 0; font-size: 1.05rem; letter-spacing: -0.01em; font-weight: 750; }
.when { margin: 0.35rem 0 0; color: var(--muted); font-size: 0.86rem; line-height: 1.4; }
.go { margin: auto 0 0; padding-top: 0.85rem; display: flex; gap: 0.4rem; }
.weeks a { text-decoration: none; background: #f1ebe2; color: var(--ink); border-radius: 999px; padding: 0.28rem 0.78rem; font-size: 0.88rem; font-weight: 650; }
.weeks a:hover, .weeks a:focus { background: var(--accent); color: white; }
@media (max-width: 1100px) {
  :root { --side: 13.5rem; }
  .pair .links { padding: 0 0.15rem 0.1rem; }
}
@media (max-width: 860px) {
  html.nav-collapsed .place:not([hidden]),
  html.nav-collapsed .week-progress:not([hidden]) { display: block; }
  body { overflow-x: hidden; }
  .layout {
    display: block;
    width: 100%;
    max-width: 100%;
    overflow-x: hidden;
  }
  .side {
    position: sticky;
    top: 0;
    width: 100%;
    max-width: 100%;
    height: auto;
    max-height: none;
    z-index: 20;
    border-right: 0;
    border-bottom: 1px solid var(--line);
    padding: 0.7rem max(0.75rem, env(safe-area-inset-right)) 0.7rem max(0.75rem, env(safe-area-inset-left));
    overflow: visible;
    box-sizing: border-box;
  }
  html.nav-collapsed .side {
    width: 100%;
    max-width: 100%;
    height: auto;
    padding: 0.7rem max(0.75rem, env(safe-area-inset-right)) 0.7rem max(0.75rem, env(safe-area-inset-left));
    overflow: visible;
    display: block;
  }
  html.nav-collapsed .brand { display: inline-flex; }
  html.nav-collapsed .fold { background: white; color: var(--ink); border-color: var(--line); }
  html.nav-collapsed #nav { display: none; }
  .fold { width: 2.5rem; height: 2.5rem; }
  #nav {
    display: none;
    max-height: min(70dvh, calc(100dvh - 5rem));
    overflow: auto;
    -webkit-overflow-scrolling: touch;
    overscroll-behavior: contain;
    padding-bottom: 0.6rem;
    margin-top: 0.35rem;
  }
  #nav.open { display: block; }
  .pair {
    margin-top: 0.5rem;
    padding: 0.65rem 0.7rem 0.7rem;
    border-radius: 14px;
  }
  .pair h2 { font-size: 0.98rem; }
  .pair .links { gap: 0.35rem; }
  .pair .links a {
    min-height: 2.15rem;
    padding: 0.4rem 0.75rem;
    display: inline-flex;
    align-items: center;
    font-size: 0.8rem;
  }
  .week-done { width: 2.2rem; height: 2.2rem; }
  .week-done svg { width: 1.05rem; height: 1.05rem; }
  .side .links a { padding: 0.55rem 0.55rem; min-height: 2.4rem; }
  main {
    width: 100%;
    max-width: 100%;
    min-width: 0;
    padding: 0.9rem max(0.75rem, env(safe-area-inset-right)) calc(4.25rem + env(safe-area-inset-bottom)) max(0.75rem, env(safe-area-inset-left));
    box-sizing: border-box;
  }
  .sheet {
    width: 100%;
    max-width: 100%;
    min-width: 0;
    padding: 1rem 0.85rem 1.2rem;
    border-radius: 12px;
    overflow-x: hidden;
  }
  .weeks { grid-template-columns: 1fr; }
  .hero h1, article h1 { font-size: 1.45rem; }
  article { font-size: 1.05rem; max-width: 100%; min-width: 0; }
  :is(p, li, td, h1, h2, h3, blockquote, .task-body) code {
    white-space: normal;
    overflow-wrap: anywhere;
    word-break: break-word;
  }
  .mark { width: 2.05rem; height: 2.05rem; }
  article :is(h1, h2, h3) .mark { opacity: 1; }
  article .q,
  article > blockquote { padding-right: 2.7rem; max-width: 100%; box-sizing: border-box; }
  .table-wrap {
    margin: 1rem 0 1.2rem;
    width: 100%;
    max-width: 100%;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
  }
  table { font-size: 0.88rem; }
  th, td { padding: 0.45rem 0.55rem; }
  .reveal {
    min-height: 2.7rem;
    padding: 0.55rem 1.1rem 0.55rem 0.9rem;
    font-size: 0.95rem;
    margin-bottom: 1.15rem;
  }
  .choice { padding: 0.7rem 0.8rem; }
  .pager { flex-direction: column; }
  .pager a:only-child { max-width: none; }
  .pager a.next { text-align: left; align-items: flex-start; margin-left: 0; }
  pre {
    font-size: 0.86rem;
    padding: 0.7rem 0.75rem;
    max-width: 100%;
  }
  .jump {
    top: auto;
    right: max(0.75rem, env(safe-area-inset-right));
    bottom: max(0.85rem, calc(0.75rem + env(safe-area-inset-bottom)));
  }
  .jump-fab { width: 3rem; height: 3rem; }
  .jump-panel {
    width: min(20rem, calc(100vw - 1.5rem - env(safe-area-inset-left) - env(safe-area-inset-right)));
    max-height: min(70dvh, calc(100dvh - 7rem));
  }
}
"""

SEARCH_JS = r"""
const input = document.querySelector("#q");
const box = document.querySelector("#results");
const fold = document.querySelector(".fold");
const nav = document.querySelector("#nav");
const wide = () => matchMedia("(min-width: 861px)").matches;
const esc = (s) => s.replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

function paintFold() {
  if (!fold) return;
  if (wide()) {
    const closed = document.documentElement.classList.contains("nav-collapsed");
    fold.setAttribute("aria-label", closed ? "目錄" : "收起目錄");
    fold.setAttribute("aria-expanded", closed ? "false" : "true");
  } else {
    const open = nav && nav.classList.contains("open");
    fold.setAttribute("aria-label", open ? "收起目錄" : "目錄");
    fold.setAttribute("aria-expanded", open ? "true" : "false");
  }
}

if (fold && nav) {
  paintFold();
  fold.addEventListener("click", () => {
    if (wide()) {
      const closed = document.documentElement.classList.toggle("nav-collapsed");
      try { localStorage.setItem("ocp-nav", closed ? "0" : "1"); } catch (error) {}
    } else {
      nav.classList.toggle("open");
      if (nav.classList.contains("open")) setJumpOpen(false);
    }
    paintFold();
  });
  nav.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => {
      if (!wide() && nav.classList.contains("open")) {
        nav.classList.remove("open");
        paintFold();
      }
    });
  });
  matchMedia("(min-width: 861px)").addEventListener("change", () => {
    if (wide()) nav.classList.remove("open");
    paintFold();
  });
}

const side = document.querySelector(".side");
const here = side && !document.documentElement.classList.contains("nav-collapsed") && side.querySelector("[aria-current='page']");
if (side && here) {
  const frame = side.getBoundingClientRect();
  const item = here.getBoundingClientRect();
  if (item.top < frame.top || item.bottom > frame.bottom) {
    side.scrollTop += item.top - frame.top - side.clientHeight / 3;
  }
}

function snippet(hay, q) {
  const lower = hay.toLowerCase();
  const at = lower.indexOf(q);
  if (at < 0) return esc(hay.slice(0, 80));
  let start = Math.max(0, at - 28);
  const space = hay.lastIndexOf(" ", start + 16);
  if (space >= 0 && space < at) start = space + 1;
  let end = Math.min(hay.length, at + q.length + 46);
  const endSpace = hay.indexOf(" ", end);
  if (endSpace !== -1 && endSpace < end + 14) end = endSpace;
  const lead = start > 0 ? "…" : "";
  const tail = end < hay.length ? "…" : "";
  return lead + esc(hay.slice(start, at)) + "<mark>" + esc(hay.slice(at, at + q.length)) + "</mark>" + esc(hay.slice(at + q.length, end)) + tail;
}

if (input && box && window.SEARCH) {
  const show = () => {
    const q = input.value.trim().toLowerCase();
    if (q.length < 2) {
      box.hidden = true;
      box.innerHTML = "";
      return;
    }
    const hits = window.SEARCH.filter((page) => page.title.toLowerCase().includes(q) || page.hay.toLowerCase().includes(q)).slice(0, 8);
    box.hidden = false;
    box.innerHTML = hits.length
      ? hits.map((page) => `<a href="${page.href}"><strong>${esc(page.title)}</strong><small>${snippet(page.hay, q)}</small></a>`).join("")
      : '<p class="empty">沒有相符的筆記</p>';
  };
  input.addEventListener("input", show);
  input.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      input.value = "";
      box.hidden = true;
      box.innerHTML = "";
    }
  });
}

try {
  document.querySelectorAll("li.task .box").forEach((button) => {
    const line = button.closest("li").textContent.trim().slice(0, 96);
    const key = "ocp-check:" + location.pathname + ":" + line;
    const saved = localStorage.getItem(key);
    if (saved === "1") {
      button.classList.add("on");
      button.setAttribute("aria-pressed", "true");
    } else if (saved === "0") {
      button.classList.remove("on");
      button.setAttribute("aria-pressed", "false");
    }
    button.addEventListener("click", () => {
      const on = button.classList.toggle("on");
      button.setAttribute("aria-pressed", on ? "true" : "false");
      localStorage.setItem(key, on ? "1" : "0");
    });
  });
} catch (error) {}

try {
  document.querySelectorAll(".pair[data-week]").forEach((section) => {
    const week = section.dataset.week;
    const key = "ocp-week-done:" + week;
    const button = section.querySelector(".week-done");
    if (!button) return;
    const paint = (on) => {
      section.classList.toggle("done", on);
      button.setAttribute("aria-pressed", on ? "true" : "false");
      button.title = on ? "取消完成本週" : "完成本週";
      button.setAttribute("aria-label", on ? "取消" + week + "完成" : "標記" + week + "完成");
    };
    paint(localStorage.getItem(key) === "1");
    button.addEventListener("click", () => {
      const on = button.getAttribute("aria-pressed") !== "true";
      localStorage.setItem(key, on ? "1" : "0");
      paint(on);
    });
  });
} catch (error) {}

const PLACE_KEY = "ocp-place";
const PLACES_KEY = "ocp-places";
const placeBox = document.querySelector("#place");
const placeHome = document.querySelector("#place-home");

function readPlaces() {
  try {
    const multi = localStorage.getItem(PLACES_KEY);
    if (multi) {
      const list = JSON.parse(multi);
      return Array.isArray(list) ? list.filter((item) => item && item.href) : [];
    }
    const legacy = localStorage.getItem(PLACE_KEY);
    if (!legacy) return [];
    const one = JSON.parse(legacy);
    return one && one.href ? [one] : [];
  } catch (error) {
    return [];
  }
}

function writePlaces(list) {
  localStorage.setItem(PLACES_KEY, JSON.stringify(list));
  localStorage.removeItem(PLACE_KEY);
}

function fileName() {
  return decodeURIComponent(location.pathname.split("/").pop() || "index.html");
}

function cleanText(node) {
  const copy = node.cloneNode(true);
  copy.querySelectorAll("button, .mark").forEach((button) => button.remove());
  return copy.textContent.replace(/\s+/g, " ").trim();
}

function headingText(heading) {
  return cleanText(heading);
}

function ensureId(el, base) {
  if (el.id) return el.id;
  let id = base.replace(/[^a-zA-Z0-9\u4e00-\u9fff\-]+/g, "-").replace(/-+/g, "-").replace(/^-|-$/g, "") || "spot";
  let n = 2;
  let candidate = id;
  while (document.getElementById(candidate)) {
    candidate = id + "-" + n;
    n += 1;
  }
  el.id = candidate;
  return candidate;
}

function headsBefore(el) {
  return [...document.querySelectorAll("article :is(h1, h2, h3)[id]")].filter(
    (heading) => heading === el || !!(heading.compareDocumentPosition(el) & Node.DOCUMENT_POSITION_FOLLOWING)
  );
}

function placePath(el) {
  const before = headsBefore(el).filter((heading) => heading !== el);
  let chapter = "";
  let section = "";
  let topic = "";
  for (let i = before.length - 1; i >= 0; i--) {
    const heading = before[i];
    if (!topic && heading.matches("h3")) topic = headingText(heading);
    if (!section && heading.matches("h2")) section = headingText(heading);
    if (!chapter && heading.matches("h1")) {
      chapter = headingText(heading);
      break;
    }
  }
  if (el.matches("h1")) return "";
  if (el.matches("h2")) return chapter;
  if (el.matches("h3")) return [chapter, section].filter(Boolean).join(" · ");
  return [chapter, section, topic].filter(Boolean).join(" · ");
}

function targetLabel(el) {
  if (el.matches("h1, h2, h3")) return headingText(el);
  if (el.matches(".q")) {
    const line = el.querySelector(":scope > p")?.textContent || el.dataset.qid || "題目";
    return line.replace(/\s+/g, " ").trim().slice(0, 72);
  }
  if (el.matches("blockquote")) {
    const line = cleanText(el);
    if (line.startsWith("必睇")) return "書 · 必睇";
    if (line.startsWith("略讀")) return "書 · 略讀";
    if (line.startsWith("唔使睇")) return "書 · 唔使睇";
    return "書備註";
  }
  return el.id;
}

function targetSnippet(el) {
  if (el.matches(".q")) {
    const pre = el.querySelector(":scope > pre");
    if (pre) return pre.textContent.replace(/\s+/g, " ").trim().slice(0, 88);
    const p = el.querySelector(":scope > p");
    return (p?.textContent || "").replace(/\s+/g, " ").trim().slice(0, 88);
  }
  if (el.matches("blockquote")) return cleanText(el).slice(0, 88);
  let next = el.nextElementSibling;
  while (next && next.matches("button, .mark")) next = next.nextElementSibling;
  if (!next || next.matches("h1, h2, h3, .q")) return "";
  return next.textContent.replace(/\s+/g, " ").trim().slice(0, 88);
}

function placeItemHtml(item) {
  return `<li class="place-item" data-href="${esc(item.href)}">
    <a href="${esc(item.href)}" title="${esc(item.heading)}">${esc(item.heading)}</a>
    <button type="button" class="place-item-clear" aria-label="移除收藏" title="移除">
      <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>
    </button>
  </li>`;
}

function paintPlace() {
  const list = readPlaces();
  [placeBox, placeHome].forEach((box) => {
    if (!box) return;
    if (!list.length) {
      box.hidden = true;
      box.innerHTML = "";
      return;
    }
    box.hidden = false;
    const clearAll = list.length > 1
      ? `<button type="button" class="place-clear" aria-label="清除全部收藏" title="清除全部"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg></button>`
      : "";
    box.innerHTML = `<div class="place-head"><p>收藏 ${list.length}</p>${clearAll}</div><ul class="place-list">${list.map(placeItemHtml).join("")}</ul>`;
    box.querySelector(".place-clear")?.addEventListener("click", () => {
      writePlaces([]);
      paintPlace();
    });
    box.querySelectorAll(".place-item-clear").forEach((button) => {
      button.addEventListener("click", () => {
        const href = button.closest(".place-item")?.dataset.href;
        writePlaces(readPlaces().filter((item) => item.href !== href));
        paintPlace();
      });
    });
  });
  paintMarks();
}

function markHost(button) {
  return button.closest("h1, h2, h3, .q, blockquote");
}

function paintMarks() {
  const hrefs = new Set(readPlaces().map((item) => item.href));
  document.querySelectorAll("article .mark").forEach((button) => {
    const host = markHost(button);
    if (!host || !host.id) return;
    const on = hrefs.has(fileName() + "#" + host.id);
    host.classList.toggle("reached", on);
    button.setAttribute("aria-label", on ? "已收藏，再撳取消" : "收藏");
    button.setAttribute("aria-pressed", on ? "true" : "false");
    button.title = on ? "已收藏 · 再撳取消" : "收藏";
  });
}

function isMarked(el) {
  if (!el?.id) return false;
  const href = fileName() + "#" + el.id;
  return readPlaces().some((item) => item.href === href);
}

function saveMark(el) {
  if (!el?.id) return;
  const href = fileName() + "#" + el.id;
  const list = readPlaces().filter((item) => item.href !== href);
  const where = document.querySelector(".crumb")?.textContent?.trim() || document.title.replace(/ · OCP Java 21$/, "");
  list.unshift({
    href,
    heading: targetLabel(el),
    path: placePath(el),
    snippet: targetSnippet(el),
    where
  });
  writePlaces(list);
  paintPlace();
}

function clearMark(el) {
  if (!el?.id) return;
  const href = fileName() + "#" + el.id;
  const list = readPlaces();
  const next = list.filter((item) => item.href !== href);
  if (next.length === list.length) return;
  writePlaces(next);
  paintPlace();
}

function toggleMark(el) {
  if (isMarked(el)) clearMark(el);
  else saveMark(el);
}

function attachMark(el) {
  if (!el || el.querySelector(":scope > .mark")) return;
  const button = document.createElement("button");
  button.type = "button";
  button.className = "mark";
  button.setAttribute("aria-label", "收藏");
  button.title = "收藏";
  button.innerHTML = '<svg class="icon-off" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 4h10v16l-5-3-5 3z"/></svg><svg class="icon-on" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 4h10v16l-5-3-5 3z"/></svg>';
  button.addEventListener("click", () => toggleMark(el));
  el.appendChild(button);
}

const markTargets = [
  ...document.querySelectorAll("article :is(h1, h2, h3)[id]"),
  ...document.querySelectorAll("article section.q[id]")
];
document.querySelectorAll("article > blockquote").forEach((quote, index) => {
  const prev = quote.previousElementSibling;
  const base = prev?.id ? prev.id + "-note" : "note-" + (index + 1);
  ensureId(quote, base);
  markTargets.push(quote);
});
markTargets.forEach(attachMark);

paintPlace();

function chapterSpots(week) {
  const flat = [];
  week.chapters.forEach((chapter, index) => {
    flat.push({ id: chapter.id, chapter: index, title: chapter.title, kind: chapter.kind });
    chapter.parts.forEach((id) => flat.push({ id, chapter: index, title: chapter.title, kind: chapter.kind }));
  });
  return flat;
}

function scrollSpotIndex(flat) {
  if (!flat.length) return -1;
  const doc = document.documentElement;
  if (window.scrollY + window.innerHeight >= doc.scrollHeight - 12) return flat.length - 1;
  const line = Math.min(160, window.innerHeight * 0.28);
  let at = -1;
  for (let i = 0; i < flat.length; i++) {
    const el = document.getElementById(flat[i].id);
    if (!el) continue;
    if (el.getBoundingClientRect().top <= line) at = i;
  }
  return at;
}

let progressKey = "";

function paintProgress() {
  const box = document.querySelector("#week-progress");
  const weeks = window.OUTLINE || [];
  if (!box) return;
  const week = weeks.find((item) => item.file === fileName());
  if (!week || !week.chapters.length) {
    progressKey = "";
    box.hidden = true;
    box.innerHTML = "";
    return;
  }
  const flat = chapterSpots(week);
  const at = scrollSpotIndex(flat);
  const chapterTotal = week.chapters.filter((chapter) => chapter.kind === "chapter").length;
  const pct = at < 0 ? 0 : Math.round(((at + 1) / flat.length) * 100);
  const spot = at < 0 ? null : flat[at];
  let where = "";
  let status = "一共 " + chapterTotal + " 章";
  if (spot) {
    const later = week.chapters.filter((chapter, index) => chapter.kind === "chapter" && index > spot.chapter).length;
    where = spot.title;
    if (pct === 100) {
      where = "";
      status = "呢週溫完";
    } else if (spot.kind !== "chapter" && later === 0) status = "章節溫完";
    else if (later === 0) status = "最後一章";
    else status = "仲有 " + later + " 章";
  }
  const key = week.file + "|" + at + "|" + pct + "|" + where + "|" + status;
  if (key === progressKey && !box.hidden) return;
  progressKey = key;
  const whereHtml = where ? `<span class="where">${esc(where)}</span>` : "";
  box.hidden = false;
  box.innerHTML = `<p><span>${esc(week.week)}</span><span class="pct">${pct}%</span></p><div class="track" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="${pct}" aria-label="${esc(week.week)}進度"><span></span></div><small>${whereHtml}${esc(status)}</small>`;
  box.querySelector(".track span").style.width = pct + "%";
}

let progressTick = 0;
function queueProgress() {
  if (progressTick) return;
  progressTick = requestAnimationFrame(() => {
    progressTick = 0;
    paintProgress();
    paintJump();
  });
}

const pageToc = document.querySelector("#page-toc");
const jump = document.querySelector("#jump");

function setJumpOpen(open) {
  if (!jump) return;
  jump.classList.toggle("open", open);
  const fab = jump.querySelector(".jump-fab");
  if (fab) fab.setAttribute("aria-expanded", open ? "true" : "false");
  if (open) paintJump();
}

function paintJump() {
  if (!jump || jump.hidden || !jump.classList.contains("open")) return;
  const links = [...jump.querySelectorAll('.jump-panel a[href^="#"]')];
  if (!links.length) return;
  const line = Math.min(160, window.innerHeight * 0.28);
  let current = "";
  links.forEach((link) => {
    const el = document.getElementById(decodeURIComponent(link.getAttribute("href").slice(1)));
    if (el && el.getBoundingClientRect().top <= line) current = link.getAttribute("href");
  });
  links.forEach((link) => {
    const on = link.getAttribute("href") === current;
    if (on) link.setAttribute("aria-current", "true");
    else link.removeAttribute("aria-current");
  });
}

if (pageToc && jump) {
  const list = pageToc.querySelector(".toc-list");
  if (list) {
    jump.innerHTML = `
<div class="jump-panel">
  <div class="jump-head"><p>本頁章節</p></div>
  ${list.outerHTML}
</div>
<button type="button" class="jump-fab" aria-expanded="false" aria-controls="jump-panel" aria-label="本頁章節" title="本頁章節">
  <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01"/></svg>
</button>`;
    const panel = jump.querySelector(".jump-panel");
    panel.id = "jump-panel";
    const fab = jump.querySelector(".jump-fab");
    fab.addEventListener("click", () => setJumpOpen(!jump.classList.contains("open")));
    jump.querySelectorAll('.jump-panel a[href^="#"]').forEach((link) => {
      link.addEventListener("click", () => setJumpOpen(false));
    });
    document.addEventListener("click", (event) => {
      if (jump.hidden || !jump.classList.contains("open")) return;
      if (!jump.contains(event.target)) setJumpOpen(false);
    });
    const watch = new IntersectionObserver(([entry]) => {
      jump.hidden = entry.isIntersecting;
      if (entry.isIntersecting) setJumpOpen(false);
      else paintJump();
    }, { threshold: 0, rootMargin: "0px 0px -40% 0px" });
    watch.observe(pageToc);
  }
}

window.addEventListener("scroll", queueProgress, { passive: true });
window.addEventListener("resize", queueProgress);
paintProgress();

function questionStore(host) {
  return "ocp-q:" + location.pathname + ":" + host.dataset.qid;
}

function grade(q) {
  const key = (q.dataset.key || "").split(",").filter(Boolean);
  const shown = q.classList.contains("shown");
  q.querySelectorAll(".choice").forEach((button) => {
    const picked = button.getAttribute("aria-pressed") === "true";
    const correct = key.includes(button.dataset.letter);
    button.classList.toggle("right", shown && correct);
    button.classList.toggle("wrong", shown && picked && !correct);
  });
}

function saveQuestion(host) {
  if (!host || !host.dataset.qid) return;
  const picks = [...host.querySelectorAll('.choice[aria-pressed="true"]')].map((button) => button.dataset.letter);
  const open = host.classList.contains("shown") || !!host.querySelector(".answer:not([hidden])");
  try { localStorage.setItem(questionStore(host), JSON.stringify({ picks, open })); } catch (error) {}
}

function paintReveal(button, open) {
  const label = open ? "收起答案" : "揭曉答案";
  button.setAttribute("aria-label", label);
  button.setAttribute("aria-expanded", open ? "true" : "false");
  button.title = label;
  const text = button.querySelector(".reveal-label");
  if (text) text.textContent = label;
}

document.querySelectorAll(".q").forEach((q) => {
  let saved = null;
  try { saved = JSON.parse(localStorage.getItem(questionStore(q)) || "null"); } catch (error) {}
  q.querySelectorAll(".choice").forEach((button) => {
    if (saved && saved.picks && saved.picks.includes(button.dataset.letter)) {
      button.setAttribute("aria-pressed", "true");
    }
    button.addEventListener("click", () => {
      const on = button.getAttribute("aria-pressed") === "true";
      if (q.dataset.multi !== "1") {
        q.querySelectorAll(".choice").forEach((other) => {
          if (other !== button) other.setAttribute("aria-pressed", "false");
        });
      }
      button.setAttribute("aria-pressed", on ? "false" : "true");
      grade(q);
      saveQuestion(q);
    });
  });
  if (saved && saved.open) {
    q.classList.add("shown");
    const panel = q.querySelector(".answer");
    if (panel) panel.hidden = false;
  }
  grade(q);
});

document.querySelectorAll(".reveal").forEach((button) => {
  const host = button.closest(".q, .kept");
  const panel = host ? host.querySelector(".answer") : null;
  if (!panel) return;
  const open = !panel.hidden;
  paintReveal(button, open);
  button.addEventListener("click", () => {
    const show = panel.hidden;
    panel.hidden = !show;
    if (host && host.classList.contains("q")) host.classList.toggle("shown", show);
    paintReveal(button, show);
    if (host && host.classList.contains("q")) grade(host);
    saveQuestion(host);
  });
});

document.querySelectorAll(".kept").forEach((host) => {
  let saved = null;
  try { saved = JSON.parse(localStorage.getItem(questionStore(host)) || "null"); } catch (error) {}
  if (!saved || !saved.open) return;
  const panel = host.querySelector(".answer");
  const button = host.querySelector(".reveal");
  if (panel) panel.hidden = false;
  if (button) paintReveal(button, true);
});
"""


FAVICON = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
  <rect width="32" height="32" rx="7" fill="#0e4a48"/>
  <path fill="#fffdf8" d="M9 8h9l6 6v10.2c0 .9-.7 1.6-1.6 1.6H9.6C8.7 25.8 8 25.1 8 24.2V9.6C8 8.7 8.7 8 9.6 8H9z"/>
  <path fill="#d5e6e2" d="M18 8v6h6z"/>
  <path fill="none" stroke="#0e4a48" stroke-width="1.4" stroke-linecap="round" d="M11.2 17.2h8.4M11.2 20.4h5.4"/>
</svg>
"""


def notes_outline(body):
    chapters = []
    current = None
    seen_h1 = 0
    for match in re.finditer(r"<h([123]) id=\"([^\"]+)\">(.*?)</h\1>", body, flags=re.S):
        level, anchor, raw = match.group(1), match.group(2), match.group(3)
        title = plain_text(raw)
        if level == "1":
            seen_h1 += 1
            if seen_h1 == 1:
                current = None
                continue
            current = {
                "id": anchor,
                "title": title,
                "kind": "chapter" if title.startswith("Chapter") else "extra",
                "parts": [],
            }
            chapters.append(current)
        elif current is not None and title and not toc_skip_title(title):
            current["parts"].append(anchor)
    return chapters


def main():
    global ASSET_V
    ASSET_V = hashlib.sha1((CSS + SEARCH_JS).encode("utf-8")).hexdigest()[:10]
    OUT.mkdir(exist_ok=True)
    (OUT / "favicon.svg").write_text(FAVICON, encoding="utf-8")
    (OUT / ".nojekyll").write_text("", encoding="utf-8")
    (OUT / "style.css").write_text(CSS, encoding="utf-8")
    index = []
    outline = []
    for dest, label, src in FLAT:
        text = (ROOT / src).read_text(encoding="utf-8")
        body = render_markdown(text)
        title = title_of(body, label)
        lang = "zh-Hant" if dest == "strategy.html" else "en"
        (OUT / dest).write_text(shell(dest, title, body, lang), encoding="utf-8")
        visible = re.sub(r'<div class="answer" hidden>.*?</div>', " ", body, flags=re.S)
        index.append({
            "href": dest,
            "title": title,
            "hay": plain_text(visible),
        })
        print(dest, title)
        if dest.endswith("-notes.html"):
            week = place_name(dest).split(" · ")[0]
            if week.startswith("第"):
                outline.append({
                    "week": week,
                    "file": dest,
                    "glossary": dest.replace("-notes.html", "-glossary.html"),
                    "chapters": notes_outline(body),
                })
    import json
    data = json.dumps(
        [{"href": item["href"], "title": item["title"], "hay": item["hay"]} for item in index],
        ensure_ascii=False,
    )
    outline_data = json.dumps(outline, ensure_ascii=False)
    (OUT / "search.js").write_text(
        "window.SEARCH = " + data + ";\nwindow.OUTLINE = " + outline_data + ";\n" + SEARCH_JS,
        encoding="utf-8",
    )
    (OUT / "index.html").write_text(home(), encoding="utf-8")
    print("pages", len(FLAT) + 1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Render DENSITY-CHAIN.md to a self-contained, theme-aware DENSITY-CHAIN.html.

The markdown is ground truth; this script only re-presents it. No external
requests: all CSS is inline, the banner is inline SVG, there is no JS beyond a
tiny theme toggle and a scroll-spy for the table of contents.
"""
import html
import os
import re
import sys

SRC = sys.argv[1]
DEST = sys.argv[2]


def esc(s):
    return html.escape(s, quote=False)


def inline(t):
    """Inline markdown: code, bold, italic, links.

    Inline code is swapped for an opaque placeholder *before* the other rules
    run, so constructs that wrap code — **`Bold`** or [`link`](url) — still
    match. Splitting on code instead would cut those in half.
    """
    stash = []

    def keep(m):
        stash.append('<code>%s</code>' % esc(m.group(1)))
        return '\x00%d\x00' % (len(stash) - 1)

    s = re.sub(r'`([^`]+)`', keep, t)
    s = esc(s)
    s = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', s)
    s = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'(?<![*\w])\*([^*\n]+)\*(?!\*)', r'<em>\1</em>', s)
    return re.sub(r'\x00(\d+)\x00', lambda m: stash[int(m.group(1))], s)


def slug(text):
    s = re.sub(r'<[^>]+>', '', text)
    s = re.sub(r'[^\w\s-]', '', s).strip().lower()
    return re.sub(r'[\s_]+', '-', s)


def render(md):
    lines = md.split('\n')
    out = []
    toc = []
    i = 0
    n = len(lines)
    in_code = False
    code_buf = []

    def close_list(stack):
        while stack:
            out.append('</%s>' % stack.pop())

    list_stack = []

    while i < n:
        line = lines[i]

        # fenced code
        if line.startswith('```'):
            if not in_code:
                in_code = True
                code_buf = []
            else:
                in_code = False
                out.append('<pre><code>%s</code></pre>' %
                           esc('\n'.join(code_buf)))
            i += 1
            continue
        if in_code:
            code_buf.append(line)
            i += 1
            continue

        # anchor passthrough
        m = re.match(r'^<a id="([^"]+)"></a>\s*$', line)
        if m:
            close_list(list_stack)
            out.append(line)
            i += 1
            continue

        # table
        if line.strip().startswith('|') and i + 1 < n and re.match(
                r'^\s*\|[\s:|-]+\|\s*$', lines[i + 1]):
            close_list(list_stack)
            header = [c.strip() for c in line.strip().strip('|').split('|')]
            i += 2
            rows = []
            while i < n and lines[i].strip().startswith('|'):
                rows.append([c.strip()
                             for c in lines[i].strip().strip('|').split('|')])
                i += 1
            t = ['<div class="tw"><table><thead><tr>']
            t += ['<th>%s</th>' % inline(c) for c in header]
            t.append('</tr></thead><tbody>')
            for r in rows:
                t.append('<tr>' + ''.join('<td>%s</td>' % inline(c)
                                          for c in r) + '</tr>')
            t.append('</tbody></table></div>')
            out.append(''.join(t))
            continue

        # heading
        m = re.match(r'^(#{1,6})\s+(.*)$', line)
        if m:
            close_list(list_stack)
            lvl = len(m.group(1))
            txt = inline(m.group(2))
            sid = slug(m.group(2))
            out.append('<h%d id="%s">%s</h%d>' % (lvl, sid, txt, lvl))
            if lvl in (2, 3):
                toc.append((lvl, sid, re.sub(r'<[^>]+>', '', txt)))
            i += 1
            continue

        # hr
        if re.match(r'^---+\s*$', line):
            close_list(list_stack)
            out.append('<hr>')
            i += 1
            continue

        # blockquote (supports > [!NOTE] style)
        if line.startswith('>'):
            close_list(list_stack)
            buf = []
            while i < n and lines[i].startswith('>'):
                buf.append(lines[i].lstrip('>').strip())
                i += 1
            body = ' '.join(x for x in buf if x)
            cls = 'note'
            body = re.sub(r'^\[!\w+\]\s*', '', body)
            out.append('<blockquote class="%s">%s</blockquote>' %
                       (cls, inline(body)))
            continue

        # list item
        m = re.match(r'^(\s*)([-*]|\d+\.)\s+(.*)$', line)
        if m:
            indent = len(m.group(1))
            tag = 'ul' if m.group(2) in ('-', '*') else 'ol'
            depth = indent // 2
            while len(list_stack) > depth + 1:
                out.append('</%s>' % list_stack.pop())
            if len(list_stack) < depth + 1:
                out.append('<%s>' % tag)
                list_stack.append(tag)
            out.append('<li>%s</li>' % inline(m.group(3)))
            i += 1
            continue

        if not line.strip():
            close_list(list_stack)
            i += 1
            continue

        # paragraph
        close_list(list_stack)
        buf = [line]
        i += 1
        while i < n and lines[i].strip() and not re.match(
                r'^(#{1,6}\s|\s*[-*]\s|\s*\d+\.\s|>|```|\||---+\s*$|<a id=)',
                lines[i]):
            buf.append(lines[i])
            i += 1
        out.append('<p>%s</p>' % inline(' '.join(buf)))

    close_list(list_stack)
    return '\n'.join(out), toc


BANNER = open(os.path.join(os.path.dirname(SRC), '..', '..', 'assets',
                           'banner.svg'), encoding='utf-8').read()

CSS = """
:root{
  --bg:#ffffff; --fg:#1f2328; --muted:#59636e; --line:#d1d9e0; --soft:#f6f8fa;
  --acc1:#58a6ff; --acc2:#9b8cf7; --acc3:#ef6fd0; --code:#f6f8fa; --link:#0969da;
}
@media (prefers-color-scheme:dark){
  :root{ --bg:#0d1117; --fg:#e6edf3; --muted:#9198a1; --line:#3d444d; --soft:#151b23;
         --code:#151b23; --link:#4493f8; }
}
:root[data-theme="dark"]{ --bg:#0d1117; --fg:#e6edf3; --muted:#9198a1; --line:#3d444d;
  --soft:#151b23; --code:#151b23; --link:#4493f8; }
:root[data-theme="light"]{ --bg:#ffffff; --fg:#1f2328; --muted:#59636e; --line:#d1d9e0;
  --soft:#f6f8fa; --code:#f6f8fa; --link:#0969da; }

*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);
  font:16px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Helvetica,Arial,sans-serif;
  -webkit-text-size-adjust:100%}
.wrap{max-width:1140px;margin:0 auto;padding:0 20px 100px}
header.hero{padding:26px 0 6px}
header.hero svg{width:100%;height:auto;display:block}

.bar{position:sticky;top:0;z-index:20;background:color-mix(in srgb,var(--bg) 88%,transparent);
  backdrop-filter:blur(8px);border-bottom:1px solid var(--line);margin-bottom:26px}
.bar .in{max-width:1140px;margin:0 auto;padding:9px 20px;display:flex;gap:14px;
  align-items:center;justify-content:space-between}
.bar b{font:600 13px ui-monospace,Menlo,Consolas,monospace;letter-spacing:.02em}
.bar b span{background:linear-gradient(90deg,var(--acc1),var(--acc2),var(--acc3));
  -webkit-background-clip:text;background-clip:text;color:transparent}
button.t{cursor:pointer;border:1px solid var(--line);background:var(--soft);color:var(--muted);
  border-radius:7px;padding:5px 11px;font:12px ui-monospace,Menlo,Consolas,monospace}
button.t:hover{color:var(--fg);border-color:var(--acc2)}

.layout{display:grid;grid-template-columns:236px minmax(0,1fr);gap:38px;align-items:start}
@media (max-width:900px){.layout{grid-template-columns:1fr}nav.toc{position:static;max-height:none;
  border-right:0;border-bottom:1px solid var(--line);padding-bottom:16px;margin-bottom:8px}}
nav.toc{position:sticky;top:64px;max-height:calc(100vh - 88px);overflow:auto;
  font-size:12.5px;border-right:1px solid var(--line);padding-right:14px}
nav.toc a{display:block;color:var(--muted);text-decoration:none;padding:3px 0;
  border-left:2px solid transparent;padding-left:9px;line-height:1.4}
nav.toc a.l3{padding-left:20px;font-size:12px;opacity:.85}
nav.toc a:hover{color:var(--fg)}
nav.toc a.on{color:var(--fg);border-left-color:var(--acc2);font-weight:600}

main{min-width:0}
h1{font-size:1.92em;line-height:1.25;margin:.4em 0 .5em;letter-spacing:-.01em}
h2{font-size:1.42em;margin:2.1em 0 .6em;padding-bottom:.28em;border-bottom:1px solid var(--line);
  letter-spacing:-.01em;scroll-margin-top:74px}
h3{font-size:1.16em;margin:1.7em 0 .5em;scroll-margin-top:74px}
h4{font-size:1.02em;margin:1.5em 0 .45em;color:var(--fg);scroll-margin-top:74px}
h4::before{content:"";display:inline-block;width:9px;height:9px;border-radius:2px;
  margin-right:9px;vertical-align:middle;
  background:linear-gradient(135deg,var(--acc1),var(--acc3))}
p{margin:.7em 0}
a{color:var(--link);text-decoration:none}
a:hover{text-decoration:underline}
hr{border:0;border-top:1px solid var(--line);margin:2.4em 0}
strong{font-weight:650}
code{font:0.87em ui-monospace,"Cascadia Code",Menlo,Consolas,monospace;
  background:var(--code);border:1px solid var(--line);border-radius:5px;padding:.12em .38em}
pre{background:var(--code);border:1px solid var(--line);border-radius:9px;padding:13px 15px;
  overflow-x:auto;margin:1em 0}
pre code{background:none;border:0;padding:0;font-size:.85em;line-height:1.55}
blockquote{margin:1.1em 0;padding:.7em 1em;border-left:3px solid var(--acc2);
  background:var(--soft);border-radius:0 8px 8px 0;color:var(--muted)}
blockquote strong{color:var(--fg)}
ul,ol{margin:.6em 0;padding-left:1.4em}
li{margin:.32em 0}
li>strong:first-child{color:var(--fg)}

.tw{overflow-x:auto;margin:1.1em 0;border:1px solid var(--line);border-radius:9px}
table{border-collapse:collapse;width:100%;font-size:13.5px;min-width:420px}
th,td{text-align:left;padding:8px 12px;border-bottom:1px solid var(--line);vertical-align:top}
th{background:var(--soft);font-weight:640;white-space:nowrap;font-size:12.5px;
  letter-spacing:.02em;text-transform:uppercase;color:var(--muted)}
tbody tr:last-child td{border-bottom:0}
tbody tr:hover{background:var(--soft)}
td code{font-size:.84em;white-space:nowrap}

/* the five-tier density ramp, applied to the tier bullets */
main li strong:first-child{position:relative}
"""

JS = """
(function(){
  var r=document.documentElement, b=document.getElementById('tg');
  function cur(){return r.getAttribute('data-theme')||
    (matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light');}
  function set(t){r.setAttribute('data-theme',t);b.textContent=t==='dark'?'light':'dark';}
  b.addEventListener('click',function(){set(cur()==='dark'?'light':'dark');});
  b.textContent=cur()==='dark'?'light':'dark';

  var links=[].slice.call(document.querySelectorAll('nav.toc a'));
  var map={}; links.forEach(function(a){var t=document.getElementById(
    a.getAttribute('href').slice(1)); if(t) map[a.getAttribute('href').slice(1)]=a;});
  var obs=new IntersectionObserver(function(es){
    es.forEach(function(e){ var a=map[e.target.id]; if(!a) return;
      if(e.isIntersecting){links.forEach(function(x){x.classList.remove('on');});
        a.classList.add('on');}});
  },{rootMargin:'-70px 0px -75% 0px'});
  Object.keys(map).forEach(function(id){
    var el=document.getElementById(id); if(el) obs.observe(el);});
})();
"""


def main():
    md = open(SRC, encoding='utf-8').read()
    # drop the H1 — the banner carries the title
    md = re.sub(r'^# .*\n', '', md, count=1)
    body, toc = render(md)

    tocs = []
    for lvl, sid, txt in toc:
        cls = 'l3' if lvl == 3 else ''
        tocs.append('<a class="%s" href="#%s">%s</a>' % (cls, sid, esc(txt)))

    doc = """<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>The Harper Density-Trellis</title>
<meta name="description" content="A branching chain-of-density map of Automattic/harper, reverse-engineered from 4,460 commits and 2,266 pull requests.">
<style>%s</style>
</head><body>
<div class="bar"><div class="in">
  <b><span>weir-rule-language</span> &nbsp;/&nbsp; the harper density-trellis</b>
  <button class="t" id="tg">dark</button>
</div></div>
<div class="wrap">
  <header class="hero">%s</header>
  <div class="layout">
    <nav class="toc">%s</nav>
    <main>%s</main>
  </div>
</div>
<script>%s</script>
</body></html>""" % (CSS, BANNER, '\n'.join(tocs), body, JS)

    open(DEST, 'w', encoding='utf-8').write(doc)
    print('rendered %d chars, %d toc entries' % (len(doc), len(toc)))


main()

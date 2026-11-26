"""Harvest Rocks & Minerals tests from scio.ly for style/coverage reference.

1. Online practice tests: every R&M test listed by
   /api/practice-tests/archive?event=rocks-and-minerals is fetched as HTML and
   reduced to plain text  -> sources/online/<season>_<tournament>.txt
2. PDF archive: every tournament folder in /api/test-archive/pdf is listed via
   Drive's public embedded folder view; a "Rocks and Minerals" subfolder (or
   files whose names mention rocks/minerals) is downloaded -> sources/pdf/

Usage: python -I tools/harvest.py <rockbank dir> [online|pdf|all]
"""
import html, json, os, re, sys, time, urllib.request, urllib.parse

ROOT = sys.argv[1]
MODE = sys.argv[2] if len(sys.argv) > 2 else "all"
SRC = os.path.join(ROOT, "sources")
UA = {"User-Agent": "Mozilla/5.0 (study-tool harvester)"}


def get(url, binary=False, tries=3):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=60) as r:
                data = r.read()
                return data if binary else data.decode("utf8", "replace")
        except Exception as e:
            if i == tries - 1:
                print("  FAIL", url, e)
                return None
            time.sleep(2)


def safe(s):
    return re.sub(r"[^\w.-]+", "_", s).strip("_")[:120]


def html_text(h):
    h = re.sub(r"(?is)<(script|style|svg|noscript)[^>]*>.*?</\1>", " ", h)
    h = re.sub(r"(?i)<br\s*/?>|</(p|div|li|h\d|tr|section)>", "\n", h)
    t = html.unescape(re.sub(r"<[^>]+>", " ", h))
    t = re.sub(r"[ \t\r\f\v]+", " ", t)
    return re.sub(r"\n\s*\n+", "\n", t).strip()


def online():
    out = os.path.join(SRC, "online")
    os.makedirs(out, exist_ok=True)
    idx = json.loads(get("https://www.scio.ly/api/practice-tests/archive?event=rocks-and-minerals"))
    tests = [(t["season"], t["tournament"], x) for t in idx["data"]["tournaments"] for x in t["tests"]
             if "C" in (x.get("division") or "")]  # Division C (and combined B/C) only
    print(len(tests), "online tests")
    for season, tour, x in tests:
        fn = os.path.join(out, f"{season}_{safe(tour)}_{safe(x['division'])}_{x['id'][:8]}.txt")
        if os.path.exists(fn):
            continue
        h = get(f"https://www.scio.ly/practice-tests/{x['id']}")
        if not h:
            continue
        t = html_text(h)
        i = t.find("Section 1")
        if i < 0:
            i = t.find("Question 1")
        t = t[max(i, 0):]
        t = re.sub(r"\n(Check|Flag|Report)\b", "", t)
        with open(fn, "w", encoding="utf8") as f:
            f.write(f"# {x['title']} | div {x['division']} | {season} | {x['questionCount']} q\n{t}\n")
        print("  ok", os.path.basename(fn), len(t))
        time.sleep(0.5)


def list_folder(fid):
    h = get(f"https://drive.google.com/embeddedfolderview?id={fid}")
    if not h:
        return []
    items = []
    for m in re.finditer(r'<a href="([^"]+)"[^>]*>.*?flip-entry-title">([^<]+)<', h, re.S):
        url, name = m.group(1), html.unescape(m.group(2)).strip()
        fm = re.search(r"/folders/([\w-]+)", url)
        if fm:
            items.append(("folder", fm.group(1), name))
            continue
        im = re.search(r"/d/([\w-]+)|[?&]id=([\w-]+)", url)
        if im:
            items.append(("file", im.group(1) or im.group(2), name))
    return items


ROCKS = re.compile(r"rock|mineral|r\s*&\s*m\b|r&m", re.I)
# names that mark a Division B item, e.g. "R&M B", "Div B", "_B.pdf", "(B)"
DIV_B = re.compile(r"(\bdiv(ision)?[\s_.-]*b\b|[\s_(\-]B[\s_)\-.]|[\s_\-]B$|\bB[\s_-]*(test|key|answer))", re.I)
DIV_C = re.compile(r"(\bdiv(ision)?[\s_.-]*c\b|[\s_(\-]C[\s_)\-.]|[\s_\-]C$|\bC[\s_-]*(test|key|answer))", re.I)


def is_div_b(name):
    base = os.path.splitext(name)[0]
    return bool(DIV_B.search(base)) and not DIV_C.search(base)


def download(fid, name, dest):
    fn = os.path.join(dest, safe(name))
    if os.path.exists(fn):
        return
    data = get(f"https://drive.usercontent.google.com/download?id={fid}&export=download&confirm=t", binary=True)
    if data is None:
        # Google Docs/Slides: export as PDF
        data = get(f"https://docs.google.com/document/d/{fid}/export?format=pdf", binary=True)
    if not data or data[:15].lower().startswith(b"<!doctype html") or data[:5].lower() == b"<html":
        print("    skip (not downloadable)", name)
        return
    with open(fn, "wb") as f:
        f.write(data)
    print("    saved", os.path.basename(fn), len(data))


def walk_rocks(fid, dest, depth=0):
    for kind, cid, name in list_folder(fid):
        if is_div_b(name):
            print("    skip Div B", name)
            continue
        if kind == "folder" and depth < 3:
            walk_rocks(cid, dest, depth + 1)
        elif kind == "file":
            download(cid, name, dest)
        time.sleep(0.2)


def pdfs():
    out = os.path.join(SRC, "pdf")
    os.makedirs(out, exist_ok=True)
    idx = json.loads(get("https://www.scio.ly/api/test-archive/pdf"))["data"]
    done = set()
    for t in idx:
        if "C" not in (t.get("division") or ""):
            continue  # Division B-only tournament
        m = re.search(r"/folders/([\w-]+)|[?&]id=([\w-]+)", t.get("url") or "")
        if not m:
            continue
        fid = m.group(1) or m.group(2)
        if fid in done:
            continue
        done.add(fid)
        entries = list_folder(fid)
        hits = [e for e in entries if ROCKS.search(e[2]) and not is_div_b(e[2])]
        if not hits:
            continue
        dest = os.path.join(out, safe(t["name"]))
        os.makedirs(dest, exist_ok=True)
        print(t["name"], "->", [h[2] for h in hits])
        for kind, cid, name in hits:
            if kind == "folder":
                walk_rocks(cid, dest)
            else:
                download(cid, name, dest)
        time.sleep(0.3)


if MODE in ("online", "all"):
    online()
if MODE in ("pdf", "all"):
    pdfs()

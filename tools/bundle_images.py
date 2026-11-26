"""Copy a small, resized set of specimen photos from ../rockid into game/images so the game can be hosted
without the full 1.8 GB photo library. Also writes game/images/CREDITS.md (most photos are Creative Commons
and need attribution).

Usage (from the rockbank folder):  python tools/bundle_images.py [per_specimen=8] [max_px=640]
Requires Pillow (pip install pillow).
"""
import json, os, re, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROCKID = os.path.join(ROOT, "..", "rockid")
OUT = os.path.join(ROOT, "game", "images")
PER = int(sys.argv[1]) if len(sys.argv) > 1 else 8
MAXPX = int(sys.argv[2]) if len(sys.argv) > 2 else 640

src = open(os.path.join(ROCKID, "app", "manifest.js"), encoding="utf8").read()
manifest = json.loads(re.search(r"window\.MANIFEST\s*=\s*(\{.*\})\s*;?\s*$", src, re.S).group(1))

credits = ["# Photo credits", "",
           "Specimen photos are from Wikimedia Commons (collected by the rockid project). Each is used under the license shown.", ""]
total = size = 0
for s in manifest["specimens"]:
    slug = s["slug"]
    os.makedirs(os.path.join(OUT, slug), exist_ok=True)
    taken = 0
    for img in s.get("images", []):
        if taken >= PER:
            break
        p = os.path.join(ROCKID, "images", slug, img["f"])
        if not os.path.exists(p):
            continue
        try:
            im = Image.open(p).convert("RGB")
        except Exception:
            continue
        im.thumbnail((MAXPX, MAXPX))
        dest = os.path.join(OUT, slug, img["f"])
        im.save(dest, "JPEG", quality=72, optimize=True, progressive=True)
        size += os.path.getsize(dest)
        total += 1
        taken += 1
        credits.append(f"- `{slug}/{img['f']}`: {img.get('a') or 'unknown author'}, {img.get('l') or 'license unknown'}, {img.get('u') or ''}")
    if taken == 0:
        print("no photos for", slug)

with open(os.path.join(OUT, "CREDITS.md"), "w", encoding="utf8") as f:
    f.write("\n".join(credits) + "\n")
print(f"{total} photos, {size / 1e6:.1f} MB, in {OUT}")

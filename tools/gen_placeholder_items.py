"""Placeholder icons for new powerups (umbrella, bridge). Replace with real art in art/v2 later,
keeping the same names, sizes and manifest entries."""
import json, math, os, shutil

# Never clobber real art: only write a file that is missing (set FORCE=1 to regenerate placeholders).
FORCE = os.environ.get("FORCE") == "1"
from PIL import Image, ImageDraw

OUT = "art/v2"
FR, SZ = 6, 48
DARK = (31, 18, 56, 255)


def sheet(draw_frame, name):
    if os.path.exists(f"{OUT}/{name}.png") and not FORCE:
        print("keeping existing", name)
        return
    im = Image.new("RGBA", (SZ * FR, SZ), (0, 0, 0, 0))
    for i in range(FR):
        f = Image.new("RGBA", (SZ, SZ), (0, 0, 0, 0))
        draw_frame(ImageDraw.Draw(f), i)
        im.alpha_composite(f, (i * SZ, 0))
    im.save(f"{OUT}/{name}.png")


def umbrella(d, i):
    bob = round(math.sin(i / FR * 2 * math.pi) * 2)
    cx, cy = 24, 24 + bob
    d.pieslice((cx - 17, cy - 15, cx + 17, cy + 19), 180, 360, fill=(235, 70, 90, 255), outline=DARK, width=2)
    for k, x in enumerate((cx - 11, cx - 4, cx + 4, cx + 11)):
        d.line((x, cy + 2, cx + (x - cx) * 0.3, cy - 14), fill=(255, 235, 240, 255), width=1)
    d.line((cx, cy + 2, cx, cy + 16), fill=DARK, width=3)
    d.line((cx, cy + 15, cx + 5, cy + 15), fill=DARK, width=3)
    d.line((cx, cy + 2, cx, cy + 15), fill=(160, 100, 60, 255), width=1)
    gx = cx - 12 + (i * 5) % 24
    d.rectangle((gx, cy - 10, gx + 1, cy - 9), fill=(255, 255, 255, 255))


def bridge(d, i):
    bob = round(math.sin(i / FR * 2 * math.pi) * 2)
    y = 18 + bob
    d.rectangle((4, y, 43, y + 13), fill=(200, 150, 95, 255), outline=DARK, width=2)
    for x in (12, 22, 32):
        d.line((x, y + 2, x, y + 11), fill=(165, 118, 70, 255))
    d.rectangle((20, y - 1, 27, y + 14), fill=(245, 225, 160, 200))
    gx = 6 + (i * 7) % 34
    d.rectangle((gx, y + 3, gx + 1, y + 4), fill=(255, 255, 255, 255))


def cookie(d, i):
    bob = round(math.sin(i / FR * 2 * math.pi) * 2)
    cx, cy = 24, 24 + bob
    d.ellipse((cx - 15, cy - 14, cx + 15, cy + 14), fill=(222, 160, 92, 255), outline=DARK, width=2)
    for (x, y) in ((cx - 7, cy - 6), (cx + 5, cy - 8), (cx + 1, cy + 1), (cx - 8, cy + 6), (cx + 8, cy + 6)):
        d.rectangle((x, y, x + 3, y + 3), fill=(92, 52, 30, 255))
    gx = cx - 12 + (i * 5) % 24
    d.rectangle((gx, cy - 9, gx + 1, cy - 8), fill=(255, 245, 190, 255))


def stopwatch(d, i):
    bob = round(math.sin(i / FR * 2 * math.pi) * 2)
    cx, cy = 24, 26 + bob
    d.rectangle((cx - 3, cy - 20, cx + 3, cy - 15), fill=(150, 160, 175, 255), outline=DARK, width=1)
    d.ellipse((cx - 16, cy - 16, cx + 16, cy + 16), fill=(205, 212, 224, 255), outline=DARK, width=2)
    d.ellipse((cx - 12, cy - 12, cx + 12, cy + 12), fill=(110, 190, 255, 255), outline=(60, 90, 160, 255))
    ang = i / FR * 2 * math.pi
    d.line((cx, cy, cx + math.sin(ang) * 9, cy - math.cos(ang) * 9), fill=DARK, width=2)
    d.line((cx, cy, cx, cy - 6), fill=(255, 255, 255, 255), width=1)


sheet(umbrella, "item_umbrella")
sheet(stopwatch, "item_stopwatch")
sheet(cookie, "item_cookie")
sheet(bridge, "item_bridge")
def copy_missing(src, dst):
    if FORCE or not os.path.exists(f"{OUT}/{dst}.png"):
        shutil.copy(f"{OUT}/{src}.png", f"{OUT}/{dst}.png")


copy_missing("item_feather_pop", "item_umbrella_pop")
copy_missing("item_feather_pop", "item_bridge_pop")
copy_missing("item_coin_pop", "item_cookie_pop")
copy_missing("item_feather_pop", "item_stopwatch_pop")
m = json.load(open(f"{OUT}/manifest.json"))
for n in ("item_umbrella", "item_bridge", "item_cookie", "item_stopwatch"):
    m[n + ".png"] = {"frame_w": SZ, "frame_h": SZ, "frames": FR, "fps": 8, "loop": True}
    m[n + "_pop.png"] = dict(m["item_feather_pop.png" if n != "item_cookie" else "item_coin_pop.png"])
json.dump(m, open(f"{OUT}/manifest.json", "w"), indent=1)
print("placeholders written")

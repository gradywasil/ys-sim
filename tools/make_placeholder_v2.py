"""Nearest-neighbour 2x upscale of art/incoming -> art/v2, used only to test the hi-res pipeline.
Real hi-res art should replace these files 1:1 (same names, double frame sizes)."""
import json, os
from PIL import Image
src, dst = "art/incoming", "art/v2"
os.makedirs(dst, exist_ok=True)
man = json.load(open(f"{src}/manifest.json"))
for name, e in man.items():
    if name == "palette.png":
        Image.open(f"{src}/{name}").save(f"{dst}/{name}"); continue
    im = Image.open(f"{src}/{name}").convert("RGBA")
    im.resize((im.width * 2, im.height * 2), Image.NEAREST).save(f"{dst}/{name}")
    e["frame_w"] *= 2; e["frame_h"] *= 2
json.dump(man, open(f"{dst}/manifest.json", "w"), indent=1)
print("wrote", len(man), "files")

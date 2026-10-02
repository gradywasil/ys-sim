"""Regenerates scripts/art_data.gd from art/v2/manifest.json. Run after new art lands."""
import json
m = json.load(open("art/v2/manifest.json"))
open("scripts/art_data.gd", "w").write(
    "# Generated from art/v2/manifest.json by tools/gen_art_data.py\nextends RefCounted\n\nconst DATA := "
    + json.dumps(m, indent=1) + "\n")
print("ok", len(m))

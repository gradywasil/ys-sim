"""Generates palette.png (32x1 strip) in art/incoming/."""

import os
from PIL import Image
from palette import PALETTE_RGB

def generate_palette_png(output_path: str = "art/incoming/palette.png"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img = Image.new("RGB", (len(PALETTE_RGB), 1))
    for x, rgb in enumerate(PALETTE_RGB):
        img.putpixel((x, 0), rgb)
    img.save(output_path, "PNG")
    print(f"Generated {output_path} ({img.width}x{img.height}) with {len(PALETTE_RGB)} colors.")

if __name__ == "__main__":
    generate_palette_png()

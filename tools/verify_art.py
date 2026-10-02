"""Younger Sibling Simulator - Art Verification Suite."""

import json
from pathlib import Path
from PIL import Image
from palette import VALID_PALETTE_RGBA

def verify():
    manifest_path = Path("art/incoming/manifest.json")
    if not manifest_path.exists():
        print("ERROR: manifest.json does not exist!")
        return False
        
    with open(manifest_path) as f:
        manifest = json.load(f)
        
    errors = []
    warnings = []
    
    print(f"--- Verifying {len(manifest)} assets in art/incoming/ ---")
    
    # Precompute palette RGB set for quick lookup
    palette_rgb = {rgba[:3] for rgba in VALID_PALETTE_RGBA}
    pure_white_rgb = (245, 248, 252) # or (255, 255, 255)
    
    for filename, meta in manifest.items():
        filepath = Path("art/incoming") / filename
        if not filepath.exists():
            errors.append(f"Missing file: {filename}")
            continue
            
        img = Image.open(filepath)
        w, h = img.size
        
        expected_w = meta["frame_w"] * meta["frames"]
        expected_h = meta["frame_h"]
        
        if (w, h) != (expected_w, expected_h):
            errors.append(
                f"{filename}: Dimension mismatch. Got ({w}, {h}), expected ({expected_w}, {expected_h})"
            )
            continue
            
        img_rgba = img.convert("RGBA")
        pixels = img_rgba.load()
        
        # 1. Semi-transparency & palette checks
        allow_semi_transparent = (filename == "item_glow.png")
        is_fx = filename.startswith("fx_") or filename == "font_pixel.png"
        
        invalid_palette_pixels = 0
        semi_transparent_pixels = 0
        
        for y in range(h):
            for x in range(w):
                r, g, b, a = pixels[x, y]
                if a == 0:
                    continue
                if not allow_semi_transparent and a != 255:
                    semi_transparent_pixels += 1
                
                # Check palette
                if is_fx:
                    if (r, g, b) != (255, 255, 255) and (r, g, b) != (245, 248, 252):
                        invalid_palette_pixels += 1
                elif not allow_semi_transparent:
                    if (r, g, b) not in palette_rgb:
                        invalid_palette_pixels += 1
                        
        if semi_transparent_pixels > 0:
            errors.append(f"{filename}: Found {semi_transparent_pixels} semi-transparent pixels!")
            
        if invalid_palette_pixels > 0:
            errors.append(f"{filename}: Found {invalid_palette_pixels} pixels outside palette!")

        # 2. Foot anchor check for P1 character sprites
        if filename.startswith("p1_"):
            frame_w = meta["frame_w"]
            frame_h = meta["frame_h"]
            for frame_idx in range(meta["frames"]):
                fx_offset = frame_idx * frame_w
                # Check if bottom row (y = frame_h - 1) has at least one solid pixel
                bottom_y = frame_h - 1
                has_foot_contact = False
                for fx in range(frame_w):
                    _, _, _, a = pixels[fx_offset + fx, bottom_y]
                    if a > 0:
                        has_foot_contact = True
                        break
                if not has_foot_contact:
                    errors.append(f"{filename} frame {frame_idx}: Foot does not touch bottom edge (y={bottom_y})!")

    print(f"Verified {len(manifest)} files.")
    if errors:
        print(f"\nFAILED with {len(errors)} error(s):")
        for err in errors:
            print("  [X]", err)
        return False
    else:
        print("\nALL ART ASSETS PASSED VERIFICATION PERFECTLY! [100% SUCCESS]")
        return True

if __name__ == "__main__":
    verify()

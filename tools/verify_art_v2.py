"""Younger Sibling Simulator - v2/v3 Art Verification Suite."""

import json
from pathlib import Path
from PIL import Image
from palette import VALID_PALETTE_RGBA, PALETTE_RGB
from stage_palettes import STAGE_RGB

def verify_v2():
    manifest_path = Path("art/v2/manifest.json")
    if not manifest_path.exists():
        print("ERROR: art/v2/manifest.json does not exist!")
        return False

    with open(manifest_path) as f:
        manifest = json.load(f)

    errors = []
    print(f"--- Verifying {len(manifest)} assets in art/v2/ ---")

    base_palette_rgb = {rgba[:3] for rgba in VALID_PALETTE_RGBA}
    pure_white_rgb = (245, 248, 252)

    # Build stage palette lookup sets
    stage_palette_rgb = {
        stage: base_palette_rgb | set(rgbs)
        for stage, rgbs in STAGE_RGB.items()
    }

    hazard_stage_map = {
        "hazard_juice_puddle.png": "kitchen",
        "hazard_marble.png": "kitchen",
        "hazard_stove_burner.png": "kitchen",
        "hazard_spill_trail.png": "kitchen",
        "hazard_sprinkler.png": "yard",
        "hazard_water_spray.png": "yard",
        "hazard_mud.png": "yard",
        "hazard_wind_gust.png": "yard",
        "fx_leaf.png": "yard",
        "fx_leaf_b.png": "yard",
        "hazard_paint_can.png": "basement",
        "hazard_drip.png": "basement",
        "hazard_mousetrap.png": "basement",
        "light_flashlight_cone.png": "basement",
        "light_dark_mask.png": "basement",
        "item_flashlight.png": "basement",
        "item_flashlight_pop.png": "basement",
        "hazard_cobweb.png": "attic",
        "hazard_loose_board.png": "attic",
        "hazard_dust_cloud.png": "attic",
        "hazard_spider_drop.png": "attic",
    }

    for filename, meta in manifest.items():
        filepath = Path("art/v2") / filename
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

        is_normal_map = filename.endswith("_n.png")
        is_light_overlay = (
            filename.startswith("light_")
            or filename == "fg_dust.png"
            or filename == "item_glow.png"
            or filename == "ui_bedtime_warning.png"
            or filename == "placed_fan.png"
            or filename == "hazard_water_spray.png"
            or filename == "fx_shield_bubble.png"
            or filename.endswith("_fg_dust.png")
        )
        is_fx = filename.startswith("fx_") or filename.startswith("font_pixel")
        allow_semi_transparent = is_light_overlay or is_normal_map

        # Determine valid palette for this asset
        valid_palette = base_palette_rgb
        if filename in hazard_stage_map:
            valid_palette = stage_palette_rgb[hazard_stage_map[filename]]
        else:
            for stage in ("kitchen", "yard", "basement", "attic"):
                if filename.startswith(f"{stage}_"):
                    valid_palette = stage_palette_rgb[stage]
                    break

        invalid_palette_pixels = 0
        semi_transparent_pixels = 0

        for y in range(h):
            for x in range(w):
                r, g, b, a = pixels[x, y]
                if a == 0:
                    continue
                if not allow_semi_transparent and a != 255:
                    semi_transparent_pixels += 1

                if not is_normal_map and not is_light_overlay:
                    if is_fx:
                        if (r, g, b) not in valid_palette and (r, g, b) != (255, 255, 255) and (r, g, b) != pure_white_rgb:
                            invalid_palette_pixels += 1
                    else:
                        if (r, g, b) not in valid_palette:
                            invalid_palette_pixels += 1

        if semi_transparent_pixels > 0:
            errors.append(f"{filename}: Found {semi_transparent_pixels} semi-transparent pixels!")

        if invalid_palette_pixels > 0:
            errors.append(f"{filename}: Found {invalid_palette_pixels} pixels outside allowed palette!")

        # Foot anchor check for P1 character sprites
        if filename.startswith("p1_") and not filename.endswith("_n.png") and meta["frame_h"] == 64:
            frame_w = meta["frame_w"]
            frame_h = meta["frame_h"]
            bottom_y = frame_h - 1  # y = 63
            for frame_idx in range(meta["frames"]):
                fx_offset = frame_idx * frame_w
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
        for err in errors[:25]:
            print("  [X]", err)
        if len(errors) > 25:
            print(f"  ... and {len(errors) - 25} more errors.")
        return False
    else:
        print("\nALL ART ASSETS PASSED VERIFICATION PERFECTLY! [100% SUCCESS]")
        return True

if __name__ == "__main__":
    verify_v2()

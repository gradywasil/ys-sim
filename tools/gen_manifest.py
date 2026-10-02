"""Younger Sibling Simulator - Art Manifest Generator."""

import json
from pathlib import Path

MANIFEST_DATA = {
    # Palette
    "palette.png": {
        "frame_w": 32, "frame_h": 1, "frames": 1, "fps": 0, "loop": False
    },

    # Player 1 Sprites
    "p1_idle.png": {
        "frame_w": 32, "frame_h": 32, "frames": 6, "fps": 8, "loop": True
    },
    "p1_wait.png": {
        "frame_w": 32, "frame_h": 32, "frames": 8, "fps": 6, "loop": True
    },
    "p1_run.png": {
        "frame_w": 32, "frame_h": 32, "frames": 10, "fps": 16, "loop": True
    },
    "p1_run_fast.png": {
        "frame_w": 32, "frame_h": 32, "frames": 8, "fps": 20, "loop": True
    },
    "p1_jump_up.png": {
        "frame_w": 32, "frame_h": 32, "frames": 3, "fps": 16, "loop": False
    },
    "p1_jump_apex.png": {
        "frame_w": 32, "frame_h": 32, "frames": 2, "fps": 12, "loop": False
    },
    "p1_fall.png": {
        "frame_w": 32, "frame_h": 32, "frames": 3, "fps": 16, "loop": True
    },
    "p1_land.png": {
        "frame_w": 32, "frame_h": 32, "frames": 4, "fps": 20, "loop": False
    },
    "p1_trip.png": {
        "frame_w": 32, "frame_h": 32, "frames": 10, "fps": 14, "loop": False
    },
    "p1_boost_jump.png": {
        "frame_w": 32, "frame_h": 32, "frames": 4, "fps": 18, "loop": False
    },
    "p1_celebrate.png": {
        "frame_w": 32, "frame_h": 32, "frames": 8, "fps": 10, "loop": True
    },

    # Player 2 Hand
    "hand_idle.png": {
        "frame_w": 32, "frame_h": 32, "frames": 6, "fps": 8, "loop": True
    },
    "hand_hold.png": {
        "frame_w": 32, "frame_h": 32, "frames": 4, "fps": 10, "loop": True
    },
    "hand_drop.png": {
        "frame_w": 32, "frame_h": 32, "frames": 5, "fps": 24, "loop": False
    },
    "hand_cooldown.png": {
        "frame_w": 32, "frame_h": 32, "frames": 4, "fps": 6, "loop": True
    },

    # Power-up Items
    "item_boots.png": {
        "frame_w": 24, "frame_h": 24, "frames": 6, "fps": 8, "loop": True
    },
    "item_boots_pop.png": {
        "frame_w": 24, "frame_h": 24, "frames": 3, "fps": 24, "loop": False
    },
    "item_feather.png": {
        "frame_w": 24, "frame_h": 24, "frames": 6, "fps": 8, "loop": True
    },
    "item_feather_pop.png": {
        "frame_w": 24, "frame_h": 24, "frames": 3, "fps": 24, "loop": False
    },
    "item_coin.png": {
        "frame_w": 24, "frame_h": 24, "frames": 6, "fps": 8, "loop": True
    },
    "item_coin_pop.png": {
        "frame_w": 24, "frame_h": 24, "frames": 3, "fps": 24, "loop": False
    },
    "item_glow.png": {
        "frame_w": 32, "frame_h": 32, "frames": 1, "fps": 1, "loop": False
    },

    # Environment Tiles
    "tileset_floor.png": {
        "frame_w": 128, "frame_h": 48, "frames": 1, "fps": 0, "loop": False,
        "tile_w": 16, "tile_h": 16, "columns": 8, "rows": 3
    },
    "toy_blocks.png": {
        "frame_w": 64, "frame_h": 48, "frames": 1, "fps": 0, "loop": False,
        "tile_w": 16, "tile_h": 16, "columns": 4, "rows": 3
    },
    "goal_flag.png": {
        "frame_w": 32, "frame_h": 64, "frames": 6, "fps": 10, "loop": True
    },
    "pit_bg.png": {
        "frame_w": 16, "frame_h": 64, "frames": 1, "fps": 0, "loop": False
    },

    # Parallax Backgrounds
    "bg_sky_gradient.png": {
        "frame_w": 1, "frame_h": 270, "frames": 1, "fps": 0, "loop": False
    },
    "bg_far.png": {
        "frame_w": 480, "frame_h": 270, "frames": 1, "fps": 0, "loop": False
    },
    "bg_far_stars.png": {
        "frame_w": 480, "frame_h": 270, "frames": 4, "fps": 3, "loop": True
    },
    "bg_mid.png": {
        "frame_w": 640, "frame_h": 270, "frames": 1, "fps": 0, "loop": False
    },
    "bg_near.png": {
        "frame_w": 480, "frame_h": 270, "frames": 1, "fps": 0, "loop": False
    },

    # Effects
    "fx_dust.png": {
        "frame_w": 16, "frame_h": 16, "frames": 6, "fps": 20, "loop": False
    },
    "fx_jump_puff.png": {
        "frame_w": 16, "frame_h": 16, "frames": 5, "fps": 24, "loop": False
    },
    "fx_stars.png": {
        "frame_w": 24, "frame_h": 24, "frames": 8, "fps": 16, "loop": True
    },
    "fx_impact.png": {
        "frame_w": 32, "frame_h": 32, "frames": 5, "fps": 30, "loop": False
    },
    "fx_speedline.png": {
        "frame_w": 24, "frame_h": 8, "frames": 4, "fps": 30, "loop": False
    },
    "fx_sparkle.png": {
        "frame_w": 8, "frame_h": 8, "frames": 5, "fps": 16, "loop": False
    },
    "fx_bubble.png": {
        "frame_w": 96, "frame_h": 24, "frames": 1, "fps": 0, "loop": False
    },

    # UI
    "ui_trouble_pip.png": {
        "frame_w": 12, "frame_h": 12, "frames": 2, "fps": 0, "loop": False
    },
    "ui_slot.png": {
        "frame_w": 52, "frame_h": 28, "frames": 2, "fps": 0, "loop": False
    },
    "ui_cooldown_bar.png": {
        "frame_w": 160, "frame_h": 6, "frames": 2, "fps": 0, "loop": False
    },
    "ui_key_1.png": {
        "frame_w": 10, "frame_h": 10, "frames": 1, "fps": 0, "loop": False
    },
    "ui_key_2.png": {
        "frame_w": 10, "frame_h": 10, "frames": 1, "fps": 0, "loop": False
    },
    "ui_key_3.png": {
        "frame_w": 10, "frame_h": 10, "frames": 1, "fps": 0, "loop": False
    },
    "font_pixel.png": {
        "frame_w": 96, "frame_h": 48, "frames": 1, "fps": 0, "loop": False
    },

    # Extra Polish
    "parent_peek.png": {
        "frame_w": 64, "frame_h": 96, "frames": 6, "fps": 6, "loop": False
    }
}

def generate_manifest():
    out_path = Path("art/incoming/manifest.json")
    with open(out_path, "w") as f:
        json.dump(MANIFEST_DATA, f, indent=2)
    print(f"Saved {out_path} ({len(MANIFEST_DATA)} entries)")

if __name__ == "__main__":
    generate_manifest()

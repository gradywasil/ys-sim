"""Younger Sibling Simulator - Phase C Player 1 Hazard Reaction Animation Generator v3.

Generates 9 Player 1 Hazard Reaction sprite sheets into art/v2/:
1. p1_slip.png            (64x64, 8 frames @ 14 fps, loop: false)
2. p1_slog.png            (64x64, 8 frames @ 10 fps, loop: true)
3. p1_lean.png            (64x64, 6 frames @ 12 fps, loop: true)
4. p1_ouch.png            (64x64, 8 frames @ 14 fps, loop: false)
5. p1_stuck.png           (64x64, 8 frames @ 10 fps, loop: true)
6. p1_sprint.png          (64x64, 8 frames @ 28 fps, loop: true)
7. p1_flashlight_idle.png (64x64, 8 frames @ 8 fps, loop: true)
8. p1_flashlight_run.png  (64x64, 12 frames @ 20 fps, loop: true)
9. p1_blown.png           (64x64, 8 frames @ 14 fps, loop: false)

Strict Art Brief v2 & v3 requirements:
- Frame size: 64x64 native
- Grounding: The lowest foot/sole pixel MUST touch row y=63 in EVERY frame!
- True pixel art: no anti-aliasing, binary alpha
- Palette: 64 colors strictly from tools/palette.py, selective dark-purple outline (#120d1f)
- Lighting: Upper-left light source
- Character details: Red hoodie with drawstrings, denim shorts with rolled cuff,
  skate sneakers with white vulcanized soles, expressive face, springy hair cowlick.
"""

import json
import math
import os
import sys
from pathlib import Path
from typing import List, Tuple, Optional

# Ensure tools directory is on sys.path
TOOLS_DIR = Path(__file__).resolve().parent
PROJECT_DIR = TOOLS_DIR.parent
sys.path.insert(0, str(TOOLS_DIR))

from canvas import PixelCanvas, assemble_strip
from palette import (
    TRANSPARENT, OUTLINE, VOID_BLACK,
    SHADOW_PURPLE_DARK, SHADOW_PURPLE_DEEP, SHADOW_PURPLE_MID, PURPLE_DARK, PURPLE_MID, PURPLE_RICH, PURPLE_LIGHT,
    DUSK_LILAC, DUSK_PINK, DUSK_ROSE, DUSK_PEACH, DUSK_BLUSH, DUSK_CREAM,
    SKIN_DEEP, SKIN_SHADOW, SKIN_MID, SKIN_LIGHT, SKIN_HIGHLIGHT,
    WOOD_BLACK, BROWN_DARKEST, BROWN_DARK, BROWN_MID, BROWN_LIGHT, WOOD_HIGHLIGHT, WOOD_LIT,
    RED_DEEP, RED_SHADOW, RED_RICH, RED_MID, RED_LIGHT, RED_HIGHLIGHT,
    BLUE_DEEP, BLUE_SHADOW, BLUE_RICH, BLUE_MID, BLUE_LIGHT, BLUE_HIGHLIGHT,
    YELLOW_DEEP, YELLOW_SHADOW, YELLOW_RICH, YELLOW_MID, YELLOW_LIGHT, YELLOW_HIGHLIGHT,
    GREEN_DEEP, GREEN_SHADOW, GREEN_RICH, GREEN_MID, GREEN_LIGHT, GREEN_HIGHLIGHT,
    ORANGE_DEEP, ORANGE_SHADOW, ORANGE_MID, ORANGE_LIGHT,
    TEAL_SHADOW, TEAL_MID, TEAL_LIGHT, TEAL_HIGHLIGHT,
    METAL_SHADOW, METAL_MID, WHITE_SHADOW, WHITE_MID, PURE_WHITE,
    VALID_PALETTE_RGBA
)
from gen_player_v2 import (
    create_base_canvas,
    draw_sneaker_v2,
    draw_leg_v2,
    draw_shorts_v2,
    draw_hoodie_v2,
    draw_head_v2,
    draw_arm_v2
)


# =============================================================================
# CUSTOM ART HELPERS FOR HAZARD REACTIONS
# =============================================================================

def draw_wind_streaks(canvas: PixelCanvas, seed: int = 0):
    """Draws horizontal rushing wind streaks from right to left."""
    streak_rows = [14, 22, 30, 38, 48]
    for idx, y in enumerate(streak_rows):
        offset = (seed * 7 + idx * 11) % 17
        x_start = 63 - offset
        length = 10 + ((seed + idx) % 5) * 3
        for x in range(max(0, x_start - length), x_start):
            if canvas.get_pixel(x, y)[3] == 0:
                color = PURE_WHITE if (x % 3 == 0) else WHITE_MID
                canvas.set_pixel(x, y, color)


def draw_flashlight(canvas: PixelCanvas, hand_x: int, hand_y: int,
                    angle_deg: float = 0.0, beam_range: int = 22,
                    illuminate_p1: bool = True, p1_tx: int = 32, p1_ty: int = 32):
    """
    Draws a chunky yellow handheld flashlight and its projected light beam.
    Barrel: YELLOW_MID, rim: YELLOW_LIGHT, bezel: OUTLINE/METAL_MID.
    Projected beam: PURE_WHITE core, YELLOW_HIGHLIGHT/YELLOW_LIGHT cone.
    Optional warm bounce reflection on character front.
    """
    rad = math.radians(angle_deg)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)

    # Flashlight dimensions
    # Barrel extends from hand_x forward by ~8px
    bx0, by0 = hand_x - 1, hand_y - 1
    bx1 = hand_x + int(round(8 * cos_a))
    by1 = hand_y + int(round(8 * sin_a))

    # Flashlight body pixels
    for step in range(8):
        t = step / 7.0
        cx = int(round(hand_x - 1 + t * 8 * cos_a))
        cy = int(round(hand_y + t * 8 * sin_a))
        # 3px thickness
        canvas.set_pixel(cx, cy - 1, YELLOW_LIGHT)
        canvas.set_pixel(cx, cy, YELLOW_MID)
        canvas.set_pixel(cx, cy + 1, YELLOW_SHADOW)

    # Flashlight grip handle & switch
    canvas.set_pixel(hand_x, hand_y - 2, OUTLINE)
    canvas.set_pixel(hand_x + 1, hand_y - 2, METAL_MID)

    # Flared beveled head
    head_x = bx1
    head_y = by1
    canvas.set_pixel(head_x, head_y - 2, OUTLINE)
    canvas.set_pixel(head_x, head_y - 1, YELLOW_LIGHT)
    canvas.set_pixel(head_x, head_y, YELLOW_MID)
    canvas.set_pixel(head_x, head_y + 1, YELLOW_SHADOW)
    canvas.set_pixel(head_x, head_y + 2, OUTLINE)

    # Lens face
    lens_x = head_x + 1
    lens_y = head_y
    canvas.set_pixel(lens_x, lens_y - 1, PURE_WHITE)
    canvas.set_pixel(lens_x, lens_y, PURE_WHITE)
    canvas.set_pixel(lens_x, lens_y + 1, WHITE_MID)

    # Projected beam cone (pixel cone to right edge)
    cone_start_x = lens_x + 1
    for dist in range(1, beam_range):
        curr_x = cone_start_x + dist
        if curr_x >= 64:
            break
        center_y = lens_y + dist * sin_a
        spread = 1 + int(round(dist * 0.45))
        min_y = int(math.floor(center_y - spread))
        max_y = int(math.ceil(center_y + spread))

        for py in range(min_y, max_y + 1):
            if 0 <= py < 64:
                # Core of the beam vs outer halo
                d_from_center = abs(py - center_y)
                if d_from_center <= 1:
                    canvas.set_pixel(curr_x, py, PURE_WHITE)
                elif d_from_center <= spread * 0.55:
                    canvas.set_pixel(curr_x, py, YELLOW_HIGHLIGHT)
                elif d_from_center <= spread:
                    # Dither outer edge of beam
                    if (curr_x + py) % 2 == 0:
                        canvas.set_pixel(curr_x, py, YELLOW_LIGHT)
                    else:
                        canvas.set_pixel(curr_x, py, DUSK_CREAM)

    # Warm yellow bounce illumination on player chest & nose
    if illuminate_p1:
        canvas.set_pixel(p1_tx + 6, p1_ty + 3, YELLOW_HIGHLIGHT)
        canvas.set_pixel(p1_tx + 7, p1_ty + 4, YELLOW_LIGHT)
        canvas.set_pixel(p1_tx + 6, p1_ty + 5, YELLOW_MID)


# =============================================================================
# 1. P1 SLIP (8 frames @ 14 fps, loop: false)
# Feet slip out forward on puddle, arms windmill back, comic hang-time slip,
# seated skid landing on butt (touching y=63).
# =============================================================================

def generate_p1_slip() -> List[PixelCanvas]:
    frames = []

    # ---------------- Frame 0: Puddle Slip Initiation ----------------
    # Steps on puddle, foot begins to skate forward, sudden panic
    c0 = create_base_canvas()
    # Puddle ripples along floor (rows 62..63)
    for x in range(32, 48):
        c0.set_pixel(x, 63, ORANGE_SHADOW if (x % 3 == 0) else ORANGE_MID)
        if x in [36, 37, 42, 43]:
            c0.set_pixel(x, 62, YELLOW_LIGHT)
    # Right foot stepping onto puddle at y=63
    draw_sneaker_v2(c0, foot_x=40, foot_y=63, pose="heel_strike", is_far=False)
    # Left foot planted on floor at y=63
    draw_sneaker_v2(c0, foot_x=24, foot_y=63, pose="flat", is_far=True)
    draw_leg_v2(c0, hip_x=28, hip_y=51, foot_x=24, foot_y=57, is_far=True)
    draw_leg_v2(c0, hip_x=34, hip_y=51, foot_x=40, foot_y=57, is_far=False)
    draw_shorts_v2(c0, sx=30, sy=45, w=18, h=9)
    # Arms starting to flail back
    draw_arm_v2(c0, shoulder_x=24, shoulder_y=33, hand_x=16, hand_y=38, is_far=True)
    draw_hoodie_v2(c0, tx=30, ty=31, w=20, h=15, drawstring_wind=1)
    draw_arm_v2(c0, shoulder_x=40, shoulder_y=33, hand_x=44, hand_y=36, is_far=False)
    draw_head_v2(c0, hx=30, hy=22, eye_state="wide", look_dir="down", mouth="o", eyebrow="raised")
    # Droplet flicking up
    c0.set_pixel(46, 58, YELLOW_LIGHT)
    assert any(c0.get_pixel(x, 63)[3] > 0 for x in range(64)), "p1_slip frame 0 missing y=63 anchor!"
    frames.append(c0)

    # ---------------- Frame 1: Feet Fly Out Forward ----------------
    # Feet launch forward-up, left heel scrapes row 63, arms windmill
    c1 = create_base_canvas()
    # Floor puddle skid streak on row 63
    for x in range(28, 48):
        c1.set_pixel(x, 63, ORANGE_MID if x % 2 == 0 else ORANGE_SHADOW)
    # Right foot kicked forward into air
    draw_sneaker_v2(c1, foot_x=46, foot_y=54, pose="toe_point", is_far=False)
    # Left foot heel skimming floor touching row 63
    draw_sneaker_v2(c1, foot_x=32, foot_y=63, pose="heel_strike", is_far=True)
    draw_leg_v2(c1, hip_x=25, hip_y=50, foot_x=32, foot_y=57, is_far=True)
    draw_leg_v2(c1, hip_x=30, hip_y=50, foot_x=46, foot_y=50, is_far=False)
    draw_shorts_v2(c1, sx=27, sy=46, w=18, h=8)
    # Windmilling arms: far arm up-back, near arm down-back
    draw_arm_v2(c1, shoulder_x=22, shoulder_y=35, hand_x=12, hand_y=22, is_far=True)
    draw_hoodie_v2(c1, tx=26, ty=35, w=20, h=14, drawstring_wind=-2, folds=1)
    draw_arm_v2(c1, shoulder_x=36, shoulder_y=35, hand_x=38, hand_y=28, is_far=False)
    draw_head_v2(c1, hx=24, hy=26, eye_state="wide", look_dir="forward", mouth="open", eyebrow="worried", hair_wind=1)
    assert any(c1.get_pixel(x, 63)[3] > 0 for x in range(64)), "p1_slip frame 1 missing y=63 anchor!"
    frames.append(c1)

    # ---------------- Frame 2: Comic Hang-Time Slip ----------------
    # Classic cartoon hang-time: body horizontal, trailing shoe heel scrapes y=63
    c2 = create_base_canvas()
    # Left heel scraping row 63
    draw_sneaker_v2(c2, foot_x=28, foot_y=63, pose="heel_strike", is_far=True)
    # Right foot kicked high up
    draw_sneaker_v2(c2, foot_x=48, foot_y=46, pose="toe_point", is_far=False)
    draw_leg_v2(c2, hip_x=23, hip_y=52, foot_x=28, foot_y=57, is_far=True)
    draw_leg_v2(c2, hip_x=27, hip_y=52, foot_x=48, foot_y=44, is_far=False)
    draw_shorts_v2(c2, sx=24, sy=48, w=18, h=8)
    # Arms spinning in windmill: far arm down, near arm high
    draw_arm_v2(c2, shoulder_x=19, shoulder_y=42, hand_x=14, hand_y=40, is_far=True)
    draw_hoodie_v2(c2, tx=22, ty=42, w=20, h=13, drawstring_wind=-3)
    draw_arm_v2(c2, shoulder_x=31, shoulder_y=42, hand_x=26, hand_y=18, is_far=False)
    draw_head_v2(c2, hx=20, hy=34, eye_state="wide", look_dir="forward", mouth="open", eyebrow="raised", hair_wind=1)
    # Skid spray
    c2.set_pixel(34, 63, ORANGE_LIGHT)
    c2.set_pixel(38, 62, PURE_WHITE)
    assert any(c2.get_pixel(x, 63)[3] > 0 for x in range(64)), "p1_slip frame 2 missing y=63 anchor!"
    frames.append(c2)

    # ---------------- Frame 3: Apex Float / Butt Descending ----------------
    # Butt falling toward floor, feet high, trailing shoe scrapes y=63
    c3 = create_base_canvas()
    # Trailing sneaker heel scrapes row 63
    draw_sneaker_v2(c3, foot_x=26, foot_y=63, pose="heel_strike", is_far=True)
    # Right foot forward
    draw_sneaker_v2(c3, foot_x=50, foot_y=50, pose="toe_point", is_far=False)
    draw_leg_v2(c3, hip_x=22, hip_y=54, foot_x=26, foot_y=57, is_far=True)
    draw_leg_v2(c3, hip_x=26, hip_y=54, foot_x=50, foot_y=48, is_far=False)
    draw_shorts_v2(c3, sx=23, sy=52, w=18, h=8)
    # Arms reaching back toward floor anticipating landing
    draw_arm_v2(c3, shoulder_x=18, shoulder_y=46, hand_x=12, hand_y=54, is_far=True)
    draw_hoodie_v2(c3, tx=23, ty=44, w=20, h=13)
    draw_arm_v2(c3, shoulder_x=30, shoulder_y=46, hand_x=28, hand_y=52, is_far=False)
    draw_head_v2(c3, hx=20, hy=36, eye_state="oof", look_dir="forward", mouth="grimace", eyebrow="worried")
    assert any(c3.get_pixel(x, 63)[3] > 0 for x in range(64)), "p1_slip frame 3 missing y=63 anchor!"
    frames.append(c3)

    # ---------------- Frame 4: Seated Skid Impact (Butt lands on y=63) ----------------
    # Butt slams hard onto floor at y=63! Splash puffs left and right.
    c4 = create_base_canvas()
    # Butt/shorts on rows 56..63 touching row 63!
    for y in range(56, 64):
        for x in range(18, 34):
            rel_y = y - 56
            if y == 63:
                c4.set_pixel(x, y, OUTLINE if x in [18, 33] else SHADOW_PURPLE_DARK)
            elif y == 62:
                c4.set_pixel(x, y, BLUE_DEEP if x <= 22 else BLUE_SHADOW)
            else:
                c4.set_pixel(x, y, BLUE_MID if x <= 28 else BLUE_SHADOW)
    # Seams & pocket on seated shorts
    c4.set_pixel(24, 58, YELLOW_LIGHT)
    c4.set_pixel(25, 59, YELLOW_MID)
    # Legs sprawled forward horizontally along floor:
    # Right sneaker flat at x=46, y=63; left sneaker flat at x=34, y=63
    draw_sneaker_v2(c4, foot_x=36, foot_y=63, pose="flat", is_far=True)
    draw_sneaker_v2(c4, foot_x=48, foot_y=63, pose="flat", is_far=False)
    # Bare legs connecting shorts to sneakers along rows 59..62
    for x in range(30, 44):
        c4.set_pixel(x, 60, SKIN_LIGHT if x % 2 == 0 else SKIN_MID)
        c4.set_pixel(x, 61, SKIN_MID)
    # Braced hands on floor
    c4.set_pixel(14, 63, SKIN_LIGHT)
    c4.set_pixel(15, 63, SKIN_MID)
    c4.set_pixel(14, 62, SKIN_HIGHLIGHT)
    # Impact splash puffs bursting out left and right on rows 62..63
    c4.set_pixel(10, 63, ORANGE_LIGHT)
    c4.set_pixel(11, 62, PURE_WHITE)
    c4.set_pixel(12, 63, YELLOW_LIGHT)
    c4.set_pixel(54, 63, ORANGE_LIGHT)
    c4.set_pixel(55, 62, PURE_WHITE)
    c4.set_pixel(56, 63, YELLOW_LIGHT)
    # Hoodie compressed forward
    draw_hoodie_v2(c4, tx=26, ty=43, w=22, h=14, folds=-1)
    # Arms planted behind
    draw_arm_v2(c4, shoulder_x=20, shoulder_y=45, hand_x=14, hand_y=61, is_far=True)
    draw_arm_v2(c4, shoulder_x=34, shoulder_y=45, hand_x=22, hand_y=60, is_far=False)
    draw_head_v2(c4, hx=28, hy=34, eye_state="oof", look_dir="forward", mouth="grimace", eyebrow="furrowed")
    assert any(c4.get_pixel(x, 63)[3] > 0 for x in range(64)), "p1_slip frame 4 missing y=63 anchor!"
    frames.append(c4)

    # ---------------- Frame 5: Seated Skid Forward ----------------
    # Sliding forward on butt along floor, friction skid lines
    c5 = create_base_canvas()
    # Friction wet skid lines along row 63
    for x in range(16, 52):
        if x % 3 == 0:
            c5.set_pixel(x, 63, ORANGE_MID)
        elif x % 3 == 1:
            c5.set_pixel(x, 63, YELLOW_LIGHT)
    # Butt/shorts on floor touching row 63
    for y in range(56, 64):
        for x in range(20, 36):
            if y == 63:
                c5.set_pixel(x, y, OUTLINE if x in [20, 35] else SHADOW_PURPLE_DARK)
            elif y == 62:
                c5.set_pixel(x, y, BLUE_SHADOW)
            else:
                c5.set_pixel(x, y, BLUE_MID)
    # Sneakers flat along row 63
    draw_sneaker_v2(c5, foot_x=38, foot_y=63, pose="flat", is_far=True)
    draw_sneaker_v2(c5, foot_x=50, foot_y=63, pose="flat", is_far=False)
    # Legs
    for x in range(32, 46):
        c5.set_pixel(x, 60, SKIN_LIGHT)
        c5.set_pixel(x, 61, SKIN_MID)
    # Hoodie
    draw_hoodie_v2(c5, tx=28, ty=42, w=22, h=14)
    draw_arm_v2(c5, shoulder_x=22, shoulder_y=44, hand_x=16, hand_y=58, is_far=True)
    draw_arm_v2(c5, shoulder_x=36, shoulder_y=44, hand_x=42, hand_y=56, is_far=False)
    # Dizzy eyes, open mouth with tongue out
    draw_head_v2(c5, hx=30, hy=33, eye_state="dizzy", look_dir="forward", mouth="open", eyebrow="worried")
    assert any(c5.get_pixel(x, 63)[3] > 0 for x in range(64)), "p1_slip frame 5 missing y=63 anchor!"
    frames.append(c5)

    # ---------------- Frame 6: Skid Deceleration / Tailbone Wobble ----------------
    # Friction stops player, sitting upright, rubbing sore tailbone
    c6 = create_base_canvas()
    # Butt seated on floor at row 63
    for y in range(56, 64):
        for x in range(22, 38):
            if y == 63:
                c6.set_pixel(x, y, OUTLINE if x in [22, 37] else SHADOW_PURPLE_DARK)
            elif y == 62:
                c6.set_pixel(x, y, BLUE_SHADOW)
            else:
                c6.set_pixel(x, y, BLUE_MID)
    draw_sneaker_v2(c6, foot_x=36, foot_y=63, pose="flat", is_far=True)
    draw_sneaker_v2(c6, foot_x=48, foot_y=63, pose="flat", is_far=False)
    for x in range(32, 44):
        c6.set_pixel(x, 60, SKIN_LIGHT)
        c6.set_pixel(x, 61, SKIN_MID)
    draw_hoodie_v2(c6, tx=30, ty=41, w=22, h=15)
    # Near arm rubbing sore tailbone/back of hip, far arm resting on knee
    draw_arm_v2(c6, shoulder_x=24, shoulder_y=43, hand_x=34, hand_y=56, is_far=True)
    draw_arm_v2(c6, shoulder_x=38, shoulder_y=43, hand_x=24, hand_y=50, is_far=False)
    draw_head_v2(c6, hx=31, hy=32, eye_state="dizzy", look_dir="forward", mouth="grimace", eyebrow="furrowed")
    # Dizzy star above head
    c6.set_pixel(33, 21, YELLOW_LIGHT)
    c6.set_pixel(34, 22, YELLOW_MID)
    c6.set_pixel(32, 22, YELLOW_MID)
    assert any(c6.get_pixel(x, 63)[3] > 0 for x in range(64)), "p1_slip frame 6 missing y=63 anchor!"
    frames.append(c6)

    # ---------------- Frame 7: Settled Seated Daze / Rubbing Head ----------------
    # Seated dazed, rubbing head with sheepish smirk
    c7 = create_base_canvas()
    # Butt seated on floor at row 63
    for y in range(56, 64):
        for x in range(22, 38):
            if y == 63:
                c7.set_pixel(x, y, OUTLINE if x in [22, 37] else SHADOW_PURPLE_DARK)
            elif y == 62:
                c7.set_pixel(x, y, BLUE_SHADOW)
            else:
                c7.set_pixel(x, y, BLUE_MID)
    draw_sneaker_v2(c7, foot_x=26, foot_y=63, pose="flat", is_far=True)
    draw_sneaker_v2(c7, foot_x=42, foot_y=63, pose="flat", is_far=False)
    for x in range(30, 40):
        c7.set_pixel(x, 60, SKIN_LIGHT)
        c7.set_pixel(x, 61, SKIN_MID)
    draw_hoodie_v2(c7, tx=31, ty=41, w=22, h=15)
    # Near arm rubs head, far arm on knee
    draw_arm_v2(c7, shoulder_x=25, shoulder_y=43, hand_x=28, hand_y=56, is_far=True)
    draw_arm_v2(c7, shoulder_x=39, shoulder_y=43, hand_x=36, hand_y=25, is_far=False)
    draw_head_v2(c7, hx=32, hy=32, eye_state="normal", look_dir="forward", mouth="smirk", eyebrow="worried", sweat=True)
    assert any(c7.get_pixel(x, 63)[3] > 0 for x in range(64)), "p1_slip frame 7 missing y=63 anchor!"
    frames.append(c7)

    return frames


# =============================================================================
# 2. P1 SLOG (8 frames @ 10 fps, loop: true)
# Trudging slowly through thick mud, each leg lifting with sucking effort,
# strained grimacing face.
# =============================================================================

def generate_p1_slog() -> List[PixelCanvas]:
    frames = []

    # Mud parameters for 8-frame walk:
    # (right_foot_x, right_foot_y, right_pose, left_foot_x, left_foot_y, left_pose,
    #  right_mud_suction, left_mud_suction, bob, tx_lean)
    cycle_data = [
        # 0: Right leg beginning suction pull; Left foot sunk at y=63
        (38, 61, "toe_push", 26, 63, "flat", True, False, 0, 33),
        # 1: Right leg high pull with dripping mud; Left foot anchored at y=63
        (40, 56, "toe_point", 26, 63, "flat", True, False, -1, 34),
        # 2: Right foot plunges down into mud with splash at y=63
        (42, 63, "squash", 25, 63, "flat", False, False, 2, 34),
        # 3: Weight transfers forward, settling into mud
        (40, 63, "flat", 24, 63, "toe_push", False, False, 0, 33),
        # 4: Left leg beginning suction pull; Right foot sunk at y=63
        (38, 63, "flat", 24, 61, "toe_push", False, True, 0, 32),
        # 5: Left leg high pull with dripping mud; Right foot anchored at y=63
        (38, 63, "flat", 22, 56, "toe_point", False, True, -1, 31),
        # 6: Left foot plunges down into mud with splash at y=63
        (38, 63, "flat", 34, 63, "squash", False, False, 2, 32),
        # 7: Settling, breathing heave, preparing next step
        (38, 63, "flat", 28, 63, "flat", False, False, 0, 32),
    ]

    for i, (r_x, r_y, r_pose, l_x, l_y, l_pose, r_mud, l_mud, bob, tx) in enumerate(cycle_data):
        c = create_base_canvas()

        # Floor mud base layer across bottom (rows 61..63)
        for mx in range(18, 50):
            c.set_pixel(mx, 63, BROWN_DARKEST if mx % 2 == 0 else BROWN_DARK)
            if mx in [22, 28, 35, 41, 46]:
                c.set_pixel(mx, 62, BROWN_MID)
                c.set_pixel(mx, 61, BROWN_DARK)

        # Draw left sneaker (far or near)
        draw_sneaker_v2(c, foot_x=l_x, foot_y=l_y, pose=l_pose, is_far=True)
        # Draw right sneaker
        draw_sneaker_v2(c, foot_x=r_x, foot_y=r_y, pose=r_pose, is_far=False)

        # Suction mud strands stretching down to row 63 when lifting
        if r_mud:
            for sy in range(r_y + 1, 64):
                c.set_pixel(r_x - 1, sy, BROWN_DARKEST)
                c.set_pixel(r_x, sy, BROWN_DARK)
                c.set_pixel(r_x + 1, sy, BROWN_MID)
            # Mud glob on sole
            c.set_pixel(r_x - 2, r_y, BROWN_DARK)
            c.set_pixel(r_x + 2, r_y, BROWN_DARK)
        if l_mud:
            for sy in range(l_y + 1, 64):
                c.set_pixel(l_x - 1, sy, BROWN_DARKEST)
                c.set_pixel(l_x, sy, BROWN_DARK)
                c.set_pixel(l_x + 1, sy, BROWN_MID)
            c.set_pixel(l_x - 2, l_y, BROWN_DARK)
            c.set_pixel(l_x + 2, l_y, BROWN_DARK)

        # Mud splash when foot plunges down (frames 2 and 6)
        if i == 2:
            c.set_pixel(r_x - 5, 62, BROWN_MID)
            c.set_pixel(r_x - 6, 61, BROWN_LIGHT)
            c.set_pixel(r_x + 5, 62, BROWN_MID)
            c.set_pixel(r_x + 6, 61, BROWN_LIGHT)
        elif i == 6:
            c.set_pixel(l_x - 5, 62, BROWN_MID)
            c.set_pixel(l_x - 6, 61, BROWN_LIGHT)
            c.set_pixel(l_x + 5, 62, BROWN_MID)
            c.set_pixel(l_x + 6, 61, BROWN_LIGHT)

        # Legs & shorts
        draw_leg_v2(c, hip_x=tx - 4, hip_y=51 + bob, foot_x=l_x, foot_y=l_y - 4, is_far=True)
        draw_leg_v2(c, hip_x=tx + 4, hip_y=51 + bob, foot_x=r_x, foot_y=r_y - 4, is_far=False)
        draw_shorts_v2(c, sx=tx, sy=46 + bob, w=18, h=9)

        # Strained arm pumping with clenched fists
        if i in [0, 1, 2, 3]:
            arm_back = (tx - 12, 42 + bob)
            arm_front = (tx + 12, 38 + bob)
        else:
            arm_back = (tx + 12, 42 + bob)
            arm_front = (tx - 12, 38 + bob)

        draw_arm_v2(c, shoulder_x=tx - 6, shoulder_y=33 + bob, hand_x=arm_back[0], hand_y=arm_back[1], is_far=True, fist=True)
        draw_hoodie_v2(c, tx=tx, ty=31 + bob, w=20, h=15, drawstring_wind=1, folds=1)
        draw_arm_v2(c, shoulder_x=tx + 8, shoulder_y=33 + bob, hand_x=arm_front[0], hand_y=arm_front[1], is_far=False, fist=True)

        # Strained grimacing face
        eye_st = "oof" if (i in [1, 5]) else "normal"
        mouth_st = "grimace" if (i not in [2, 6]) else "o"
        draw_head_v2(c, hx=tx + 2, hy=22 + bob, eye_state=eye_st, look_dir="forward",
                     mouth=mouth_st, eyebrow="furrowed", sweat=True)

        assert any(c.get_pixel(x, 63)[3] > 0 for x in range(64)), f"p1_slog frame {i} missing y=63 anchor!"
        frames.append(c)

    return frames


# =============================================================================
# 3. P1 LEAN (6 frames @ 12 fps, loop: true)
# Leaning forward aggressively into heavy headwind, hoodie and cowlick blown
# straight back, shielding face with arm.
# =============================================================================

def generate_p1_lean() -> List[PixelCanvas]:
    frames = []

    # 6-frame digging cycle into gale
    # (front_x, back_x, back_pose, bob, dip_x)
    lean_steps = [
        (40, 22, "flat", 0, 0),
        (42, 23, "toe_push", 1, 1),
        (41, 24, "flat", 0, -1),
        (39, 26, "flat", -1, 0),
        (41, 24, "flat", 1, 1),
        (40, 23, "flat", 0, 0),
    ]

    for i, (fx, bx, bp, bob, dip_x) in enumerate(lean_steps):
        c = create_base_canvas()

        # Rushing wind streaks crossing frame right to left
        draw_wind_streaks(c, seed=i)

        # Feet planted wide on y=63
        draw_sneaker_v2(c, foot_x=bx, foot_y=63, pose=bp, is_far=True)
        draw_sneaker_v2(c, foot_x=fx, foot_y=63, pose="flat", is_far=False)

        # Body pitched aggressively forward
        sx = 30 + dip_x
        tx = 34 + dip_x
        hx = 38 + dip_x
        sy = 46 + bob
        ty = 32 + bob
        hy = 24 + bob

        draw_leg_v2(c, hip_x=sx - 4, hip_y=51 + bob, foot_x=bx, foot_y=57, is_far=True)
        draw_leg_v2(c, hip_x=sx + 4, hip_y=51 + bob, foot_x=fx, foot_y=57, is_far=False)
        draw_shorts_v2(c, sx=sx, sy=sy, w=18, h=9)

        # Far arm trailing low-back for balance
        draw_arm_v2(c, shoulder_x=tx - 7, shoulder_y=34 + bob, hand_x=tx - 18, hand_y=42 + bob, is_far=True, fist=True)

        # Hoodie leaning hard into wind, drawstrings whipped straight left!
        draw_hoodie_v2(c, tx=tx, ty=ty, w=20, h=15, drawstring_wind=-4, folds=1)

        # Additional wind-whipped horizontal drawstrings
        c.line(tx - 3, ty + 4, tx - 13, ty + 3, PURE_WHITE)
        c.line(tx + 3, ty + 4, tx - 9, ty + 4, PURE_WHITE)

        # Near arm shielding face!
        # Hand raised to brow, forearm sheltering eyes
        draw_arm_v2(c, shoulder_x=tx + 7, shoulder_y=33 + bob, hand_x=hx - 2, hand_y=hy + 2, is_far=False)
        # Extra sleeve bunching around shielding forearm
        c.line(tx + 8, ty + 3, hx - 1, hy + 3, RED_LIGHT)
        c.line(tx + 8, ty + 4, hx - 1, hy + 4, RED_MID)

        # Head tucked into wind, hair cowlick whipped straight back horizontally
        draw_head_v2(c, hx=hx, hy=hy, eye_state="oof", look_dir="forward",
                     mouth="grimace", eyebrow="furrowed", hair_wind=1)

        # Extra horizontal hair streaks streaming back
        c.line(hx - 5, 17 + bob, hx - 16, 16 + bob, BROWN_MID)
        c.line(hx - 6, 18 + bob, hx - 17, 17 + bob, WOOD_HIGHLIGHT)
        c.line(hx - 7, 19 + bob, hx - 18, 18 + bob, WOOD_LIT)

        assert any(c.get_pixel(x, 63)[3] > 0 for x in range(64)), f"p1_lean frame {i} missing y=63 anchor!"
        frames.append(c)

    return frames


# =============================================================================
# 4. P1 OUCH (8 frames @ 14 fps, loop: false)
# Snapped toe/foot ouch: hopping on one foot (touching y=63), clutching other
# ankle in hands, wincing teeth.
# =============================================================================

def generate_p1_ouch() -> List[PixelCanvas]:
    frames = []

    # Right foot is the hopping foot (grounded at y=63)
    # Left foot is the hurt foot (clutched in both hands)
    hops = [
        # (r_pose, r_x, hop_dy, l_y, l_x, eye, mouth, pain_sparks)
        ("flat", 26, 0, 63, 42, "wide", "o", True),         # 0: Stub impact shock
        ("squash", 26, 1, 48, 38, "pain", "grimace", True),  # 1: Recoil grab ankle
        ("toe_push", 26, -2, 45, 38, "pain", "open", False), # 2: Hop 1 launch
        ("flat", 27, 0, 48, 38, "pain", "grimace", False),   # 3: Hop 1 land
        ("squash", 27, 1, 48, 38, "pain", "grimace", True),  # 4: Hop 2 crouch
        ("toe_push", 28, -2, 45, 38, "pain", "o", False),    # 5: Hop 2 launch
        ("flat", 28, 0, 52, 37, "oof", "grimace", False),    # 6: Hop 2 land & settle
        ("flat", 28, 0, 56, 36, "normal", "pout", False),    # 7: Relieved wincing smirk
    ]

    for i, (rp, rx, dy, ly, lx, eye, mouth, sparks) in enumerate(hops):
        c = create_base_canvas()

        # Right sneaker always touches y=63
        draw_sneaker_v2(c, foot_x=rx, foot_y=63, pose=rp, is_far=False)

        # Left hurt sneaker
        if i == 0:
            # Just stubbed on floor
            draw_sneaker_v2(c, foot_x=lx, foot_y=63, pose="flat", is_far=True)
            draw_leg_v2(c, hip_x=30, hip_y=51, foot_x=lx, foot_y=57, is_far=True)
            # Pain spark at toe
            c.set_pixel(lx + 7, 63, YELLOW_LIGHT)
            c.set_pixel(lx + 8, 62, YELLOW_MID)
            c.set_pixel(lx + 9, 63, ORANGE_LIGHT)
        else:
            # Clutched in air
            draw_sneaker_v2(c, foot_x=lx, foot_y=ly, pose="flat", is_far=True)
            draw_leg_v2(c, hip_x=28, hip_y=51 + dy, foot_x=lx, foot_y=ly - 4, is_far=True)

        # Right supporting leg & shorts
        draw_leg_v2(c, hip_x=34, hip_y=51 + dy, foot_x=rx, foot_y=57, is_far=False)
        draw_shorts_v2(c, sx=31, sy=45 + dy, w=18, h=9)

        # Hoodie
        draw_hoodie_v2(c, tx=31, ty=31 + dy, w=20, h=15)

        # Arms clutching hurt ankle/shin
        if i == 0:
            # Arms shooting down
            draw_arm_v2(c, shoulder_x=24, shoulder_y=33, hand_x=28, hand_y=46, is_far=True)
            draw_arm_v2(c, shoulder_x=38, shoulder_y=33, hand_x=36, hand_y=46, is_far=False)
        elif i in [1, 2, 3, 4, 5]:
            # Both hands clasping ankle firmly
            draw_arm_v2(c, shoulder_x=24, shoulder_y=33 + dy, hand_x=lx - 2, hand_y=ly - 4, is_far=True)
            draw_arm_v2(c, shoulder_x=38, shoulder_y=33 + dy, hand_x=lx + 2, hand_y=ly - 4, is_far=False)
        elif i == 6:
            # Transitioning hands
            draw_arm_v2(c, shoulder_x=24, shoulder_y=33, hand_x=lx - 1, hand_y=ly - 3, is_far=True)
            draw_arm_v2(c, shoulder_x=38, shoulder_y=33, hand_x=lx + 2, hand_y=ly - 3, is_far=False)
        else: # 7
            # One hand on shin, other wiping brow
            draw_arm_v2(c, shoulder_x=24, shoulder_y=33, hand_x=lx, hand_y=ly - 2, is_far=True)
            draw_arm_v2(c, shoulder_x=38, shoulder_y=33, hand_x=36, hand_y=23, is_far=False)

        # Head with wincing / screaming expression
        draw_head_v2(c, hx=31, hy=22 + dy, eye_state=eye, look_dir="down" if i > 0 else "forward",
                     mouth=mouth, eyebrow="furrowed" if eye == "pain" else "worried", sweat=True)

        # Pain sparks / stars popping around hurt toe
        if sparks and i > 0:
            c.set_pixel(lx + 6, ly - 2, YELLOW_LIGHT)
            c.set_pixel(lx + 8, ly - 3, YELLOW_MID)
            c.set_pixel(lx + 7, ly - 5, PURE_WHITE)

        assert any(c.get_pixel(x, 63)[3] > 0 for x in range(64)), f"p1_ouch frame {i} missing y=63 anchor!"
        frames.append(c)

    return frames


# =============================================================================
# 5. P1 STUCK (8 frames @ 10 fps, loop: true)
# Stuck in cobwebs: wriggling torso, pulling arms against sticky web strands,
# panicked eyes looking around.
# =============================================================================

def generate_p1_stuck() -> List[PixelCanvas]:
    frames = []

    # Wriggle sequence: shifting torso and darting eyes
    wriggles = [
        # (tx, hx, eye_dir, mouth, lp, rp, arm_l, arm_r)
        (30, 30, "up", "o", "flat", "flat", (16, 36), (46, 34)),
        (32, 33, "forward", "grimace", "flat", "toe_push", (22, 32), (48, 30)),
        (34, 35, "forward", "o", "flat", "flat", (24, 34), (44, 36)),
        (33, 33, "down", "grimace", "toe_push", "flat", (20, 24), (46, 40)),
        (31, 31, "up", "o", "flat", "flat", (18, 32), (44, 32)),
        (30, 29, "forward", "grimace", "flat", "flat", (16, 38), (42, 38)),
        (32, 32, "forward", "grimace", "flat", "flat", (22, 36), (42, 36)),
        (31, 31, "up", "o", "flat", "flat", (18, 34), (45, 34)),
    ]

    for i, (tx, hx, eye_d, mouth, lp, rp, arm_l, arm_r) in enumerate(wriggles):
        c = create_base_canvas()

        # Both sneakers firmly grounded at row y=63
        draw_sneaker_v2(c, foot_x=26, foot_y=63, pose=lp, is_far=True)
        draw_sneaker_v2(c, foot_x=38, foot_y=63, pose=rp, is_far=False)

        draw_leg_v2(c, hip_x=tx - 4, hip_y=51, foot_x=26, foot_y=57, is_far=True)
        draw_leg_v2(c, hip_x=tx + 4, hip_y=51, foot_x=38, foot_y=57, is_far=False)
        draw_shorts_v2(c, sx=tx, sy=45, w=18, h=9)

        # Arms struggling against sticky web
        draw_arm_v2(c, shoulder_x=tx - 7, shoulder_y=33, hand_x=arm_l[0], hand_y=arm_l[1], is_far=True, fist=True)
        draw_hoodie_v2(c, tx=tx, ty=31, w=20, h=15, folds=1)
        draw_arm_v2(c, shoulder_x=tx + 7, shoulder_y=33, hand_x=arm_r[0], hand_y=arm_r[1], is_far=False, fist=True)

        # Head with panicked eyes looking around
        draw_head_v2(c, hx=hx, hy=22, eye_state="wide", look_dir=eye_d,
                     mouth=mouth, eyebrow="worried", sweat=True)

        # Sticky elastic spider cobweb strands!
        # Left anchor strand stretching from left edge to left wrist
        c.line(2, 26, arm_l[0], arm_l[1], PURE_WHITE)
        c.line(2, 27, arm_l[0], arm_l[1] + 1, WHITE_SHADOW)
        # Right anchor strand stretching from right edge to right wrist
        c.line(61, 24, arm_r[0], arm_r[1], PURE_WHITE)
        c.line(61, 25, arm_r[0], arm_r[1] + 1, WHITE_SHADOW)
        # Top ceiling anchor strand
        c.line(32, 2, tx, 30, PURE_WHITE)
        c.line(33, 2, tx + 1, 30, WHITE_MID)
        # Sticky web fibers criss-crossing chest & elbows
        c.line(arm_l[0], arm_l[1], tx + 4, 36, DUSK_CREAM)
        c.line(arm_r[0], arm_r[1], tx - 4, 38, DUSK_CREAM)

        assert any(c.get_pixel(x, 63)[3] > 0 for x in range(64)), f"p1_stuck frame {i} missing y=63 anchor!"
        frames.append(c)

    return frames


# =============================================================================
# 6. P1 SPRINT (8 frames @ 28 fps, loop: true)
# Extreme sugar-rush hyper sprint: blur wheel legs, wide manic grinning eyes,
# horizontal wind-swept hair, leaning 45 degrees forward.
# =============================================================================

def generate_p1_sprint() -> List[PixelCanvas]:
    frames = []

    # Extreme 45-degree forward lean coordinates
    sx = 34
    sy = 46
    tx = 38
    ty = 33
    hx = 42
    hy = 23

    # Pinwheel rotating blur wheel phases (8 phases across 360 deg)
    # Each phase has a lower foot sweep touching row 63!
    # (sweep_x, back_foot_x, back_foot_y, arm_front_x, arm_front_y, arm_back_x, arm_back_y)
    wheel_phases = [
        (42, 20, 46, 50, 36, 18, 42),
        (38, 24, 44, 46, 38, 22, 40),
        (32, 28, 45, 38, 42, 26, 36),
        (26, 32, 48, 24, 40, 44, 36),
        (42, 20, 46, 18, 42, 50, 36),
        (38, 24, 44, 22, 40, 46, 38),
        (32, 28, 45, 26, 36, 38, 42),
        (26, 32, 48, 44, 36, 24, 40),
    ]

    for i, (sw_x, bk_x, bk_y, af_x, af_y, ab_x, ab_y) in enumerate(wheel_phases):
        c = create_base_canvas()

        # Rainbow sugar-rush speed sparks trailing behind at row 63
        c.set_pixel(14 - (i % 4), 63, YELLOW_LIGHT)
        c.set_pixel(10 - (i % 4), 62, BLUE_LIGHT)
        c.set_pixel(8 - (i % 4), 63, PURE_WHITE)

        # ---------------- Blur Wheel Legs (Cartoon Roadrunner Pinwheel) ----------------
        # 1. Lower ground-sweep sneaker touching row 63!
        draw_sneaker_v2(c, foot_x=sw_x, foot_y=63, pose="flat", speed_boot=False, is_far=(i % 2 == 1))
        # 2. Upper back-kick sneaker
        draw_sneaker_v2(c, foot_x=bk_x, foot_y=bk_y, pose="toe_point", speed_boot=False, is_far=(i % 2 == 0))

        # 3. Motion blur arcs connecting the spinning wheel around hip (34, 50)
        # Red and blue motion trails
        c.line(sw_x - 4, 61, bk_x + 2, bk_y + 4, RED_LIGHT)
        c.line(sw_x - 5, 62, bk_x + 1, bk_y + 5, RED_MID)
        c.line(bk_x - 2, bk_y, sw_x - 8, 56, WHITE_MID)
        c.line(bk_x - 1, bk_y + 1, sw_x - 7, 57, BLUE_LIGHT)

        # Circular wheel ghost rim
        for angle in range(0, 360, 45):
            rad = math.radians(angle + i * 45)
            wx = int(round(34 + 11 * math.cos(rad)))
            wy = int(round(52 + 10 * math.sin(rad)))
            if 0 <= wx < 64 and 0 <= wy < 63:
                c.set_pixel(wx, wy, RED_LIGHT if (angle % 90 == 0) else WHITE_SHADOW)

        # Legs connecting into shorts
        draw_leg_v2(c, hip_x=sx - 3, hip_y=sy + 5, foot_x=bk_x, foot_y=bk_y - 2, is_far=True)
        draw_leg_v2(c, hip_x=sx + 3, hip_y=sy + 5, foot_x=sw_x, foot_y=59, is_far=False)

        # Shorts tilted forward
        draw_shorts_v2(c, sx=sx, sy=sy, w=18, h=9, tilt=1)

        # Supersonic piston arms with blur streaks
        draw_arm_v2(c, shoulder_x=tx - 7, shoulder_y=ty + 2, hand_x=ab_x, hand_y=ab_y, is_far=True, fist=True)
        draw_hoodie_v2(c, tx=tx, ty=ty, w=20, h=15, drawstring_wind=4, folds=1)
        draw_arm_v2(c, shoulder_x=tx + 7, shoulder_y=ty + 2, hand_x=af_x, hand_y=af_y, is_far=False, fist=True)

        # Drawstrings whipped horizontally flat back
        c.line(tx - 3, ty + 4, tx - 14, ty + 2, PURE_WHITE)
        c.line(tx + 3, ty + 4, tx - 10, ty + 3, PURE_WHITE)

        # Manic grinning face: wide eyes, ecstatic toothy smile, blushing pink cheeks
        draw_head_v2(c, hx=hx, hy=hy, eye_state="wide", look_dir="forward",
                     mouth="grin", eyebrow="raised", hair_wind=1, blush=True)

        # Horizontal hair wind trails streaming far back
        c.line(hx - 5, 17, hx - 17, 16, BROWN_MID)
        c.line(hx - 6, 18, hx - 18, 17, WOOD_HIGHLIGHT)
        c.line(hx - 7, 19, hx - 19, 18, WOOD_LIT)

        assert any(c.get_pixel(x, 63)[3] > 0 for x in range(64)), f"p1_sprint frame {i} missing y=63 anchor!"
        frames.append(c)

    return frames


# =============================================================================
# 7. P1 FLASHLIGHT IDLE (8 frames @ 8 fps, loop: true)
# Standing idle holding heavy yellow flashlight in right hand, sweeping beam
# side to side, nervous eyes.
# =============================================================================

def generate_p1_flashlight_idle() -> List[PixelCanvas]:
    frames = []

    # Sweep angles for flashlight across 8 frames:
    # 0: downward scan (+18 deg)
    # 1: down-mid (+9 deg)
    # 2: level beam (0 deg)
    # 3: up-mid (-9 deg)
    # 4: high scan (-18 deg)
    # 5: up-mid (-9 deg)
    # 6: level beam (0 deg)
    # 7: down-mid (+9 deg)
    angles = [18.0, 9.0, 0.0, -9.0, -18.0, -9.0, 0.0, 9.0]
    bobs = [0, 0, -1, -1, -1, 0, 0, 0]
    eye_dirs = ["down", "down", "forward", "forward", "up", "forward", "forward", "down"]

    for i in range(8):
        c = create_base_canvas()
        bob = bobs[i]
        angle = angles[i]

        # Both sneakers firmly planted touching row y=63
        draw_sneaker_v2(c, foot_x=26, foot_y=63, pose="flat", is_far=True)
        draw_sneaker_v2(c, foot_x=38, foot_y=63, pose="flat", is_far=False)

        draw_leg_v2(c, hip_x=28, hip_y=52 + bob, foot_x=26, foot_y=57, is_far=True)
        draw_leg_v2(c, hip_x=36, hip_y=52 + bob, foot_x=38, foot_y=57, is_far=False)
        draw_shorts_v2(c, sx=32, sy=45 + bob, w=18, h=9)

        # Far arm resting at side
        draw_arm_v2(c, shoulder_x=24, shoulder_y=33 + bob, hand_x=22, hand_y=42 + bob, is_far=True)

        # Hoodie
        draw_hoodie_v2(c, tx=32, ty=31 + bob, w=20, h=15)

        # Near arm holds heavy yellow flashlight
        hand_x = 42
        hand_y = 38 + bob
        draw_arm_v2(c, shoulder_x=40, shoulder_y=33 + bob, hand_x=hand_x, hand_y=hand_y, is_far=False)

        # Draw flashlight and sweeping beam
        draw_flashlight(c, hand_x=hand_x, hand_y=hand_y, angle_deg=angle,
                        beam_range=20, illuminate_p1=True, p1_tx=32, p1_ty=31 + bob)

        # Head with nervous eyes following the beam
        draw_head_v2(c, hx=32, hy=22 + bob, eye_state="wide" if i in [2, 6] else "normal",
                     look_dir=eye_dirs[i], mouth="pout", eyebrow="worried", sweat=True)

        assert any(c.get_pixel(x, 63)[3] > 0 for x in range(64)), f"p1_flashlight_idle frame {i} missing y=63 anchor!"
        frames.append(c)

    return frames


# =============================================================================
# 8. P1 FLASHLIGHT RUN (12 frames @ 20 fps, loop: true)
# Complete 12-frame run cycle holding flashlight beam projected forward,
# illuminated chest/face.
# =============================================================================

def generate_p1_flashlight_run() -> List[PixelCanvas]:
    frames = []

    # 12-frame athletic double-step run cycle:
    bobs = [0, 2, 0, -2, -3, -1, 0, 2, 0, -2, -3, -1]

    for i in range(12):
        c = create_base_canvas()
        bob = bobs[i]

        # Far arm pumps in cadence with running legs
        if i in [0, 1, 2]:
            far_hand = (22, 40 + bob)
        elif i in [3, 4, 5]:
            far_hand = (18, 44 + bob)
        elif i in [6, 7, 8]:
            far_hand = (42, 42 + bob)
        else: # 9, 10, 11
            far_hand = (46, 36 + bob)

        # Draw legs matching canonical p1_run cycle (every frame touches y=63!)
        if i == 0:
            draw_sneaker_v2(c, foot_x=20, foot_y=57, pose="toe_point", is_far=True)
            draw_sneaker_v2(c, foot_x=42, foot_y=63, pose="heel_strike", is_far=False)
            draw_leg_v2(c, hip_x=30, hip_y=52 + bob, foot_x=20, foot_y=53, is_far=True)
            draw_leg_v2(c, hip_x=35, hip_y=52 + bob, foot_x=42, foot_y=59, is_far=False)
        elif i == 1:
            draw_sneaker_v2(c, foot_x=26, foot_y=57, pose="flat", is_far=True)
            draw_sneaker_v2(c, foot_x=38, foot_y=63, pose="squash", is_far=False)
            draw_leg_v2(c, hip_x=30, hip_y=52 + bob, foot_x=26, foot_y=53, is_far=True)
            draw_leg_v2(c, hip_x=35, hip_y=52 + bob, foot_x=38, foot_y=57, is_far=False)
        elif i == 2:
            draw_sneaker_v2(c, foot_x=42, foot_y=53, pose="flat", is_far=True)
            draw_sneaker_v2(c, foot_x=32, foot_y=63, pose="flat", is_far=False)
            draw_leg_v2(c, hip_x=30, hip_y=52 + bob, foot_x=42, foot_y=49, is_far=True)
            draw_leg_v2(c, hip_x=35, hip_y=52 + bob, foot_x=32, foot_y=57, is_far=False)
        elif i == 3:
            draw_sneaker_v2(c, foot_x=44, foot_y=51, pose="flat", is_far=True)
            draw_sneaker_v2(c, foot_x=26, foot_y=63, pose="toe_push", is_far=False)
            draw_leg_v2(c, hip_x=30, hip_y=52 + bob, foot_x=44, foot_y=47, is_far=True)
            draw_leg_v2(c, hip_x=35, hip_y=52 + bob, foot_x=26, foot_y=57, is_far=False)
        elif i == 4:
            draw_sneaker_v2(c, foot_x=45, foot_y=50, pose="flat", is_far=True)
            draw_sneaker_v2(c, foot_x=24, foot_y=63, pose="toe_point", is_far=False)
            draw_leg_v2(c, hip_x=30, hip_y=52 + bob, foot_x=45, foot_y=46, is_far=True)
            draw_leg_v2(c, hip_x=35, hip_y=52 + bob, foot_x=24, foot_y=57, is_far=False)
        elif i == 5:
            draw_sneaker_v2(c, foot_x=44, foot_y=63, pose="heel_strike", is_far=True)
            draw_sneaker_v2(c, foot_x=22, foot_y=58, pose="toe_point", is_far=False)
            draw_leg_v2(c, hip_x=30, hip_y=52 + bob, foot_x=44, foot_y=59, is_far=True)
            draw_leg_v2(c, hip_x=35, hip_y=52 + bob, foot_x=22, foot_y=54, is_far=False)
        elif i == 6:
            draw_sneaker_v2(c, foot_x=42, foot_y=63, pose="heel_strike", is_far=True)
            draw_sneaker_v2(c, foot_x=20, foot_y=57, pose="toe_point", is_far=False)
            draw_leg_v2(c, hip_x=30, hip_y=52 + bob, foot_x=42, foot_y=59, is_far=True)
            draw_leg_v2(c, hip_x=35, hip_y=52 + bob, foot_x=20, foot_y=53, is_far=False)
        elif i == 7:
            draw_sneaker_v2(c, foot_x=38, foot_y=63, pose="squash", is_far=True)
            draw_sneaker_v2(c, foot_x=26, foot_y=57, pose="flat", is_far=False)
            draw_leg_v2(c, hip_x=30, hip_y=52 + bob, foot_x=38, foot_y=57, is_far=True)
            draw_leg_v2(c, hip_x=35, hip_y=52 + bob, foot_x=26, foot_y=53, is_far=False)
        elif i == 8:
            draw_sneaker_v2(c, foot_x=32, foot_y=63, pose="flat", is_far=True)
            draw_sneaker_v2(c, foot_x=42, foot_y=53, pose="flat", is_far=False)
            draw_leg_v2(c, hip_x=30, hip_y=52 + bob, foot_x=32, foot_y=57, is_far=True)
            draw_leg_v2(c, hip_x=35, hip_y=52 + bob, foot_x=42, foot_y=49, is_far=False)
        elif i == 9:
            draw_sneaker_v2(c, foot_x=26, foot_y=63, pose="toe_push", is_far=True)
            draw_sneaker_v2(c, foot_x=44, foot_y=51, pose="flat", is_far=False)
            draw_leg_v2(c, hip_x=30, hip_y=52 + bob, foot_x=26, foot_y=57, is_far=True)
            draw_leg_v2(c, hip_x=35, hip_y=52 + bob, foot_x=44, foot_y=47, is_far=False)
        elif i == 10:
            draw_sneaker_v2(c, foot_x=24, foot_y=63, pose="toe_point", is_far=True)
            draw_sneaker_v2(c, foot_x=45, foot_y=50, pose="flat", is_far=False)
            draw_leg_v2(c, hip_x=30, hip_y=52 + bob, foot_x=24, foot_y=57, is_far=True)
            draw_leg_v2(c, hip_x=35, hip_y=52 + bob, foot_x=45, foot_y=46, is_far=False)
        else: # 11
            draw_sneaker_v2(c, foot_x=22, foot_y=58, pose="toe_point", is_far=True)
            draw_sneaker_v2(c, foot_x=44, foot_y=63, pose="heel_strike", is_far=False)
            draw_leg_v2(c, hip_x=30, hip_y=52 + bob, foot_x=22, foot_y=54, is_far=True)
            draw_leg_v2(c, hip_x=35, hip_y=52 + bob, foot_x=44, foot_y=59, is_far=False)

        draw_shorts_v2(c, sx=33, sy=45 + bob, w=18, h=9)

        # Far arm pumping
        draw_arm_v2(c, shoulder_x=25, shoulder_y=33 + bob, hand_x=far_hand[0], hand_y=far_hand[1], is_far=True)

        # Hoodie thrust forward
        draw_hoodie_v2(c, tx=33, ty=31 + bob, w=20, h=15, drawstring_wind=2, folds=1)

        # Near arm holds flashlight extended forward
        hand_x = 45
        hand_y = 35 + bob
        draw_arm_v2(c, shoulder_x=41, shoulder_y=33 + bob, hand_x=hand_x, hand_y=hand_y, is_far=False)

        # Flashlight held forward projecting bright beam ahead
        draw_flashlight(c, hand_x=hand_x, hand_y=hand_y, angle_deg=0.0,
                        beam_range=18, illuminate_p1=True, p1_tx=33, p1_ty=31 + bob)

        # Head looking forward alertly into beam
        draw_head_v2(c, hx=34, hy=22 + bob, eye_state="wide", look_dir="forward",
                     mouth="grin", eyebrow="normal", hair_bob=-1 if bob < 0 else 0, hair_wind=1)

        assert any(c.get_pixel(x, 63)[3] > 0 for x in range(64)), f"p1_flashlight_run frame {i} missing y=63 anchor!"
        frames.append(c)

    return frames


# =============================================================================
# 9. P1 BLOWN (8 frames @ 14 fps, loop: false)
# Struck by strong wind gust: knocked backward a step, arms thrown wide,
# sliding back onto heels.
# =============================================================================

def generate_p1_blown() -> List[PixelCanvas]:
    frames = []

    # ---------------- Frame 0: Sudden Impact Blast ----------------
    # Gale strikes chest, torso rocked backward, arms start flaring
    c0 = create_base_canvas()
    draw_wind_streaks(c0, seed=1)
    draw_sneaker_v2(c0, foot_x=26, foot_y=63, pose="flat", is_far=True)
    draw_sneaker_v2(c0, foot_x=38, foot_y=63, pose="flat", is_far=False)
    draw_leg_v2(c0, hip_x=26, hip_y=51, foot_x=26, foot_y=57, is_far=True)
    draw_leg_v2(c0, hip_x=34, hip_y=51, foot_x=38, foot_y=57, is_far=False)
    draw_shorts_v2(c0, sx=30, sy=46, w=18, h=9)
    # Arms blown wide
    draw_arm_v2(c0, shoulder_x=22, shoulder_y=32, hand_x=14, hand_y=28, is_far=True)
    draw_hoodie_v2(c0, tx=28, ty=32, w=20, h=15, drawstring_wind=-3)
    draw_arm_v2(c0, shoulder_x=36, shoulder_y=32, hand_x=48, hand_y=28, is_far=False)
    draw_head_v2(c0, hx=27, hy=22, eye_state="wide", look_dir="forward", mouth="o", eyebrow="raised", hair_wind=1)
    assert any(c0.get_pixel(x, 63)[3] > 0 for x in range(64)), "p1_blown frame 0 missing y=63 anchor!"
    frames.append(c0)

    # ---------------- Frame 1: Knocked Backward onto Heels ----------------
    # Tilted back onto heels at row y=63, arms thrown wide open
    c1 = create_base_canvas()
    draw_wind_streaks(c1, seed=2)
    # Both sneakers in heel_strike on row 63
    draw_sneaker_v2(c1, foot_x=24, foot_y=63, pose="heel_strike", is_far=True)
    draw_sneaker_v2(c1, foot_x=36, foot_y=63, pose="heel_strike", is_far=False)
    draw_leg_v2(c1, hip_x=24, hip_y=52, foot_x=24, foot_y=57, is_far=True)
    draw_leg_v2(c1, hip_x=32, hip_y=52, foot_x=36, foot_y=57, is_far=False)
    draw_shorts_v2(c1, sx=28, sy=47, w=18, h=8)
    draw_arm_v2(c1, shoulder_x=20, shoulder_y=34, hand_x=10, hand_y=24, is_far=True)
    draw_hoodie_v2(c1, tx=25, ty=34, w=20, h=14, drawstring_wind=-4)
    draw_arm_v2(c1, shoulder_x=34, shoulder_y=34, hand_x=50, hand_y=24, is_far=False)
    draw_head_v2(c1, hx=22, hy=25, eye_state="oof", look_dir="forward", mouth="open", eyebrow="worried", hair_wind=1)
    assert any(c1.get_pixel(x, 63)[3] > 0 for x in range(64)), "p1_blown frame 1 missing y=63 anchor!"
    frames.append(c1)

    # ---------------- Frame 2: Backward Heel Skid (Peak Velocity) ----------------
    # Sliding backward on heels along floor, skid dust puffs at row 63
    c2 = create_base_canvas()
    draw_wind_streaks(c2, seed=3)
    # Skid dust puffs kicked up to right of heels on row 63
    c2.set_pixel(28, 63, WHITE_SHADOW)
    c2.set_pixel(29, 62, PURE_WHITE)
    c2.set_pixel(40, 63, WHITE_SHADOW)
    c2.set_pixel(41, 62, PURE_WHITE)
    # Heels digging into y=63
    draw_sneaker_v2(c2, foot_x=22, foot_y=63, pose="heel_strike", is_far=True)
    draw_sneaker_v2(c2, foot_x=34, foot_y=63, pose="heel_strike", is_far=False)
    draw_leg_v2(c2, hip_x=21, hip_y=53, foot_x=22, foot_y=57, is_far=True)
    draw_leg_v2(c2, hip_x=29, hip_y=53, foot_x=34, foot_y=57, is_far=False)
    draw_shorts_v2(c2, sx=25, sy=48, w=18, h=8)
    draw_arm_v2(c2, shoulder_x=17, shoulder_y=36, hand_x=8, hand_y=26, is_far=True)
    draw_hoodie_v2(c2, tx=22, ty=36, w=20, h=13, drawstring_wind=-5)
    draw_arm_v2(c2, shoulder_x=31, shoulder_y=36, hand_x=48, hand_y=26, is_far=False)
    draw_head_v2(c2, hx=18, hy=28, eye_state="oof", look_dir="forward", mouth="grimace", eyebrow="furrowed", hair_wind=1)
    assert any(c2.get_pixel(x, 63)[3] > 0 for x in range(64)), "p1_blown frame 2 missing y=63 anchor!"
    frames.append(c2)

    # ---------------- Frame 3: Reaching Back to Catch Fall ----------------
    # Left foot reaches back to catch balance at x=16, y=63
    c3 = create_base_canvas()
    draw_wind_streaks(c3, seed=4)
    draw_sneaker_v2(c3, foot_x=16, foot_y=63, pose="flat", is_far=True)
    draw_sneaker_v2(c3, foot_x=32, foot_y=63, pose="heel_strike", is_far=False)
    draw_leg_v2(c3, hip_x=20, hip_y=54, foot_x=16, foot_y=57, is_far=True)
    draw_leg_v2(c3, hip_x=28, hip_y=54, foot_x=32, foot_y=57, is_far=False)
    draw_shorts_v2(c3, sx=24, sy=50, w=18, h=8)
    # Arms swinging forward to regain balance
    draw_arm_v2(c3, shoulder_x=18, shoulder_y=38, hand_x=22, hand_y=36, is_far=True)
    draw_hoodie_v2(c3, tx=23, ty=38, w=20, h=14, drawstring_wind=-2)
    draw_arm_v2(c3, shoulder_x=32, shoulder_y=38, hand_x=40, hand_y=36, is_far=False)
    draw_head_v2(c3, hx=22, hy=29, eye_state="oof", look_dir="forward", mouth="grimace", eyebrow="worried")
    assert any(c3.get_pixel(x, 63)[3] > 0 for x in range(64)), "p1_blown frame 3 missing y=63 anchor!"
    frames.append(c3)

    # ---------------- Frame 4: Deep Absorbing Crouch ----------------
    # Low absorbing crouch, feet braced on row 63
    c4 = create_base_canvas()
    draw_sneaker_v2(c4, foot_x=18, foot_y=63, pose="squash", is_far=True)
    draw_sneaker_v2(c4, foot_x=34, foot_y=63, pose="flat", is_far=False)
    draw_leg_v2(c4, hip_x=21, hip_y=54, foot_x=18, foot_y=59, is_far=True)
    draw_leg_v2(c4, hip_x=29, hip_y=54, foot_x=34, foot_y=57, is_far=False)
    draw_shorts_v2(c4, sx=25, sy=51, w=20, h=8)
    # Arms forward for counter-balance
    draw_arm_v2(c4, shoulder_x=19, shoulder_y=40, hand_x=24, hand_y=44, is_far=True)
    draw_hoodie_v2(c4, tx=25, ty=39, w=22, h=14, folds=-1)
    draw_arm_v2(c4, shoulder_x=33, shoulder_y=40, hand_x=40, hand_y=44, is_far=False)
    draw_head_v2(c4, hx=26, hy=30, eye_state="wide", look_dir="forward", mouth="o", eyebrow="worried")
    assert any(c4.get_pixel(x, 63)[3] > 0 for x in range(64)), "p1_blown frame 4 missing y=63 anchor!"
    frames.append(c4)

    # ---------------- Frame 5: Pushing Back Up Against Breeze ----------------
    # Straightening legs, one arm shielding, feet on y=63
    c5 = create_base_canvas()
    draw_sneaker_v2(c5, foot_x=22, foot_y=63, pose="flat", is_far=True)
    draw_sneaker_v2(c5, foot_x=36, foot_y=63, pose="flat", is_far=False)
    draw_leg_v2(c5, hip_x=24, hip_y=52, foot_x=22, foot_y=57, is_far=True)
    draw_leg_v2(c5, hip_x=32, hip_y=52, foot_x=36, foot_y=57, is_far=False)
    draw_shorts_v2(c5, sx=28, sy=47, w=18, h=9)
    # Shielding arm
    draw_arm_v2(c5, shoulder_x=21, shoulder_y=35, hand_x=18, hand_y=42, is_far=True)
    draw_hoodie_v2(c5, tx=28, ty=34, w=20, h=15)
    draw_arm_v2(c5, shoulder_x=35, shoulder_y=35, hand_x=38, hand_y=26, is_far=False)
    draw_head_v2(c5, hx=30, hy=25, eye_state="normal", look_dir="forward", mouth="grimace", eyebrow="furrowed")
    assert any(c5.get_pixel(x, 63)[3] > 0 for x in range(64)), "p1_blown frame 5 missing y=63 anchor!"
    frames.append(c5)

    # ---------------- Frame 6: Stepping Forward Defiantly ----------------
    # Taking a step forward on y=63, shaking off gust
    c6 = create_base_canvas()
    draw_sneaker_v2(c6, foot_x=24, foot_y=63, pose="flat", is_far=True)
    draw_sneaker_v2(c6, foot_x=38, foot_y=63, pose="flat", is_far=False)
    draw_leg_v2(c6, hip_x=26, hip_y=52, foot_x=24, foot_y=57, is_far=True)
    draw_leg_v2(c6, hip_x=34, hip_y=52, foot_x=38, foot_y=57, is_far=False)
    draw_shorts_v2(c6, sx=30, sy=45, w=18, h=9)
    draw_arm_v2(c6, shoulder_x=22, shoulder_y=33, hand_x=20, hand_y=42, is_far=True)
    draw_hoodie_v2(c6, tx=30, ty=32, w=20, h=15)
    draw_arm_v2(c6, shoulder_x=36, shoulder_y=33, hand_x=40, hand_y=38, is_far=False)
    draw_head_v2(c6, hx=31, hy=23, eye_state="normal", look_dir="forward", mouth="smirk", eyebrow="normal")
    assert any(c6.get_pixel(x, 63)[3] > 0 for x in range(64)), "p1_blown frame 6 missing y=63 anchor!"
    frames.append(c6)

    # ---------------- Frame 7: Settled Ready Stance, Cocky Defiance ----------------
    # Wiping dust from cheek/nose with sleeve, feet flat on y=63
    c7 = create_base_canvas()
    draw_sneaker_v2(c7, foot_x=26, foot_y=63, pose="flat", is_far=True)
    draw_sneaker_v2(c7, foot_x=38, foot_y=63, pose="flat", is_far=False)
    draw_leg_v2(c7, hip_x=28, hip_y=52, foot_x=26, foot_y=57, is_far=True)
    draw_leg_v2(c7, hip_x=36, hip_y=52, foot_x=38, foot_y=57, is_far=False)
    draw_shorts_v2(c7, sx=32, sy=45, w=18, h=9)
    # Wipes cheek with near sleeve
    draw_arm_v2(c7, shoulder_x=24, shoulder_y=33, hand_x=22, hand_y=42, is_far=True)
    draw_hoodie_v2(c7, tx=32, ty=31, w=20, h=15)
    draw_arm_v2(c7, shoulder_x=40, shoulder_y=33, hand_x=36, hand_y=26, is_far=False)
    draw_head_v2(c7, hx=32, hy=22, eye_state="normal", look_dir="forward", mouth="smirk", eyebrow="normal")
    assert any(c7.get_pixel(x, 63)[3] > 0 for x in range(64)), "p1_blown frame 7 missing y=63 anchor!"
    frames.append(c7)

    return frames


# =============================================================================
# MAIN BUILDER & INTEGRATION PIPELINE
# =============================================================================

REACTION_SPECS = {
    "p1_slip.png":            (generate_p1_slip, 64, 64, 8, 14, False),
    "p1_slog.png":            (generate_p1_slog, 64, 64, 8, 10, True),
    "p1_lean.png":            (generate_p1_lean, 64, 64, 6, 12, True),
    "p1_ouch.png":            (generate_p1_ouch, 64, 64, 8, 14, False),
    "p1_stuck.png":           (generate_p1_stuck, 64, 64, 8, 10, True),
    "p1_sprint.png":          (generate_p1_sprint, 64, 64, 8, 28, True),
    "p1_flashlight_idle.png": (generate_p1_flashlight_idle, 64, 64, 8, 8, True),
    "p1_flashlight_run.png":  (generate_p1_flashlight_run, 64, 64, 12, 20, True),
    "p1_blown.png":           (generate_p1_blown, 64, 64, 8, 14, False),
}


def build_reactions(output_dir: str = "art/v2"):
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    print(f"=== Generating 9 Player 1 Hazard Reaction Sheets into {out_path} ===")

    manifest_file = out_path / "manifest.json"
    manifest = {}
    if manifest_file.exists():
        with open(manifest_file, "r") as f:
            manifest = json.load(f)

    for filename, (gen_fn, fw, fh, num_frames, fps, loop) in REACTION_SPECS.items():
        print(f"Drawing {filename} ({num_frames} frames @ {fps} fps)...")
        frames = gen_fn()
        assert len(frames) == num_frames, f"{filename}: expected {num_frames} frames, got {len(frames)}"

        # Strict check on y=63 ground contact on every frame
        for f_idx, fr in enumerate(frames):
            has_contact = any(fr.get_pixel(x, 63)[3] > 0 for x in range(64))
            assert has_contact, f"CRITICAL ERROR: {filename} frame {f_idx} has NO PIXELS at row y=63!"

        file_path = str(out_path / filename)
        assemble_strip(frames, file_path)

        manifest[filename] = {
            "frame_w": fw,
            "frame_h": fh,
            "frames": num_frames,
            "fps": fps,
            "loop": loop
        }

    # Save manifest.json
    with open(manifest_file, "w") as f:
        json.dump(manifest, f, indent=1)
    print(f"Updated {manifest_file} with {len(manifest)} total entries.")

    # Regenerate scripts/art_data.gd
    gen_art_script = Path("tools/gen_art_data.py")
    if gen_art_script.exists():
        import subprocess
        subprocess.run(["python3", str(gen_art_script)], check=True)
        print("Regenerated scripts/art_data.gd successfully.")


if __name__ == "__main__":
    build_reactions()

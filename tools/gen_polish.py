"""Younger Sibling Simulator - Extra Polish (Parent Peek Generator)."""

import math
from typing import List
from canvas import PixelCanvas, assemble_strip
from palette import (
    TRANSPARENT, OUTLINE,
    SHADOW_DEEP, SHADOW_MID, PURPLE_MID, PURPLE_LIGHT,
    DUSK_PINK,
    SKIN_SHADOW, SKIN_MID,
    BROWN_DARKEST, BROWN_DARK, BROWN_MID, WOOD_HIGHLIGHT,
    RED_SHADOW, RED_MID, RED_LIGHT,
    YELLOW_SHADOW, YELLOW_MID, YELLOW_LIGHT,
    WHITE_SHADOW, PURE_WHITE,
    VOID_BLACK
)


def generate_parent_peek() -> List[PixelCanvas]:
    """
    64x96, 6 frames, fps 6 -> 384x96 px strip.
    Parent silhouette peeking through cracked door for trouble screen,
    with dramatic cracked door on right, bright hallway light beam,
    imposing bathrobe silhouette with curlers, angry glowing red eye,
    and GIANT animated pointing finger shaking up and down with comic anger steam marks!
    """
    frames = []
    # Dynamic shaking offsets for the giant pointing finger
    finger_y_offsets = [0, -3, 2, -2, 3, 0]

    for i in range(6):
        c = PixelCanvas(64, 96, TRANSPARENT)
        fy = 48 + finger_y_offsets[i]

        # 1. Door frame / wall molding on right edge (x=56..63)
        c.rect(56, 0, 8, 96, BROWN_MID, outline=OUTLINE)
        c.line(56, 0, 56, 95, WOOD_HIGHLIGHT)
        c.line(62, 0, 62, 95, BROWN_DARKEST)
        c.line(63, 0, 63, 95, VOID_BLACK)

        # 2. Cracked open wooden door slab (x=door_x..56)
        door_x = 42 + (i % 2)  # subtle 1px door vibration
        c.rect(door_x, 0, 56 - door_x, 96, BROWN_DARKEST)
        # Inner vertical edge of door catching blazing hallway light
        c.line(door_x, 0, door_x, 95, WOOD_HIGHLIGHT)
        c.set_pixel(door_x, 0, PURE_WHITE)
        c.set_pixel(door_x, 48, PURE_WHITE)
        # Recessed wood panel detailing on the door slab
        for py0, py1 in [(8, 38), (54, 88)]:
            if 54 > door_x + 3:
                c.rect(door_x + 3, py0, 52 - door_x, py1 - py0, BROWN_DARK, outline=OUTLINE)
        # Brass door knob
        c.rect(door_x + 2, 50, 3, 4, YELLOW_MID, outline=OUTLINE)
        c.set_pixel(door_x + 3, 51, YELLOW_LIGHT)
        c.set_pixel(door_x + 3, 53, YELLOW_SHADOW)

        # 3. Blinding hallway light beam pouring into dark bedroom
        # Spreads diagonally from the door opening across the room & floor
        for y in range(96):
            # Light width expands toward the bottom
            beam_left = max(6, int(door_x - 18 - (y * 0.18)))
            for x in range(beam_left, door_x):
                # Light intensity ramp
                dist_from_door = door_x - x
                if dist_from_door < 6:
                    c.set_pixel(x, y, YELLOW_LIGHT)
                elif dist_from_door < 14:
                    c.set_pixel(x, y, YELLOW_LIGHT if (x + y) % 2 == 0 else YELLOW_MID)
                elif dist_from_door < 22:
                    if (x + y) % 2 == 0:
                        c.set_pixel(x, y, YELLOW_MID)
                    elif (x + y) % 4 == 0:
                        c.set_pixel(x, y, YELLOW_SHADOW)
                elif (x + y) % 4 == 0:
                    c.set_pixel(x, y, YELLOW_SHADOW)

        # Bedroom floorboards illuminated by light puddle (y=80..95)
        for y in range(80, 96):
            for x in range(8, door_x):
                if (x + y) % 3 == 0 and c.get_pixel(x, y) == TRANSPARENT:
                    c.set_pixel(x, y, WOOD_HIGHLIGHT if y % 4 == 0 else BROWN_DARK)

        # 4. Imposing Parent Silhouette in doorway (x=22..46)
        # Towering bathrobe body
        for y in range(28, 92):
            bw = int(12 + (y - 28) * 0.22)
            bx0 = 34 - (bw // 2)
            bx1 = bx0 + bw
            c.rect(bx0, y, bw, 1, OUTLINE)
            # Bathrobe shadow volume
            c.rect(bx0 + 2, y, max(1, bw - 4), 1, SHADOW_DEEP)
            # Hallway rim-light on back edge (right)
            c.set_pixel(bx1 - 1, y, YELLOW_LIGHT)
            c.set_pixel(bx1 - 2, y, YELLOW_MID)

        # Bathrobe sash / belt tied at waist (y=52..56)
        c.rect(26, 52, 16, 3, SHADOW_MID, outline=OUTLINE)
        c.line(28, 55, 30, 62, PURPLE_LIGHT)  # knotted rope drop
        c.line(29, 55, 31, 64, OUTLINE)

        # Head silhouette (centered at (32, 20), radius 8)
        c.circle(32, 20, 8, OUTLINE)
        c.circle(32, 20, 6, SHADOW_DEEP)
        # Hallway rim-light on back of head
        c.line(39, 16, 40, 24, YELLOW_LIGHT)
        c.line(38, 14, 39, 22, YELLOW_MID)

        # 4 Curlers / Rollers in hair
        curlers = [
            (26, 11),  # top-front
            (32, 9),   # top-center
            (38, 11),  # top-back
            (41, 17),  # side-back
        ]
        for cx, cy in curlers:
            c.rect(cx - 2, cy - 2, 4, 3, PURPLE_LIGHT, outline=OUTLINE)
            c.set_pixel(cx - 1, cy - 1, DUSK_PINK)
            c.set_pixel(cx + 1, cy - 1, YELLOW_LIGHT)  # rim catch-light

        # Angry glowing red eye glaring in shadow at (26, 20)
        c.set_pixel(26, 20, RED_LIGHT)
        c.set_pixel(27, 20, RED_MID)
        c.set_pixel(26, 19, OUTLINE)  # angry brow ridge over eye
        c.set_pixel(27, 19, OUTLINE)
        c.set_pixel(25, 20, RED_SHADOW)
        # Eye glare streak when shaking with anger (frames 1, 3, 4)
        if i in (1, 3, 4):
            c.line(21, 20, 24, 20, RED_LIGHT)
            c.set_pixel(20, 20, RED_MID)

        # 5. GIANT ANGRY POINTING FINGER extending LEFT into bedroom!
        # Sleeve reaching from bathrobe
        c.rect(26, fy - 3, 8, 9, OUTLINE)
        c.rect(27, fy - 2, 6, 7, SHADOW_DEEP)
        c.line(26, fy - 3, 26, fy + 5, PURPLE_LIGHT)  # sleeve cuff rim

        # Forearm / wrist
        c.rect(20, fy - 2, 7, 7, SHADOW_DEEP, outline=OUTLINE)

        # Giant Clenched Fist (x=16..22, y=fy-1..fy+7)
        c.rect(16, fy - 1, 6, 8, SHADOW_DEEP, outline=OUTLINE)
        # Knuckles of curled fingers (middle, ring, pinky) tucked underneath
        for ky in [fy + 2, fy + 4, fy + 6]:
            c.line(16, ky, 21, ky, OUTLINE)
            c.set_pixel(17, ky - 1, PURPLE_LIGHT)
            c.set_pixel(18, ky - 1, SKIN_SHADOW)

        # GIANT ACCUSATORY INDEX FINGER extending dramatically LEFT to x=3!
        # Finger body: length 15px, thickness 5px (y=fy-2..fy+2)
        c.rect(3, fy - 2, 14, 5, SHADOW_DEEP, outline=OUTLINE)
        # Top rim-light along the entire length of the giant finger
        c.line(4, fy - 2, 16, fy - 2, PURPLE_LIGHT)
        c.line(4, fy - 1, 16, fy - 1, SKIN_MID)
        # Dark underside shadow
        c.line(3, fy + 2, 16, fy + 2, OUTLINE)
        # Rounded fingertip pointing left at player
        c.set_pixel(3, fy - 1, OUTLINE)
        c.set_pixel(3, fy, PURPLE_LIGHT)
        c.set_pixel(3, fy + 1, OUTLINE)
        c.set_pixel(2, fy, OUTLINE)
        # Fingernail accent at tip
        c.set_pixel(5, fy - 1, WHITE_SHADOW)
        c.set_pixel(6, fy - 1, WHITE_SHADOW)

        # 6. Comic anger steam marks & popping cross-veins over head
        # Animated steam puffs venting upward
        if i in (0, 5):
            # Small steam puff
            c.circle(28, 6, 2, WHITE_SHADOW)
            c.set_pixel(28, 6, PURE_WHITE)
        elif i in (1, 2):
            # Expanding explosive steam cloud
            c.circle(26, 4, 3, WHITE_SHADOW)
            c.circle(26, 4, 2, PURE_WHITE)
            c.circle(31, 3, 2, WHITE_SHADOW)
            c.set_pixel(31, 3, PURE_WHITE)
            # Red anger cross-vein pop mark!
            c.line(35, 3, 39, 3, RED_LIGHT)
            c.line(35, 5, 39, 5, RED_LIGHT)
            c.line(36, 2, 36, 6, RED_LIGHT)
            c.line(38, 2, 38, 6, RED_LIGHT)
            c.set_pixel(37, 4, RED_MID)
        elif i in (3, 4):
            # Dual venting steam jets + pulsating anger marks
            c.circle(24, 3, 2, WHITE_SHADOW)
            c.set_pixel(24, 3, PURE_WHITE)
            c.circle(33, 2, 3, WHITE_SHADOW)
            c.circle(33, 2, 2, PURE_WHITE)
            # Sharp red tick mark
            c.line(20, 6, 23, 9, RED_MID)
            c.line(23, 6, 20, 9, RED_MID)
            c.set_pixel(21, 7, RED_LIGHT)
            c.set_pixel(22, 8, RED_LIGHT)

        frames.append(c)

    return frames


def generate_all_polish():
    assemble_strip(generate_parent_peek(), "art/incoming/parent_peek.png")


if __name__ == "__main__":
    generate_all_polish()

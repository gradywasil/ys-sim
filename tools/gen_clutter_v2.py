"""Younger Sibling Simulator - Floor Clutter v2 Generator.

Generates 21 distinct floor clutter items (deco_*.png) and matching 1-bit shadow
sprites (deco_*_shadow.png) in art/v2/:
 1. sock
 2. cereal_bowl
 3. toy_car
 4. controller
 5. sneaker
 6. juice_box
 7. crayons
 8. marble
 9. pizza
10. slime
11. pencil
12. bouncy_ball
13. coin
14. cassette
15. action_figure
16. battery
17. paper_plane
18. yo_yo
19. rubiks_cube
20. candy_wrapper
21. dice
"""

import math
from typing import Tuple, Dict, Callable
from canvas import PixelCanvas
from palette import (
    TRANSPARENT, OUTLINE, VOID_BLACK,
    SHADOW_DEEP, SHADOW_MID, SHADOW_PURPLE_DARK, PURPLE_DARK, PURPLE_MID, PURPLE_LIGHT,
    DUSK_LILAC, DUSK_PINK, DUSK_ROSE, DUSK_PEACH, DUSK_BLUSH, DUSK_CREAM,
    SKIN_DEEP, SKIN_SHADOW, SKIN_MID, SKIN_LIGHT, SKIN_HIGHLIGHT,
    WOOD_BLACK, BROWN_DARKEST, BROWN_DARK, BROWN_MID, BROWN_LIGHT, WOOD_HIGHLIGHT, WOOD_LIT,
    RED_DEEP, RED_SHADOW, RED_RICH, RED_MID, RED_LIGHT, RED_HIGHLIGHT,
    BLUE_DEEP, BLUE_SHADOW, BLUE_RICH, BLUE_MID, BLUE_LIGHT, BLUE_HIGHLIGHT,
    YELLOW_DEEP, YELLOW_SHADOW, YELLOW_RICH, YELLOW_MID, YELLOW_LIGHT, YELLOW_HIGHLIGHT,
    GREEN_DEEP, GREEN_SHADOW, GREEN_RICH, GREEN_MID, GREEN_LIGHT, GREEN_HIGHLIGHT,
    ORANGE_DEEP, ORANGE_SHADOW, ORANGE_MID, ORANGE_LIGHT,
    TEAL_SHADOW, TEAL_MID, TEAL_LIGHT, TEAL_HIGHLIGHT,
    METAL_SHADOW, METAL_MID, WHITE_SHADOW, WHITE_MID, PURE_WHITE
)


def make_shadow(w: int, h: int, cx: int, cy: int, rx: int, ry: int) -> PixelCanvas:
    """Creates matching 1-bit hard-banded shadow sprite in OUTLINE color."""
    c = PixelCanvas(w, h, TRANSPARENT)
    for y in range(max(0, cy - ry), min(h, cy + ry + 1)):
        for x in range(max(0, cx - rx), min(w, cx + rx + 1)):
            dx = (x - cx) / float(rx)
            dy = (y - cy) / float(ry)
            if dx * dx + dy * dy <= 1.0:
                c.set_pixel(x, y, OUTLINE)
    return c


# ==============================================================================
# ITEM DRAWING FUNCTIONS
# ==============================================================================

def draw_sock() -> Tuple[PixelCanvas, PixelCanvas]:
    """36x24. Wrinkled striped tube sock lying on floor."""
    w, h = 36, 24
    c = PixelCanvas(w, h, TRANSPARENT)

    # Folded sock body
    # Ankle cuff on left
    c.rect(4, 8, 8, 12, PURE_WHITE, outline=OUTLINE)
    c.line(4, 10, 11, 10, BLUE_MID)
    c.line(4, 14, 11, 14, RED_MID)
    c.line(4, 18, 11, 18, BLUE_MID)

    # Foot section trailing right onto floor
    c.polygon([(10, 12), (28, 12), (32, 16), (32, 21), (10, 21)], PURE_WHITE, outline=OUTLINE)
    # Heel patch
    c.circle(11, 19, 3, RED_SHADOW, outline=OUTLINE)
    # Red & Blue candy stripes across foot
    c.line(16, 12, 16, 21, RED_MID)
    c.line(17, 12, 17, 21, RED_MID)
    c.line(22, 12, 22, 21, BLUE_MID)
    c.line(23, 12, 23, 21, BLUE_MID)
    c.line(27, 13, 27, 21, RED_MID)

    # Toe cap
    c.polygon([(29, 14), (32, 16), (32, 21), (29, 21)], RED_SHADOW, outline=OUTLINE)
    # Shadow and fold shading
    c.line(12, 21, 31, 21, WHITE_SHADOW)
    c.line(14, 15, 20, 15, WHITE_SHADOW)

    s = make_shadow(w, h, 20, 22, 13, 2)
    return c, s


def draw_cereal_bowl() -> Tuple[PixelCanvas, PixelCanvas]:
    """52x32. Blue bowl with spilled milk and fruit cereal loops."""
    w, h = 52, 32
    c = PixelCanvas(w, h, TRANSPARENT)

    # Spilled milk puddle on floor (y=22..30, x=4..46)
    c.polygon([
        (6, 26), (14, 23), (28, 22), (44, 25), (48, 28),
        (42, 30), (24, 30), (10, 29)
    ], PURE_WHITE, outline=OUTLINE)
    c.line(8, 28, 38, 28, WHITE_SHADOW)

    # Floating cereal loops in the spilled puddle
    c.circle(12, 26, 2, RED_MID, outline=OUTLINE)
    c.circle(20, 27, 2, YELLOW_MID, outline=OUTLINE)
    c.circle(42, 27, 2, GREEN_MID, outline=OUTLINE)
    c.circle(36, 24, 2, ORANGE_MID, outline=OUTLINE)

    # Blue ceramic/plastic cereal bowl (x=16..46, y=6..25)
    c.polygon([
        (18, 12), (20, 24), (42, 24), (44, 12)
    ], BLUE_MID, outline=OUTLINE)
    c.line(20, 24, 42, 24, BLUE_SHADOW)
    c.line(19, 13, 43, 13, BLUE_LIGHT)

    # Bowl rim oval
    for y in range(7, 14):
        for x in range(17, 45):
            dx = (x - 31) / 13.0
            dy = (y - 10) / 3.0
            if dx * dx + dy * dy <= 1.0:
                c.set_pixel(x, y, PURE_WHITE)
            elif dx * dx + dy * dy <= 1.3:
                c.set_pixel(x, y, OUTLINE)

    # Cereal loops inside the bowl
    c.circle(26, 10, 2, RED_MID, outline=OUTLINE)
    c.circle(31, 9, 2, YELLOW_MID, outline=OUTLINE)
    c.circle(36, 10, 2, GREEN_MID, outline=OUTLINE)
    c.circle(29, 11, 2, BLUE_RICH, outline=OUTLINE)
    c.circle(34, 11, 2, ORANGE_MID, outline=OUTLINE)

    s = make_shadow(w, h, 28, 30, 20, 2)
    return c, s


def draw_toy_car() -> Tuple[PixelCanvas, PixelCanvas]:
    """54x30. Red toy roadster muscle car with yellow flame decals."""
    w, h = 54, 30
    c = PixelCanvas(w, h, TRANSPARENT)

    # Car body silhouette
    # Main lower chassis
    c.rect(6, 16, 42, 9, RED_MID, outline=OUTLINE)
    # Hood & roof cabin
    c.polygon([(18, 16), (24, 8), (38, 8), (42, 16)], RED_MID, outline=OUTLINE)
    c.line(24, 8, 38, 8, RED_LIGHT)
    c.line(7, 16, 47, 16, RED_LIGHT)

    # Windshield and side window
    c.polygon([(26, 9), (30, 9), (30, 15), (22, 15)], BLUE_LIGHT, outline=OUTLINE)
    c.line(25, 10, 28, 10, PURE_WHITE)  # glass gleam
    c.polygon([(32, 9), (36, 9), (38, 15), (32, 15)], BLUE_MID, outline=OUTLINE)

    # Yellow flame decal on side door
    c.polygon([(20, 18), (32, 18), (28, 21), (22, 21)], YELLOW_MID)
    c.set_pixel(33, 18, YELLOW_LIGHT)
    c.set_pixel(31, 19, YELLOW_LIGHT)

    # Chrome front bumper & headlights
    c.rect(46, 18, 3, 5, METAL_MID, outline=OUTLINE)
    c.circle(46, 18, 2, YELLOW_LIGHT, outline=OUTLINE)
    # Rear spoiler
    c.line(7, 12, 12, 12, RED_MID)
    c.line(7, 12, 7, 16, OUTLINE)

    # 2 Big black wheels with silver hubcaps
    # Front wheel at x=38, rear at x=14
    for wx in [14, 38]:
        c.circle(wx, 24, 5, WOOD_BLACK, outline=OUTLINE)
        c.circle(wx, 24, 2, METAL_MID, outline=OUTLINE)
        c.set_pixel(wx, 24, PURE_WHITE)

    s = make_shadow(w, h, 26, 28, 22, 2)
    return c, s


def draw_controller() -> Tuple[PixelCanvas, PixelCanvas]:
    """56x36. Retro gamepad with curly wire cord."""
    w, h = 56, 36
    c = PixelCanvas(w, h, TRANSPARENT)

    # Curly wire cord trailing off to the top-right
    cord_pts = [
        (28, 14), (32, 8), (40, 6), (46, 10), (52, 6), (54, 2)
    ]
    for i in range(len(cord_pts) - 1):
        c.line(cord_pts[i][0], cord_pts[i][1], cord_pts[i+1][0], cord_pts[i+1][1], PURPLE_DARK)
        c.line(cord_pts[i][0], cord_pts[i][1] + 1, cord_pts[i+1][0], cord_pts[i+1][1] + 1, OUTLINE)

    # Gamepad main body (rounded rectangle)
    c.rect(6, 14, 44, 18, METAL_SHADOW, outline=OUTLINE)
    # Bevel highlight on top, shadow on bottom
    c.line(7, 15, 48, 15, METAL_MID)
    c.line(7, 15, 7, 30, METAL_MID)
    c.line(7, 31, 48, 31, PURPLE_DARK)
    c.line(49, 15, 49, 31, PURPLE_DARK)

    # Ergonomic side grip cutouts
    c.circle(12, 28, 4, METAL_SHADOW, outline=OUTLINE)
    c.circle(44, 28, 4, METAL_SHADOW, outline=OUTLINE)

    # D-pad on left (x=12..20, y=19..27)
    c.rect(14, 19, 4, 8, OUTLINE)
    c.rect(12, 21, 8, 4, OUTLINE)
    c.set_pixel(15, 20, PURPLE_MID)
    c.set_pixel(15, 25, PURPLE_MID)
    c.set_pixel(13, 22, PURPLE_MID)
    c.set_pixel(18, 22, PURPLE_MID)

    # Select / Start buttons in center
    c.line(24, 25, 27, 25, OUTLINE)
    c.line(29, 25, 32, 25, OUTLINE)

    # 4 Colored action buttons in diamond arrangement on right
    c.set_pixel(40, 19, YELLOW_MID)  # Top
    c.set_pixel(40, 20, OUTLINE)
    c.set_pixel(37, 22, BLUE_MID)    # Left
    c.set_pixel(37, 23, OUTLINE)
    c.set_pixel(43, 22, RED_MID)     # Right
    c.set_pixel(43, 23, OUTLINE)
    c.set_pixel(40, 25, GREEN_MID)   # Bottom
    c.set_pixel(40, 26, OUTLINE)

    s = make_shadow(w, h, 28, 33, 22, 2)
    return c, s


def draw_sneaker() -> Tuple[PixelCanvas, PixelCanvas]:
    """52x32. High-top retro canvas sneaker lying flat."""
    w, h = 52, 32
    c = PixelCanvas(w, h, TRANSPARENT)

    # Blue canvas shoe upper
    # Ankle collar
    c.polygon([(8, 10), (22, 10), (22, 18), (8, 18)], BLUE_MID, outline=OUTLINE)
    c.line(8, 10, 22, 10, BLUE_LIGHT)
    # Foot vamp reaching forward
    c.polygon([(10, 16), (40, 16), (44, 24), (10, 24)], BLUE_MID, outline=OUTLINE)

    # Red circular ankle star patch
    c.circle(15, 14, 3, PURE_WHITE, outline=OUTLINE)
    c.set_pixel(15, 14, RED_MID)

    # White tongue & laces
    c.line(22, 11, 30, 17, PURE_WHITE)
    for lx in [20, 24, 28, 32]:
        c.line(lx, 15, lx + 2, 18, PURE_WHITE)
        c.set_pixel(lx + 1, 16, OUTLINE)

    # Rubber white toe cap bumper
    c.polygon([(40, 18), (48, 22), (48, 27), (40, 27)], PURE_WHITE, outline=OUTLINE)
    c.line(40, 20, 46, 23, WHITE_SHADOW)

    # Thick white rubber sole (y=24..29)
    c.rect(8, 24, 42, 6, PURE_WHITE, outline=OUTLINE)
    c.line(8, 26, 48, 26, RED_MID)  # sporty red sole stripe
    c.line(8, 29, 48, 29, WHITE_SHADOW)  # bottom tread shadow

    s = make_shadow(w, h, 28, 30, 22, 2)
    return c, s


def draw_juice_box() -> Tuple[PixelCanvas, PixelCanvas]:
    """32x40. Juice box with bent straw."""
    w, h = 32, 40
    c = PixelCanvas(w, h, TRANSPARENT)

    # Bent plastic straw sticking out top (x=16..24, y=4..16)
    # Vertical segment
    c.line(16, 12, 16, 17, PURE_WHITE)
    c.line(17, 12, 17, 17, WHITE_SHADOW)
    # 45-degree bend
    c.line(16, 12, 24, 4, PURE_WHITE)
    c.line(17, 13, 25, 5, OUTLINE)
    c.line(15, 12, 23, 4, OUTLINE)
    # Straw hole foil seal
    c.circle(16, 17, 2, METAL_MID, outline=OUTLINE)

    # Isometric top face of juice box
    c.polygon([(6, 17), (16, 13), (26, 17), (16, 21)], ORANGE_LIGHT, outline=OUTLINE)

    # Front face of juice box (y=21..37)
    c.polygon([(6, 21), (20, 21), (20, 38), (6, 38)], ORANGE_MID, outline=OUTLINE)
    # Side shadow face
    c.polygon([(20, 21), (26, 17), (26, 34), (20, 38)], ORANGE_SHADOW, outline=OUTLINE)

    # Fruit illustration / punch graphic on front
    c.circle(13, 28, 4, RED_MID, outline=OUTLINE)
    c.set_pixel(13, 25, GREEN_MID)  # fruit leaf
    c.line(8, 34, 18, 34, YELLOW_MID)  # text stripe

    s = make_shadow(w, h, 16, 38, 12, 2)
    return c, s


def draw_crayons() -> Tuple[PixelCanvas, PixelCanvas]:
    """48x26. Open crayon box with spilled wax crayons."""
    w, h = 48, 26
    c = PixelCanvas(w, h, TRANSPARENT)

    # Tipped crayon box on left (green/yellow box)
    c.polygon([(6, 8), (20, 6), (22, 22), (8, 24)], GREEN_MID, outline=OUTLINE)
    c.polygon([(8, 12), (20, 10), (21, 16), (9, 18)], YELLOW_MID)
    c.line(6, 8, 20, 6, GREEN_LIGHT)

    # Spilled crayons rolling out to the right
    # Red crayon
    c.rect(20, 12, 18, 3, RED_MID, outline=OUTLINE)
    c.polygon([(38, 12), (42, 13), (38, 15)], RED_MID, outline=OUTLINE)  # tip
    c.line(26, 12, 32, 12, PURE_WHITE)  # paper band

    # Blue crayon
    c.rect(18, 17, 20, 3, BLUE_MID, outline=OUTLINE)
    c.polygon([(38, 17), (43, 18), (38, 20)], BLUE_MID, outline=OUTLINE)
    c.line(24, 17, 30, 17, PURE_WHITE)

    # Yellow crayon rolling slightly forward
    c.rect(16, 21, 22, 3, YELLOW_MID, outline=OUTLINE)
    c.polygon([(38, 21), (44, 22), (38, 24)], YELLOW_MID, outline=OUTLINE)
    c.line(22, 21, 28, 21, PURE_WHITE)

    s = make_shadow(w, h, 26, 24, 20, 2)
    return c, s


def draw_marble() -> Tuple[PixelCanvas, PixelCanvas]:
    """24x24. Glass cat-eye swirl marble."""
    w, h = 24, 24
    c = PixelCanvas(w, h, TRANSPARENT)

    cx, cy, r = 12, 12, 9
    c.circle(cx, cy, r, TEAL_MID, outline=OUTLINE)

    # Glass depth shading
    c.circle(cx - 2, cy - 2, r - 3, TEAL_LIGHT)

    # Inner cat-eye swirl ribbon (orange/yellow helix)
    c.polygon([
        (cx - 4, cy + 5), (cx - 1, cy), (cx + 4, cy - 4),
        (cx + 2, cy - 2), (cx - 1, cy + 2), (cx - 3, cy + 6)
    ], ORANGE_MID)
    c.line(cx - 1, cy, cx + 3, cy - 3, YELLOW_LIGHT)

    # Specular glass glints
    c.set_pixel(cx - 4, cy - 5, PURE_WHITE)
    c.set_pixel(cx - 3, cy - 5, PURE_WHITE)
    c.set_pixel(cx - 4, cy - 4, PURE_WHITE)
    c.set_pixel(cx + 4, cy + 5, TEAL_HIGHLIGHT)

    s = make_shadow(w, h, 12, 22, 8, 2)
    return c, s


def draw_pizza() -> Tuple[PixelCanvas, PixelCanvas]:
    """56x34. Pepperoni pizza slice on a paper plate."""
    w, h = 56, 34
    c = PixelCanvas(w, h, TRANSPARENT)

    # White scalloped paper plate
    c.circle(28, 20, 16, PURE_WHITE, outline=OUTLINE)
    c.circle(28, 20, 14, WHITE_SHADOW)
    c.circle(28, 20, 12, PURE_WHITE)

    # Golden browned crust at the back
    c.polygon([(16, 12), (38, 12), (36, 16), (18, 16)], BROWN_LIGHT, outline=OUTLINE)
    c.line(17, 13, 37, 13, WOOD_HIGHLIGHT)

    # Cheese slice triangle tapering down to the tip at (27, 28)
    c.polygon([(18, 15), (36, 15), (27, 29)], YELLOW_MID, outline=OUTLINE)
    c.line(19, 16, 35, 16, YELLOW_LIGHT)

    # Gooey melted cheese highlights & red tomato sauce borders
    c.line(18, 15, 22, 24, RED_SHADOW)
    c.line(36, 15, 32, 24, RED_SHADOW)

    # 3 Shiny pepperoni rounds with grease pools
    c.circle(24, 18, 3, RED_MID, outline=OUTLINE)
    c.set_pixel(24, 18, RED_LIGHT)
    c.circle(30, 20, 3, RED_MID, outline=OUTLINE)
    c.set_pixel(30, 20, RED_LIGHT)
    c.circle(26, 24, 2, RED_MID, outline=OUTLINE)

    s = make_shadow(w, h, 28, 31, 20, 2)
    return c, s


def draw_slime() -> Tuple[PixelCanvas, PixelCanvas]:
    """52x22. Viscous puddle of neon toxic green slime."""
    w, h = 52, 22
    c = PixelCanvas(w, h, TRANSPARENT)

    # Spreading gooey slime puddle
    c.polygon([
        (6, 16), (12, 10), (22, 12), (32, 8), (42, 11),
        (48, 16), (44, 20), (28, 21), (12, 20)
    ], GREEN_MID, outline=OUTLINE)

    # Slime body depth
    c.line(8, 18, 44, 18, GREEN_DEEP)
    c.line(10, 19, 40, 19, GREEN_DEEP)

    # Toxic neon highlights & gloss bubbles
    c.circle(18, 13, 3, GREEN_LIGHT)
    c.set_pixel(17, 12, GREEN_HIGHLIGHT)
    c.circle(34, 11, 4, GREEN_LIGHT)
    c.set_pixel(33, 10, GREEN_HIGHLIGHT)
    c.circle(42, 14, 2, GREEN_LIGHT)

    # Wet gloss specular flecks
    c.line(14, 14, 20, 14, PURE_WHITE)
    c.line(30, 11, 36, 11, PURE_WHITE)

    s = make_shadow(w, h, 26, 20, 22, 2)
    return c, s


def draw_pencil() -> Tuple[PixelCanvas, PixelCanvas]:
    """54x18. Classic yellow #2 pencil lying sideways."""
    w, h = 54, 18
    c = PixelCanvas(w, h, TRANSPARENT)

    # Pink rubber eraser on left
    c.rect(4, 7, 6, 6, DUSK_ROSE, outline=OUTLINE)
    c.line(4, 7, 9, 7, DUSK_BLUSH)
    # Metal ferrule band
    c.rect(10, 7, 4, 6, METAL_MID, outline=OUTLINE)
    c.line(11, 7, 11, 12, PURE_WHITE)

    # Yellow hexagonal pencil body (x=14..40, y=7..12)
    c.rect(14, 7, 26, 6, YELLOW_MID, outline=OUTLINE)
    c.line(14, 7, 39, 7, YELLOW_LIGHT)  # top facet
    c.line(14, 10, 39, 10, OUTLINE)      # hex ridge
    c.line(14, 12, 39, 12, YELLOW_SHADOW) # bottom facet

    # Sharpened wood cone
    c.polygon([(40, 7), (48, 10), (40, 13)], SKIN_HIGHLIGHT, outline=OUTLINE)
    # Sharp graphite lead point
    c.polygon([(46, 9), (50, 10), (46, 11)], OUTLINE)

    s = make_shadow(w, h, 26, 16, 22, 2)
    return c, s


def draw_bouncy_ball() -> Tuple[PixelCanvas, PixelCanvas]:
    """28x28. Swirled two-tone rubber bouncy ball."""
    w, h = 28, 28
    c = PixelCanvas(w, h, TRANSPARENT)

    cx, cy, r = 14, 14, 10
    c.circle(cx, cy, r, DUSK_PINK, outline=OUTLINE)

    # Swirling cyan/blue half
    for y in range(cy - r, cy + r + 1):
        for x in range(cx - r, cx + r + 1):
            if (x - cx) ** 2 + (y - cy) ** 2 <= r * r:
                # Wave equation for swirl divider
                wave = math.sin((y - cy) * 0.3) * 4.0
                if x > cx + wave:
                    c.set_pixel(x, y, BLUE_LIGHT)

    # Outer outline redraw
    c.circle(cx, cy, r, TRANSPARENT, outline=OUTLINE)

    # Highlight glint
    c.circle(cx - 3, cy - 4, 2, PURE_WHITE)
    c.set_pixel(cx - 3, cy - 4, PURE_WHITE)

    s = make_shadow(w, h, 14, 25, 9, 2)
    return c, s


def draw_coin() -> Tuple[PixelCanvas, PixelCanvas]:
    """24x24. Shiny gold coin resting on floor."""
    w, h = 24, 24
    c = PixelCanvas(w, h, TRANSPARENT)

    cx, cy, r = 12, 12, 8
    c.circle(cx, cy, r, YELLOW_MID, outline=OUTLINE)
    c.circle(cx, cy, r - 2, YELLOW_LIGHT, outline=YELLOW_SHADOW)

    # Stamped star emblem in center
    c.polygon([
        (cx, cy - 3), (cx + 2, cy - 1), (cx + 3, cy + 2),
        (cx, cy + 1), (cx - 3, cy + 2), (cx - 2, cy - 1)
    ], YELLOW_SHADOW)
    c.set_pixel(cx, cy, PURE_WHITE)

    # Beveled rim gleam
    c.line(cx - 4, cy - 6, cx + 4, cy - 6, PURE_WHITE)

    s = make_shadow(w, h, 12, 21, 8, 2)
    return c, s


def draw_cassette() -> Tuple[PixelCanvas, PixelCanvas]:
    """52x34. Retro audio cassette tape."""
    w, h = 52, 34
    c = PixelCanvas(w, h, TRANSPARENT)

    # Outer plastic shell
    c.rect(4, 6, 44, 24, PURPLE_DARK, outline=OUTLINE)
    c.line(5, 7, 46, 7, PURPLE_MID)
    c.line(5, 29, 46, 29, VOID_BLACK)

    # White label sticker (x=10..42, y=9..21)
    c.rect(10, 9, 32, 13, PURE_WHITE, outline=OUTLINE)
    # Handwritten pencil line
    c.line(13, 11, 39, 11, METAL_SHADOW)

    # Tape window (x=16..36, y=14..20)
    c.rect(16, 14, 20, 7, VOID_BLACK, outline=OUTLINE)
    # Two tape reels with teeth sprockets
    c.circle(20, 17, 3, BROWN_DARK)
    c.circle(20, 17, 1, PURE_WHITE)
    c.circle(32, 17, 3, BROWN_DARK)
    c.circle(32, 17, 1, PURE_WHITE)

    # Bottom trapezoid wedge (where magnetic tape is exposed)
    c.polygon([(14, 30), (38, 30), (36, 26), (16, 26)], BROWN_DARKEST, outline=OUTLINE)
    c.circle(18, 28, 1, PURE_WHITE)
    c.circle(34, 28, 1, PURE_WHITE)

    s = make_shadow(w, h, 26, 31, 21, 2)
    return c, s


def draw_action_figure() -> Tuple[PixelCanvas, PixelCanvas]:
    """44x52. Space hero action figure lying on back."""
    w, h = 44, 52
    c = PixelCanvas(w, h, TRANSPARENT)

    # Torso with purple & teal armor
    c.rect(14, 18, 16, 16, PURPLE_MID, outline=OUTLINE)
    c.polygon([(16, 20), (28, 20), (26, 26), (18, 26)], TEAL_LIGHT, outline=OUTLINE)
    c.rect(14, 32, 16, 4, YELLOW_MID, outline=OUTLINE)  # utility belt

    # Gold visor space helmet head
    c.circle(22, 11, 8, PURPLE_MID, outline=OUTLINE)
    c.rect(17, 9, 10, 5, YELLOW_LIGHT, outline=OUTLINE)
    c.line(18, 10, 24, 10, PURE_WHITE)  # visor glare

    # Arms splayed out
    c.rect(6, 20, 8, 5, PURPLE_MID, outline=OUTLINE)
    c.rect(6, 25, 6, 8, TEAL_MID, outline=OUTLINE)  # gauntlet
    c.circle(9, 34, 3, SKIN_MID, outline=OUTLINE)   # fist

    c.rect(30, 20, 8, 5, PURPLE_MID, outline=OUTLINE)
    c.rect(32, 25, 6, 8, TEAL_MID, outline=OUTLINE)
    c.circle(35, 34, 3, SKIN_MID, outline=OUTLINE)

    # Legs extended downward (y=36..49)
    c.rect(14, 36, 6, 12, PURPLE_DARK, outline=OUTLINE)
    c.rect(12, 45, 8, 5, TEAL_MID, outline=OUTLINE)  # boot
    c.rect(24, 36, 6, 12, PURPLE_DARK, outline=OUTLINE)
    c.rect(24, 45, 8, 5, TEAL_MID, outline=OUTLINE)

    s = make_shadow(w, h, 22, 50, 17, 2)
    return c, s


def draw_battery() -> Tuple[PixelCanvas, PixelCanvas]:
    """32x20. AA battery rolling on floor."""
    w, h = 32, 20
    c = PixelCanvas(w, h, TRANSPARENT)

    # Black battery cylinder body
    c.rect(6, 6, 18, 10, WOOD_BLACK, outline=OUTLINE)
    c.line(6, 7, 23, 7, METAL_SHADOW)
    c.line(6, 14, 23, 14, VOID_BLACK)

    # Copper / orange top end (x=24..28)
    c.rect(24, 6, 4, 10, ORANGE_MID, outline=OUTLINE)
    c.line(24, 7, 27, 7, ORANGE_LIGHT)

    # Positive nub terminal at right tip
    c.rect(28, 9, 2, 4, METAL_MID, outline=OUTLINE)

    # Stamped "+" sign on body
    c.line(12, 10, 16, 10, PURE_WHITE)
    c.line(14, 8, 14, 12, PURE_WHITE)

    s = make_shadow(w, h, 17, 17, 12, 2)
    return c, s


def draw_paper_plane() -> Tuple[PixelCanvas, PixelCanvas]:
    """40x24. Folded paper dart airplane."""
    w, h = 40, 24
    c = PixelCanvas(w, h, TRANSPARENT)

    # Folded wings
    # Upper left wing
    c.polygon([(4, 12), (36, 4), (20, 16)], PURE_WHITE, outline=OUTLINE)
    c.line(5, 12, 35, 5, WHITE_MID)

    # Center fuselage fold
    c.polygon([(4, 12), (36, 4), (32, 18)], WHITE_SHADOW, outline=OUTLINE)

    # Right lower wing
    c.polygon([(16, 16), (36, 4), (28, 20)], WHITE_MID, outline=OUTLINE)

    # Blue notebook paper line hint
    c.line(12, 11, 26, 8, BLUE_LIGHT)

    s = make_shadow(w, h, 20, 21, 15, 2)
    return c, s


def draw_yo_yo() -> Tuple[PixelCanvas, PixelCanvas]:
    """36x28. Red plastic yo-yo with spilled string loop."""
    w, h = 36, 28
    c = PixelCanvas(w, h, TRANSPARENT)

    # White cotton string trailing out in loose loop (x=4..16, y=14..24)
    string_pts = [(4, 24), (8, 20), (12, 24), (16, 18), (20, 18)]
    for i in range(len(string_pts) - 1):
        c.line(string_pts[i][0], string_pts[i][1], string_pts[i+1][0], string_pts[i+1][1], PURE_WHITE)

    # Yo-yo half rims (angled circle)
    c.circle(25, 16, 9, RED_MID, outline=OUTLINE)
    # Inner wheel concave groove
    c.circle(25, 16, 7, RED_LIGHT)
    c.circle(25, 16, 4, RED_SHADOW, outline=OUTLINE)
    # Axle center
    c.circle(25, 16, 2, YELLOW_MID, outline=OUTLINE)

    # Specular curved gleam on red rim
    c.line(22, 9, 27, 9, RED_HIGHLIGHT)

    s = make_shadow(w, h, 25, 25, 9, 2)
    return c, s


def draw_rubiks_cube() -> Tuple[PixelCanvas, PixelCanvas]:
    """40x40. Isometric twisted puzzle cube."""
    w, h = 40, 40
    c = PixelCanvas(w, h, TRANSPARENT)

    # Isometric cube layout
    # Center vertex at (20, 18)
    # Top face
    c.polygon([(20, 4), (34, 11), (20, 18), (6, 11)], OUTLINE)
    # Front-left face
    c.polygon([(6, 11), (20, 18), (20, 34), (6, 27)], OUTLINE)
    # Front-right face
    c.polygon([(20, 18), (34, 11), (34, 27), (20, 34)], OUTLINE)

    # Colored sticker facets with black grid dividers
    # Top face tiles (Yellow & White)
    tiles_top = [
        ([(20, 5), (24, 7), (20, 9), (16, 7)], YELLOW_LIGHT),
        ([(24, 7), (29, 9), (25, 11), (20, 9)], YELLOW_MID),
        ([(29, 9), (33, 11), (29, 13), (25, 11)], PURE_WHITE),
        ([(16, 7), (20, 9), (16, 11), (12, 9)], PURE_WHITE),
        ([(12, 9), (16, 11), (12, 13), (8, 11)], YELLOW_MID),
        ([(20, 9), (25, 11), (20, 14), (16, 11)], YELLOW_LIGHT),
    ]
    for pts, col in tiles_top:
        c.polygon(pts, col)

    # Front-left face tiles (Red & Orange)
    tiles_left = [
        ([(7, 13), (11, 15), (11, 19), (7, 17)], RED_MID),
        ([(11, 15), (15, 17), (15, 21), (11, 19)], ORANGE_MID),
        ([(15, 17), (19, 19), (19, 23), (15, 21)], RED_LIGHT),
        ([(7, 18), (11, 20), (11, 24), (7, 22)], ORANGE_LIGHT),
        ([(11, 20), (15, 22), (15, 26), (11, 24)], RED_MID),
        ([(15, 22), (19, 24), (19, 28), (15, 26)], RED_SHADOW),
    ]
    for pts, col in tiles_left:
        c.polygon(pts, col)

    # Front-right face tiles (Blue & Green)
    tiles_right = [
        ([(21, 19), (25, 17), (25, 21), (21, 23)], BLUE_MID),
        ([(25, 17), (29, 15), (29, 19), (25, 21)], GREEN_MID),
        ([(29, 15), (33, 13), (33, 17), (29, 19)], BLUE_LIGHT),
        ([(21, 24), (25, 22), (25, 26), (21, 28)], GREEN_LIGHT),
        ([(25, 22), (29, 20), (29, 24), (25, 26)], BLUE_RICH),
        ([(29, 20), (33, 18), (33, 22), (29, 24)], GREEN_MID),
    ]
    for pts, col in tiles_right:
        c.polygon(pts, col)

    s = make_shadow(w, h, 20, 36, 15, 3)
    return c, s


def draw_candy_wrapper() -> Tuple[PixelCanvas, PixelCanvas]:
    """36x20. Shiny crinkled candy wrapper with twisted bowtie ends."""
    w, h = 36, 20
    c = PixelCanvas(w, h, TRANSPARENT)

    # Left twisted bowtie flare
    c.polygon([(4, 6), (12, 10), (4, 15)], DUSK_ROSE, outline=OUTLINE)
    c.line(4, 7, 11, 10, DUSK_BLUSH)
    # Right twisted bowtie flare
    c.polygon([(32, 6), (24, 10), (32, 15)], DUSK_ROSE, outline=OUTLINE)
    c.line(32, 7, 25, 10, DUSK_BLUSH)

    # Center candy body
    c.polygon([(11, 7), (25, 7), (26, 14), (10, 14)], DUSK_PINK, outline=OUTLINE)
    # Metallic foil reflection sheen
    c.line(12, 8, 24, 8, PURE_WHITE)
    c.line(11, 11, 25, 11, DUSK_LILAC)
    c.line(11, 13, 25, 13, SHADOW_DEEP)

    s = make_shadow(w, h, 18, 16, 13, 2)
    return c, s


def draw_dice() -> Tuple[PixelCanvas, PixelCanvas]:
    """32x30. Pair of white gaming dice with black pips."""
    w, h = 32, 30
    c = PixelCanvas(w, h, TRANSPARENT)

    # Die 1 (Front, showing 5 pips) at x=4..18, y=12..26
    c.rect(4, 12, 14, 14, PURE_WHITE, outline=OUTLINE)
    c.line(5, 13, 16, 13, WHITE_MID)
    c.line(5, 25, 16, 25, WHITE_SHADOW)
    # 5 pips
    pips = [(6, 14), (14, 14), (10, 18), (6, 22), (14, 22)]
    for px, py in pips:
        c.rect(px, py, 2, 2, OUTLINE)

    # Die 2 (Angled behind at x=16..28, y=6..20, showing 3 pips)
    c.polygon([(16, 10), (24, 6), (28, 14), (20, 18)], WHITE_SHADOW, outline=OUTLINE)
    c.polygon([(16, 10), (20, 18), (20, 26), (16, 18)], WHITE_MID, outline=OUTLINE)
    c.polygon([(20, 18), (28, 14), (28, 22), (20, 26)], PURE_WHITE, outline=OUTLINE)
    # 3 pips on front face
    c.set_pixel(22, 24, OUTLINE)
    c.set_pixel(24, 20, OUTLINE)
    c.set_pixel(26, 16, OUTLINE)

    s = make_shadow(w, h, 16, 27, 13, 2)
    return c, s


# ==============================================================================
# MAIN CLUTTER GENERATION RUNNER
# ==============================================================================

CLUTTER_REGISTRY: Dict[str, Callable[[], Tuple[PixelCanvas, PixelCanvas]]] = {
    "sock": draw_sock,
    "cereal_bowl": draw_cereal_bowl,
    "toy_car": draw_toy_car,
    "controller": draw_controller,
    "sneaker": draw_sneaker,
    "juice_box": draw_juice_box,
    "crayons": draw_crayons,
    "marble": draw_marble,
    "pizza": draw_pizza,
    "slime": draw_slime,
    "pencil": draw_pencil,
    "bouncy_ball": draw_bouncy_ball,
    "coin": draw_coin,
    "cassette": draw_cassette,
    "action_figure": draw_action_figure,
    "battery": draw_battery,
    "paper_plane": draw_paper_plane,
    "yo_yo": draw_yo_yo,
    "rubiks_cube": draw_rubiks_cube,
    "candy_wrapper": draw_candy_wrapper,
    "dice": draw_dice,
}


def generate_all_clutter():
    print(f"--- Generating {len(CLUTTER_REGISTRY)} Floor Clutter Items & Shadows (art/v2/) ---")
    for name, func in CLUTTER_REGISTRY.items():
        canvas, shadow = func()
        item_path = f"art/v2/deco_{name}.png"
        shadow_path = f"art/v2/deco_{name}_shadow.png"

        canvas.to_image().save(item_path, "PNG")
        shadow.to_image().save(shadow_path, "PNG")
        print(f"Saved {item_path} & {shadow_path} ({canvas.width}x{canvas.height})")


if __name__ == "__main__":
    generate_all_clutter()

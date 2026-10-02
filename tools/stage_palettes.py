"""Younger Sibling Simulator - Stage-Specific 16-Color Accent Palettes for v3."""

from typing import Dict, Tuple, List
from PIL import Image
from palette import hex_to_rgb

STAGE_HEX: Dict[str, List[str]] = {
    "kitchen": [
        "#f7f0df",  # 0: cream tile light
        "#dfd4be",  # 1: cream tile shadow
        "#2a4b49",  # 2: checkerboard dark teal deep
        "#3b6b68",  # 3: checkerboard dark teal mid
        "#528f8b",  # 4: checkerboard dark teal light
        "#a8ded9",  # 5: mint tile highlight
        "#d1663b",  # 6: warm terracotta / toaster orange
        "#fa9352",  # 7: warm toast glow
        "#fedc82",  # 8: egg yolk yellow
        "#fff2b8",  # 9: flour pale yellow
        "#8b2f3e",  # 10: cherry / jam red
        "#45505e",  # 11: stove cast iron dark
        "#6b788a",  # 12: stainless steel mid
        "#a2b0c2",  # 13: stainless steel specular
        "#5a3825",  # 14: coffee / toast crust dark
        "#7a9150",  # 15: grape / olive kitchen green
    ],
    "yard": [
        "#0d2b18",  # 0: deep turf shadow
        "#194d27",  # 1: lush grass shadow
        "#2a7a3b",  # 2: grass blade mid
        "#46ad59",  # 3: grass blade highlight
        "#7eed8f",  # 4: fresh sprout bright green
        "#302213",  # 5: garden soil loam dark
        "#593f24",  # 6: garden soil loam mid
        "#8c6840",  # 7: garden dirt dry
        "#c4562d",  # 8: flowerpot terracotta dark
        "#eb7844",  # 9: flowerpot terracotta light
        "#f5b338",  # 10: string light warm gold
        "#ffeb80",  # 11: string light filament glow
        "#203b57",  # 12: dusk fence shadow
        "#3a638c",  # 13: dusk fence blue-gray
        "#d43b68",  # 14: garden flower magenta
        "#8fedf7",  # 15: water droplet / dragonfly cyan
    ],
    "basement": [
        "#1e2530",  # 0: concrete deep shadow
        "#2f3b4c",  # 1: concrete slab dark
        "#4a5a70",  # 2: concrete mid
        "#6e8099",  # 3: concrete light
        "#94a6bd",  # 4: concrete highlight
        "#151b24",  # 5: cast iron drain grate
        "#693521",  # 6: pipe rust dark
        "#994e2b",  # 7: pipe rust mid
        "#c46e37",  # 8: pipe rust / furnace ember orange
        "#f79434",  # 9: furnace fire flame yellow-orange
        "#fed147",  # 10: furnace fire bright core
        "#2b4859",  # 11: industrial slate dark
        "#3f6c85",  # 12: water puddle blue-gray
        "#5fa2b8",  # 13: drip ripple highlight
        "#3e2a47",  # 14: oil stain iridescent purple
        "#80705a",  # 15: dry sawdust amber-tan
    ],
    "attic": [
        "#241910",  # 0: aged attic timber deep
        "#3d2919",  # 1: dusty oak board dark
        "#5c3e24",  # 2: attic floorboard mid
        "#825832",  # 3: attic floorboard light
        "#b37f49",  # 4: warm wood grain amber
        "#deb073",  # 5: golden honey beam highlight
        "#544b3c",  # 6: dust layer dark olive-tan
        "#80735d",  # 7: dust layer mid
        "#b5a68d",  # 8: dusty cobweb gray-linen
        "#e8dec8",  # 9: parchment letter yellow-ivory
        "#804a5e",  # 10: antique faded rose
        "#ad6d83",  # 11: antique doll dress rose
        "#69592a",  # 12: tarnished trunk brass dark
        "#a38e42",  # 13: tarnished brass mid
        "#d9c264",  # 14: brass latch specular
        "#697894",  # 15: moonlit window dust blue-gray
    ]
}

for name, colors in STAGE_HEX.items():
    assert len(colors) == 16, f"Stage {name} must have exactly 16 colors, got {len(colors)}"

STAGE_RGB: Dict[str, List[Tuple[int, int, int]]] = {
    name: [hex_to_rgb(h) for h in colors] for name, colors in STAGE_HEX.items()
}

STAGE_RGBA: Dict[str, List[Tuple[int, int, int, int]]] = {
    name: [(r, g, b, 255) for (r, g, b) in rgb_list] for name, rgb_list in STAGE_RGB.items()
}

def export_palettes():
    for name, rgbs in STAGE_RGB.items():
        img = Image.new("RGB", (16, 1))
        for x, c in enumerate(rgbs):
            img.putpixel((x, 0), c)
        path = f"art/v2/palette_{name}.png"
        img.save(path)
        print(f"Exported {path} (16x1)")

if __name__ == "__main__":
    export_palettes()

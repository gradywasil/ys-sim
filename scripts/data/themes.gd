extends RefCounted
## Visual themes. Stage i uses theme (i % THEMES.size()), so the endless mode cycles through all rooms.
## Bedroom files have no prefix; every other theme prefixes its files (e.g. "kitchen_bg_far").

const THEMES := [
	{"id": "bedroom", "p": "", "light": Color(1.0, 0.95, 0.75)},
	{"id": "kitchen", "p": "kitchen_", "light": Color(1.0, 0.9, 0.6)},
	{"id": "yard", "p": "yard_", "light": Color(0.8, 0.95, 1.0)},
	{"id": "basement", "p": "basement_", "light": Color(0.7, 0.85, 1.0)},
	{"id": "attic", "p": "attic_", "light": Color(1.0, 0.85, 0.6)},
]

# World-space animated props per theme: [sheet suffix, placement, vertical position].
# placement: "floor" (bottom on the floor lip), "hang" (top at y), "air" (centered at y).
const PROPS := {
	1: [["prop_fridge_light", "floor", 0], ["prop_kettle", "floor", 0], ["prop_toaster", "floor", 0], ["prop_dripping_tap", "hang", 36], ["prop_fruit_fly", "air", 110], ["prop_clock", "air", 70]],
	2: [["prop_gnome", "floor", 0], ["prop_sprinkler_idle", "floor", 0], ["prop_swing", "floor", 0], ["prop_windmill", "floor", 0], ["prop_string_lights", "hang", 6], ["prop_butterflies", "air", 120]],
	3: [["prop_furnace", "floor", 0], ["prop_washer", "floor", 0], ["prop_tv_static", "floor", 0], ["prop_bulb", "hang", 0], ["prop_pipe_drip", "hang", 24], ["prop_spider", "hang", 0]],
	4: [["prop_rocking_chair", "floor", 0], ["prop_sheet_ghost", "floor", 0], ["prop_music_box", "floor", 0], ["prop_mobile", "hang", 0], ["prop_cobweb", "hang", 0], ["prop_moon_window", "air", 80]],
}


static func theme_of_stage(i: int) -> int:
	return i % THEMES.size()


static func prefix(theme: int) -> String:
	return THEMES[theme].p


## File name of a themed sheet, e.g. file(1, "bg_far") -> "kitchen_bg_far".
static func file(theme: int, base: String) -> String:
	return THEMES[theme].p + base

extends RefCounted
## Stage definitions. `d0`/`d1` is the difficulty ramp (0..1) across the stage's chunks,
## `unlock` lists powerups that become available when the stage begins.

const STAGES := [
	{"name": "BEDROOM", "sub": "Warm-up", "chunks": 10, "d0": 0.0, "d1": 0.35, "bedtime": 75.0, "unlock": ["boots", "feather", "coin"], "tint": Color(1, 1, 1)},
	{"name": "KITCHEN", "sub": "Don't touch the stove", "chunks": 12, "d0": 0.2, "d1": 0.5, "bedtime": 85.0, "unlock": ["umbrella", "stopwatch", "slippers"], "tint": Color(1.0, 0.94, 0.8)},
	{"name": "BACKYARD", "sub": "Mom said stay inside", "chunks": 14, "d0": 0.35, "d1": 0.65, "bedtime": 95.0, "unlock": ["bridge", "trampoline", "cookie", "fan"], "tint": Color(0.82, 1.0, 0.86)},
	{"name": "BASEMENT", "sub": "Something is down here", "chunks": 14, "d0": 0.5, "d1": 0.8, "bedtime": 100.0, "unlock": ["ramp", "sugar", "flashlight", "tape", "bubblewrap"], "tint": Color(0.66, 0.72, 0.96)},
	{"name": "ATTIC", "sub": "Dusty and dangerous", "chunks": 16, "d0": 0.65, "d1": 1.0, "bedtime": 105.0, "unlock": ["gloves"], "tint": Color(0.96, 0.82, 0.72)},
]


## Stage definition by index; past the last stage the game loops a harder "night shift".
static func get_stage(i: int) -> Dictionary:
	if i < STAGES.size():
		return STAGES[i]
	var lap := i - STAGES.size() + 1
	return {"name": "NIGHT SHIFT %d" % lap, "sub": "Bedtime was hours ago", "chunks": 16, "d0": 1.0, "d1": 1.0, "bedtime": 100.0, "unlock": [], "tint": Color(0.7, 0.7, 0.95)}


## Every powerup unlocked by the time stage `i` begins.
static func unlocked_through(i: int) -> Array:
	var out: Array = []
	for n in mini(i + 1, STAGES.size()):
		for id in STAGES[n].unlock:
			if not out.has(id):
				out.append(id)
	return out

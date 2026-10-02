extends RefCounted
## Seeded chunk generator. Each chunk is a list of primitives ["flat"|"block"|"gap"|"coins", size] plus
## `needs`: the powerups that can solve it, so the generator can guarantee every chunk is solvable.

# id, weight, min difficulty. Weights shift toward harder chunks as difficulty rises.
const LIB := [
	{"id": "rest", "w": 3.0, "min": 0.0, "hard": 0.0},
	{"id": "coins", "w": 2.5, "min": 0.0, "hard": 0.0},
	{"id": "hop_s", "w": 4.0, "min": 0.0, "hard": 0.2},
	{"id": "hop_m", "w": 3.0, "min": 0.05, "hard": 0.4},
	{"id": "gap_s", "w": 4.0, "min": 0.0, "hard": 0.3},
	{"id": "wide", "w": 3.0, "min": 0.1, "hard": 0.7},
	{"id": "tower", "w": 3.0, "min": 0.1, "hard": 0.7},
	{"id": "hop_gap", "w": 2.0, "min": 0.25, "hard": 0.6},
	{"id": "gap_hop", "w": 2.0, "min": 0.25, "hard": 0.6},
	{"id": "double_gap", "w": 2.0, "min": 0.3, "hard": 0.8},
	{"id": "tower_wide", "w": 2.0, "min": 0.5, "hard": 1.0},
	{"id": "wide_tower", "w": 2.0, "min": 0.55, "hard": 1.0},
	# Cycling hazards appear from a given stage on (index into the stage list).
	{"id": "burner", "w": 3.0, "min": 0.0, "hard": 0.6, "stage": 1},
	{"id": "sprinkler", "w": 3.0, "min": 0.0, "hard": 0.6, "stage": 2},
	{"id": "marbles", "w": 3.0, "min": 0.1, "hard": 0.6, "stage": 1},
	{"id": "cans", "w": 3.0, "min": 0.1, "hard": 0.6, "stage": 3},
	{"id": "puddle", "w": 3.0, "min": 0.0, "hard": 0.5, "stage": 1},
	{"id": "puddle_gap", "w": 2.0, "min": 0.25, "hard": 0.9, "stage": 1},
	{"id": "mud", "w": 3.0, "min": 0.0, "hard": 0.5, "stage": 2},
	{"id": "wind", "w": 3.0, "min": 0.0, "hard": 0.5, "stage": 2},
	{"id": "mousetrap", "w": 3.0, "min": 0.0, "hard": 0.6, "stage": 3},
	{"id": "drip", "w": 3.0, "min": 0.0, "hard": 0.6, "stage": 3},
	{"id": "spider", "w": 2.5, "min": 0.1, "hard": 0.6, "stage": 3},
	{"id": "cobweb", "w": 3.0, "min": 0.0, "hard": 0.6, "stage": 4},
	{"id": "board", "w": 3.0, "min": 0.1, "hard": 0.8, "stage": 4},
	{"id": "dust", "w": 2.0, "min": 0.0, "hard": 0.3, "stage": 4},
	{"id": "burner_hop", "w": 2.0, "min": 0.3, "hard": 0.8, "stage": 1},
	{"id": "sprinkler_gap", "w": 2.0, "min": 0.3, "hard": 0.8, "stage": 2},
]

var rng := RandomNumberGenerator.new()
var last_ids: Array = []
var forced: Array = []   # dev: chunk ids to emit first (see --first= in main.gd)


func _init(seed_value: int = 0) -> void:
	rng.seed = seed_value


func _rest(d: float) -> int:
	# Breathing room shrinks as difficulty rises; always a multiple of 16.
	var base := lerpf(176.0, 96.0, d)
	return int(round((base + rng.randf_range(-16.0, 32.0)) / 16.0)) * 16


func next_chunk(d: float, stage: int = 0) -> Dictionary:
	if not forced.is_empty():
		var id: String = forced.pop_front()
		last_ids.append(id)
		return build(id, d)
	var pool: Array = []
	var total := 0.0
	for c in LIB:
		if d < c.min or stage < c.get("stage", 0):
			continue
		var w: float = c.w * lerpf(1.0, 1.0 + c.hard * 2.0, d)
		# Don't repeat the same chunk three times in a row.
		if last_ids.size() >= 2 and last_ids[-1] == c.id and last_ids[-2] == c.id:
			continue
		pool.append([c, w])
		total += w
	var pick := rng.randf() * total
	var chosen: Dictionary = pool[0][0]
	for entry in pool:
		pick -= entry[1]
		if pick <= 0.0:
			chosen = entry[0]
			break
	last_ids.append(chosen.id)
	if last_ids.size() > 4:
		last_ids.pop_front()
	return build(chosen.id, d)


func build(id: String, d: float) -> Dictionary:
	var r := _rest(d)
	var prims: Array = []
	var needs: Array = []
	match id:
		"rest":
			prims = [["flat", r + 32]]
		"coins":
			prims = [["flat", 32], ["coins", 5], ["flat", r]]
		"hop_s":
			prims = [["flat", r], ["block", 16], ["flat", 64]]
		"hop_m":
			prims = [["flat", r], ["block", 32], ["flat", 64]]
		"gap_s":
			prims = [["flat", r], ["gap", 32 if rng.randf() < 0.5 else 48], ["flat", 64]]
		"wide":
			prims = [["flat", r], ["gap", 96], ["flat", 96]]
			needs = ["boots", "umbrella", "bridge"]
		"tower":
			prims = [["flat", r], ["block", 64], ["flat", 96]]
			needs = ["feather"]
		"hop_gap":
			prims = [["flat", r], ["block", 16], ["flat", 80], ["gap", 48], ["flat", 64]]
		"gap_hop":
			prims = [["flat", r], ["gap", 48], ["flat", 80], ["block", 32], ["flat", 64]]
		"double_gap":
			prims = [["flat", r], ["gap", 48], ["flat", 80], ["gap", 48], ["flat", 64]]
		"tower_wide":
			prims = [["flat", r], ["block", 64], ["flat", 112], ["gap", 96], ["flat", 96]]
			needs = ["feather", "boots|umbrella|bridge"]
		"burner":
			prims = [["flat", r], ["hazard", "burner"], ["flat", 96]]
			needs = ["wait|stopwatch"]
		"sprinkler":
			prims = [["flat", r], ["hazard", "sprinkler"], ["flat", 96]]
			needs = ["wait|stopwatch|umbrella"]
		"marbles":
			prims = [["flat", r], ["hazard", "marbles"], ["flat", 96]]
			needs = ["wait|stopwatch|trampoline|ramp"]
		"cans":
			prims = [["flat", r], ["hazard", "cans"], ["flat", 96]]
			needs = ["wait|stopwatch|trampoline|ramp"]
		"puddle":
			prims = [["flat", r], ["zone", "puddle"], ["flat", 128]]
			needs = ["slippers"]
		"puddle_gap":
			# A slip carries P1 about 160 units: this puddle slides it into the gap unless it has slippers or a bridge.
			prims = [["flat", r], ["zone", "puddle"], ["flat", 112], ["gap", 48], ["flat", 96]]
			needs = ["slippers|bridge"]
		"mud":
			prims = [["flat", r], ["zone", "mud"], ["flat", 96]]
			needs = ["slippers|sugar"]
		"wind":
			prims = [["flat", r], ["zone", "wind"], ["flat", 96]]
			needs = ["fan|sugar|stopwatch"]
		"mousetrap":
			prims = [["flat", r], ["hazard", "mousetrap"], ["flat", 96]]
			needs = ["wait|stopwatch|tape"]
		"drip":
			prims = [["flat", r], ["hazard", "drip"], ["flat", 96]]
			needs = ["wait|stopwatch|umbrella|tape"]
		"spider":
			prims = [["flat", r], ["zone", "spider"], ["flat", 96]]
			needs = ["flashlight|gloves"]
		"cobweb":
			prims = [["flat", r], ["zone", "cobweb"], ["flat", 96]]
			needs = ["gloves"]
		"board":
			# Becomes a 96-unit pit once P1 steps on it: solvable like a wide gap, or tape it first.
			prims = [["flat", r], ["board", 96], ["flat", 96]]
			needs = ["tape|boots|umbrella|bridge|sugar"]
		"dust":
			prims = [["flat", r], ["zone", "dust"], ["flat", 96]]
			needs = []
		"burner_hop":
			prims = [["flat", r], ["hazard", "burner"], ["flat", 96], ["block", 32], ["flat", 64]]
			needs = ["wait|stopwatch"]
		"sprinkler_gap":
			prims = [["flat", r], ["hazard", "sprinkler"], ["flat", 112], ["gap", 48], ["flat", 64]]
			needs = ["wait|stopwatch|umbrella"]
		"wide_tower":
			prims = [["flat", r], ["gap", 96], ["flat", 128], ["block", 64], ["flat", 96]]
			needs = ["boots|umbrella|bridge", "feather"]
	return {"id": id, "prims": prims, "needs": needs}

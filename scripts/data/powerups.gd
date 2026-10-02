extends RefCounted
## Powerup definitions. `kind`: "buff" is collected by P1 (timing matters), "placeable" lands in the
## world (position matters), "instant" is score only. `trips()` is the "wrong moment" rule for buffs.

const ORDER := ["boots", "feather", "umbrella", "bridge", "trampoline", "ramp", "stopwatch", "slippers", "sugar", "flashlight", "bubblewrap", "gloves", "fan", "tape", "cookie", "coin"]

const DEFS := {
	"boots": {
		"name": "BOOTS", "kind": "buff", "dur": 4.5, "color": Color(1.0, 0.6, 0.2),
		"toast": "SPEED BOOTS!", "rule": "Not mid-air",
	},
	"feather": {
		"name": "FEATHER", "kind": "buff", "dur": 6.0, "color": Color(0.75, 0.92, 1.0),
		"toast": "FEATHER JUMP!", "rule": "Only when P1 is waiting",
	},
	"umbrella": {
		"name": "UMBRELLA", "kind": "buff", "dur": 6.0, "color": Color(1.0, 0.45, 0.5),
		"toast": "GLIDE!", "rule": "Not while running on the ground",
	},
	"bridge": {
		"name": "BRIDGE", "kind": "placeable", "dur": 0.0, "color": Color(0.85, 0.65, 0.4),
		"toast": "BRIDGE!", "rule": "Drop near a gap; don't drop it on P1",
	},
	"trampoline": {
		"name": "TRAMPOLINE", "kind": "placeable", "dur": 0.0, "color": Color(0.35, 0.6, 1.0),
		"toast": "BOING!", "rule": "Drop just before a roller lane; don't drop it on P1",
	},
	"ramp": {
		"name": "RAMP", "kind": "placeable", "dur": 0.0, "color": Color(0.95, 0.75, 0.3),
		"toast": "RAMP!", "rule": "Like the trampoline, but a lower, faster launch",
	},
	"stopwatch": {
		"name": "STOPWATCH", "kind": "buff", "dur": 5.0, "color": Color(0.5, 0.8, 1.0),
		"toast": "TIME STOP!", "rule": "Freezes hazards. Dizzies P1 if boots are active",
	},
	"slippers": {
		"name": "SLIPPERS", "kind": "buff", "dur": 6.0, "color": Color(1.0, 0.55, 0.75),
		"toast": "GRIP!", "rule": "Only while P1 is running on the ground",
	},
	"sugar": {
		"name": "SUGAR RUSH", "kind": "buff", "dur": 4.0, "color": Color(0.3, 0.95, 1.0),
		"toast": "SUGAR RUSH!", "rule": "Not mid-air. P1 won't stop for anything, then crashes",
	},
	"flashlight": {
		"name": "FLASHLIGHT", "kind": "buff", "dur": 9.0, "color": Color(1.0, 0.93, 0.5),
		"toast": "LIGHTS!", "rule": "Not while P1 is holding an umbrella or feather (hands full)",
	},
	"bubblewrap": {
		"name": "BUBBLE WRAP", "kind": "buff", "dur": 12.0, "color": Color(0.7, 0.9, 1.0),
		"toast": "WRAPPED!", "rule": "Absorbs one hit. Not while boots or sugar are active",
	},
	"gloves": {
		"name": "GLOVES", "kind": "buff", "dur": 9.0, "color": Color(0.5, 0.9, 0.4),
		"toast": "STICKY!", "rule": "Tears through cobwebs. Not while P1 is in mud or on a puddle",
	},
	"fan": {
		"name": "FAN", "kind": "placeable", "dur": 0.0, "color": Color(0.6, 0.75, 0.95),
		"toast": "WHOOSH!", "rule": "Blows P1 forward and cancels wind gusts nearby",
	},
	"tape": {
		"name": "TAPE", "kind": "placeable", "dur": 0.0, "color": Color(0.3, 0.55, 1.0),
		"toast": "TAPED!", "rule": "Pins down a trap, burner, sprinkler, drip or loose board for good",
	},
	"cookie": {
		"name": "COOKIE", "kind": "instant", "dur": 0.0, "color": Color(0.9, 0.62, 0.3), "limited": true,
		"toast": "YUM!", "rule": "Limited stock. P1 stops to eat it, but Mom calms down",
	},
	"coin": {
		"name": "COIN", "kind": "instant", "dur": 0.0, "color": Color(1.0, 0.85, 0.25),
		"toast": "+1", "rule": "Always safe",
	},
}


static func color(id: String) -> Color:
	return DEFS[id].color


static func kind(id: String) -> String:
	return DEFS[id].kind


## True when handing this buff to P1 right now would trip it.
static func trips(id: String, p) -> bool:
	match id:
		"boots":
			return not p.is_on_floor()
		"feather":
			return p.wait_t <= 0.0
		"umbrella":
			return p.is_on_floor() and p.wait_t <= 0.0
		"stopwatch":
			return p.boots_t > 0.0
		"slippers":
			# They only go on a P1 that is running: standing still or mid-air is the wrong moment.
			return p.wait_t > 0.0 or not p.is_on_floor()
		"sugar":
			return not p.is_on_floor()
		"flashlight":
			return p.umbrella_t > 0.0 or p.feather_t > 0.0
		"bubblewrap":
			return p.boots_t > 0.0 or p.sugar_t > 0.0
		"gloves":
			return p.mud_t > 0.0 or p.slip_t > 0.0
	return false

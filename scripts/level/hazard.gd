extends Area2D
## A floor hazard P1 can't simply jump. Two families:
##  - cycling (burner, sprinkler): idle -> warning -> dangerous on a loop.
##  - lane (marbles, paint cans): P1 getting close triggers a stream of rollers across the lane.
## P1 waits the hazard out, which burns bedtime; powerups (and placed launchers) skip the wait.

const TYPES := {
	"burner": {"w": 32.0, "h": 30.0, "period": 3.4, "warn": 0.7, "on": 1.3, "counters": ["stopwatch", "tape"]},
	"sprinkler": {"w": 96.0, "h": 44.0, "period": 4.2, "warn": 0.7, "on": 1.8, "counters": ["stopwatch", "umbrella", "tape"]},
	# Frames: fr_idle, fr_warn, fr_on are [first, last] ranges of the sheet.
	"mousetrap": {"w": 28.0, "h": 14.0, "period": 3.2, "warn": 0.7, "on": 0.4, "sheet": "hazard_mousetrap", "fr_idle": [4, 7], "fr_warn": [0, 2], "fr_on": [3, 3], "counters": ["stopwatch", "tape"]},
	"drip": {"w": 14.0, "h": 26.0, "period": 3.4, "warn": 1.0, "on": 0.5, "sheet": "hazard_drip", "fr_idle": [0, 0], "fr_warn": [0, 3], "fr_on": [4, 9], "counters": ["stopwatch", "umbrella", "tape"]},
	"marbles": {"w": 96.0, "h": 14.0, "lane": true, "sheet": "hazard_marble", "count": 7, "gap": 0.6, "speed": 80.0, "r": 5.0, "counters": ["stopwatch", "trampoline", "ramp"]},
	"cans": {"w": 96.0, "h": 22.0, "lane": true, "sheet": "hazard_paint_can", "count": 4, "gap": 1.1, "speed": 70.0, "r": 9.0, "counters": ["stopwatch", "trampoline", "ramp"]},
}
const TRIGGER_DIST := 230.0

var kind := "burner"
var width := 64.0
var height := 56.0
var period := 3.4
var warn := 0.7
var on := 1.3
var lane := false
var counters: Array = []
var t := 0.0
var level
var art: Node2D
var body_spr: AnimatedSprite2D
var spray: AnimatedSprite2D
var warn_icon: AnimatedSprite2D
# lane state
var state := "idle"     # idle -> active -> done
var spawned := 0
var spawn_t := 0.0
var rollers: Array = []
var p1
var taped := false
var spec: Dictionary


static func width_of(k: String) -> float:
	return TYPES[k].w


func _ready() -> void:
	var d: Dictionary = TYPES[kind]
	spec = d
	width = d.w
	height = d.h
	lane = d.get("lane", false)
	period = d.get("period", 1.0)
	warn = d.get("warn", 0.0)
	on = d.get("on", 0.0)
	counters = d.counters
	# Deterministic phase from position, so a seed always produces the same hazard timing.
	t = fmod(position.x * 0.0371, 1.0) * period
	add_to_group("hazard")
	collision_layer = 0
	collision_mask = 2
	if not lane:
		var cs := CollisionShape2D.new()
		var shape := RectangleShape2D.new()
		shape.size = Vector2(maxf(width - 8.0, 8.0), height)
		cs.shape = shape
		cs.position = Vector2(width * 0.5, -height * 0.5)
		add_child(cs)
	level = get_tree().get_first_node_in_group("level")
	art = Node2D.new()
	art.z_index = 2
	add_child(art)
	if not lane:
		_build_art()


func is_frozen() -> bool:
	return level != null and level.freeze_t > 0.0


## 0 idle, 1 warning, 2 dangerous (cycling hazards only).
func phase() -> int:
	var m := fmod(t, period)
	if m >= period - on:
		return 2
	if m >= period - on - warn:
		return 1
	return 0


func is_dangerous() -> bool:
	if taped:
		return false
	if lane:
		return state != "done" and not is_frozen()
	return phase() == 2 and not is_frozen()


## True if it is dangerous now, or will become dangerous within `sec` seconds.
func dangerous_within(sec: float) -> bool:
	if taped:
		return false
	if is_frozen():
		return level.freeze_t < sec
	if lane:
		return state != "done"
	var m := fmod(t, period)
	var on_start := period - on
	return m >= on_start or on_start - m <= sec


func _physics_process(delta: float) -> void:
	if lane:
		_lane_tick(delta)
		return
	if not is_frozen():
		t += delta
	if is_dangerous():
		for b in get_overlapping_bodies():
			if b.has_method("hurt") and not ((kind == "sprinkler" or kind == "drip") and b.umbrella_t > 0.0):
				b.hurt(kind)


## Pins the hazard down for good (the tape powerup).
func tape() -> bool:
	if taped or lane:
		return false
	taped = true
	var tp := Art.sprite("placed_tape", false)
	var sz := Art.frame_size("placed_tape")
	tp.position = Vector2(width * 0.5, -sz.y * 0.5 + 1.0)
	tp.z_index = 6
	add_child(tp)
	Juice.float_text(get_parent(), global_position + Vector2(width * 0.5, -height - 6.0), "TAPED!", Color(0.5, 0.75, 1.0))
	return true


# --- roller lane --------------------------------------------------------------

func _lane_tick(delta: float) -> void:
	if p1 == null:
		p1 = get_tree().get_first_node_in_group("p1")
		if p1 == null:
			return
	var d: Dictionary = TYPES[kind]
	if state == "idle" and p1.global_position.x > global_position.x - TRIGGER_DIST:
		state = "active"
	var frozen := is_frozen()
	if state == "active" and not frozen:
		spawn_t -= delta
		if spawned < d.count and spawn_t <= 0.0:
			spawn_t = d.gap
			spawned += 1
			_spawn_roller(d)
	for r in rollers.duplicate():
		if not is_instance_valid(r):
			rollers.erase(r)
			continue
		if not frozen:
			r.position.x -= d.speed * delta
		r.speed_scale = 0.0 if frozen else 1.0
		if r.position.x < 12.0:  # vanish before reaching the spot where a launcher sits
			rollers.erase(r)
			Art.fx(get_parent(), global_position + Vector2(0, -6), "fx_dust", Color(0.95, 0.85, 0.75), 0.6)
			r.queue_free()
			continue
		if not frozen and _hits_p1(r, d.r):
			p1.hurt(kind)
	if state == "active" and spawned >= d.count and rollers.is_empty():
		state = "done"


func _spawn_roller(d: Dictionary) -> void:
	var r := Art.sprite(d.sheet)
	var sz := Art.frame_size(d.sheet)
	r.centered = true
	# Spawn a little inside the lane so a launched P1 landing just past the end is never on top of a fresh roller.
	r.position = Vector2(width - 12.0, -sz.y * 0.5 + 1.0)
	r.frame = randi() % 8
	art.add_child(r)
	rollers.append(r)


func _hits_p1(r: Node2D, radius: float) -> bool:
	var c: Vector2 = r.global_position
	var p: Vector2 = p1.global_position
	return absf(c.x - p.x) < radius + 5.0 and absf(c.y - p.y) < radius + 9.0


# --- cycling hazard art -------------------------------------------------------

func _build_art() -> void:
	if spec.has("sheet"):
		body_spr = Art.sprite(spec.sheet, false)
		body_spr.position = Vector2(width * 0.5, -Art.frame_size(spec.sheet).y * 0.5 + 1.0)
		art.add_child(body_spr)
		warn_icon = Art.sprite("fx_warning_exclaim")
		warn_icon.position = Vector2(width * 0.5, -height - 14.0)
		warn_icon.visible = false
		warn_icon.z_index = 5
		art.add_child(warn_icon)
		return
	if kind == "burner":
		body_spr = Art.sprite("hazard_stove_burner", false)
		body_spr.position = Vector2(width * 0.5, -Art.frame_size("hazard_stove_burner").y * 0.5 + 1.0)
		art.add_child(body_spr)
	else:
		body_spr = Art.sprite("hazard_sprinkler", false)
		body_spr.position = Vector2(12.0, -Art.frame_size("hazard_sprinkler").y * 0.5 + 1.0)
		art.add_child(body_spr)
		spray = Art.sprite("hazard_water_spray")
		spray.position = Vector2(8.0 + Art.frame_size("hazard_water_spray").x * 0.5, -Art.frame_size("hazard_water_spray").y * 0.5 + 6.0)
		spray.modulate.a = 0.85
		spray.visible = false
		art.add_child(spray)
	warn_icon = Art.sprite("fx_warning_exclaim")
	warn_icon.position = Vector2(width * 0.5, -height - 14.0)
	warn_icon.visible = false
	warn_icon.z_index = 5
	art.add_child(warn_icon)


func _process(_delta: float) -> void:
	var frozen := is_frozen()
	art.modulate = Color(0.6, 0.85, 1.0) if frozen else Color.WHITE
	if lane:
		return
	var ph := phase()
	var time := Time.get_ticks_msec() * 0.001
	if spec.has("sheet"):
		var rng: Array = spec.fr_idle if ph == 0 else (spec.fr_warn if ph == 1 else spec.fr_on)
		var n: int = int(rng[1]) - int(rng[0]) + 1
		var f2: int = int(rng[0]) + int(time * 8.0) % n
		if ph == 2 and not frozen:
			# Play the "on" frames once across the dangerous window.
			var m := fmod(t, period) - (period - on)
			f2 = int(rng[0]) + clampi(int(m / on * float(n)), 0, n - 1)
		body_spr.frame = f2
		warn_icon.visible = ph == 1 and not frozen and not taped
		return
	# Sheets are laid out: frames 0-2 idle, 3-4 warning, 5-9 dangerous.
	var f := int(time * 3.0) % 3
	if ph == 1:
		f = 3 + int(time * 10.0) % 2
	elif ph == 2:
		f = 5 + int(time * 10.0) % 5
	if frozen and ph == 2:
		f = 5
	body_spr.frame = f
	warn_icon.visible = ph == 1 and not frozen
	if spray != null:
		spray.visible = ph == 2 and not frozen

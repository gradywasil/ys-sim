extends Area2D
## Floor and air zones that change how P1 moves or what it suffers. P1 doesn't see these coming, so Player 2
## has to spot them and act: slippers (puddle, mud), a fan (wind), gloves (cobweb), a flashlight (spider).
##  - always on until used: puddle, mud, cobweb, spider
##  - cycling: wind (gusts), dust (puffs)

const TYPES := {
	"puddle": {"w": 48.0, "sheet": "hazard_juice_puddle", "tiles": 1},
	"mud": {"w": 96.0, "sheet": "hazard_mud", "tiles": 2},
	"wind": {"w": 128.0, "sheet": "hazard_wind_gust", "tiles": 1, "cycle": [4.4, 0.9, 2.0], "h": 40.0},
	"cobweb": {"w": 40.0, "sheet": "hazard_cobweb", "tiles": 1, "h": 44.0},
	"spider": {"w": 28.0, "sheet": "hazard_spider_drop", "tiles": 1, "h": 40.0},
	"dust": {"w": 72.0, "sheet": "hazard_dust_cloud", "tiles": 1, "cycle": [4.0, 0.8, 1.6], "h": 36.0},
}

var kind := "puddle"
var width := 48.0
var spec: Dictionary
var period := 1.0
var warn := 0.0
var on := 0.0
var cycles := false
var t := 0.0
var used := false
var level
var p1
var spr: AnimatedSprite2D
var warn_icon: AnimatedSprite2D


static func width_of(k: String) -> float:
	return TYPES[k].w


func _ready() -> void:
	spec = TYPES[kind]
	width = spec.w
	add_to_group("zone")
	collision_layer = 0
	collision_mask = 2
	if spec.has("cycle"):
		cycles = true
		period = spec.cycle[0]
		warn = spec.cycle[1]
		on = spec.cycle[2]
		t = fmod(position.x * 0.0371, 1.0) * period
	var h: float = spec.get("h", 8.0)
	var cs := CollisionShape2D.new()
	var shape := RectangleShape2D.new()
	shape.size = Vector2(width - 6.0, h)
	cs.shape = shape
	cs.position = Vector2(width * 0.5, -h * 0.5)
	add_child(cs)
	level = get_tree().get_first_node_in_group("level")
	_build_art()


func _build_art() -> void:
	var sheet: String = spec.sheet
	var sz := Art.frame_size(sheet)
	match kind:
		"puddle", "mud":
			for i in int(spec.tiles):
				var s := Art.sprite(sheet)
				s.position = Vector2(sz.x * 0.5 + sz.x * float(i), -sz.y * 0.5 + 2.0)
				s.frame = (i * 2) % 6
				s.z_index = 1
				add_child(s)
			if kind == "puddle":
				# A spill trail leading in, so an attentive Player 2 can see it coming.
				for i in 3:
					var tr := Art.sprite("hazard_spill_trail")
					tr.position = Vector2(-18.0 - 30.0 * float(i), -Art.frame_size("hazard_spill_trail").y * 0.5 + 2.0)
					tr.frame = i
					tr.z_index = 1
					add_child(tr)
		"wind":
			spr = Art.sprite(sheet, false)
			spr.position = Vector2(width * 0.5, -sz.y * 0.5 - 4.0)
			spr.scale = Vector2(Art.W * width / sz.x * 1.0, Art.W)
			spr.modulate.a = 0.0
			spr.z_index = 3
			add_child(spr)
		"cobweb":
			spr = Art.sprite(sheet)
			spr.position = Vector2(width * 0.5, -sz.y * 0.5 - 8.0)
			spr.z_index = 3
			add_child(spr)
		"spider":
			spr = Art.sprite(sheet, false)
			spr.position = Vector2(width * 0.5, -sz.y * 0.5 - 24.0)
			spr.z_index = 3
			add_child(spr)
		"dust":
			spr = Art.sprite(sheet, false)
			spr.position = Vector2(width * 0.5, -sz.y * 0.5)
			spr.modulate.a = 0.0
			spr.z_index = 3
			add_child(spr)
	if cycles:
		warn_icon = Art.sprite("fx_warning_exclaim")
		warn_icon.position = Vector2(width * 0.5, -(spec.get("h", 30.0)) - 10.0)
		warn_icon.visible = false
		warn_icon.z_index = 5
		add_child(warn_icon)


func is_frozen() -> bool:
	return level != null and level.freeze_t > 0.0


## 0 idle, 1 warning, 2 active (cycling zones).
func phase() -> int:
	var m := fmod(t, period)
	if m >= period - on:
		return 2
	if m >= period - on - warn:
		return 1
	return 0


## True while the zone should affect P1.
func is_active() -> bool:
	if used:
		return false
	if cycles:
		return phase() == 2 and not is_frozen()
	return true


## A placed fan close by cancels a wind gust.
func _fan_near() -> bool:
	for f in get_tree().get_nodes_in_group("fan"):
		if f.global_position.x > global_position.x - 70.0 and f.global_position.x < global_position.x + width + 70.0:
			return true
	return false


func _physics_process(delta: float) -> void:
	if cycles and not is_frozen():
		t += delta
	if p1 == null:
		p1 = get_tree().get_first_node_in_group("p1")
	match kind:
		"spider":
			_spider_tick()
			return
		"wind":
			if _fan_near():
				return
		"dust":
			if is_active():
				var m := get_tree().get_first_node_in_group("main")
				for b in get_overlapping_bodies():
					if b.has_method("enter_zone") and m != null:
						m.fog(1.6)
			return
	if not is_active():
		return
	for b in get_overlapping_bodies():
		if b.has_method("enter_zone"):
			if b.enter_zone(kind) and kind == "cobweb":
				_tear()


func _tear() -> void:
	used = true
	if spr != null:
		var tw := create_tween()
		tw.tween_property(spr, "modulate:a", 0.0, 0.4)
	Juice.burst(get_parent(), global_position + Vector2(width * 0.5, -22.0), Color(0.9, 0.88, 0.8), 8, 50.0, 60.0, 0.6, Vector2.UP, 180.0)


# The spider drops when P1 gets close, unless P1 has a light or sticky gloves.
var spider_state := "idle"


func _spider_tick() -> void:
	if p1 == null or spider_state == "done":
		return
	var dx: float = p1.global_position.x - (global_position.x + width * 0.5)
	if spider_state == "idle" and dx > -70.0 and dx < 0.0:
		spider_state = "drop"
		spr.play("default")
		if p1.flashlight_t > 0.0 or p1.gloves_t > 0.0:
			spider_state = "done"
			spr.modulate.a = 0.0
			Juice.float_text(get_parent(), global_position + Vector2(width * 0.5, -50.0), "SHOO!", Color(1.0, 0.95, 0.6))
	if spider_state == "drop" and absf(dx) < 12.0:
		spider_state = "done"
		p1.enter_zone("spider")
		var tw := create_tween()
		tw.tween_property(spr, "modulate:a", 0.0, 0.6)


func _process(_delta: float) -> void:
	if not cycles:
		return
	var ph := phase()
	var frozen := is_frozen()
	if spr != null:
		var on_now := ph == 2 and not frozen and not used
		spr.modulate.a = move_toward(spr.modulate.a, 0.9 if on_now else 0.0, 0.1)
		spr.modulate.b = 1.0
		if on_now:
			spr.play("default")
		elif not frozen:
			spr.pause()
	if warn_icon != null:
		warn_icon.visible = ph == 1 and not frozen and not _fan_near()

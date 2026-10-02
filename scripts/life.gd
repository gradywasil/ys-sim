extends Node
## Ambient life: animated props, cats, floor clutter, light shafts, floating dust, foreground parallax.

const CatS = preload("res://scripts/cat.gd")
const Themes = preload("res://scripts/data/themes.gd")
const DECOS := [
	"sock", "cereal_bowl", "toy_car", "controller", "sneaker", "juice_box", "crayons", "marble", "pizza",
	"slime", "pencil", "bouncy_ball", "action_figure", "battery", "candy_wrapper", "cassette", "dice",
	"paper_plane", "rubiks_cube", "yo_yo",
]
const GROUND_Y := 200.0

var world: Node2D
var p1
var cats: Array = []
var spawned: Array = []
var next_cat_x := 110.0
var next_prop_x := 200.0
var dust_layers: Array = []
var motes: Array = []
var robot: AnimatedSprite2D
var robot_dir := 1.0
var rng := RandomNumberGenerator.new()


## Places an animated prop. anchor: "bottom", "top" or "center" relative to `pos` (world units).
func prop(parent: Node, n: String, pos: Vector2, anchor: String = "bottom", flip: bool = false) -> AnimatedSprite2D:
	var s := Art.sprite(n)
	var sz := Art.frame_size(n)
	match anchor:
		"bottom":
			s.position = pos + Vector2(0, -sz.y * 0.5)
		"top":
			s.position = pos + Vector2(0, sz.y * 0.5)
		_:
			s.position = pos
	s.flip_h = flip
	s.frame = rng.randi() % maxi(1, Art.frame_count(n))
	s.speed_scale = rng.randf_range(0.9, 1.1)
	parent.add_child(s)
	return s


func _additive(item: CanvasItem) -> void:
	var m := CanvasItemMaterial.new()
	m.blend_mode = CanvasItemMaterial.BLEND_MODE_ADD
	item.material = m


func _layer(bg: ParallaxBackground, motion: float, mirror: float) -> ParallaxLayer:
	var l := ParallaxLayer.new()
	l.motion_scale = Vector2(motion, 1.0)
	l.motion_mirroring = Vector2(mirror, 0.0)
	bg.add_child(l)
	return l


## Background props, light and dust. `bg` is the main ParallaxBackground.
func build_background(bg: ParallaxBackground) -> void:
	rng.seed = 5
	# Wall layer (same depth as bg_far): curtains, ceiling fan, mobile, the clock.
	var far := _layer(bg, 0.12, 480.0)
	prop(far, "prop_curtain", Vector2(261, 18), "top")
	prop(far, "prop_curtain", Vector2(396, 18), "top", true)
	prop(far, "prop_fan", Vector2(190, 0), "top")
	prop(far, "prop_mobile", Vector2(330, 0), "top")
	prop(far, "prop_clock", Vector2(455, 70), "center")

	# Shelf-top and desk props ride on the mid layer, matching bg_mid.
	var mid := _layer(bg, 0.4, 640.0)
	prop(mid, "prop_lavalamp", Vector2(50, 38))
	prop(mid, "prop_snowglobe", Vector2(85, 38))
	prop(mid, "prop_lamp", Vector2(122, 38))
	prop(mid, "prop_fishbowl", Vector2(232, 144))
	prop(mid, "prop_plant", Vector2(637, GROUND_Y))
	robot = prop(mid, "prop_windup_robot", Vector2(60, GROUND_Y))

	# Moonlight shaft + drifting dust, additive so they glow over everything behind.
	var shaft_layer := _layer(bg, 0.3, 960.0)
	var shaft := Art.sprite("light_godray_anim")
	shaft.centered = false
	shaft.position = Vector2(270, 0)
	shaft.modulate = Color(1, 1, 1, 0.55)
	_additive(shaft)
	shaft_layer.add_child(shaft)
	for i in 22:
		var m := Art.sprite("fx_mote")
		m.position = Vector2(rng.randf_range(250, 400), rng.randf_range(10, 200))
		m.modulate = Color(1.0, 0.95, 0.75, rng.randf_range(0.4, 0.9))
		m.frame = rng.randi() % 6
		_additive(m)
		shaft_layer.add_child(m)
		motes.append({"n": m, "v": Vector2(rng.randf_range(-3, 6), rng.randf_range(2, 8)), "ph": rng.randf() * TAU})
	for i in 6:
		var f := Art.sprite("fx_firefly")
		f.position = Vector2(rng.randf_range(30, 450), rng.randf_range(60, 170))
		f.frame = rng.randi() % 8
		_additive(f)
		mid.add_child(f)
		motes.append({"n": f, "v": Vector2(rng.randf_range(-6, 6), rng.randf_range(-4, 4)), "ph": rng.randf() * TAU})


## Foreground parallax for one theme, drawn above the world (below the HUD). Returns its ParallaxBackground.
func build_foreground(parent: Node, theme: int = 0) -> ParallaxBackground:
	var pre := Themes.prefix(theme)
	var fg := ParallaxBackground.new()
	fg.layer = 5
	parent.add_child(fg)
	var legs := _layer(fg, 1.45, 480.0)
	var s := Sprite2D.new()
	s.texture = Art.tex(pre + "fg_legs")
	s.centered = false
	s.scale = Vector2(Art.W, Art.W)
	# P1 sits ~35% across the screen; fade foreground silhouettes out around it so they never hide the action.
	var sh := Shader.new()
	sh.code = """shader_type canvas_item;
void fragment() {
	float d = abs(SCREEN_UV.x - 0.35);
	COLOR.a *= smoothstep(0.2, 0.36, d);
}"""
	var mat := ShaderMaterial.new()
	mat.shader = sh
	s.material = mat
	legs.add_child(s)
	var dust := _layer(fg, 1.9, 480.0)
	var d := Sprite2D.new()
	d.texture = Art.tex(pre + "fg_dust")
	d.centered = false
	d.scale = Vector2(Art.W, Art.W)
	d.modulate = Color(1, 1, 1, 0.45)
	_additive(d)
	dust.add_child(d)
	dust_layers.append(dust)
	return fg


## Hooks the streaming level into the life system.
func setup(world_node: Node2D, player) -> void:
	world = world_node
	p1 = player
	rng.seed = 21


## Scatters clutter, themed props and the occasional cat over a freshly built flat stretch of floor.
func decorate(x0: float, x1: float, blocks: Array, theme: int = 0) -> void:
	var x := x0 + rng.randf_range(60.0, 100.0)
	while x < x1 - 40.0:
		if x > 110.0 and not _near_block(x, blocks):
			_deco(x, theme)
		x += rng.randf_range(90.0, 170.0)
	if theme != 0 and x1 - x0 >= 64.0 and x0 >= next_prop_x:
		_world_prop(theme, x0, x1, blocks)
	if x1 - x0 >= 128.0 and x0 >= next_cat_x and rng.randf() < 0.6:
		var c := CatS.new()
		c.position = Vector2(x0 + (x1 - x0) * 0.4, GROUND_Y + 1.0)
		c.p1 = p1
		world.add_child(c)
		cats.append(c)
		spawned.append({"node": c, "x": x1})
		next_cat_x = x0 + rng.randf_range(450.0, 700.0)


func _near_block(x: float, blocks: Array) -> bool:
	for bx in blocks:
		if absf(x - bx) < 60.0:
			return true
	return false


func _deco(x: float, theme: int) -> void:
	var pre := Themes.prefix(theme) + "deco_"
	var names: Array = DECOS.map(func(n): return "deco_" + n) if theme == 0 else Art.list(pre, ["shadow"])
	var n: String = names[rng.randi() % names.size()]
	var sz := Art.frame_size(n)
	var flip := rng.randf() < 0.5
	for suffix in ["_shadow", ""]:
		var s := Sprite2D.new()
		s.texture = Art.tex(n + suffix)
		s.scale = Vector2(-Art.W if flip else Art.W, Art.W)
		s.position = Vector2(x, GROUND_Y + 1.0 - sz.y * 0.5)
		s.z_index = -1 if suffix != "" else 0
		world.add_child(s)
		spawned.append({"node": s, "x": x})


## Animated room props in the world layer (floor pieces, hanging pieces, and things floating in the air).
func _world_prop(theme: int, x0: float, x1: float, blocks: Array) -> void:
	var defs: Array = Themes.PROPS[theme]
	var d: Array = defs[rng.randi() % defs.size()]
	var x := rng.randf_range(x0 + 24.0, x1 - 24.0)
	if d[1] == "floor" and (_near_block(x, blocks) or x < 110.0):
		return
	var sheet: String = Themes.prefix(theme) + d[0]
	var pos := Vector2(x, GROUND_Y + 1.0)
	var anchor := "bottom"
	if d[1] == "hang":
		pos = Vector2(x, float(d[2]))
		anchor = "top"
	elif d[1] == "air":
		pos = Vector2(x, float(d[2]))
		anchor = "center"
	var spr := prop(world, sheet, pos, anchor, rng.randf() < 0.5)
	spr.z_index = -1
	spawned.append({"node": spr, "x": x})
	next_prop_x = x1 + rng.randf_range(60.0, 200.0)


## Frees decor and cats that are far behind the camera.
func cull(limit: float) -> void:
	var keep: Array = []
	for e in spawned:
		if e.x < limit:
			if is_instance_valid(e.node):
				e.node.queue_free()
		else:
			keep.append(e)
	spawned = keep
	cats = cats.filter(func(c): return is_instance_valid(c) and c.global_position.x >= limit)


func on_trip() -> void:
	for c in cats:
		c.on_trip()


func on_cleared_gap() -> void:
	for c in cats:
		c.on_cleared_gap()


func confetti(parent: Node, pos: Vector2) -> void:
	for i in 28:
		var s := Art.sprite("fx_confetti")
		s.modulate = Color.from_hsv(rng.randf(), 0.6, 1.0)
		s.position = pos
		s.z_index = 60
		s.frame = rng.randi() % 10
		parent.add_child(s)
		var end := pos + Vector2(rng.randf_range(-90, 90), rng.randf_range(-70, 50))
		var tw := s.create_tween()
		tw.set_parallel(true)
		tw.tween_property(s, "position:x", end.x, 1.4).set_ease(Tween.EASE_OUT)
		tw.tween_property(s, "position:y", pos.y - rng.randf_range(40, 100), 0.5).set_ease(Tween.EASE_OUT)
		tw.chain().tween_property(s, "position:y", pos.y + 120.0, 1.0).set_ease(Tween.EASE_IN)
		tw.parallel().tween_property(s, "modulate:a", 0.0, 1.0)
		tw.chain().tween_callback(s.queue_free)


func _process(delta: float) -> void:
	var t := Time.get_ticks_msec() * 0.001
	for m in motes:
		var n: Node2D = m.n
		n.position += m.v * delta
		n.position.x += sin(t * 0.8 + m.ph) * 4.0 * delta
		if n.position.y > 210.0:
			n.position.y = 8.0
		elif n.position.y < 0.0:
			n.position.y = 200.0
	if is_instance_valid(robot):
		robot.position.x += robot_dir * 14.0 * delta
		if robot.position.x > 600.0:
			robot_dir = -1.0
		elif robot.position.x < 30.0:
			robot_dir = 1.0
		robot.flip_h = robot_dir < 0.0
	for dl in dust_layers:
		dl.motion_offset.x -= 6.0 * delta
		dl.motion_offset.y = sin(t * 0.3) * 6.0

extends Node2D
## Builds the level, HUD, and P2 hand in code, and runs the trouble/win loop.

const PickupS = preload("res://scripts/pickup.gd")
const PlayerS = preload("res://scripts/player1.gd")
const LifeS = preload("res://scripts/life.gd")
const BuilderS = preload("res://scripts/level/level_builder.gd")
const Stages = preload("res://scripts/data/stages.gd")
const Powerups = preload("res://scripts/data/powerups.gd")
const Themes = preload("res://scripts/data/themes.gd")

const GROUND_Y := 200.0
const COOLDOWN := 1.0
const MAX_TROUBLE := 3
const YELLS := ["HEY!!", "WHAT DID YOU DO?!", "I'M TELLING MOM!", "QUIT IT!"]

# Art-pixel sizes derived from Art.SCALE (autoload values can't be used in const expressions).
var peek_in := 440.0 * Art.SCALE
var peek_out := 520.0 * Art.SCALE
var world: Node2D
var life
var level
var groups: Array = []   # per theme: {sky, bg, fg}
var cur_theme := -1
var card_bg: TextureRect
var run_seed := 0
var stage := 0
var unlocked: Array = []
var avail: Array = []
var cull_t := 0.0
var card: Label
var stage_label: Label
var hud: CanvasLayer
var bot: Dictionary = {}
var start_stage := 0
var first_chunks: Array = []
var stock: Dictionary = {}
var stock_labels: Dictionary = {}
var slot_nodes: Array = []
var win_start := 0
const SLOT_WINDOW := 8
var bedtime_left := 75.0
var bedtime_max := 75.0
var bed_atlas: AtlasTexture
var bed_fill: TextureRect
var bed_label: Label
var clock_atlas: AtlasTexture
var moon_atlas: AtlasTexture
var bed_warning: AnimatedSprite2D
var badges: Dictionary = {}
var parent_anims := ["peek", "point", "sigh"]
var p1
var cam: Camera2D
var hand: Node2D
var hand_spr: AnimatedSprite2D
var ghost: Node2D
var selected := 0  # index into avail
var cooldown := 0.0
var drop_anim_t := 0.0
var hand_sx := 170.0
var trouble := 0
var coins := 0
var over := false

var pips: Array[TextureRect] = []
var slots: Array[Control] = []
var cd_fill: TextureRect
var cd_atlas: AtlasTexture
var coin_label: Label
var portrait: TextureRect
var banner: AnimatedSprite2D
var yell_bubble: Sprite2D
var parent_spr_name := "peek"
var portrait_hold := 0.0
var msg: Label
var yell: Label
var hint: Label
var parent_peek: AnimatedSprite2D
var vig_mat: ShaderMaterial
var dark_mat: ShaderMaterial
var dark_amt := 0.0
var fog_rect: ColorRect
var fog_t := 0.0
var cone_amt := 0.0


func _ready() -> void:
	add_to_group("main")
	Input.mouse_mode = Input.MOUSE_MODE_HIDDEN
	_parse_args()
	life = LifeS.new()
	add_child(life)
	_build_background()
	world = Node2D.new()
	add_child(world)
	level = BuilderS.new()
	world.add_child(level)
	level.stage_idx = start_stage
	stage = start_stage
	level.forced_chunks = first_chunks
	life.setup(world, null)
	level.setup(world, life, run_seed)
	_build_player()
	life.p1 = p1
	for th in Themes.THEMES.size():
		groups[th].fg = life.build_foreground(self, th)
	_set_theme(0, true)
	_build_camera()
	_build_hand()
	unlocked = Stages.unlocked_through(stage)
	p1.unlocked = unlocked
	for id in unlocked:
		if Powerups.DEFS[id].get("limited", false):
			stock[id] = 1
	_build_darkness()
	_build_hud()
	_rebuild_slots()
	_apply_stage(stage, true)
	level.ensure(cam.position.x + 240.0)


# --- building ---------------------------------------------------------------

func _build_background() -> void:
	var sky_layer := CanvasLayer.new()
	sky_layer.layer = -20
	add_child(sky_layer)
	for th in Themes.THEMES.size():
		var pre := Themes.prefix(th)
		var g := {}
		var grad := TextureRect.new()
		grad.texture = Art.tex("bg_sky_gradient" if th == 0 else pre + "sky_gradient")
		grad.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		grad.stretch_mode = TextureRect.STRETCH_SCALE
		grad.size = Vector2(480, 270) * Art.SCALE
		sky_layer.add_child(grad)
		g.sky = grad
		var bg := ParallaxBackground.new()
		bg.layer = -10
		add_child(bg)
		g.bg = bg
		var far := _layer(bg, 0.12, 480.0)
		_bg_sprite(far, Sprite2D.new(), pre + "bg_far")
		var anim := Art.sprite("bg_far_stars" if th == 0 else pre + "bg_far_anim")
		anim.centered = false
		far.add_child(anim)
		_bg_sprite(_layer(bg, 0.4, 640.0), Sprite2D.new(), pre + "bg_mid")
		_bg_sprite(_layer(bg, 0.7, 480.0), Sprite2D.new(), pre + "bg_near")
		if th == 0:
			life.build_background(bg)
		g.fg = null
		groups.append(g)


## Cross-fades the room (sky, parallax layers, foreground) to theme `th`.
func _set_theme(th: int, instant: bool = false) -> void:
	if th == cur_theme:
		return
	cur_theme = th
	var dur := 0.0 if instant else 1.4
	for i in groups.size():
		var g: Dictionary = groups[i]
		var a := 1.0 if i == th else 0.0
		var nodes: Array = [g.sky]
		nodes.append_array(g.bg.get_children())
		if g.fg != null:
			nodes.append_array(g.fg.get_children())
		if a > 0.0:
			g.bg.visible = true
			if g.fg != null:
				g.fg.visible = true
		for n in nodes:
			var tw: Tween = n.create_tween()
			tw.tween_property(n, "modulate:a", a, dur)
		if a == 0.0:
			var tw2 := create_tween()
			tw2.tween_interval(dur)
			tw2.tween_callback(func():
				if cur_theme != i:
					g.bg.visible = false
					if g.fg != null:
						g.fg.visible = false)


func _bg_sprite(layer: ParallaxLayer, s: Sprite2D, n: String) -> void:
	s.texture = Art.tex(n)
	s.centered = false
	s.scale = Vector2(Art.W, Art.W)
	layer.add_child(s)


func _layer(bg: ParallaxBackground, motion: float, mirror: float) -> ParallaxLayer:
	var l := ParallaxLayer.new()
	l.motion_scale = Vector2(motion, 1.0)
	l.motion_mirroring = Vector2(mirror, 0.0)
	bg.add_child(l)
	return l


func _build_player() -> void:
	p1 = PlayerS.new()
	p1.position = Vector2(40, GROUND_Y - 10.0)
	world.add_child(p1)
	p1.tripped.connect(_on_tripped)
	p1.collected.connect(_on_collected)
	p1.hurt_by_hazard.connect(func(): _add_time(-4.0))
	p1.slipped.connect(func(): _add_time(-3.0))
	p1.penalty.connect(func(sec): _add_time(sec))
	p1.cleared_gap.connect(life.on_cleared_gap)


func _build_camera() -> void:
	cam = Camera2D.new()
	cam.position = Vector2(240, 135)
	cam.zoom = Vector2(Art.SCALE, Art.SCALE)
	cam.limit_left = 0
	add_child(cam)
	cam.make_current()
	Juice.camera = cam


func _build_hand() -> void:
	hand = Node2D.new()
	hand.z_index = 50
	world.add_child(hand)
	var line := Line2D.new()
	line.points = PackedVector2Array([Vector2(0, 30), Vector2(0, GROUND_Y - 24.0)])
	line.width = 1.0
	line.default_color = Color(1, 1, 1, 0.18)
	hand.add_child(line)
	# The item is added first so the fingers draw over it.
	ghost = Node2D.new()
	ghost.position = Vector2(0, 19)
	hand.add_child(ghost)
	hand_spr = AnimatedSprite2D.new()
	hand_spr.sprite_frames = Art.frames_multi("hand_", ["idle", "hold", "drop", "cooldown"])
	hand_spr.scale = Vector2(Art.W, Art.W)
	hand.add_child(hand_spr)
	hand_spr.play("hold")


## Basement darkness: a full-screen overlay (above the world, below the HUD) with a lit circle around P1,
## a flashlight cone when P1 has one, and a small light around the hand so Player 2 can still see to play.
func _build_darkness() -> void:
	var layer := CanvasLayer.new()
	layer.layer = 6
	add_child(layer)
	var rect := ColorRect.new()
	rect.size = Vector2(480, 270) * Art.SCALE
	rect.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var sh := Shader.new()
	sh.code = """shader_type canvas_item;
uniform vec2 p1 = vec2(0.35, 0.7);
uniform vec2 hand = vec2(0.35, 0.1);
uniform float dark = 0.0;
uniform float cone = 0.0;
uniform float facing = 1.0;
void fragment() {
	vec2 d = (UV - p1) * vec2(16.0, 9.0);
	float lit = 1.0 - smoothstep(1.7, 2.6, length(d));
	float along = d.x * facing;
	float across = abs(d.y);
	float c = cone * step(0.0, along) * (1.0 - smoothstep(0.0, 1.0, across / (0.5 + along * 0.3))) * (1.0 - smoothstep(5.5, 7.5, along));
	vec2 h = (UV - hand) * vec2(16.0, 9.0);
	float hl = 1.0 - smoothstep(0.7, 1.4, length(h));
	float l = clamp(max(max(lit, c), hl), 0.0, 1.0);
	l = floor(l * 6.0 + 0.5) / 6.0;
	COLOR = vec4(0.02, 0.02, 0.08, dark * (1.0 - l) * 0.93);
}"""
	dark_mat = ShaderMaterial.new()
	dark_mat.shader = sh
	rect.material = dark_mat
	layer.add_child(rect)


## Dust cloud: the whole play area fogs up for a moment, so you can't see what's ahead.
func fog(sec: float) -> void:
	if fog_rect == null:
		var layer := CanvasLayer.new()
		layer.layer = 7
		add_child(layer)
		fog_rect = ColorRect.new()
		fog_rect.size = Vector2(480, 270) * Art.SCALE
		fog_rect.color = Color(0.82, 0.76, 0.62, 0.0)
		fog_rect.mouse_filter = Control.MOUSE_FILTER_IGNORE
		layer.add_child(fog_rect)
	if fog_t > 0.0:
		fog_t = sec
		return
	fog_t = sec
	var tw := create_tween()
	tw.tween_property(fog_rect, "color:a", 0.78, 0.3)
	tw.tween_callback(func(): fog_fade())


func fog_fade() -> void:
	var tw := create_tween()
	tw.tween_interval(maxf(0.1, fog_t - 0.3))
	tw.tween_property(fog_rect, "color:a", 0.0, 0.8)
	tw.tween_callback(func(): fog_t = 0.0)


func _update_darkness(delta: float) -> void:
	dark_amt = move_toward(dark_amt, 1.0 if cur_theme == 3 else 0.0, delta * 0.8)
	cone_amt = move_toward(cone_amt, 1.0 if p1.flashlight_t > 0.0 else 0.0, delta * 3.0)
	var left := cam.position.x - 240.0
	dark_mat.set_shader_parameter("dark", dark_amt)
	dark_mat.set_shader_parameter("cone", cone_amt)
	dark_mat.set_shader_parameter("facing", p1.facing)
	dark_mat.set_shader_parameter("p1", Vector2((p1.global_position.x - left) * 2.0 / 960.0, (p1.global_position.y - 4.0) * 2.0 / 540.0))
	dark_mat.set_shader_parameter("hand", Vector2((hand.global_position.x - left) * 2.0 / 960.0, (hand.global_position.y + 8.0) * 2.0 / 540.0))


func _build_hud() -> void:
	# The HUD lives in screen pixels (960x540), so layout values are written in world units and scaled by S.
	var S := float(Art.SCALE)
	hud = CanvasLayer.new()
	hud.layer = 10
	add_child(hud)

	var vig := ColorRect.new()
	vig.size = Vector2(480, 270) * S
	vig.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var sh := Shader.new()
	sh.code = """shader_type canvas_item;
uniform float strength = 0.4;
uniform vec4 flash_color : source_color = vec4(1.0, 0.1, 0.1, 1.0);
uniform float flash = 0.0;
uniform float pulse = 0.0;
void fragment() {
	vec2 uv = UV - 0.5;
	float v = smoothstep(0.3, 0.85, length(uv * vec2(1.0, 1.15)));
	float f = max(flash, pulse);
	COLOR = vec4(mix(vec3(0.0), flash_color.rgb, f), v * strength + f * v * 0.9);
}"""
	vig_mat = ShaderMaterial.new()
	vig_mat.shader = sh
	vig.material = vig_mat
	hud.add_child(vig)
	bed_warning = Art.sprite("ui_bedtime_warning")
	bed_warning.scale = Vector2.ONE
	bed_warning.position = Vector2(480, 270)
	bed_warning.visible = false
	hud.add_child(bed_warning)

	portrait = TextureRect.new()
	portrait.texture = Art.tex("portrait_p1_happy")
	portrait.position = Vector2(12, 8)
	hud.add_child(portrait)
	_label(hud, "TROUBLE", Vector2(84, 14), 16, Color(1, 0.8, 0.8))
	for i in MAX_TROUBLE:
		var pip := TextureRect.new()
		pip.position = Vector2(84 + i * 30, 38)
		pip.size = Vector2(24, 24)
		hud.add_child(pip)
		pips.append(pip)
	_update_pips()
	coin_label = _label(hud, "COINS 0", Vector2(784, 14), 16, Color(1, 0.9, 0.35))
	coin_label.custom_minimum_size = Vector2(160, 0)
	coin_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT

	stage_label = _label(hud, "", Vector2(0, 14), 16, Color(1, 1, 1, 0.9))
	stage_label.custom_minimum_size = Vector2(960, 0)
	stage_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	# Bedtime: Mom's "lights out" countdown, shown as a draining bar with a clock.
	var bw := 160 * Art.SCALE
	var bed_track := TextureRect.new()
	bed_track.texture = Art.atlas("ui_cooldown_bar", Rect2(0, 0, bw, 6 * Art.SCALE))
	bed_track.position = Vector2(320, 46)
	hud.add_child(bed_track)
	bed_atlas = Art.atlas("ui_cooldown_bar", Rect2(bw, 0, bw, 6 * Art.SCALE))
	bed_fill = TextureRect.new()
	bed_fill.texture = bed_atlas
	bed_fill.position = Vector2(320, 46)
	hud.add_child(bed_fill)
	var clock := TextureRect.new()
	clock_atlas = Art.atlas("ui_bedtime_clock", Rect2(0, 0, 96, 96))
	clock.texture = clock_atlas
	clock.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	clock.size = Vector2(48, 48)
	clock.position = Vector2(266, 28)
	hud.add_child(clock)
	var moon := TextureRect.new()
	moon_atlas = Art.atlas("ui_bedtime_moon", Rect2(0, 0, 48, 48))
	moon.texture = moon_atlas
	moon.position = Vector2(716, 26)
	hud.add_child(moon)
	bed_label = _label(hud, "", Vector2(652, 40), 16, Color(1, 1, 1, 0.95))
	card_bg = TextureRect.new()
	card_bg.position = Vector2(240, 118)
	card_bg.modulate.a = 0.0
	hud.add_child(card_bg)
	card = _label(hud, "", Vector2(0, 150), 16, Color(1, 0.95, 0.7))
	card.custom_minimum_size = Vector2(960, 0)
	card.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	card.modulate.a = 0.0

	var bar_w := 160 * Art.SCALE
	var track := TextureRect.new()
	track.texture = Art.atlas("ui_cooldown_bar", Rect2(0, 0, bar_w, 6 * Art.SCALE))
	track.position = Vector2(163, 265) * S
	hud.add_child(track)
	cd_atlas = Art.atlas("ui_cooldown_bar", Rect2(bar_w, 0, bar_w, 6 * Art.SCALE))
	cd_fill = TextureRect.new()
	cd_fill.texture = cd_atlas
	cd_fill.position = Vector2(163, 265) * S
	hud.add_child(cd_fill)

	parent_peek = AnimatedSprite2D.new()
	if Art.has("parent_happy"):
		parent_anims.append("happy")
	if Art.has("parent_bedtime"):
		parent_anims.append("bedtime")
	parent_peek.sprite_frames = Art.frames_multi("parent_", parent_anims)
	parent_peek.position = Vector2(peek_out, 400.0)
	parent_peek.play("peek")
	hud.add_child(parent_peek)

	yell_bubble = Sprite2D.new()
	yell_bubble.texture = Art.tex("parent_speech_yell")
	yell_bubble.position = Vector2(720, 250)
	yell_bubble.modulate.a = 0.0
	hud.add_child(yell_bubble)
	yell = _label(hud, "", Vector2(624, 222), 16, Color(0.3, 0.05, 0.1))
	yell.custom_minimum_size = Vector2(192, 0)
	yell.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	Art.style_label(yell, 16, Color(0.3, 0.05, 0.1), 0)

	banner = AnimatedSprite2D.new()
	banner.position = Vector2(480, 150)
	banner.visible = false
	hud.add_child(banner)
	msg = _label(hud, "", Vector2(0, 216), 16, Color.WHITE)
	msg.custom_minimum_size = Vector2(960, 0)
	msg.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	hint = _label(hud, "CLICK/SPACE drop  |  A/D move  |  1-9, Q/E or wheel pick item  |  R restart", Vector2(0, 440), 16, Color(1, 1, 1, 0.8))
	hint.custom_minimum_size = Vector2(960, 0)
	hint.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	var tw := hint.create_tween()
	tw.tween_interval(6.0)
	tw.tween_property(hint, "modulate:a", 0.0, 1.0)


func _label(parent: Node, text: String, pos: Vector2, size: int, color: Color) -> Label:
	var l := Label.new()
	l.text = text
	l.position = pos
	Art.style_label(l, size, color, 4)
	parent.add_child(l)
	return l


func _update_pips() -> void:
	for i in pips.size():
		var ps := 12 * Art.SCALE
		pips[i].texture = Art.atlas("ui_trouble_pip", Rect2(ps if i < trouble else 0, 0, ps, ps))


# --- gameplay ---------------------------------------------------------------

func _process(delta: float) -> void:
	cooldown = maxf(0.0, cooldown - delta)
	drop_anim_t = maxf(0.0, drop_anim_t - delta)
	var target_x := maxf(240.0, p1.global_position.x + 70.0)
	cam.position.x = lerpf(cam.position.x, target_x, minf(1.0, 6.0 * delta))
	var dir := Input.get_axis("ui_left", "ui_right")
	if Input.is_key_pressed(KEY_A):
		dir -= 1.0
	if Input.is_key_pressed(KEY_D):
		dir += 1.0
	hand_sx = clampf(hand_sx + clampf(dir, -1.0, 1.0) * 220.0 * delta, 8.0, 472.0)
	hand.global_position = Vector2(cam.position.x - 240.0 + hand_sx, 30.0 + sin(Time.get_ticks_msec() * 0.005) * 1.5)
	ghost.visible = cooldown <= 0.0 and drop_anim_t <= 0.0 and not over
	var want := "idle" if over else ("drop" if drop_anim_t > 0.0 else ("cooldown" if cooldown > 0.0 else "hold"))
	if hand_spr.animation != want:
		hand_spr.play(want)
	var bar_w := 160.0 * Art.SCALE
	cd_atlas.region = Rect2(bar_w, 0, maxf(1.0, bar_w * (1.0 - cooldown / COOLDOWN)), 6 * Art.SCALE)
	cd_fill.size = cd_atlas.region.size
	portrait_hold = maxf(0.0, portrait_hold - delta)
	var face := "tripped" if portrait_hold > 0.0 else ("happy" if trouble == 0 else ("worried" if trouble == 1 else "angry"))
	portrait.texture = Art.tex("portrait_p1_" + face)
	if not over:
		bedtime_left -= delta
		if bot.get("showcase", false) and bedtime_left < 25.0:
			bedtime_left = bedtime_max  # showcase captures never run out of time
		if bedtime_left <= 0.0:
			bedtime_left = 0.0
			_finish("bedtime")
	_update_bedtime_hud()
	_update_status()
	_update_darkness(delta)
	level.ensure(cam.position.x + 240.0)
	cull_t += delta
	if cull_t > 1.0:
		cull_t = 0.0
		level.cull(cam.position.x - 240.0)
	level.show_preview(avail[selected], hand.global_position.x, cooldown <= 0.0 and not over)
	if not level.gates.is_empty() and p1.global_position.x > level.gates[0].x:
		_on_stage_cleared(level.gates.pop_front().stage)
	if not bot.is_empty():
		_bot_tick(delta)


func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventMouseMotion:
		hand_sx = event.position.x / float(Art.SCALE)
	elif event is InputEventMouseButton and event.pressed:
		match event.button_index:
			MOUSE_BUTTON_LEFT:
				_drop()
			MOUSE_BUTTON_WHEEL_UP:
				_select(selected - 1)
			MOUSE_BUTTON_WHEEL_DOWN:
				_select(selected + 1)
	elif event is InputEventKey and event.pressed and not event.echo:
		if event.keycode >= KEY_1 and event.keycode <= KEY_9:
			if int(event.keycode - KEY_1) < avail.size():
				_select(int(event.keycode - KEY_1))
			return
		match event.keycode:
			KEY_Q:
				_select(selected - 1)
			KEY_E:
				_select(selected + 1)
			KEY_SPACE:
				_drop()
			KEY_T:
				if OS.is_debug_build():
					p1.trip("debug")
			KEY_N:
				if OS.is_debug_build():
					# Debug: jump the generator to the next stage so the floor, obstacles and room all change.
					level.stage_idx = stage + 1
					level.stage_chunks_done = 0
					_on_stage_cleared(stage + 1)
			KEY_M:
				if OS.is_debug_build():
					p1.global_position.x += 700.0  # debug: skip ahead
			KEY_H, KEY_J:
				if OS.is_debug_build():
					var hz = preload("res://scripts/level/hazard.gd").new()
					hz.kind = "burner" if event.keycode == KEY_H else "sprinkler"
					hz.position = Vector2(p1.global_position.x + 150.0, GROUND_Y)
					world.add_child(hz)
			KEY_R:
				Engine.time_scale = 1.0
				get_tree().reload_current_scene()


func _select(i: int) -> void:
	if avail.is_empty():
		return
	selected = wrapi(i, 0, avail.size())
	# Keep the selection inside the visible window of slots; rebuild the widgets only when it scrolls.
	var new_start := clampi(win_start, maxi(0, selected - SLOT_WINDOW + 1), mini(selected, maxi(0, avail.size() - SLOT_WINDOW)))
	if new_start != win_start or slots.is_empty():
		win_start = new_start
		_build_slot_widgets()
	for n in slots.size():
		var on: bool = win_start + n == selected
		slots[n].texture = Art.atlas("ui_slot", Rect2((52 * Art.SCALE) if on else 0, 0, 52 * Art.SCALE, 28 * Art.SCALE))
	for c in ghost.get_children():
		c.queue_free()
	ghost.add_child(PickupS.build_icon(avail[selected]))


func _drop() -> void:
	if over or cooldown > 0.0:
		return
	var id: String = avail[selected]
	if Powerups.DEFS[id].get("limited", false):
		if stock.get(id, 0) <= 0:
			Juice.shake(0.05)
			Juice.float_text(world, hand.global_position + Vector2(0, 40), "NONE LEFT", Color(1.0, 0.6, 0.5))
			return
		stock[id] -= 1
		_update_stock()
	cooldown = COOLDOWN
	drop_anim_t = 0.22
	var it = PickupS.new()
	it.kind = id
	it.position = hand.global_position + Vector2(0, 22)
	world.add_child(it)


## Recomputes the available items from what's unlocked (coins are world-only, not droppable here).
func _rebuild_slots() -> void:
	var prev: String = avail[selected] if not avail.is_empty() and selected < avail.size() else ""
	avail = Powerups.ORDER.filter(func(id): return unlocked.has(id))
	win_start = 0
	slots.clear()
	selected = maxi(0, avail.find(prev)) if prev != "" else 0
	_select(selected)


## Builds the visible window of item slots, with arrows when more items are off-screen.
func _build_slot_widgets() -> void:
	for sl in slot_nodes:
		sl.queue_free()
	slot_nodes.clear()
	slots.clear()
	stock_labels.clear()
	var S := float(Art.SCALE)
	var count := mini(SLOT_WINDOW, avail.size() - win_start)
	var total := 55.0 * float(count) - 3.0
	var x0 := 240.0 - total * 0.5
	for n in count:
		var idx := win_start + n
		var slot := TextureRect.new()
		slot.position = Vector2(x0 + 55.0 * float(n), 236) * S
		slot.size = Vector2(52, 28) * S
		hud.add_child(slot)
		slots.append(slot)
		slot_nodes.append(slot)
		var icon: Node2D = PickupS.build_icon(avail[idx])
		icon.position = Vector2(32, 14) * S
		icon.scale = Vector2(S, S)
		slot.add_child(icon)
		if idx < 3:
			var key := TextureRect.new()
			key.texture = Art.tex("ui_key_%d" % (idx + 1))
			key.position = Vector2(4, 9) * S
			slot.add_child(key)
		else:
			var kl := _label(slot, "%d" % (idx + 1), Vector2(8, 12), 16, Color.WHITE)
			kl.add_theme_constant_override("outline_size", 4)
		if Powerups.DEFS[avail[idx]].get("limited", false):
			stock_labels[avail[idx]] = _label(slot, "", Vector2(74, 32), 16, Color(1, 0.95, 0.6))
	if win_start > 0:
		var la := _label(hud, "<", Vector2(x0 * S - 22.0, 242.0 * S), 16, Color(1, 1, 1, 0.8))
		slot_nodes.append(la)
	if win_start + count < avail.size():
		var ra := _label(hud, ">", Vector2((x0 + total) * S + 8.0, 242.0 * S), 16, Color(1, 1, 1, 0.8))
		slot_nodes.append(ra)
	_update_stock()


func _on_collected(kind: String) -> void:
	if kind == "coin":
		coins += 1
		coin_label.text = "COINS %d" % coins
	elif kind == "cookie":
		if trouble > 0:
			trouble -= 1
			_update_pips()
		_add_time(10.0)
		_say("MMM... COOKIE!")
		_peek_parent("happy" if parent_anims.has("happy") else "sigh")


func _on_tripped(kind: String) -> void:
	trouble += 1
	if not bot.is_empty():
		var lx := 0.0
		for hz in get_tree().get_nodes_in_group("hazard"):
			if hz.global_position.x > p1.global_position.x - 120.0 and (lx == 0.0 or hz.global_position.x < lx):
				lx = hz.global_position.x
		print("  [lane x0=%d p1=%d p1y=%d vy=%d]" % [int(lx), int(p1.global_position.x), int(p1.global_position.y), int(p1.velocity.y)])
		for pk in get_tree().get_nodes_in_group("pickups"):
			print("    pickup %s at (%d,%d) landed=%s" % [pk.kind, int(pk.global_position.x), int(pk.global_position.y), pk.landed])
		var gp: Dictionary = level.nearest_gap(p1.global_position.x + 40.0, 160.0)
		if not gp.is_empty():
			print("    gap %d-%d bridged=%s" % [int(gp.x0), int(gp.x1), gp.bridged])
		print("  TRIP %s x=%d floor=%s wait=%.2f need=%s boots=%.1f umb=%.1f feather=%.1f stage=%d" % [kind, int(p1.global_position.x), p1.is_on_floor(), p1.wait_t, str(p1.need_ids), p1.boots_t, p1.umbrella_t, p1.feather_t, stage + 1])
	_update_pips()
	portrait_hold = 1.0
	life.on_trip()
	_add_time(-5.0)
	vig_mat.set_shader_parameter("flash", 1.0)
	create_tween().tween_property(vig_mat, "shader_parameter/flash", 0.0, 0.7)
	_say(YELLS[randi() % YELLS.size()])
	if trouble >= MAX_TROUBLE:
		_finish("grounded")
		return
	_peek_parent("peek")


## Shows the parent's speech bubble with `text`, then fades it.
func _say(text: String) -> void:
	yell.text = text
	yell.modulate.a = 1.0
	yell_bubble.modulate.a = 1.0
	var tw := create_tween()
	tw.tween_interval(1.0)
	tw.tween_property(yell, "modulate:a", 0.0, 0.4)
	tw.parallel().tween_property(yell_bubble, "modulate:a", 0.0, 0.4)


func _peek_parent(anim: String) -> void:
	parent_peek.play(anim)
	var peek := create_tween()
	peek.tween_property(parent_peek, "position:x", peek_in, 0.15).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	peek.tween_interval(1.1)
	peek.tween_property(parent_peek, "position:x", peek_out, 0.2)


# --- bedtime & stock ----------------------------------------------------------

func _add_time(sec: float) -> void:
	bedtime_left = clampf(bedtime_left + sec, 0.0, bedtime_max * 1.2)
	var l := _label(hud, "%+ds" % int(sec), Vector2(660, 62), 16, Color(0.6, 1.0, 0.6) if sec > 0.0 else Color(1.0, 0.45, 0.4))
	var tw := l.create_tween()
	tw.set_parallel(true)
	tw.tween_property(l, "position:y", 40.0, 0.9)
	tw.tween_property(l, "modulate:a", 0.0, 0.5).set_delay(0.5)
	tw.chain().tween_callback(l.queue_free)


func _update_bedtime_hud() -> void:
	var frac := clampf(bedtime_left / bedtime_max, 0.0, 1.0)
	var bw := 160.0 * Art.SCALE
	bed_atlas.region = Rect2(bw, 0, maxf(1.0, bw * frac), 6 * Art.SCALE)
	bed_fill.size = bed_atlas.region.size
	bed_fill.modulate = Color.WHITE.lerp(Color(1.0, 0.35, 0.3), clampf(1.0 - frac * 4.0, 0.0, 1.0))
	# Clock: 12 frames from "plenty of time" to "midnight"; it rings in the last seconds.
	if bedtime_left < 8.0 and not over:
		clock_atlas.atlas = Art.tex("ui_bedtime_clock_ring")
		clock_atlas.region = Rect2((int(Time.get_ticks_msec() * 0.016) % 6) * 96, 0, 96, 96)
	else:
		clock_atlas.atlas = Art.tex("ui_bedtime_clock")
		clock_atlas.region = Rect2(clampi(int((1.0 - frac) * 11.99), 0, 11) * 96, 0, 96, 96)
	moon_atlas.region = Rect2((0 if frac > 0.66 else (1 if frac > 0.33 else (2 if frac > 0.12 else 3))) * 48, 0, 48, 48)
	bed_warning.visible = bedtime_left < 15.0 and not over
	bed_warning.modulate.a = 0.35 + 0.35 * sin(Time.get_ticks_msec() * 0.006)
	var secs := int(ceil(bedtime_left))
	bed_label.text = "%d:%02d" % [secs / 60, secs % 60]
	# The room gets darker as bedtime closes in, and the edges pulse red at the end.
	vig_mat.set_shader_parameter("strength", lerpf(0.4, 0.85, clampf(1.0 - bedtime_left / 25.0, 0.0, 1.0)))
	var pulse := 0.0
	if bedtime_left < 12.0 and not over:
		pulse = 0.22 * maxf(0.0, sin(Time.get_ticks_msec() * 0.007))
	vig_mat.set_shader_parameter("pulse", pulse)


## Active timed buffs: a badge with a draining ring and the item's icon.
func _update_status() -> void:
	var active := {
		"boots": p1.boots_t, "feather": p1.feather_t, "umbrella": p1.umbrella_t, "stopwatch": level.freeze_t,
		"slippers": p1.slippers_t, "sugar": p1.sugar_t, "flashlight": p1.flashlight_t, "gloves": p1.gloves_t, "bubblewrap": p1.shield_t,
	}
	var slot := 0
	for id in active:
		var rem: float = active[id]
		var dur: float = Powerups.DEFS[id].dur
		if rem <= 0.0:
			if badges.has(id):
				badges[id].queue_free()
				badges.erase(id)
			continue
		if not badges.has(id):
			var b := Control.new()
			var bgt := TextureRect.new()
			bgt.texture = Art.tex("ui_status_bg")
			b.add_child(bgt)
			var ring := TextureRect.new()
			ring.name = "ring"
			ring.position = Vector2(4, 4)
			b.add_child(ring)
			var icon := Art.sprite("item_" + id)
			icon.scale = Vector2(0.55, 0.55)
			icon.position = Vector2(28, 28)
			b.add_child(icon)
			hud.add_child(b)
			badges[id] = b
		var badge: Control = badges[id]
		badge.position = Vector2(12 + slot * 62, 92)
		var frame := clampi(int((1.0 - rem / dur) * 15.99), 0, 15)
		badge.get_node("ring").texture = Art.atlas("ui_status_ring", Rect2(frame * 48, 0, 48, 48))
		slot += 1


func _update_stock() -> void:
	for id in stock_labels:
		var n: int = stock.get(id, 0)
		stock_labels[id].text = "x%d" % n
	for n in slots.size():
		var id: String = avail[win_start + n]
		var limited: bool = Powerups.DEFS[id].get("limited", false)
		slots[n].modulate = Color(1, 1, 1, 0.45) if limited and stock.get(id, 0) <= 0 else Color.WHITE


func _finish(reason: String) -> void:
	if over:
		return
	over = true
	p1.active = false
	banner.visible = true
	var banner_name := "ui_banner_bedtime" if reason == "bedtime" and Art.has("ui_banner_bedtime") else "ui_banner_grounded"
	banner.sprite_frames = Art.frames(banner_name)
	banner.play("default")
	var why := "Mom turned the lights off." if reason == "bedtime" else "Mom took away the console."
	msg.text = "%s\nReached stage %d: %s\nCoins: %d\nPress R to try again" % [why, stage + 1, Stages.get_stage(stage).name, coins]
	msg.add_theme_color_override("font_color", Color(1.0, 0.45, 0.4))
	if reason == "bedtime":
		yell_bubble.texture = Art.tex("parent_speech_bedtime")
		_say("BEDTIME!")
	var anim := "bedtime" if reason == "bedtime" and parent_anims.has("bedtime") else "point"
	parent_peek.play(anim)
	create_tween().tween_property(parent_peek, "position:x", peek_in, 0.25).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)


# --- stages -------------------------------------------------------------------

func _on_stage_cleared(next_stage: int) -> void:
	var prev_unlocked := unlocked.duplicate()
	stage = next_stage
	unlocked = Stages.unlocked_through(stage)
	p1.unlocked = unlocked
	var fresh: Array = unlocked.filter(func(id): return not prev_unlocked.has(id))
	# Clearing a stage calms Mom down a little.
	if trouble > 0:
		trouble -= 1
		_update_pips()
	life.confetti(world, p1.global_position + Vector2(0, -30))
	p1.react_t = 0.8
	for id in unlocked:
		if Powerups.DEFS[id].get("limited", false):
			stock[id] = mini(3, stock.get(id, 0) + 1)
	if not fresh.is_empty():
		_rebuild_slots()
	else:
		_update_stock()
	_apply_stage(stage, false, fresh)


func _apply_stage(idx: int, first: bool, fresh: Array = []) -> void:
	var st := Stages.get_stage(idx)
	var budget: float = st.bedtime
	if first:
		bedtime_left = budget
	else:
		# Leftover time carries over at half value, so fast clears are rewarded.
		var carried := minf(bedtime_left * 0.5, budget * 0.25)
		bedtime_left = budget + carried
	bedtime_max = bedtime_left
	stage_label.text = "STAGE %d  %s" % [idx + 1, st.name]
	var lines := ["STAGE %d" % (idx + 1), st.name, st.sub]
	for id in fresh:
		lines.append("NEW: %s" % Powerups.DEFS[id].name)
	var th := Themes.theme_of_stage(idx)
	_set_theme(th, first)
	_show_card("\n".join(lines), th)


func _show_card(text: String, th: int) -> void:
	card.text = text
	var lines := text.count("\n") + 1
	card.position.y = 118.0 + (144.0 - float(lines) * 20.0) * 0.5
	card_bg.texture = Art.atlas("ui_stage_card", Rect2(th * 480, 0, 480, 144))
	card.modulate.a = 0.0
	card_bg.modulate.a = 0.0
	var tw := create_tween()
	tw.set_parallel(true)
	tw.tween_property(card, "modulate:a", 1.0, 0.25)
	tw.tween_property(card_bg, "modulate:a", 1.0, 0.25)
	tw.chain().tween_interval(2.4)
	tw.chain().tween_property(card, "modulate:a", 0.0, 0.6)
	tw.parallel().tween_property(card_bg, "modulate:a", 0.0, 0.6)


# --- test bot -----------------------------------------------------------------

## `-- --bot` plays as P2 by handing P1 whatever it asks for, to verify generated levels are solvable.
## Options: --seed=N  --stages=N (stop after clearing N)  --max=SECONDS (game time).
## Run with `godot --headless --fixed-fps 60 --path . -- --bot ...` to fast-forward without changing the physics step.
func _parse_args() -> void:
	run_seed = randi() % 100000
	var args := OS.get_cmdline_user_args()
	for a in args:
		if a.begins_with("--seed="):
			run_seed = int(a.substr(7))
		elif a.begins_with("--start-stage="):
			start_stage = int(a.substr(14))
		elif a.begins_with("--first="):
			first_chunks = a.substr(8).split(",")
	if not (args.has("--bot") or args.has("--showcase")):
		return
	bot = {"stages": 3, "max": 600.0, "t": 0.0, "last_x": 0.0, "stuck": 0.0, "pick": RandomNumberGenerator.new(), "drops": 0}
	for a in args:
		if a.begins_with("--stages="):
			bot.stages = int(a.substr(9))
		elif a.begins_with("--max="):
			bot.max = float(a.substr(6))
		elif a == "--nohelp":
			bot.nohelp = true  # dev: the bot only answers P1's requests, never helps proactively
		elif a.begins_with("--prefer="):
			bot.prefer = a.substr(9)  # dev: always pick this item when it is one of the options
	if args.has("--showcase"):
		# Showcase: the bot plays on screen for video capture and never ends the run on its own.
		bot.stages = 9999
		bot.max = 99999.0
		bot.showcase = true
	bot.pick.seed = run_seed


## True if a floor hazard or zone lies within `dist` units ahead of x.
func _hazard_ahead(x: float, dist: float, groups: Array = ["hazard", "zone"]) -> bool:
	for g in groups:
		for hz in get_tree().get_nodes_in_group(g):
			var d: float = hz.global_position.x - x
			if d > -10.0 and d < dist:
				return true
	return false


## Proactive help for floor zones and traps P1 can't see coming.
const BOT_ZONE_ITEM := {"puddle": "slippers", "mud": "slippers", "wind": "fan", "cobweb": "gloves", "spider": "flashlight"}


func _bot_proactive() -> void:
	if bot.get("nohelp", false):
		return
	if cooldown > 0.0 or not p1.is_on_floor() or p1.tripped_t > 0.0:
		return
	var pref: String = bot.get("prefer", "")
	if pref == "flashlight" and avail.has("flashlight") and p1.flashlight_t <= 0.0 and p1.umbrella_t <= 0.0 and p1.feather_t <= 0.0 and absf(p1.velocity.x) > 20.0:
		_bot_buff("flashlight")
		return
	if absf(p1.velocity.x) < 20.0:
		return
	# Nearest thing ahead that needs help: a zone or a loose board.
	var target = null
	var kind := ""
	for z in get_tree().get_nodes_in_group("zone"):
		var d: float = z.global_position.x - p1.global_position.x
		if d > 70.0 and d < 230.0 and BOT_ZONE_ITEM.has(z.kind) and (target == null or z.global_position.x < target.global_position.x):
			target = z
			kind = z.kind
	for bd in get_tree().get_nodes_in_group("board"):
		var d2: float = bd.global_position.x - p1.global_position.x
		if d2 > 70.0 and d2 < 230.0 and not bd.taped and (target == null or bd.global_position.x < target.global_position.x):
			target = bd
			kind = "board"
	if target == null or target.get_meta("handled", false):
		return
	# Don't hand anything over right before P1 jumps (a mid-air P1 would trip on slippers, sugar or gloves).
	for g in level.gaps:
		if g.x0 > p1.global_position.x - 5.0 and g.x0 < p1.global_position.x + 150.0:
			return
	for bx in level.block_xs:
		if bx > p1.global_position.x - 5.0 and bx < p1.global_position.x + 150.0:
			return
	var id: String = "tape" if kind == "board" else BOT_ZONE_ITEM[kind]
	if kind == "mud" and pref == "sugar" and avail.has("sugar") and not _hazard_ahead(p1.global_position.x + 120.0, 900.0, ["hazard"]):
		id = "sugar"
	if not avail.has(id):
		target.set_meta("handled", true)
		return
	# Skip items P1 already has, or that would trip it right now.
	if (id == "slippers" and p1.slippers_t > 0.0) or (id == "sugar" and p1.sugar_t > 0.0) or (id == "gloves" and (p1.gloves_t > 0.0 or p1.mud_t > 0.0 or p1.slip_t > 0.0)):
		return
	if id == "flashlight" and (p1.flashlight_t > 0.0 or p1.umbrella_t > 0.0 or p1.feather_t > 0.0):
		return
	if pref == "" and bot.pick.randf() < 0.5:
		target.set_meta("handled", true)  # sometimes the bot lets P1 take the hit
		return
	target.set_meta("handled", true)
	if id == "fan":
		_bot_place("fan", target.global_position.x - 12.0)
	elif id == "tape":
		_bot_place("tape", target.global_position.x + target.width * 0.5)
	else:
		_bot_buff(id)


## Hands a buff to P1 by dropping it a little ahead of the running P1.
func _bot_buff(id: String) -> void:
	_select(avail.find(id))
	var lead: float = 70.0 * (1.8 if p1.boots_t > 0.0 else 1.0)
	hand_sx = clampf(p1.global_position.x + lead - (cam.position.x - 240.0), 8.0, 472.0)
	hand.global_position.x = cam.position.x - 240.0 + hand_sx
	bot.drops += 1
	_drop()


## Drops a placeable at world x.
func _bot_place(id: String, x: float) -> void:
	_select(avail.find(id))
	hand_sx = clampf(x - (cam.position.x - 240.0), 8.0, 472.0)
	hand.global_position.x = cam.position.x - 240.0 + hand_sx
	bot.drops += 1
	_drop()


func _bot_report(result: String) -> void:
	print("BOT seed=%d result=%s stage=%d x=%d t=%.0fs drops=%d coins=%d trouble=%d hurts=%d %s min_bed=%.0fs hazards=%d" % [run_seed, result, stage + 1, int(p1.global_position.x), bot.t, bot.drops, coins, trouble, p1.hurts, str(p1.hurt_src), bot.get("min_bed", 999.0), level.chunk_log.filter(func(c): return c.id.begins_with("burner") or c.id.begins_with("sprinkler")).size()])
	if result != "OK":
		for c in level.chunk_log:
			if c.x > p1.global_position.x - 400.0 and c.x < p1.global_position.x + 200.0:
				print("   near chunk: ", c.id, " @", int(c.x))
	get_tree().quit()


func _bot_tick(delta: float) -> void:
	bot.t += delta
	bot.min_bed = minf(bot.get("min_bed", 999.0), bedtime_left)
	if over:
		if bot.get("showcase", false):
			return
		_bot_report("GAME_OVER")
		return
	if stage >= bot.stages:
		_bot_report("OK")
		return
	if bot.t > bot.max:
		_bot_report("TIMEOUT")
		return
	# Only help when P1 is actually standing still, the way a person would.
	_bot_proactive()
	var waiting: bool = not p1.need_ids.is_empty() and p1.wait_t > 0.0 and absf(p1.velocity.x) < 8.0
	if p1.global_position.x > bot.last_x + 4.0:
		bot.last_x = p1.global_position.x
		bot.stuck = 0.0
	elif not waiting:
		bot.stuck += delta
		if bot.stuck > 12.0:
			_bot_report("STUCK")
			return
	if waiting and not bot.get("was_waiting", false):
		# Hazard waits resolve on their own, so the bot sometimes just waits them out.
		var hazard_only: bool = not (p1.need_ids.has("feather") or p1.need_ids.has("boots") or p1.need_ids.has("bridge"))
		bot.ignore = hazard_only and bot.pick.randf() < 0.4
	bot.was_waiting = waiting
	if waiting and bot.get("ignore", false):
		return
	if waiting and cooldown <= 0.0 and p1.is_on_floor() and p1.tripped_t <= 0.0:
		var options: Array = p1.need_ids
		if options.has("sugar") and _hazard_ahead(p1.global_position.x, 900.0):
			options = options.filter(func(i): return i != "sugar")  # a sugared P1 won't stop for hazards
		if options.is_empty():
			return
		if options.has(bot.get("prefer", "")):
			options = [bot.prefer]
		# Hazard waits: the stopwatch is timing-proof (the umbrella can arrive after the window opens and trip P1).
		if options.has("stopwatch"):
			var launchers: Array = options.filter(func(i): return i == "trampoline" or i == "ramp")
			if not launchers.is_empty() and bot.pick.randf() < 0.6:
				options = launchers  # placed launchers are timing-proof too
			else:
				if p1.boots_t > 0.0:
					return  # the stopwatch dizzies P1 while boots are active; wait for them to run out
				options = ["stopwatch"]
		var id: String = options[bot.pick.randi() % options.size()]
		_select(avail.find(id))
		var target_x: float = p1.global_position.x
		if id == "trampoline" or id == "ramp":
			var lane_x := 1.0e9
			for hz in get_tree().get_nodes_in_group("hazard"):
				if hz.lane and hz.global_position.x > p1.global_position.x - 4.0:
					lane_x = minf(lane_x, hz.global_position.x)
			if lane_x > 1.0e8:
				return
			target_x = lane_x - 8.0
			for lu in get_tree().get_nodes_in_group("launcher"):
				if absf(lu.global_position.x - target_x) < 40.0:
					return  # one is already there; let P1 reach it
		elif id == "tape":
			# Only a trap ahead of P1: tape that lands behind or on P1 would just bonk it.
			var tgt = null
			for g in ["hazard", "board"]:
				for h in get_tree().get_nodes_in_group(g):
					if (g == "hazard" and (h.lane or h.taped)) or (g == "board" and (h.taped or h.state == "fallen")):
						continue
					if h.global_position.x > p1.global_position.x + 8.0 and (tgt == null or h.global_position.x < tgt.global_position.x):
						tgt = h
			if tgt == null:
				return
			target_x = tgt.global_position.x + tgt.width * 0.5
		elif id == "bridge":
			var g: Dictionary = level.nearest_gap(p1.global_position.x + 40.0, 160.0)
			if g.is_empty():
				return
			target_x = (g.x0 + g.x1) * 0.5
		hand_sx = clampf(target_x - (cam.position.x - 240.0), 8.0, 472.0)
		hand.global_position.x = cam.position.x - 240.0 + hand_sx
		bot.drops += 1
		var rep: int = bot.get("rep", 0)
		if absf(target_x - bot.get("last_drop_x", -999.0)) < 8.0:
			rep += 1
		else:
			rep = 0
		bot.rep = rep
		bot.last_drop_x = target_x
		if rep == 4:
			print("  REPEAT drop %s: P1 x=%.1f y=%.1f vx=%.0f vy=%.0f floor=%s feather=%.1f boots=%.1f umb=%.1f wait=%.2f falls=%d need=%s" % [id, p1.global_position.x, p1.global_position.y, p1.velocity.x, p1.velocity.y, p1.is_on_floor(), p1.feather_t, p1.boots_t, p1.umbrella_t, p1.wait_t, p1.falls, str(p1.need_ids)])
		_drop()

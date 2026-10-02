extends CharacterBody2D
## Player 1: auto-runs right, jumps hazards on its own, and stops when it needs help.

signal tripped(kind: String)
signal collected(kind: String)
signal cleared_gap
signal hurt_by_hazard
signal slipped
signal penalty(sec: float)

const GRAVITY := 900.0
const BASE_SPEED := 110.0
const JUMP_V := -300.0
const HALF_H := 9.0
const TRIP_TIME := 1.2
const ANIMS := ["idle", "wait", "run", "run_fast", "jump_up", "jump_apex", "fall", "land", "trip", "boost_jump", "celebrate",
	"wait_point", "react_cheer", "react_angry", "ouch", "slip", "slog", "sprint", "flashlight_idle", "flashlight_run", "lean", "stuck", "react_scared", "idle_yawn", "idle_stretch", "idle_bounce"]
const Powerups = preload("res://scripts/data/powerups.gd")

var active := true
var celebrating := false
var boots_t := 0.0
var feather_t := 0.0
var tripped_t := 0.0
var wait_t := 0.0
var land_t := 0.0
var want := ""
var need_ids: Array = []
var unlocked: Array = ["boots", "feather", "coin"]
var umbrella_t := 0.0
var bubble_key := ""
var umbrella_vis: AnimatedSprite2D
var last_ground := Vector2.ZERO
var squash := Vector2.ONE
var facing := 1.0
var was_on_floor := true
var last_vy := 0.0
var fx_t := 0.0
var react_t := 0.0
var sweat_t := 0.0
var idle_t := 0.0
var idle_variant := ""
var jumped_wide := false
var falls := 0
var eat_t := 0.0
var boost_t := 0.0
var slip_t := 0.0
var slide_v := 0.0
var mud_t := 0.0
var sugar_t := 0.0
var crash_t := 0.0
var slippers_t := 0.0
var sugar_fx_t := 0.0
var flashlight_t := 0.0
var stuck_t := 0.0
var scare_t := 0.0
var wind_t := 0.0
var fan_t := 0.0
var gloves_t := 0.0
var shield_t := 0.0
var shield_vis: AnimatedSprite2D
var boost_mult := 1.0
var hurt_t := 0.0
var hurts := 0
var hurt_src: Dictionary = {}
var hz_wait_t := 0.0

var visual: Node2D
var spr: AnimatedSprite2D
var stars: AnimatedSprite2D
var bubble: Node2D
var bubble_label: Label


func _ready() -> void:
	add_to_group("p1")
	collision_layer = 2
	collision_mask = 1
	var cs := CollisionShape2D.new()
	var shape := RectangleShape2D.new()
	shape.size = Vector2(10, HALF_H * 2.0)
	cs.shape = shape
	add_child(cs)
	last_ground = global_position

	# Squash/stretch pivots at the feet; the 32x32 frame's bottom edge is the feet.
	visual = Node2D.new()
	visual.position = Vector2(0, HALF_H)
	add_child(visual)
	spr = AnimatedSprite2D.new()
	spr.sprite_frames = Art.frames_multi("p1_", ANIMS)
	spr.position = Vector2(0, -16)
	spr.scale = Vector2(Art.W, Art.W)
	visual.add_child(spr)
	spr.play("idle")

	bubble = Node2D.new()
	bubble.z_index = 30
	bubble.visible = false
	add_child(bubble)
	var bg := Sprite2D.new()
	bg.texture = Art.tex("fx_bubble")
	bg.position = Vector2(0, -12)
	bg.scale = Vector2(Art.W, Art.W)
	bubble.add_child(bg)
	bubble_label = Label.new()
	bubble_label.text = "NEEDS"
	Art.style_label(bubble_label, 16, Color(0.2, 0.1, 0.3), 0)
	bubble_label.scale = Vector2(Art.W, Art.W)
	bubble.add_child(bubble_label)

	umbrella_vis = AnimatedSprite2D.new()
	umbrella_vis.sprite_frames = Art.frames_ranges("fx_umbrella_canopy", {"open": [0, 3, false], "sway": [3, 8, true]})
	umbrella_vis.scale = Vector2(Art.W, Art.W)
	umbrella_vis.position = Vector2(0, -29)
	umbrella_vis.z_index = 5
	umbrella_vis.visible = false
	umbrella_vis.animation_finished.connect(func():
		if umbrella_vis.animation == "open":
			umbrella_vis.play("sway"))
	add_child(umbrella_vis)

	shield_vis = AnimatedSprite2D.new()
	shield_vis.sprite_frames = Art.frames_ranges("fx_shield_bubble", {"idle": [0, 5, true], "pop": [5, 8, false]})
	shield_vis.scale = Vector2(Art.W, Art.W)
	shield_vis.position = Vector2(0, -2)
	shield_vis.z_index = 6
	shield_vis.visible = false
	shield_vis.animation_finished.connect(func():
		if shield_vis.animation == "pop":
			shield_vis.visible = false)
	add_child(shield_vis)


func _ray(from: Vector2, to: Vector2) -> Dictionary:
	var q := PhysicsRayQueryParameters2D.create(global_position + from, global_position + to, 1)
	return get_world_2d().direct_space_state.intersect_ray(q)


func _gap_width() -> float:
	var k := 14.0
	while k < 200.0:
		if not _ray(Vector2(k, 0), Vector2(k, 30)).is_empty():
			return k - 14.0
		k += 4.0
	return 999.0


func _magnet_dx() -> float:
	var best := 0.0
	var best_d := 90.0
	for it in get_tree().get_nodes_in_group("pickups"):
		if not it.landed:
			continue
		var dx: float = it.global_position.x - global_position.x
		if absf(dx) >= best_d or absf(it.global_position.y - global_position.y) > 30.0:
			continue
		var s := signf(dx)
		if _ray(Vector2(s * 12.0, 0), Vector2(s * 12.0, 30)).is_empty():
			continue
		best_d = absf(dx)
		best = dx
	return best


func _ai(delta: float) -> void:
	if not active:
		velocity.x = move_toward(velocity.x, 0.0, 600.0 * delta)
		return
	var speed := BASE_SPEED * (1.6 if boots_t > 0.0 else 1.0) * (boost_mult if boost_t > 0.0 else 1.0)
	if sugar_t > 0.0:
		speed *= 1.8
	elif crash_t > 0.0:
		speed *= 0.55
	if mud_t > 0.0 and is_on_floor():
		speed *= 0.7 if slippers_t > 0.0 else 0.35
	if wind_t > 0.0 and fan_t <= 0.0 and is_on_floor():
		speed *= 0.3  # leaning into a gust
	if fan_t > 0.0 and is_on_floor():
		speed *= 1.5  # blown along by a fan
	if not is_on_floor():
		# Keep pushing forward mid-air so a wall bump can't leave P1 hopping in place.
		velocity.x = speed
		return
	wait_t = maxf(0.0, wait_t - delta)
	var stop := false
	var jump := false
	var need: Array = []
	var low := _ray(Vector2(0, 4), Vector2(48, 4))
	if not low.is_empty():
		var d: float = low.position.x - global_position.x
		var tall := not _ray(Vector2(0, -43), Vector2(48, -43)).is_empty()
		if tall:
			if feather_t > 0.0:
				jump = d < 38.0
			elif d < 44.0:
				stop = true
				need = ["feather"]
		elif d < 26.0:
			jump = true
	elif _ray(Vector2(14, 0), Vector2(14, 30)).is_empty():
		var gw := _gap_width()
		if gw > 64.0 and boots_t <= 0.0 and umbrella_t <= 0.0 and sugar_t <= 0.0:
			stop = true
			need = ["boots", "umbrella", "bridge", "sugar"]
		else:
			jump = true
			jumped_wide = gw > 64.0
	if not stop and not jump:
		var hz = _hazard_ahead()
		if hz != null:
			var hd: float = hz.global_position.x - global_position.x
			var cross_t: float = (maxf(hd, 0.0) + hz.width + 30.0) / speed  # includes the walk up to the hazard
			var shielded: bool = hz.kind == "sprinkler" and umbrella_t >= cross_t + 0.3
			if hd > 0.0 and hd < 54.0 and not shielded and hz.dangerous_within(cross_t + 0.3) and _launcher_ahead() == null:
				stop = true
				hz_wait_t += delta
				# Only ask for help after waiting a bit; the safe window may open on its own.
				need = hz.counters.filter(func(i): return i != "wait") if hz_wait_t > 0.8 else []
	if not stop:
		hz_wait_t = 0.0
	if sugar_t > 0.0:
		stop = false  # on a sugar rush P1 won't wait for anything
	if stop:
		wait_t = 0.5
		need_ids = need.filter(func(i): return unlocked.has(i))
		want = need_ids[0] if not need_ids.is_empty() else ""
		velocity.x = move_toward(velocity.x, 0.0, 800.0 * delta)
		return
	if wait_t <= 0.0:
		want = ""
		need_ids = []
	else:
		var mag := _magnet_dx()
		if absf(mag) > 3.0:
			wait_t = 0.5
			velocity.x = signf(mag) * 70.0
			return
	velocity.x = speed
	if jump:
		_jump()


func _hazard_ahead():
	var best = null
	var best_d := 80.0
	for hz in get_tree().get_nodes_in_group("hazard"):
		var d: float = hz.global_position.x - global_position.x
		if d > -4.0 and d < best_d:
			best_d = d
			best = hz
	return best


## Soaks up one bad event if P1 is wrapped in bubble wrap.
func _absorb() -> bool:
	if shield_t <= 0.0:
		return false
	shield_t = 0.0
	shield_vis.play("pop")
	Juice.float_text(get_parent(), global_position + Vector2(0, -30), "POP!", Color(0.7, 0.9, 1.0))
	Juice.burst(get_parent(), global_position + Vector2(0, -4), Color(0.8, 0.95, 1.0), 8, 70.0, 60.0, 0.5, Vector2.UP, 180.0)
	return true


## Called every physics frame while P1 overlaps an active zone. Returns true if the zone was "used up".
func enter_zone(kind: String) -> bool:
	match kind:
		"puddle":
			if is_on_floor() and slip_t <= 0.0 and slippers_t <= 0.0 and tripped_t <= 0.0 and hurt_t <= 0.0:
				if _absorb():
					return false
				slip_t = 1.1
				slide_v = maxf(absf(velocity.x), BASE_SPEED) * 1.35
				slipped.emit()
				Juice.shake(0.15)
				Art.fx(get_parent(), global_position + Vector2(0, 8), "fx_slip_swirl", Color(1.0, 0.8, 0.4), 1.0)
				Juice.float_text(get_parent(), global_position + Vector2(0, -30), "WHOA!", Color(1.0, 0.8, 0.4))
		"mud":
			mud_t = 0.15
		"wind":
			wind_t = 0.15
		"cobweb":
			if gloves_t > 0.0:
				Juice.float_text(get_parent(), global_position + Vector2(0, -30), "RIP!", Color(0.7, 1.0, 0.5))
				return true
			if _absorb():
				return true
			stuck_t = 1.3
			velocity.x = 0.0
			penalty.emit(-2.0)
			Juice.float_text(get_parent(), global_position + Vector2(0, -30), "STUCK!", Color(0.95, 0.9, 0.7))
			return true
		"spider":
			if _absorb():
				return false
			scare_t = 0.9
			velocity.x = 0.0
			penalty.emit(-2.0)
			Juice.shake(0.12)
			Juice.float_text(get_parent(), global_position + Vector2(0, -30), "EEK!", Color(1.0, 0.7, 0.7))
	return false


## A placed fan is blowing on P1.
func blow() -> void:
	fan_t = 0.2
	wind_t = 0.0


func hurt(src: String = "?") -> void:
	if hurt_t > 0.0 or tripped_t > 0.0:
		return
	if _absorb():
		return
	hurt_t = 0.9
	hurts += 1
	var tag := src + ("+slip" if slip_t > 0.0 else "") + ("+mud" if mud_t > 0.0 else "") + ("+boots" if boots_t > 0.0 else "") + ("+launch" if boost_t > 0.0 else "") + ("+sugar" if sugar_t > 0.0 else "") + ("+crash" if crash_t > 0.0 else "")
	hurt_src[tag] = hurt_src.get(tag, 0) + 1
	velocity = Vector2(-60.0, -110.0)
	hurt_by_hazard.emit()
	Juice.shake(0.3)
	Art.fx(get_parent(), global_position + Vector2(0, -6), "fx_impact", Color(1.0, 0.6, 0.3), 1.0)
	Juice.float_text(get_parent(), global_position + Vector2(0, -30), "OUCH!", Color(1.0, 0.5, 0.3))


## Launched upward by a trampoline or ramp.
func launch(vy: float, boost: float) -> void:
	velocity.y = vy
	if boost > 1.0:
		boost_mult = boost
		boost_t = 1.0
	squash = Vector2(0.8, 1.3)
	Juice.float_text(get_parent(), global_position + Vector2(0, -30), "BOING!", Color(0.5, 0.8, 1.0))


## A placed launcher just ahead of P1 (within reach), if any.
func _launcher_ahead():
	for lu in get_tree().get_nodes_in_group("launcher"):
		var d: float = lu.global_position.x - global_position.x
		if d > -2.0 and d < 90.0:
			return lu
	return null


func _jump() -> void:
	velocity.y = JUMP_V * (1.25 if feather_t > 0.0 else 1.0)
	squash = Vector2(0.85, 1.15)
	var feet := global_position + Vector2(0, HALF_H)
	Art.fx(get_parent(), feet + Vector2(0, -6), "fx_jump_puff", Color(0.95, 0.85, 0.75))
	Juice.burst(get_parent(), feet, Color(0.9, 0.8, 0.7), 4, 40.0, 100.0, 0.35, Vector2.UP, 90.0)


func collect(kind: String) -> void:
	collected.emit(kind)
	var def: Dictionary = Powerups.DEFS[kind]
	# A placeable only reaches P1 by landing on it.
	if def.kind == "placeable" or Powerups.trips(kind, self):
		trip(kind)
		return
	match kind:
		"boots":
			boots_t = def.dur
		"feather":
			feather_t = def.dur
		"umbrella":
			umbrella_t = def.dur
		"cookie":
			eat_t = 1.2
		"slippers":
			slippers_t = def.dur
		"sugar":
			sugar_t = def.dur
		"flashlight":
			flashlight_t = def.dur
		"gloves":
			gloves_t = def.dur
		"bubblewrap":
			shield_t = def.dur
			shield_vis.visible = true
			shield_vis.play("idle")
		"stopwatch":
			var lv = get_tree().get_first_node_in_group("level")
			if lv:
				lv.freeze(def.dur)
	Juice.float_text(get_parent(), global_position + Vector2(0, -26), def.toast, def.color)
	Art.fx(get_parent(), global_position + Vector2(0, -8), "fx_sparkle", def.color, 2.0)
	if kind != "coin":
		Art.fx(get_parent(), global_position + Vector2(0, -34), "fx_text_nice")
	react_t = 0.5
	squash = Vector2(1.15, 0.88)


func trip(kind: String) -> void:
	tripped_t = TRIP_TIME
	velocity = Vector2(-50.0, -140.0)
	tripped.emit(kind)
	Juice.hitstop(0.1)
	Juice.shake(0.7)
	Art.fx(get_parent(), global_position + Vector2(-4, -4), "fx_impact", Color(1.0, 0.9, 0.4), 1.4)
	Juice.burst(get_parent(), global_position + Vector2(0, -6), Color(1.0, 0.9, 0.3), 8, 90.0, 220.0, 0.6, Vector2.UP, 180.0)
	Art.fx(get_parent(), global_position + Vector2(0, -34), "fx_text_" + ["oof", "yikes", "whoops"][randi() % 3])
	if is_instance_valid(stars):
		stars.queue_free()
	stars = Art.sprite("fx_stars")
	stars.position = Vector2(0, -12)
	stars.modulate = Color(1.0, 0.9, 0.4)
	stars.z_index = 25
	add_child(stars)


func _physics_process(delta: float) -> void:
	boots_t = maxf(0.0, boots_t - delta)
	feather_t = maxf(0.0, feather_t - delta)
	umbrella_t = maxf(0.0, umbrella_t - delta)
	land_t = maxf(0.0, land_t - delta)
	boost_t = maxf(0.0, boost_t - delta)
	slippers_t = maxf(0.0, slippers_t - delta)
	flashlight_t = maxf(0.0, flashlight_t - delta)
	gloves_t = maxf(0.0, gloves_t - delta)
	shield_t = maxf(0.0, shield_t - delta)
	wind_t = maxf(0.0, wind_t - delta)
	fan_t = maxf(0.0, fan_t - delta)
	mud_t = maxf(0.0, mud_t - delta)
	crash_t = maxf(0.0, crash_t - delta)
	if sugar_t > 0.0:
		sugar_t -= delta
		if sugar_t <= 0.0:
			sugar_t = 0.0
			crash_t = 1.0  # the sugar crash
	if not is_on_floor():
		velocity.y += GRAVITY * delta
		if umbrella_t > 0.0 and velocity.y > 60.0:
			velocity.y = 60.0
	last_vy = velocity.y
	if tripped_t > 0.0:
		tripped_t -= delta
		velocity.x = move_toward(velocity.x, 0.0, 500.0 * delta)
		if tripped_t <= 0.0 and is_instance_valid(stars):
			stars.queue_free()
	elif stuck_t > 0.0 or scare_t > 0.0:
		stuck_t = maxf(0.0, stuck_t - delta)
		scare_t = maxf(0.0, scare_t - delta)
		velocity.x = 0.0
	elif slip_t > 0.0:
		slip_t -= delta
		velocity.x = slide_v  # out of control: no steering, no jumping
	elif hurt_t > 0.0:
		hurt_t -= delta
		velocity.x = move_toward(velocity.x, 0.0, 500.0 * delta)
	elif eat_t > 0.0:
		eat_t -= delta
		velocity.x = move_toward(velocity.x, 0.0, 700.0 * delta)
	else:
		_ai(delta)
	move_and_slide()
	var on := is_on_floor()
	if on and not was_on_floor:
		squash = Vector2(1.15, 0.88)
		land_t = 0.17
		var feet := global_position + Vector2(0, HALF_H)
		Art.fx(get_parent(), feet + Vector2(0, -6), "fx_dust", Color(0.95, 0.85, 0.75))
		Juice.burst(get_parent(), feet, Color(0.9, 0.8, 0.7), 5, 50.0, 100.0, 0.4, Vector2.UP, 120.0)
		if last_vy > 250.0:
			Juice.shake(0.12)
			Art.fx(get_parent(), feet + Vector2(0, -16), "fx_shockwave", Color(1, 0.95, 0.85), 0.6)
		if jumped_wide:
			jumped_wide = false
			cleared_gap.emit()
	was_on_floor = on
	if on and not _ray(Vector2(14, 0), Vector2(14, 30)).is_empty():
		last_ground = global_position
	if global_position.y > 340.0:
		falls += 1
		global_position = last_ground + Vector2(-16, -6)
		velocity = Vector2.ZERO
		Juice.shake(0.25)
	fx_t += delta
	if fx_t > 0.07:
		fx_t = 0.0
		_trail_fx()


func _trail_fx() -> void:
	if boots_t > 0.0 and tripped_t <= 0.0 and is_on_floor():
		Art.fx(get_parent(), global_position + Vector2(-16, 2), "fx_speedline", Color(1.0, 0.65, 0.25))
	if feather_t > 0.0:
		Art.fx(get_parent(), global_position + Vector2(randf_range(-6, 6), randf_range(-8, 4)), "fx_sparkle", Color(0.8, 0.95, 1.0))
	if sugar_t > 0.0 and is_on_floor():
		Art.fx(get_parent(), global_position + Vector2(-20.0 * facing, -2.0), "fx_sugar_blur", Color.WHITE, 1.0, facing < 0.0)


func _pick_anim() -> String:
	if tripped_t > 0.0:
		return "trip" if tripped_t > 0.5 else "react_angry"
	if hurt_t > 0.0:
		return "ouch"
	if slip_t > 0.0:
		return "slip"
	if stuck_t > 0.0:
		return "stuck"
	if scare_t > 0.0:
		return "react_scared"
	if celebrating:
		return "celebrate"
	if not is_on_floor():
		if velocity.y < -60.0:
			return "boost_jump" if feather_t > 0.0 else "jump_up"
		if velocity.y > 60.0:
			return "fall"
		return "jump_apex"
	if land_t > 0.0:
		return "land"
	if react_t > 0.0 or eat_t > 0.0:
		return "react_cheer"
	if mud_t > 0.0 and absf(velocity.x) > 5.0:
		return "slog"
	if wind_t > 0.0 and fan_t <= 0.0 and absf(velocity.x) > 5.0:
		return "lean"
	if absf(velocity.x) > 10.0:
		if sugar_t > 0.0:
			return "sprint"
		if flashlight_t > 0.0 and boots_t <= 0.0:
			return "flashlight_run"
		return "run_fast" if boots_t > 0.0 else "run"
	if wait_t > 0.0:
		if want != "" and int(Time.get_ticks_msec() / 2500) % 2 == 0:
			return "wait_point"
		return "wait"
	if flashlight_t > 0.0:
		return "flashlight_idle"
	return idle_variant if idle_variant != "" else "idle"


func _process(delta: float) -> void:
	if absf(velocity.x) > 5.0:
		facing = signf(velocity.x)
	spr.flip_h = facing < 0.0
	# The frames already carry their own squash, so only apply a light extra layer.
	squash = squash.lerp(Vector2.ONE, minf(1.0, 12.0 * delta))
	visual.scale = squash
	react_t = maxf(0.0, react_t - delta)
	# Occasional idle flourish when P1 is just standing around.
	if is_on_floor() and absf(velocity.x) <= 10.0 and wait_t <= 0.0 and tripped_t <= 0.0:
		idle_t += delta
		if idle_variant == "" and idle_t > 4.0:
			idle_variant = ["idle_yawn", "idle_stretch", "idle_bounce"][randi() % 3]
			idle_t = 0.0
	else:
		idle_t = 0.0
		idle_variant = ""
	if want != "" and wait_t > 0.0 and tripped_t <= 0.0:
		sweat_t -= delta
		if sweat_t <= 0.0:
			sweat_t = 1.4
			Art.fx(get_parent(), global_position + Vector2(facing * 8.0, -16.0), "fx_sweat", Color(0.7, 0.9, 1.0), 1.0)
	var anim := _pick_anim()
	if spr.animation != anim:
		spr.play(anim)
	var glide := umbrella_t > 0.0 and not is_on_floor()
	if glide and not umbrella_vis.visible:
		umbrella_vis.play("open")
	umbrella_vis.visible = glide
	bubble.visible = not need_ids.is_empty() and wait_t > 0.0 and tripped_t <= 0.0
	if bubble.visible:
		_layout_bubble()
		bubble.position.y = -22.0 + sin(Time.get_ticks_msec() * 0.008) * 2.0


## Shows the powerups that would help as icons: "NEEDS [boots] [umbrella] [bridge]".
func _layout_bubble() -> void:
	var key := ",".join(need_ids)
	if key == bubble_key:
		return
	bubble_key = key
	for c in bubble.get_children():
		if c != bubble_label and c.name != "Bg" and not (c is Sprite2D):
			c.queue_free()
	var label_w := 62.0   # screen pixels
	var step := 34.0
	var total := label_w + step * float(need_ids.size())
	var x0 := -total * 0.5
	bubble_label.position = Vector2(x0 * Art.W, -22.0)
	for i in need_ids.size():
		var icon: Node2D = preload("res://scripts/pickup.gd").build_icon(need_ids[i])
		icon.scale = Vector2(0.62, 0.62)
		icon.position = Vector2((x0 + label_w + step * (float(i) + 0.5)) * Art.W, -12.0)
		bubble.add_child(icon)

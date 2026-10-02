extends Node2D
## A cat that naps on the floor behind the action and reacts to Player 1.

const ANIMS := ["sleep", "wake", "watch", "startle", "lick", "yawn", "zoomies"]

var p1
var state := "sleep"
var idle_t := 0.0
var run_dir := 1.0
var run_t := 0.0
var home_x := 0.0
var spr: AnimatedSprite2D
var zzz: AnimatedSprite2D


func _ready() -> void:
	home_x = position.x
	z_index = -1
	var h := Art.frame_size("cat_sleep").y
	spr = AnimatedSprite2D.new()
	spr.sprite_frames = Art.frames_multi("cat_", ANIMS)
	spr.scale = Vector2(Art.W, Art.W)
	spr.position = Vector2(0, -h * 0.5)
	add_child(spr)
	spr.animation_finished.connect(_on_anim_done)
	zzz = Art.sprite("fx_sleepz")
	zzz.position = Vector2(-14, -h - 4)
	zzz.modulate = Color(0.85, 0.9, 1.0, 0.9)
	add_child(zzz)
	_to("sleep")


func _to(s: String) -> void:
	state = s
	idle_t = 0.0
	spr.play(s)
	zzz.visible = s == "sleep"


func _on_anim_done() -> void:
	match state:
		"wake", "startle":
			_to("watch")
		"lick", "yawn":
			_to("sleep")


func on_trip() -> void:
	if absf(p1.global_position.x - global_position.x) < 260.0 and state != "startle" and state != "zoomies":
		_to("startle")
		Juice.burst(get_parent(), global_position + Vector2(0, -16), Color(1.0, 0.75, 0.4), 6, 60.0, 120.0, 0.5, Vector2.UP, 180.0)


func on_cleared_gap() -> void:
	if absf(p1.global_position.x - global_position.x) < 320.0 and state != "zoomies" and state != "startle":
		_to("zoomies")
		run_t = 1.3
		run_dir = 1.0


func _process(delta: float) -> void:
	var dx: float = p1.global_position.x - global_position.x
	idle_t += delta
	match state:
		"sleep":
			if absf(dx) < 150.0:
				_to("wake")
			elif idle_t > 5.0 and randf() < 0.01:
				_to("lick" if randf() < 0.5 else "yawn")
		"watch":
			spr.flip_h = dx < 0.0
			if absf(dx) > 260.0 and idle_t > 1.5:
				_to("sleep")
		"zoomies":
			run_t -= delta
			position.x += run_dir * 150.0 * delta
			spr.flip_h = run_dir < 0.0
			if run_t < 0.65 and run_dir > 0.0:
				run_dir = -1.0
			if run_t <= 0.0:
				position.x = home_x
				_to("watch")

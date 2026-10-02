extends Node2D
## A loose floorboard bridging a pit. It looks like floor, so P1 runs onto it; once stepped on it creaks,
## tilts and drops, turning into a pit. Tape pins it for good; the stopwatch pauses the countdown.

const SHEET := "hazard_loose_board"
const CREAK := 0.4
const TILT := 0.2

var width := 96.0
var level
var body: StaticBody2D
var det: Area2D
var sprites: Array = []
var state := "idle"     # idle -> creak -> tilt -> fallen
var timer := 0.0
var taped := false


func _ready() -> void:
	add_to_group("board")
	level = get_tree().get_first_node_in_group("level")
	body = StaticBody2D.new()
	body.collision_layer = 1
	body.collision_mask = 0
	var cs := CollisionShape2D.new()
	var r := RectangleShape2D.new()
	r.size = Vector2(width, 8)
	cs.shape = r
	cs.position = Vector2(width * 0.5, 4.0)
	body.add_child(cs)
	add_child(body)
	# Detector: P1 standing on top of the board starts the countdown.
	det = Area2D.new()
	det.collision_layer = 0
	det.collision_mask = 2
	var dcs := CollisionShape2D.new()
	var dr := RectangleShape2D.new()
	dr.size = Vector2(width - 8.0, 6)
	dcs.shape = dr
	dcs.position = Vector2(width * 0.5, -3.0)
	det.add_child(dcs)
	add_child(det)
	var sz := Art.frame_size(SHEET)
	var n := int(ceil(width / sz.x))
	for i in n:
		var s := Art.sprite(SHEET, false)
		s.position = Vector2(sz.x * 0.5 + sz.x * float(i), sz.y * 0.5)
		s.frame = 0
		s.z_index = 1
		add_child(s)
		sprites.append(s)


## Pins the board down (tape powerup).
func tape() -> bool:
	if taped or state == "fallen":
		return false
	taped = true
	var tp := Art.sprite("placed_tape", false)
	tp.position = Vector2(width * 0.5, -2.0)
	tp.z_index = 6
	add_child(tp)
	Juice.float_text(get_parent(), global_position + Vector2(width * 0.5, -16.0), "TAPED!", Color(0.5, 0.75, 1.0))
	return true


func _physics_process(delta: float) -> void:
	if taped or state == "fallen":
		return
	var frozen: bool = level != null and level.freeze_t > 0.0
	if state == "idle":
		for b in det.get_overlapping_bodies():
			if b.has_method("enter_zone") and b.is_on_floor():
				state = "creak"
				timer = CREAK
				break
	elif not frozen:
		timer -= delta
		if state == "creak":
			var k := 1.0 - timer / CREAK
			for s in sprites:
				s.frame = 1 if int(k * 6.0) % 2 == 0 else 2
				s.position.x += sin(k * 90.0) * 0.05
			if timer <= 0.0:
				state = "tilt"
				timer = TILT
				for s in sprites:
					s.frame = 3
				Juice.shake(0.12)
		elif state == "tilt":
			if timer <= 0.0:
				_fall()


func _fall() -> void:
	state = "fallen"
	body.get_child(0).set_deferred("disabled", true)
	for s in sprites:
		s.frame = 4
	var tw := create_tween()
	tw.tween_interval(0.25)
	tw.tween_callback(func():
		for s in sprites:
			s.frame = 5)
	Juice.shake(0.2)
	Juice.burst(get_parent(), global_position + Vector2(width * 0.5, 4.0), Color(0.6, 0.45, 0.3), 12, 70.0, 220.0, 0.6, Vector2.UP, 180.0)
	if level != null:
		level.gaps.append({"x0": global_position.x, "x1": global_position.x + width, "bridged": false})

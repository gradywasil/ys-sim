extends Node
## Autoload: screen shake, hitstop, particle bursts, and small drawing helpers.

var camera: Camera2D
var trauma := 0.0
var _stopping := false


func shake(amount: float) -> void:
	trauma = minf(1.0, trauma + amount)


func hitstop(duration: float = 0.08) -> void:
	if _stopping:
		return
	_stopping = true
	Engine.time_scale = 0.05
	await get_tree().create_timer(duration, true, false, true).timeout
	Engine.time_scale = 1.0
	_stopping = false


func _process(delta: float) -> void:
	trauma = maxf(0.0, trauma - 1.6 * delta)
	if is_instance_valid(camera):
		var s := trauma * trauma * 10.0
		camera.offset = Vector2(randf_range(-1.0, 1.0), randf_range(-1.0, 1.0)) * s


func burst(parent: Node, pos: Vector2, color: Color, amount: int = 10, speed: float = 60.0, gravity: float = 200.0, life: float = 0.5, dir: Vector2 = Vector2.UP, spread: float = 60.0) -> void:
	var p := CPUParticles2D.new()
	p.position = pos
	p.one_shot = true
	p.explosiveness = 1.0
	p.amount = amount
	p.lifetime = life
	p.direction = dir
	p.spread = spread
	p.initial_velocity_min = speed * 0.5
	p.initial_velocity_max = speed
	p.gravity = Vector2(0.0, gravity)
	p.scale_amount_min = 0.75
	p.scale_amount_max = 1.5
	p.color = color
	var g := Gradient.new()
	g.set_color(0, Color.WHITE)
	g.set_color(1, Color(1, 1, 1, 0))
	p.color_ramp = g
	p.z_index = 20
	p.emitting = true
	parent.add_child(p)
	get_tree().create_timer(life + 0.3).timeout.connect(p.queue_free)


func float_text(parent: Node, pos: Vector2, text: String, color: Color) -> void:
	var l := Label.new()
	l.text = text
	l.custom_minimum_size = Vector2(240, 0)
	l.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	Art.style_label(l, 16, color, 4)
	# World-space labels are drawn at 1 art pixel per screen pixel, like the sprites.
	l.scale = Vector2(Art.W, Art.W)
	l.position = pos - Vector2(60, 0)
	l.z_index = 100
	parent.add_child(l)
	var tw := l.create_tween()
	tw.set_parallel(true)
	tw.tween_property(l, "position:y", pos.y - 24.0, 0.8)
	tw.tween_property(l, "modulate:a", 0.0, 0.5).set_delay(0.4)
	tw.chain().tween_callback(l.queue_free)


static func circle_pts(radius: float, n: int = 12) -> PackedVector2Array:
	var pts := PackedVector2Array()
	for i in n:
		var a := TAU * float(i) / float(n)
		pts.append(Vector2(cos(a), sin(a)) * radius)
	return pts


static func rect_pts(x: float, y: float, w: float, h: float) -> PackedVector2Array:
	return PackedVector2Array([Vector2(x, y), Vector2(x + w, y), Vector2(x + w, y + h), Vector2(x, y + h)])


static func poly(parent: Node, pts: PackedVector2Array, color: Color, pos: Vector2 = Vector2.ZERO) -> Polygon2D:
	var p := Polygon2D.new()
	p.polygon = pts
	p.color = color
	p.position = pos
	parent.add_child(p)
	return p

extends Node2D
## Dev-only: trips P1 on flat ground in slow motion so the trip animation and fx can be inspected.

func _ready() -> void:
	var body := StaticBody2D.new()
	body.collision_layer = 1
	var cs := CollisionShape2D.new()
	var r := RectangleShape2D.new()
	r.size = Vector2(2000, 100)
	cs.shape = r
	cs.position = Vector2(0, 250)
	body.add_child(cs)
	add_child(body)
	var floor_rect := ColorRect.new()
	floor_rect.color = Color(0.5, 0.33, 0.22)
	floor_rect.position = Vector2(-1000, 200)
	floor_rect.size = Vector2(2000, 100)
	add_child(floor_rect)
	var cam := Camera2D.new()
	cam.position = Vector2(0, 150)
	add_child(cam)
	Juice.camera = cam
	var p1 = preload("res://scripts/player1.gd").new()
	p1.position = Vector2(0, 190)
	add_child(p1)
	await get_tree().create_timer(0.6).timeout
	p1.trip("feather")
	await get_tree().create_timer(0.25, true, false, true).timeout
	Engine.time_scale = 0.12

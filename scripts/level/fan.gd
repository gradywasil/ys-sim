extends Area2D
## A placed fan. P1 near it is blown forward, and it cancels wind gusts around it.

var cool := 0.0
var spr: AnimatedSprite2D


func _ready() -> void:
	add_to_group("fan")
	collision_layer = 0
	collision_mask = 2
	var cs := CollisionShape2D.new()
	var shape := RectangleShape2D.new()
	shape.size = Vector2(110, 24)
	cs.shape = shape
	cs.position = Vector2(30.0, -12.0)
	add_child(cs)
	spr = Art.sprite("placed_fan")
	spr.position = Vector2(0, -Art.frame_size("placed_fan").y * 0.5 + 1.0)
	spr.z_index = 2
	add_child(spr)
	scale = Vector2(1.0, 0.1)
	create_tween().tween_property(self, "scale:y", 1.0, 0.15).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)


func _physics_process(_delta: float) -> void:
	for b in get_overlapping_bodies():
		if b.has_method("blow"):
			b.blow()

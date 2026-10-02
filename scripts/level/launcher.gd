extends Area2D
## A placed trampoline or ramp. When P1 reaches its middle it is launched upward (the ramp also adds speed),
## which carries P1 over a roller lane.

const SPECS := {
	"trampoline": {"sheet": "placed_trampoline", "vy": -460.0, "boost": 1.0},
	"ramp": {"sheet": "placed_ramp", "vy": -400.0, "boost": 1.25},
}

var kind := "trampoline"
var cool := 0.0
var spr: AnimatedSprite2D
var still: Sprite2D


func _ready() -> void:
	add_to_group("launcher")
	collision_layer = 0
	collision_mask = 2
	var cs := CollisionShape2D.new()
	var shape := RectangleShape2D.new()
	shape.size = Vector2(40, 14)
	cs.shape = shape
	cs.position = Vector2(0, -7)
	add_child(cs)
	var sheet: String = SPECS[kind].sheet
	var sz := Art.frame_size(sheet)
	if Art.frame_count(sheet) > 1:
		spr = Art.sprite(sheet, false)
		spr.position = Vector2(0, -sz.y * 0.5 + 1.0)
		spr.sprite_frames.set_animation_loop("default", false)
		add_child(spr)
	else:
		still = Sprite2D.new()
		still.texture = Art.tex(sheet)
		still.scale = Vector2(Art.W, Art.W)
		still.position = Vector2(0, -sz.y * 0.5 + 1.0)
		add_child(still)
	z_index = 1
	# Pop in.
	scale = Vector2(1.0, 0.1)
	create_tween().tween_property(self, "scale:y", 1.0, 0.15).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)


func _physics_process(delta: float) -> void:
	cool = maxf(0.0, cool - delta)
	if cool > 0.0:
		return
	for b in get_overlapping_bodies():
		if b.has_method("launch") and b.is_on_floor() and absf(b.global_position.x - global_position.x) < 8.0:
			cool = 0.6
			var spec: Dictionary = SPECS[kind]
			b.launch(spec.vy, spec.boost)
			if spr != null:
				spr.play("default")
			Juice.shake(0.1)
			Art.fx(get_parent(), global_position + Vector2(0, -4), "fx_jump_puff", Color.WHITE, 1.2)
			break

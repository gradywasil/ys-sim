extends Node2D
## Dev-only: shows the cycling hazards on a flat floor so their phases and the freeze tint can be inspected.

func _ready() -> void:
	var floor_rect := ColorRect.new()
	floor_rect.color = Color(0.5, 0.33, 0.22)
	floor_rect.position = Vector2(0, 200)
	floor_rect.size = Vector2(480, 80)
	add_child(floor_rect)
	var lvl := preload("res://scripts/level/level_builder.gd").new()
	add_child(lvl)
	lvl.add_to_group("level")
	for spec in [["burner", 70.0], ["sprinkler", 220.0]]:
		var hz := preload("res://scripts/level/hazard.gd").new()
		hz.kind = spec[0]
		hz.position = Vector2(spec[1], 200)
		add_child(hz)
	var cam := Camera2D.new()
	cam.position = Vector2(240, 135)
	cam.zoom = Vector2(Art.SCALE, Art.SCALE)
	add_child(cam)
	await get_tree().create_timer(6.0).timeout
	lvl.freeze(3.0)

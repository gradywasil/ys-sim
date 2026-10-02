extends Area2D
## A power-up in the world. Dropped items fall, land, and wait for Player 1; placeables (the bridge)
## resolve where they land instead; world items (coins) are simply placed on the floor.

const Powerups = preload("res://scripts/data/powerups.gd")
const GROUND_Y := 200.0

var kind := "coin"
var world_item := false
var landed := false
var fall_v := 0.0
var life := 14.0
var t := 0.0
var vis: Node2D


static func build_icon(k: String) -> Node2D:
	var root := Node2D.new()
	var glow := Sprite2D.new()
	glow.texture = Art.tex("item_glow")
	glow.modulate = Color(Powerups.color(k), 0.55)
	glow.scale = Vector2(Art.W, Art.W)
	root.add_child(glow)
	root.add_child(Art.sprite("item_" + k))
	return root


func _ready() -> void:
	add_to_group("pickups")
	collision_layer = 4
	collision_mask = 3
	landed = world_item
	if world_item:
		life = INF
	var cs := CollisionShape2D.new()
	var shape := CircleShape2D.new()
	shape.radius = 8.0
	cs.shape = shape
	add_child(cs)
	vis = build_icon(kind)
	add_child(vis)
	body_entered.connect(_on_body_entered)


func _physics_process(delta: float) -> void:
	life -= delta
	if life <= 0.0 or position.y > 340.0:
		queue_free()
		return
	t += delta
	if life < 3.0:
		vis.visible = fmod(life, 0.3) > 0.12
	if not landed:
		fall_v += 600.0 * delta
		position.y += fall_v * delta
		if Powerups.kind(kind) == "placeable" and position.y >= GROUND_Y - 10.0:
			_resolve_placeable()
	else:
		vis.position.y = sin(t * 5.0 + position.x) * 1.5


## Placeables don't wait on the floor: they snap over a nearby gap, or fizzle.
func _resolve_placeable() -> void:
	var level = get_tree().get_first_node_in_group("level")
	var ok: bool = level != null and level.place(kind, global_position.x)
	if not ok:
		Juice.float_text(get_parent(), global_position + Vector2(0, -10), "NO GAP!" if kind == "bridge" else "NO FLOOR!", Color(1.0, 0.6, 0.5))
		Juice.burst(get_parent(), global_position, Color(0.85, 0.7, 0.55), 6, 50.0, 120.0, 0.35, Vector2.UP, 160.0)
	queue_free()


func _on_body_entered(body: Node2D) -> void:
	if body.has_method("collect"):
		body.collect(kind)
		Art.fx(get_parent(), global_position, "item_%s_pop" % kind)
		Juice.burst(get_parent(), global_position, Powerups.color(kind), 6, 70.0, 150.0, 0.4, Vector2.UP, 180.0)
		queue_free()
	elif body is StaticBody2D and not body.is_in_group("block") and not landed and Powerups.kind(kind) != "placeable":
		landed = true
		var q := PhysicsRayQueryParameters2D.create(global_position + Vector2(0, -20), global_position + Vector2(0, 30), 1)
		var hit := get_world_2d().direct_space_state.intersect_ray(q)
		if not hit.is_empty():
			position.y = hit.position.y - 10.0
		Art.fx(get_parent(), global_position + Vector2(0, 2), "fx_dust", Color(0.95, 0.85, 0.75), 0.7)

extends Node2D
## Streams the level. Generates chunks ahead of the camera, builds floor, hazards and decor,
## and frees everything that falls far behind. Floor collision is one body per unbroken run.

signal stage_gate_added(stage_index: int)

const GROUND_Y := 200.0
const BLOCK_THEMES := ["books", "lego", "blocks", "box", "blocks", "books"]
const GenS = preload("res://scripts/level/level_gen.gd")
const Stages = preload("res://scripts/data/stages.gd")
const PickupS = preload("res://scripts/pickup.gd")
const HazardS = preload("res://scripts/level/hazard.gd")
const LauncherS = preload("res://scripts/level/launcher.gd")
const ZoneS = preload("res://scripts/level/zone.gd")
const BoardS = preload("res://scripts/level/board.gd")
const FanS = preload("res://scripts/level/fan.gd")
const Themes = preload("res://scripts/data/themes.gd")

var gen
var life
var world: Node2D
var rng := RandomNumberGenerator.new()
var tile := 16 * Art.SCALE
var floor_layer: TileMapLayer
var cursor := 0.0
var seg: Dictionary = {}
var gaps: Array = []        # {x0, x1, bridged}
var gates: Array = []       # {x, stage}  (stage = index of the stage that begins here)
var items: Array = []       # {node, x}   freed once far behind the camera
var tile_runs: Array = []   # {c0, c1, x}
var block_xs: Array = []
var stage_idx := 0
var stage_chunks_done := 0
var block_count := 0
var chunk_log: Array = []
var preview: Polygon2D
var freeze_t := 0.0
var forced_chunks: Array = []


func setup(world_node: Node2D, life_ref, seed_value: int) -> void:
	add_to_group("level")
	world = world_node
	life = life_ref
	rng.seed = seed_value
	gen = GenS.new(seed_value + 1)
	gen.forced = forced_chunks.duplicate()
	var ts := TileSet.new()
	ts.tile_size = Vector2i(tile, tile)
	# One atlas source per theme; the source id is the theme index.
	for th in Themes.THEMES.size():
		var src := TileSetAtlasSource.new()
		src.texture = Art.tex(Themes.file(th, "tileset_floor"))
		src.texture_region_size = Vector2i(tile, tile)
		for cx in 8:
			for cy in 3:
				src.create_tile(Vector2i(cx, cy))
		ts.add_source(src, th)
	floor_layer = TileMapLayer.new()
	floor_layer.tile_set = ts
	floor_layer.position = Vector2(0, GROUND_Y)
	floor_layer.scale = Vector2(Art.W, Art.W)
	world.add_child(floor_layer)
	preview = Juice.poly(world, Juice.rect_pts(-6, 0, 12, 8), Color(1, 1, 1, 0.35))
	preview.z_index = 30
	preview.visible = false
	_open_seg(0.0)
	_append("flat", 224)


## Freezes every cycling hazard for `sec` seconds (the stopwatch powerup).
func freeze(sec: float) -> void:
	freeze_t = sec


func _process(delta: float) -> void:
	freeze_t = maxf(0.0, freeze_t - delta)


## Builds ahead until the cursor is `ahead` units past the camera's right edge.
func ensure(cam_right: float, ahead: float = 800.0) -> void:
	while cursor < cam_right + ahead:
		_next_chunk()


func _next_chunk() -> void:
	var st := Stages.get_stage(stage_idx)
	if stage_chunks_done >= st.chunks:
		_add_gate()
		return
	var p := float(stage_chunks_done) / maxf(1.0, float(st.chunks - 1))
	var d := lerpf(st.d0, st.d1, p)
	var chunk: Dictionary = gen.next_chunk(d, stage_idx)
	chunk_log.append({"id": chunk.id, "x": cursor, "stage": stage_idx, "needs": chunk.needs})
	for prim in chunk.prims:
		_append(prim[0], prim[1])
	stage_chunks_done += 1


## Theme of the stage currently being generated.
func theme_now() -> int:
	return Themes.theme_of_stage(stage_idx)


func _add_gate() -> void:
	var th := theme_now()
	var gate_sheet := "goal_flag" if th == 0 else Themes.file(th, "goal")
	var flag := Art.sprite(gate_sheet)
	flag.position = Vector2(cursor + 16.0, GROUND_Y - Art.frame_size(gate_sheet).y * 0.5)
	world.add_child(flag)
	items.append({"node": flag, "x": cursor})
	gates.append({"x": cursor + 16.0, "stage": stage_idx + 1})
	_append("flat", 160)
	stage_idx += 1
	stage_chunks_done = 0
	stage_gate_added.emit(stage_idx)


# --- primitives -------------------------------------------------------------

func _append(kind: String, size: Variant) -> void:
	match kind:
		"flat":
			_extend(float(size))
			life.decorate(cursor, cursor + float(size), block_xs, theme_now())
			cursor += float(size)
		"board":
			# A loose board looks like floor but drops after P1 steps on it; the pit is registered as a gap once it falls.
			_close_seg()
			_pit(cursor, float(size))
			var bd := BoardS.new()
			bd.width = float(size)
			bd.position = Vector2(cursor, GROUND_Y)
			world.add_child(bd)
			items.append({"node": bd, "x": cursor + float(size)})
			cursor += float(size)
			_open_seg(cursor)
		"zone":
			var zn := ZoneS.new()
			zn.kind = size
			zn.position = Vector2(cursor, GROUND_Y)
			var zw: float = ZoneS.width_of(size)
			_extend(zw)
			world.add_child(zn)
			items.append({"node": zn, "x": cursor + zw})
			cursor += zw
		"hazard":
			var hz := HazardS.new()
			hz.kind = size
			hz.position = Vector2(cursor, GROUND_Y)
			var hw: float = HazardS.width_of(size)
			_extend(hw)
			world.add_child(hz)
			items.append({"node": hz, "x": cursor + hw})
			cursor += hw
		"block":
			_block(cursor, float(size))
			_extend(16.0)
			cursor += 16.0
		"gap":
			_close_seg()
			_pit(cursor, float(size))
			gaps.append({"x0": cursor, "x1": cursor + float(size), "bridged": false})
			cursor += float(size)
			_open_seg(cursor)
		"coins":
			for i in int(size):
				var c := PickupS.new()
				c.kind = "coin"
				c.world_item = true
				c.position = Vector2(cursor + 24.0 + 24.0 * float(i), GROUND_Y - 14.0 - 6.0 * sin(float(i) * 0.9))
				world.add_child(c)


func _open_seg(x0: float) -> void:
	var body := StaticBody2D.new()
	body.collision_layer = 1
	body.collision_mask = 0
	var cs := CollisionShape2D.new()
	var shape := RectangleShape2D.new()
	shape.size = Vector2(0.0, 200.0)
	cs.shape = shape
	body.add_child(cs)
	world.add_child(body)
	seg = {"x0": x0, "x1": x0, "body": body, "cs": cs, "shape": shape, "c0": int(x0 / 16.0)}


func _extend(w: float) -> void:
	var old_x1: float = seg.x1
	seg.x1 += w
	var width: float = seg.x1 - seg.x0
	seg.shape.size.x = width
	seg.cs.position = Vector2(seg.x0 + width * 0.5, GROUND_Y + 100.0)
	for i in int(w / 16.0):
		var col: int = int(old_x1 / 16.0) + i
		_set_column(col, 2 if col == seg.c0 else (rng.randi() % 2))
		seg.theme = theme_now()


func _close_seg() -> void:
	if seg.is_empty() or seg.x1 <= seg.x0:
		return
	var last: int = int(seg.x1 / 16.0) - 1
	_set_column(last, 3, seg.get("theme", theme_now()))
	tile_runs.append({"c0": seg.c0, "c1": last, "x": seg.x1})
	items.append({"node": seg.body, "x": seg.x1})
	seg = {}


func _set_column(col: int, ax: int, theme: int = -1) -> void:
	var th := theme_now() if theme < 0 else theme
	for row in 5:
		var tx := ax
		if ax < 2 and row < 2 and rng.randf() < 0.07:
			tx = 4 + rng.randi() % 4
		floor_layer.set_cell(Vector2i(col, row), th, Vector2i(tx, mini(row, 2)))


func _pit(x: float, w: float) -> void:
	var pit := TextureRect.new()
	pit.texture = Art.tex(Themes.file(theme_now(), "pit_bg"))
	pit.stretch_mode = TextureRect.STRETCH_TILE
	pit.position = Vector2(x, GROUND_Y)
	pit.size = Vector2(w, 64) * Art.SCALE
	pit.scale = Vector2(Art.W, Art.W)
	pit.z_index = -1
	world.add_child(pit)
	var deep := ColorRect.new()
	deep.color = Color(0.03, 0.02, 0.06)
	deep.position = Vector2(x, GROUND_Y + 64.0)
	deep.size = Vector2(w, 80)
	deep.z_index = -1
	world.add_child(deep)
	items.append({"node": pit, "x": x + w})
	items.append({"node": deep, "x": x + w})


func _block(x: float, h: float) -> void:
	var body := StaticBody2D.new()
	body.add_to_group("block")  # dropped items fall past blocks instead of landing on top
	body.collision_layer = 1
	body.collision_mask = 0
	var cs := CollisionShape2D.new()
	var r := RectangleShape2D.new()
	r.size = Vector2(16, h)
	cs.shape = r
	cs.position = Vector2(x + 8.0, GROUND_Y - h * 0.5)
	body.add_child(cs)
	world.add_child(body)
	items.append({"node": body, "x": x + 16.0})
	var th := theme_now()
	var skin: String = BLOCK_THEMES[block_count % BLOCK_THEMES.size()]
	block_count += 1
	block_xs.append(x + 8.0)
	var sheet_name := "toy_blocks"
	if th != 0:
		sheet_name = Themes.file(th, "obstacles")
	else:
		match skin:
			"books":
				sheet_name = "obstacle_books"
			"lego":
				sheet_name = "obstacle_lego"
			"box":
				sheet_name = "obstacle_box"
	var sheet := Art.tex(sheet_name)
	var cubes := int(h / 16.0)
	for i in cubes:
		var s := Sprite2D.new()
		s.texture = sheet
		s.region_enabled = true
		if th != 0:
			# Themed stacks: four body skins, and a recognizable cap on the top block.
			if i == cubes - 1:
				s.texture = Art.tex(Themes.file(th, "obstacles_tall"))
			s.region_rect = Rect2((rng.randi() % 4) * tile, 0, tile, tile)
		else:
			match skin:
				"blocks":
					s.region_rect = Rect2((rng.randi() % 4) * tile, (rng.randi() % 3) * tile, tile, tile)
				"box":
					s.region_rect = Rect2(0, 0, tile, tile)
				_:
					s.region_rect = Rect2((rng.randi() % 4) * tile, 0, tile, tile)
		s.scale = Vector2(Art.W, Art.W)
		s.centered = false
		s.position = Vector2(x, GROUND_Y - 16.0 * float(i + 1))
		world.add_child(s)
		items.append({"node": s, "x": x + 16.0})


# --- placeables ---------------------------------------------------------------

## The nearest un-bridged gap within `reach` units of x, or an empty dictionary.
func nearest_gap(x: float, reach: float = 80.0) -> Dictionary:
	var best := {}
	var best_d := reach
	for g in gaps:
		if g.bridged:
			continue
		var d := absf((g.x0 + g.x1) * 0.5 - x)
		if d < best_d:
			best_d = d
			best = g
	return best


## Shows where a placeable would land: the snapped gap for a bridge, the snapped spot for a launcher.
func show_preview(kind: String, x: float, on: bool) -> void:
	preview.visible = false
	if not on:
		return
	if kind == "bridge":
		var g := nearest_gap(x)
		if g.is_empty():
			return
		var w: float = g.x1 - g.x0 + 24.0
		preview.polygon = Juice.rect_pts(-w * 0.5, 0, w, 8)
		preview.position = Vector2((g.x0 + g.x1) * 0.5, GROUND_Y)
		preview.color = Color(1, 1, 1, 0.35)
		preview.visible = true
	elif kind == "tape":
		var tgt = _tape_target(x)
		if tgt == null:
			return
		var tw: float = tgt.width
		preview.polygon = Juice.rect_pts(0, -6, tw, 8)
		preview.position = Vector2(tgt.global_position.x, GROUND_Y)
		preview.color = Color(0.5, 0.75, 1.0, 0.5)
		preview.visible = true
	elif kind == "fan":
		var near_wind := false
		for z in get_tree().get_nodes_in_group("zone"):
			if z.kind == "wind" and x > z.global_position.x - 70.0 and x < z.global_position.x + z.width + 70.0:
				near_wind = true
		preview.polygon = Juice.rect_pts(-16, 0, 32, 6)
		preview.position = Vector2(x, GROUND_Y)
		preview.color = Color(0.5, 1.0, 0.6, 0.55) if near_wind else Color(1, 1, 1, 0.3)
		preview.visible = true
	elif kind == "trampoline" or kind == "ramp":
		var snap := _launcher_spot(x)
		preview.polygon = Juice.rect_pts(-24, 0, 48, 6)
		preview.position = Vector2(snap.x, GROUND_Y)
		# Green when it will snap to a roller lane, plain white otherwise.
		preview.color = Color(0.5, 1.0, 0.6, 0.55) if snap.lane else Color(1, 1, 1, 0.3)
		preview.visible = true


## Where a launcher dropped at x ends up: snapped just before a nearby roller lane, otherwise where it fell.
func _launcher_spot(x: float) -> Dictionary:
	var best = null
	var best_d := 70.0
	for hz in get_tree().get_nodes_in_group("hazard"):
		if not hz.lane:
			continue
		var d: float = hz.global_position.x - x
		if d > -26.0 and d < best_d:
			best_d = d
			best = hz
	if best != null:
		return {"x": best.global_position.x - 8.0, "lane": true}
	return {"x": x, "lane": false}


## Places a bridge or a launcher. Returns false (a wasted drop) if it can't land anywhere useful.
func place(kind: String, x: float) -> bool:
	match kind:
		"bridge":
			return place_bridge(x)
		"tape":
			return place_tape(x)
		"fan":
			return place_fan(x)
	return place_launcher(kind, x)


## The nearest thing tape can pin (a cycling hazard or a loose board) within reach of x.
func _tape_target(x: float):
	var best = null
	var best_d := 90.0
	for g in ["hazard", "board"]:
		for h in get_tree().get_nodes_in_group(g):
			if (g == "hazard" and (h.lane or h.taped)) or (g == "board" and (h.taped or h.state == "fallen")):
				continue
			var d := absf(h.global_position.x + h.width * 0.5 - x)
			if d < best_d:
				best_d = d
				best = h
	return best


func place_tape(x: float) -> bool:
	var tgt = _tape_target(x)
	return tgt != null and tgt.tape()


func place_fan(x: float) -> bool:
	var q := PhysicsRayQueryParameters2D.create(Vector2(x, 120.0), Vector2(x, 260.0), 1)
	var hit := get_world_2d().direct_space_state.intersect_ray(q)
	if hit.is_empty() or absf(hit.position.y - GROUND_Y) > 3.0:
		return false
	var f := FanS.new()
	f.position = Vector2(x, GROUND_Y)
	world.add_child(f)
	items.append({"node": f, "x": x + 80.0})
	Juice.burst(world, Vector2(x, GROUND_Y), Color(0.85, 0.9, 1.0), 8, 60.0, 80.0, 0.4, Vector2.UP, 160.0)
	return true


func place_launcher(kind: String, x: float) -> bool:
	var spot := _launcher_spot(x)
	var cx: float = spot.x
	var q := PhysicsRayQueryParameters2D.create(Vector2(cx, 120.0), Vector2(cx, 260.0), 1)
	var hit := get_world_2d().direct_space_state.intersect_ray(q)
	# Needs flat floor right there (not over a pit, not on top of a block).
	if hit.is_empty() or absf(hit.position.y - GROUND_Y) > 3.0:
		return false
	var lu := LauncherS.new()
	lu.kind = kind
	lu.position = Vector2(cx, GROUND_Y)
	world.add_child(lu)
	items.append({"node": lu, "x": cx + 30.0})
	Juice.burst(world, Vector2(cx, GROUND_Y), Color(0.9, 0.85, 0.7), 8, 60.0, 130.0, 0.4, Vector2.UP, 160.0)
	return true


## Lays a cardboard bridge over the nearest gap. Returns false (a wasted drop) if none is near.
func place_bridge(x: float) -> bool:
	var g := nearest_gap(x)
	if g.is_empty():
		return false
	g.bridged = true
	var w: float = g.x1 - g.x0 + 24.0
	var cx: float = (g.x0 + g.x1) * 0.5
	var body := StaticBody2D.new()
	body.collision_layer = 1
	body.collision_mask = 0
	var cs := CollisionShape2D.new()
	var r := RectangleShape2D.new()
	r.size = Vector2(w, 8)
	cs.shape = r
	cs.position = Vector2(cx, GROUND_Y + 4.0)
	body.add_child(cs)
	world.add_child(body)
	var plank := Sprite2D.new()
	plank.texture = Art.tex("bridge_plank")
	plank.centered = false
	var nat_w := Art.frame_size("bridge_plank").x
	plank.scale = Vector2(Art.W * w / nat_w, Art.W)
	plank.position = Vector2(cx - w * 0.5, GROUND_Y)
	plank.z_index = 1
	world.add_child(plank)
	Art.fx(world, Vector2(cx, GROUND_Y - 6.0), "bridge_land", Color.WHITE, w / Art.frame_size("bridge_land").x)
	Juice.shake(0.12)
	items.append({"node": body, "x": g.x1})
	items.append({"node": plank, "x": g.x1})
	return true


# --- cleanup ------------------------------------------------------------------

func cull(cam_left: float) -> void:
	var limit := cam_left - 600.0
	var keep: Array = []
	for it in items:
		if it.x < limit:
			if is_instance_valid(it.node):
				it.node.queue_free()
		else:
			keep.append(it)
	items = keep
	var runs: Array = []
	for r in tile_runs:
		if r.x < limit:
			for c in range(r.c0, r.c1 + 1):
				for row in 5:
					floor_layer.erase_cell(Vector2i(c, row))
		else:
			runs.append(r)
	tile_runs = runs
	gaps = gaps.filter(func(g): return g.x1 > limit)
	block_xs = block_xs.filter(func(b): return b > limit)
	for p in get_tree().get_nodes_in_group("pickups"):
		if p.global_position.x < limit:
			p.queue_free()
	life.cull(limit)

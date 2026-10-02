extends Node
## Autoload: builds textures, SpriteFrames, and one-shot effect sprites from the art manifest data.

const DIR := "res://art/v2/"
## Art pixels per game-world unit. The world stays in 480x270 units; the camera zooms by SCALE
## and every world-space sprite is scaled by W so one art pixel lands on one screen pixel.
const SCALE := 2
const W := 1.0 / float(SCALE)
const _Data = preload("res://scripts/art_data.gd")

var _frames := {}
var font: FontFile


func _ready() -> void:
	font = load("res://assets/fonts/Silkscreen-Regular.ttf")
	font.antialiasing = TextServer.FONT_ANTIALIASING_NONE
	font.hinting = TextServer.HINTING_NONE
	font.subpixel_positioning = TextServer.SUBPIXEL_POSITIONING_DISABLED


## Styles a label with the pixel font. `px` is in screen pixels (use multiples of 8 for Silkscreen).
## World-space labels should also get `scale = Vector2(W, W)` so they match sprite pixels.
func style_label(l: Label, px: int, color: Color, outline: int = 2) -> void:
	l.add_theme_font_override("font", font)
	l.add_theme_font_size_override("font_size", px)
	l.add_theme_color_override("font_color", color)
	if outline > 0:
		l.add_theme_color_override("font_outline_color", Color(0.06, 0.03, 0.12))
		l.add_theme_constant_override("outline_size", outline)


## Frame size of a sheet in world units.
func frame_size(n: String) -> Vector2:
	var d: Dictionary = _Data.DATA[n + ".png"]
	return Vector2(d.frame_w, d.frame_h) * W


## True when a sheet is listed in the manifest data (lets the game prefer real art over placeholders).
func has(n: String) -> bool:
	return _Data.DATA.has(n + ".png")


## Sheet names (without ".png") that start with `prefix` and don't contain any of `skip`.
func list(prefix: String, skip: Array = []) -> Array:
	var out: Array = []
	for k in _Data.DATA:
		var n: String = k.trim_suffix(".png")
		if not n.begins_with(prefix):
			continue
		var bad := false
		for sk in skip:
			if n.contains(sk):
				bad = true
		if not bad:
			out.append(n)
	out.sort()
	return out


## SpriteFrames with several named animations cut from one sheet: {"name": [first, end_exclusive, loop]}.
func frames_ranges(sheet: String, ranges: Dictionary) -> SpriteFrames:
	var sf := SpriteFrames.new()
	sf.remove_animation("default")
	var d: Dictionary = _Data.DATA[sheet + ".png"]
	var t := tex(sheet)
	for anim in ranges:
		var r: Array = ranges[anim]
		sf.add_animation(anim)
		sf.set_animation_speed(anim, maxf(1.0, float(d.fps)))
		sf.set_animation_loop(anim, r[2])
		for i in range(r[0], r[1]):
			var at := AtlasTexture.new()
			at.atlas = t
			at.region = Rect2(i * d.frame_w, 0, d.frame_w, d.frame_h)
			sf.add_frame(anim, at)
	return sf


func frame_count(n: String) -> int:
	return int(_Data.DATA[n + ".png"].frames)


func tex(n: String) -> Texture2D:
	return load(DIR + n + ".png")


func frames(n: String) -> SpriteFrames:
	if _frames.has(n):
		return _frames[n]
	var sf := SpriteFrames.new()
	_add_anim(sf, "default", n)
	_frames[n] = sf
	return sf


## One SpriteFrames holding several sheets, each named by its sheet name minus the prefix.
func frames_multi(prefix: String, names: Array) -> SpriteFrames:
	var sf := SpriteFrames.new()
	sf.remove_animation("default")
	for n in names:
		sf.add_animation(n)
		_add_anim(sf, n, prefix + n)
	return sf


func _add_anim(sf: SpriteFrames, anim: String, sheet: String) -> void:
	var d: Dictionary = _Data.DATA[sheet + ".png"]
	var t := tex(sheet)
	sf.set_animation_speed(anim, maxf(1.0, float(d.fps)))
	sf.set_animation_loop(anim, d.loop)
	for i in int(d.frames):
		var at := AtlasTexture.new()
		at.atlas = t
		at.region = Rect2(i * d.frame_w, 0, d.frame_w, d.frame_h)
		sf.add_frame(anim, at)


func sprite(n: String, autoplay: bool = true) -> AnimatedSprite2D:
	var s := AnimatedSprite2D.new()
	s.sprite_frames = frames(n)
	s.scale = Vector2(W, W)
	if autoplay:
		s.play("default")
	return s


## Plays a sheet once at a world position, then frees itself.
func fx(parent: Node, pos: Vector2, n: String, tint: Color = Color.WHITE, size: float = 1.0, flip: bool = false) -> AnimatedSprite2D:
	var s := AnimatedSprite2D.new()
	var sf := SpriteFrames.new()
	_add_anim(sf, "default", n)
	sf.set_animation_loop("default", false)
	s.sprite_frames = sf
	s.position = pos
	s.modulate = tint
	s.scale = Vector2(size * W, size * W)
	s.flip_h = flip
	s.z_index = 40
	parent.add_child(s)
	s.play("default")
	s.animation_finished.connect(s.queue_free)
	return s


func atlas(n: String, region: Rect2) -> AtlasTexture:
	var at := AtlasTexture.new()
	at.atlas = tex(n)
	at.region = region
	return at

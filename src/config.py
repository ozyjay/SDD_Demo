import pygame as pg
import sys
import os

# Detect if running in pygbag (WebAssembly browser environment)
RUNNING_IN_PYGBAG = sys.platform == "emscripten"

# Display (pygbag compatible - fixed resolution)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BG_COLOR = (255, 255, 255)

# Physics
G = 1800.0
V_FLAP = -520.0
V_MAX_UP = -800.0
V_MAX_DOWN = 900.0
SCROLL_SPEED = 320.0  # px/s

# Randomisation
GAP_SIZE_RANGE = (140, 220)     # min/max gap size px
SPAWN_INTERVAL_RANGE = (1000, 1800)  # ms between obstacles

# Emoji rendering
EMOJI_SIZE = 64
PLAYER_EMOJI = "🐤"
OBSTACLE_EMOJI = "🟩"
BG_EMOJIS = ["☁️", "⭐", "🌤️"]

# UI/HUD
SCORE_FONT_SIZE = 48
GAME_OVER_FONT_SIZE = 64
INSTRUCTION_FONT_SIZE = 32
TEXT_COLOR = (0, 0, 0)
GAME_OVER_COLOR = (255, 0, 0)
SCORE_POSITION = (20, 20)

# Sound (REQ-007)
SOUND_ENABLED_DEFAULT = True
# TODO: Add sound file paths when implementing audio
# SOUND_FLAP = "assets/sounds/flap.wav"
# SOUND_SCORE = "assets/sounds/score.wav"
# SOUND_CRASH = "assets/sounds/crash.wav"

# Window setup
def get_screen():
	"""Create pygame screen with fixed resolution for web compatibility."""
	return pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


def get_emoji_font(size):
	"""
	Load a system font that supports emoji rendering.
	REQ-010: Emoji display support.
	
	Tries multiple emoji-capable fonts in order of preference.
	Falls back to default font if none found (may show boxes).
	For pygbag/WebAssembly, uses default font since system fonts aren't available.
	
	Args:
		size: Font size in pixels
		
	Returns:
		pygame.font.Font object
	"""
	# Ensure font module is initialized
	if not pg.font.get_init():
		pg.font.init()
	
	# In pygbag/WebAssembly environment, system fonts aren't available
	# Use default font (will render emoji as boxes, but that's expected in browser)
	if RUNNING_IN_PYGBAG:
		print("[INFO] Running in pygbag/browser - using default font")
		return pg.font.Font(None, size)
	
	# List of fonts known to support emoji, in order of preference
	EMOJI_FONTS = [
		'Noto Color Emoji',      # Linux (Google Noto)
		'Apple Color Emoji',      # macOS
		'Segoe UI Emoji',         # Windows 10+
		'Segoe UI Symbol',        # Windows fallback
		'DejaVu Sans',           # Common Linux fallback
		'FreeSans',              # Another Linux option
	]
	
	for font_name in EMOJI_FONTS:
		try:
			font = pg.font.SysFont(font_name, size)
			# Test if it can actually render an emoji
			test_surface = font.render('🐤', True, (255, 255, 255))
			if test_surface and test_surface.get_width() > 0:
				print(f"[INFO] Using emoji font: {font_name}")
				return font
		except Exception:
			continue
	
	# Fallback to default font (will likely show boxes)
	print("[WARNING] No emoji-compatible font found. Emoji may display as boxes.")
	print("[WARNING] Install 'fonts-noto-color-emoji' package for proper emoji display.")
	return pg.font.Font(None, size)


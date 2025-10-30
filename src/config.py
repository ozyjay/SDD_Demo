import pygame as pg

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

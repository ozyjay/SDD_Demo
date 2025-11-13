"""
Emoji Flappy - Game Loop and State Logic
REQ-001: Web-based display (pygbag compatible)
REQ-002: Flap and gravity physics
REQ-003: Randomised obstacle generation
REQ-004: Collision detection
REQ-005: Score tracking
REQ-006: Restart after game over
REQ-007: Mute toggle
REQ-008: Quit shortcut
REQ-009: Async compatibility
"""

import asyncio
import pygame as pg
import random
import sys
from config import (
	SCREEN_WIDTH, SCREEN_HEIGHT, BG_COLOR, G, V_FLAP, V_MAX_UP, V_MAX_DOWN,
	SCROLL_SPEED, GAP_SIZE_RANGE, SPAWN_INTERVAL_RANGE,
	EMOJI_SIZE, PLAYER_EMOJI, OBSTACLE_EMOJI,
	SCORE_FONT_SIZE, GAME_OVER_FONT_SIZE, INSTRUCTION_FONT_SIZE,
	TEXT_COLOR, GAME_OVER_COLOR, SCORE_POSITION,
	SOUND_ENABLED_DEFAULT, get_screen, get_emoji_font
)


class Player:
	"""
	Player entity with flap physics.
	REQ-002: Flap and gravity physics
	"""
	
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.velocity = 0.0
		self.size = EMOJI_SIZE
		
		# Render emoji with emoji-compatible font (REQ-010)
		self.font = get_emoji_font(self.size)
		self.surface = self.font.render(PLAYER_EMOJI, True, (0, 0, 0))
		
		# Check if emoji rendered properly (width > size/2 indicates real emoji, not box)
		# If it's just a box character, create a colored circle instead
		if self.surface.get_width() < self.size // 2:
			# Emoji didn't render - use a yellow circle instead
			self.surface = pg.Surface((self.size, self.size), pg.SRCALPHA)
			pg.draw.circle(self.surface, (255, 220, 0), (self.size // 2, self.size // 2), self.size // 2)
			# Add a simple eye
			pg.draw.circle(self.surface, (0, 0, 0), (self.size // 2 + 5, self.size // 2 - 5), 3)
		
		self.rect = self.surface.get_rect(center=(self.x, self.y))
	
	def flap(self):
		"""Apply upward impulse (REQ-002)."""
		self.velocity = V_FLAP
	
	def update(self, dt):
		"""
		Update player position with gravity (REQ-002).
		dt: delta time in seconds
		"""
		# Apply gravity
		self.velocity += G * dt
		
		# Clamp velocity
		self.velocity = max(V_MAX_UP, min(V_MAX_DOWN, self.velocity))
		
		# Update position
		self.y += self.velocity * dt
		self.rect.center = (self.x, self.y)
	
	def draw(self, screen):
		"""Render player emoji."""
		screen.blit(self.surface, self.rect)
	
	def getRect(self):
		"""Get collision rect."""
		return self.rect


class Obstacle:
	"""
	Obstacle pair (top and bottom).
	REQ-003: Randomised obstacle generation
	"""
	
	def __init__(self, x, screen_height):
		self.x = x
		self.screen_height = screen_height
		
		# Random gap size and position (REQ-003)
		gap_size = random.randint(GAP_SIZE_RANGE[0], GAP_SIZE_RANGE[1])
		gap_center = random.randint(
			gap_size // 2 + 50,
			screen_height - gap_size // 2 - 50
		)
		
		self.gap_top = gap_center - gap_size // 2
		self.gap_bottom = gap_center + gap_size // 2
		
		# Render obstacles with emoji-compatible font (REQ-010)
		self.font = get_emoji_font(EMOJI_SIZE)
		self.emoji_surface = self.font.render(OBSTACLE_EMOJI, True, (0, 0, 0))
		
		# Check if emoji rendered properly
		if self.emoji_surface.get_width() < EMOJI_SIZE // 2:
			# Emoji didn't render - use a green rectangle instead
			self.emoji_surface = pg.Surface((EMOJI_SIZE, EMOJI_SIZE))
			self.emoji_surface.fill((34, 139, 34))  # Forest green
			# Add darker border
			pg.draw.rect(self.emoji_surface, (0, 100, 0), (0, 0, EMOJI_SIZE, EMOJI_SIZE), 2)
		
		self.emoji_width = self.emoji_surface.get_width()
		
		# Track if player passed this obstacle
		self.passed = False
	
	def update(self, dt):
		"""Move obstacle left."""
		self.x -= SCROLL_SPEED * dt
	
	def draw(self, screen):
		"""Render obstacle emojis."""
		# Top obstacle (repeated emojis)
		for y in range(0, int(self.gap_top), EMOJI_SIZE):
			screen.blit(self.emoji_surface, (self.x, y))
		
		# Bottom obstacle (repeated emojis)
		for y in range(int(self.gap_bottom), self.screen_height, EMOJI_SIZE):
			screen.blit(self.emoji_surface, (self.x, y))
	
	def isOffScreen(self):
		"""Check if obstacle has moved off screen."""
		return self.x + self.emoji_width < 0
	
	def checkCollision(self, player_rect):
		"""
		Check collision with player (REQ-004).
		Returns True if collision detected.
		"""
		# Create rects for top and bottom obstacles
		top_rect = pg.Rect(self.x, 0, self.emoji_width, self.gap_top)
		bottom_rect = pg.Rect(self.x, self.gap_bottom, self.emoji_width, 
							  self.screen_height - self.gap_bottom)
		
		return player_rect.colliderect(top_rect) or player_rect.colliderect(bottom_rect)
	
	def checkPassed(self, player_x):
		"""Check if player has passed this obstacle."""
		if not self.passed and player_x > self.x + self.emoji_width:
			self.passed = True
			return True
		return False


class Game:
	"""
	Main game class handling game loop and state.
	REQ-001: Web-based display (pygbag compatible)
	REQ-002: Flap and gravity physics
	REQ-003: Randomised obstacle generation
	REQ-004: Collision detection
	REQ-009: Async compatibility
	"""
	
	def __init__(self):
		# REQ-001: Web-based display with fixed resolution
		self.screen = get_screen()
		self.screen_width = SCREEN_WIDTH
		self.screen_height = SCREEN_HEIGHT
		pg.display.set_caption("Emoji Flappy")
		
		self.clock = pg.time.Clock()
		self.running = True
		self.game_over = False
		
		# Initialize player
		self.player = Player(self.screen_width // 4, self.screen_height // 2)
		
		# Initialize obstacles list
		self.obstacles = []
		
		# Spawn timer (REQ-003: randomised intervals)
		self.next_spawn_time = pg.time.get_ticks() + random.randint(
			SPAWN_INTERVAL_RANGE[0], SPAWN_INTERVAL_RANGE[1]
		)
		
		# REQ-005: Score tracking
		self.score = 0
		self.high_score = 0
		
		# REQ-007: Mute toggle
		self.sound_enabled = SOUND_ENABLED_DEFAULT
		# TODO: Load sound files when implementing audio
		# self.sound_flap = pg.mixer.Sound(SOUND_FLAP)
		# self.sound_score = pg.mixer.Sound(SOUND_SCORE)
		# self.sound_crash = pg.mixer.Sound(SOUND_CRASH)
		
		# Font for UI (REQ-010: use emoji-compatible font)
		self.score_font = get_emoji_font(SCORE_FONT_SIZE)
		self.game_over_font = get_emoji_font(GAME_OVER_FONT_SIZE)
		self.instruction_font = get_emoji_font(INSTRUCTION_FONT_SIZE)
	
	def handleEvents(self):
		"""
		Process input events.
		REQ-002: Flap input
		REQ-006: Restart after game over
		REQ-007: Mute toggle
		REQ-008: Quit shortcut
		"""
		for event in pg.event.get():
			if event.type == pg.QUIT:
				self.running = False
			
			elif event.type == pg.KEYDOWN:
				# REQ-008: Quit shortcuts
				if event.key in (pg.K_ESCAPE, pg.K_q):
					self.running = False
				
				# REQ-002: Flap with space
				elif event.key == pg.K_SPACE:
					if not self.game_over:
						self.player.flap()
						# TODO: REQ-007 - Play flap sound
						# if self.sound_enabled:
						#     self.sound_flap.play()
					# REQ-006: Restart after game over
					else:
						self.restart()
				
				# REQ-007: Mute toggle
				elif event.key == pg.K_m:
					self.toggleMute()
	
	def spawnObstacle(self):
		"""
		Spawn new obstacle at randomised interval (REQ-003).
		"""
		current_time = pg.time.get_ticks()
		
		if current_time >= self.next_spawn_time:
			# Spawn at right edge of screen
			obstacle = Obstacle(self.screen_width, self.screen_height)
			self.obstacles.append(obstacle)
			
			# Set next random spawn time (REQ-003)
			self.next_spawn_time = current_time + random.randint(
				SPAWN_INTERVAL_RANGE[0], SPAWN_INTERVAL_RANGE[1]
			)
	
	def update(self, dt):
		"""
		Update game state.
		REQ-002: Physics update
		REQ-003: Obstacle spawning and movement
		REQ-004: Collision detection
		REQ-005: Score increment
		"""
		if self.game_over:
			return
		
		# Update player (REQ-002)
		self.player.update(dt)
		
		# Check screen boundary collision (REQ-004)
		if self.player.y - self.player.size // 2 <= 0:
			self.game_over = True
			self.onGameOver()
		if self.player.y + self.player.size // 2 >= self.screen_height:
			self.game_over = True
			self.onGameOver()
		
		# Spawn obstacles (REQ-003)
		self.spawnObstacle()
		
		# Update obstacles
		for obstacle in self.obstacles:
			obstacle.update(dt)
			
			# REQ-004: Check collision
			if obstacle.checkCollision(self.player.getRect()):
				self.game_over = True
				self.onGameOver()
			
			# REQ-005: Score increment when passing obstacle
			if obstacle.checkPassed(self.player.x):
				self.score += 1
				# TODO: REQ-007 - Play score sound
				# if self.sound_enabled:
				#     self.sound_score.play()
		
		# Remove off-screen obstacles
		self.obstacles = [obs for obs in self.obstacles if not obs.isOffScreen()]
	
	def draw(self):
		"""
		Render all game elements.
		REQ-005: Score display
		REQ-006: Game over screen with restart prompt
		"""
		# Clear screen
		self.screen.fill(BG_COLOR)
		
		# Draw obstacles
		for obstacle in self.obstacles:
			obstacle.draw(self.screen)
		
		# Draw player
		self.player.draw(self.screen)
		
		# REQ-005: Draw score
		score_text = self.score_font.render(f"Score: {self.score}", True, TEXT_COLOR)
		self.screen.blit(score_text, SCORE_POSITION)
		
		# REQ-006: Draw game over screen
		if self.game_over:
			# Semi-transparent overlay
			overlay = pg.Surface((self.screen_width, self.screen_height))
			overlay.set_alpha(128)
			overlay.fill((0, 0, 0))
			self.screen.blit(overlay, (0, 0))
			
			# Game over text
			game_over_text = self.game_over_font.render("GAME OVER", True, GAME_OVER_COLOR)
			text_rect = game_over_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 60))
			self.screen.blit(game_over_text, text_rect)
			
			# Final score
			final_score_text = self.score_font.render(f"Score: {self.score}", True, TEXT_COLOR)
			score_rect = final_score_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
			self.screen.blit(final_score_text, score_rect)
			
			# High score
			high_score_text = self.instruction_font.render(f"High Score: {self.high_score}", True, TEXT_COLOR)
			high_rect = high_score_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 40))
			self.screen.blit(high_score_text, high_rect)
			
			# Restart instruction
			restart_text = self.instruction_font.render("Press Space to Restart", True, TEXT_COLOR)
			restart_rect = restart_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 80))
			self.screen.blit(restart_text, restart_rect)
			
			# Mute status (REQ-007)
			mute_status = "Sound: ON" if self.sound_enabled else "Sound: OFF"
			mute_text = self.instruction_font.render(f"{mute_status} (M to toggle)", True, TEXT_COLOR)
			mute_rect = mute_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 120))
			self.screen.blit(mute_text, mute_rect)
		
		pg.display.flip()
	
	def restart(self):
		"""
		Restart game after game over (REQ-006).
		Resets all game state without closing the app.
		"""
		# Update high score (REQ-005)
		if self.score > self.high_score:
			self.high_score = self.score
		
		# Reset game state
		self.game_over = False
		self.score = 0
		
		# Reset player position
		self.player = Player(self.screen_width // 4, self.screen_height // 2)
		
		# Clear obstacles
		self.obstacles = []
		
		# Reset spawn timer
		self.next_spawn_time = pg.time.get_ticks() + random.randint(
			SPAWN_INTERVAL_RANGE[0], SPAWN_INTERVAL_RANGE[1]
		)
	
	def toggleMute(self):
		"""
		Toggle sound on/off (REQ-007).
		"""
		self.sound_enabled = not self.sound_enabled
		# TODO: When sound files are added, set volume accordingly
		# if self.sound_enabled:
		#     self.sound_flap.set_volume(1.0)
		#     self.sound_score.set_volume(1.0)
		#     self.sound_crash.set_volume(1.0)
		# else:
		#     self.sound_flap.set_volume(0.0)
		#     self.sound_score.set_volume(0.0)
		#     self.sound_crash.set_volume(0.0)
	
	def onGameOver(self):
		"""
		Handle game over event.
		REQ-004: Collision triggers game over
		"""
		# TODO: REQ-007 - Play crash sound
		# if self.sound_enabled:
		#     self.sound_crash.play()
		pass
	
	async def run(self):
		"""
		Main game loop (async for pygbag compatibility).
		REQ-001: Web-based game execution
		REQ-009: Async/await for pygbag
		NFR-001: 60 FPS target
		"""
		while self.running:
			# Delta time in seconds
			dt = self.clock.tick(60) / 1000.0
			
			self.handleEvents()
			self.update(dt)
			self.draw()
			
			# REQ-009: Required for pygbag to yield control to browser
			await asyncio.sleep(0)

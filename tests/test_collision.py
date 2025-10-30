"""
Tests for collision detection.
REQ-004: Confirm collisions trigger game-over state.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import pytest
import pygame as pg
from game import Player, Obstacle, Game


# Initialize pygame for testing
pg.init()


class TestCollision:
	"""Test collision detection implementation."""
	
	def testPlayerObstacleCollision_overlap_collisionDetected(self):
		"""REQ-004: Collision with obstacle should be detected."""
		screen_height = 800
		obstacle = Obstacle(100, screen_height)
		
		# Create player at position that collides with top obstacle
		player = Player(100, 50)
		
		collision = obstacle.checkCollision(player.getRect())
		
		# Should detect collision with top obstacle
		assert collision is True
	
	def testPlayerObstacleCollision_noOverlap_noCollision(self):
		"""REQ-004: No collision when player is in gap."""
		screen_height = 800
		obstacle = Obstacle(100, screen_height)
		
		# Create player at position in the gap
		gap_center = (obstacle.gap_top + obstacle.gap_bottom) / 2
		player = Player(100, gap_center)
		
		collision = obstacle.checkCollision(player.getRect())
		
		# Should not detect collision in gap
		assert collision is False
	
	def testGameOverOnCollision_playerHitsObstacle_gameOverTriggered(self):
		"""REQ-004: Game over state should be triggered on collision."""
		# Create a minimal game instance
		game = Game()
		
		# Create obstacle at player position to force collision
		obstacle = Obstacle(game.player.x, game.screen_height)
		# Force gap to be away from player
		obstacle.gap_top = 0
		obstacle.gap_bottom = game.player.y - 100
		game.obstacles.append(obstacle)
		
		assert game.game_over is False
		
		# Update game - should detect collision
		game.update(0.016)
		
		assert game.game_over is True
	
	def testGameOverOnBoundary_playerBelowScreen_gameOverTriggered(self):
		"""REQ-004: Game over when player hits screen boundary."""
		game = Game()
		
		# Move player below screen
		game.player.y = game.screen_height + 100
		
		assert game.game_over is False
		
		game.update(0.016)
		
		assert game.game_over is True
	
	def testGameOverOnBoundary_playerAboveScreen_gameOverTriggered(self):
		"""REQ-004: Game over when player hits top boundary."""
		game = Game()
		
		# Move player above screen
		game.player.y = -10
		
		assert game.game_over is False
		
		game.update(0.016)
		
		assert game.game_over is True

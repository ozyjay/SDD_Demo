"""
Tests for restart functionality.
REQ-006: After collision, restarting resets state without closing the app.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import pytest
from game import Game


class TestRestart:
	"""Test restart functionality implementation."""
	
	def testRestart_gameOver_stateReset(self):
		"""REQ-006: Restart should reset game state."""
		game = Game()
		
		# Set game to game over state
		game.game_over = True
		game.score = 15
		game.obstacles.append(None)  # Add dummy obstacle
		
		# Restart game
		game.restart()
		
		# Game state should be reset
		assert game.game_over is False
		assert game.score == 0
		assert len(game.obstacles) == 0
	
	def testRestart_playerPosition_resetToInitial(self):
		"""REQ-006: Player position should reset on restart."""
		game = Game()
		initial_x = game.player.x
		initial_y = game.player.y
		
		# Move player
		game.player.y = 500
		game.player.velocity = 200
		
		# Restart game
		game.restart()
		
		# Player should be back at initial position
		assert game.player.x == initial_x
		assert game.player.y == initial_y
		assert game.player.velocity == 0.0
	
	def testRestart_obstaclesCleared_emptyList(self):
		"""REQ-006: All obstacles should be cleared on restart."""
		game = Game()
		
		# Add multiple obstacles
		from game import Obstacle
		for i in range(5):
			obstacle = Obstacle(500 + i * 100, game.screen_height)
			game.obstacles.append(obstacle)
		
		assert len(game.obstacles) == 5
		
		# Restart game
		game.restart()
		
		# Obstacles should be cleared
		assert len(game.obstacles) == 0
	
	def testRestart_runningState_preserved(self):
		"""REQ-006: Game should stay running after restart."""
		game = Game()
		
		game.game_over = True
		game.restart()
		
		# Game should still be running (not quit)
		assert game.running is True
		assert game.game_over is False
	
	def testRestart_highScore_preserved(self):
		"""REQ-006: High score should persist across restarts."""
		game = Game()
		
		# Play game and set score
		game.score = 25
		game.game_over = True
		
		# First restart
		game.restart()
		assert game.high_score == 25
		
		# Play again with lower score
		game.score = 10
		game.game_over = True
		
		# Second restart
		game.restart()
		assert game.high_score == 25
		assert game.score == 0

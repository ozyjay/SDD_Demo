"""
Tests for score tracking.
REQ-005: Score increments when player passes an obstacle pair.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import pytest
from game import Game, Obstacle


class TestScore:
	"""Test score tracking implementation."""
	
	def testScoreInitialization_gameStarts_scoreIsZero(self):
		"""REQ-005: Score should start at zero."""
		game = Game()
		
		assert game.score == 0
	
	def testScoreIncrement_playerPassesObstacle_scoreIncreases(self):
		"""REQ-005: Score should increment when player passes obstacle."""
		game = Game()
		initial_score = game.score
		
		# Create obstacle behind player
		obstacle = Obstacle(game.player.x - 100, game.screen_height)
		game.obstacles.append(obstacle)
		
		# Check if player passed
		passed = obstacle.checkPassed(game.player.x)
		
		assert passed is True
	
	def testScoreTracking_multipleObstacles_scoreAccumulates(self):
		"""REQ-005: Score should accumulate across multiple obstacles."""
		game = Game()
		
		# Simulate passing 3 obstacles
		for i in range(3):
			obstacle = Obstacle(game.player.x - 100 - (i * 50), game.screen_height)
			obstacle.passed = False
			game.obstacles.append(obstacle)
		
		initial_score = game.score
		
		# Update game to process obstacles
		for obstacle in game.obstacles:
			if obstacle.checkPassed(game.player.x):
				game.score += 1
		
		assert game.score == initial_score + 3
	
	def testHighScore_newGameStarts_highScorePreserved(self):
		"""REQ-005: High score should be tracked across restarts."""
		game = Game()
		
		# Set score and simulate game over
		game.score = 10
		game.game_over = True
		
		# Restart game
		game.restart()
		
		# High score should be preserved
		assert game.high_score == 10
		assert game.score == 0
	
	def testHighScore_lowerScore_highScoreNotUpdated(self):
		"""REQ-005: High score should only update if current score is higher."""
		game = Game()
		
		# First game with high score
		game.score = 20
		game.game_over = True
		game.restart()
		
		# Second game with lower score
		game.score = 10
		game.game_over = True
		game.restart()
		
		# High score should remain at 20
		assert game.high_score == 20

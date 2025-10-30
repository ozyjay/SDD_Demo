"""
Tests for physics implementation.
REQ-002: Verify velocity updates correctly with gravity/flap over dt.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import pytest
from game import Player
from config import G, V_FLAP, V_MAX_UP, V_MAX_DOWN


class TestPhysics:
	"""Test physics behavior for flap and gravity."""
	
	def testGravityAppliedOverTime_velocityIncreases_correctAcceleration(self):
		"""REQ-002: Gravity should accelerate player downward."""
		player = Player(100, 100)
		initial_velocity = player.velocity
		dt = 0.016  # ~60 FPS
		
		player.update(dt)
		
		# Velocity should increase by G * dt
		expected_velocity = initial_velocity + G * dt
		assert abs(player.velocity - expected_velocity) < 0.1
	
	def testFlapApplied_velocityChanges_upwardImpulse(self):
		"""REQ-002: Flap should apply upward velocity."""
		player = Player(100, 100)
		
		player.flap()
		
		assert player.velocity == V_FLAP
		assert player.velocity < 0  # Negative is upward
	
	def testVelocityClamping_exceedsMax_clampedToLimit(self):
		"""REQ-002: Velocity should be clamped to max values."""
		player = Player(100, 100)
		
		# Simulate falling for a long time
		for _ in range(100):
			player.update(1.0)
		
		assert player.velocity <= V_MAX_DOWN
		assert player.velocity >= V_MAX_UP
	
	def testPositionUpdate_velocityApplied_correctMovement(self):
		"""REQ-002: Position should update based on velocity."""
		player = Player(100, 100)
		player.velocity = 100.0  # Set known velocity
		dt = 0.1
		initial_y = player.y
		
		player.update(dt)
		
		# Position should change by velocity * dt (plus gravity effect)
		# Check that position has changed
		assert player.y != initial_y

"""
Tests for randomised obstacle spawning.
REQ-003: Ensure spawns vary across runs; no repeating sequences.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import pytest
from game import Obstacle
from config import GAP_SIZE_RANGE


class TestRandomSpawns:
	"""Test randomised obstacle generation."""
	
	def testObstacleGeneration_multipleCreations_differentGapSizes(self):
		"""REQ-003: Gap sizes should vary randomly."""
		screen_height = 800
		gap_sizes = []
		
		# Create multiple obstacles
		for _ in range(20):
			obstacle = Obstacle(500, screen_height)
			gap_size = obstacle.gap_bottom - obstacle.gap_top
			gap_sizes.append(gap_size)
		
		# Should have variation in gap sizes
		unique_gaps = set(gap_sizes)
		assert len(unique_gaps) > 1, "Gap sizes should vary"
		
		# All gaps should be within range
		for gap in gap_sizes:
			assert GAP_SIZE_RANGE[0] <= gap <= GAP_SIZE_RANGE[1]
	
	def testObstacleGeneration_multipleCreations_differentPositions(self):
		"""REQ-003: Gap positions should vary randomly."""
		screen_height = 800
		gap_positions = []
		
		# Create multiple obstacles
		for _ in range(20):
			obstacle = Obstacle(500, screen_height)
			gap_center = (obstacle.gap_top + obstacle.gap_bottom) / 2
			gap_positions.append(gap_center)
		
		# Should have variation in gap positions
		unique_positions = set(gap_positions)
		assert len(unique_positions) > 1, "Gap positions should vary"
	
	def testNonDeterministicSpawns_twoRuns_differentSequences(self):
		"""REQ-003: No fixed seed - sequences should differ between runs."""
		screen_height = 800
		
		# First run
		sequence1 = []
		for _ in range(10):
			obs = Obstacle(500, screen_height)
			sequence1.append((obs.gap_top, obs.gap_bottom))
		
		# Second run
		sequence2 = []
		for _ in range(10):
			obs = Obstacle(500, screen_height)
			sequence2.append((obs.gap_top, obs.gap_bottom))
		
		# Sequences should differ (extremely unlikely to be identical)
		assert sequence1 != sequence2, "Obstacle sequences should not be deterministic"

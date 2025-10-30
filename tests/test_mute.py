"""
Tests for mute toggle functionality.
REQ-007: Press "M" to toggle sounds (flap, score, crash).
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import pytest
from game import Game
from config import SOUND_ENABLED_DEFAULT


class TestMute:
	"""Test mute toggle implementation."""
	
	def testMuteInitialization_gameStarts_defaultSoundState(self):
		"""REQ-007: Sound should be enabled by default."""
		game = Game()
		
		assert game.sound_enabled == SOUND_ENABLED_DEFAULT
	
	def testToggleMute_soundOn_turnsOff(self):
		"""REQ-007: Toggle should turn sound off when it's on."""
		game = Game()
		game.sound_enabled = True
		
		game.toggleMute()
		
		assert game.sound_enabled is False
	
	def testToggleMute_soundOff_turnsOn(self):
		"""REQ-007: Toggle should turn sound on when it's off."""
		game = Game()
		game.sound_enabled = False
		
		game.toggleMute()
		
		assert game.sound_enabled is True
	
	def testToggleMute_multipleTimes_alternates(self):
		"""REQ-007: Multiple toggles should alternate sound state."""
		game = Game()
		initial_state = game.sound_enabled
		
		game.toggleMute()
		assert game.sound_enabled == (not initial_state)
		
		game.toggleMute()
		assert game.sound_enabled == initial_state
		
		game.toggleMute()
		assert game.sound_enabled == (not initial_state)
	
	def testMuteState_persistsAcrossRestart_maintained(self):
		"""REQ-007: Mute state should persist across game restarts."""
		game = Game()
		
		# Turn sound off
		game.sound_enabled = True
		game.toggleMute()
		assert game.sound_enabled is False
		
		# Restart game
		game.restart()
		
		# Sound should still be off (not reset to default)
		# Note: This behavior depends on design decision
		# For now, we'll test that toggleMute works independently
		game.toggleMute()
		assert game.sound_enabled is True

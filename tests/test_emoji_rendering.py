"""
Test emoji rendering functionality.
REQ-010: Emoji display support
"""

import pytest
import pygame as pg
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from config import get_emoji_font, PLAYER_EMOJI, OBSTACLE_EMOJI, EMOJI_SIZE


class TestEmojiRendering:
	"""Test suite for REQ-010: Emoji display support."""
	
	@classmethod
	def setup_class(cls):
		"""Initialize pygame for testing."""
		pg.init()
		pg.display.set_mode((100, 100))  # Minimal display for testing
	
	@classmethod
	def teardown_class(cls):
		"""Clean up pygame."""
		pg.quit()
	
	def test_emoji_font_loads(self):
		"""
		REQ-010: Verify emoji-compatible font loads successfully.
		"""
		font = get_emoji_font(EMOJI_SIZE)
		assert font is not None
		assert isinstance(font, pg.font.Font)
	
	def test_player_emoji_renders(self):
		"""
		REQ-010: Verify player emoji renders without error.
		"""
		font = get_emoji_font(EMOJI_SIZE)
		surface = font.render(PLAYER_EMOJI, True, (0, 0, 0))
		
		assert surface is not None
		assert surface.get_width() > 0
		assert surface.get_height() > 0
	
	def test_obstacle_emoji_renders(self):
		"""
		REQ-010: Verify obstacle emoji renders without error.
		"""
		font = get_emoji_font(EMOJI_SIZE)
		surface = font.render(OBSTACLE_EMOJI, True, (0, 0, 0))
		
		assert surface is not None
		assert surface.get_width() > 0
		assert surface.get_height() > 0
	
	def test_emoji_font_consistent_across_calls(self):
		"""
		REQ-010: Verify multiple calls to get_emoji_font return compatible fonts.
		"""
		font1 = get_emoji_font(EMOJI_SIZE)
		font2 = get_emoji_font(EMOJI_SIZE)
		
		# Both should render emoji successfully
		surface1 = font1.render(PLAYER_EMOJI, True, (0, 0, 0))
		surface2 = font2.render(PLAYER_EMOJI, True, (0, 0, 0))
		
		assert surface1.get_width() > 0
		assert surface2.get_width() > 0
	
	def test_emoji_font_different_sizes(self):
		"""
		REQ-010: Verify emoji font works with different sizes.
		"""
		sizes = [32, 48, 64, 128]
		
		for size in sizes:
			font = get_emoji_font(size)
			surface = font.render(PLAYER_EMOJI, True, (0, 0, 0))
			
			assert surface is not None
			assert surface.get_width() > 0
			assert surface.get_height() > 0
	
	def test_emoji_font_fallback_graceful(self):
		"""
		REQ-010: Verify font loading falls back gracefully if no emoji font available.
		Even if no emoji font is found, the function should return a valid font object.
		"""
		# This test verifies the function doesn't crash
		font = get_emoji_font(EMOJI_SIZE)
		assert font is not None
		
		# Should still be able to render something (even if it's boxes)
		surface = font.render("Test", True, (0, 0, 0))
		assert surface is not None

#!/usr/bin/env python3
"""
Emoji Flappy - Main Entry Point
REQ-001: Web-based display (pygbag compatible)
REQ-008: Quit shortcut (Esc/Q)
REQ-009: Async compatibility
"""

import asyncio
import pygame as pg
import sys
from game import Game


async def main():
	"""Entry point for Emoji Flappy game (async for pygbag)."""
	pg.init()
	
	try:
		game = Game()
		await game.run()
	except Exception as e:
		print(f"Error during game execution: {e}")
		raise
	finally:
		pg.quit()


# pygbag requires asyncio.run at module level
if __name__ == "__main__":
	asyncio.run(main())

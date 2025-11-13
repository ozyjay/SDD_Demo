# Emoji Flappy — Acceptance Criteria

## Overview
This document defines the acceptance criteria for each functional requirement in `requirements.md`.

---

## REQ-001: Web-based display
**Given** the game is launched via pygbag in a web browser  
**When** the player navigates to the forwarded port  
**Then** the game should display at 800x600 resolution and respond to input  
**And** closing the browser tab should cleanly terminate the game

---

## REQ-002: Flap and gravity physics
**Given** the game is running  
**When** the player presses Space  
**Then** the player emoji should move upward with velocity V_FLAP  
**And** gravity should continuously pull the player downward at rate G  
**And** velocity should be clamped between V_MAX_UP and V_MAX_DOWN

---

## REQ-003: Randomised obstacle generation
**Given** the game is running  
**When** obstacles spawn  
**Then** each obstacle should have a random gap size within GAP_SIZE_RANGE  
**And** obstacles should spawn at random intervals within SPAWN_INTERVAL_RANGE  
**And** gap position should be randomized vertically  
**And** no two playthroughs should have identical obstacle patterns

---

## REQ-004: Collision detection
**Given** the player is navigating obstacles  
**When** the player emoji overlaps with an obstacle or screen boundary  
**Then** the game should immediately enter game-over state  
**And** all physics updates should stop

---

## REQ-005: Score tracking
**Given** the player is playing  
**When** the player passes through an obstacle pair  
**Then** the score should increment by 1  
**And** the score should be displayed on screen  
**And** when the game ends, if the score exceeds the high score, the high score should be updated

---

## REQ-006: Restart after game over
**Given** the game is in game-over state  
**When** the player presses Space  
**Then** the game should reset all state (score, obstacles, player position)  
**And** gameplay should resume from the initial state  
**And** the high score should persist across restarts

---

## REQ-007: Mute toggle
**Given** the game is running (with sound effects implemented)  
**When** the player presses M  
**Then** sound effects should toggle between on and off  
**And** the current sound state should be displayed on the game-over screen

---

## REQ-008: Quit shortcut
**Given** the game is running  
**When** the player presses Esc or Q  
**Then** the game should quit cleanly  
**And** all resources should be released properly

---

## REQ-009: Async compatibility
**Given** the game code uses pygame  
**When** the game is built with pygbag for WebAssembly  
**Then** the main game loop should use `async def` and `await asyncio.sleep(0)`  
**And** the game should run without blocking the browser

---

## REQ-010: Emoji display support
**Given** the game needs to render emoji characters  
**When** the game initializes fonts  
**Then** the system should attempt to load emoji-compatible fonts (Noto Color Emoji, Apple Color Emoji, Segoe UI Emoji)  
**And** if an emoji font is found, emoji should render properly (not as boxes)  
**And** if no emoji font is available or running in pygbag/WebAssembly, the system should use graphical fallbacks (yellow circle with eye for player, green rectangles for obstacles)  
**And** the console should log which font is being used

---

## Version History
| Version | Date | Changes |
|---------|------|---------|
| 0.1 | 2025-11-13 | Initial acceptance criteria for REQ-001 through REQ-010 |

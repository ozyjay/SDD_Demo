# Emoji Flappy - PyGame + pygbag Implementation

A web-based PyGame clone of Flappy Bird using emojis with randomised obstacle generation. Runs in browser via pygbag/WebAssembly.

## Implementation Status

### ✅ Completed (REQ-001 to REQ-009)

- **REQ-001**: Web-based display
  - Game runs in browser at 800x600 resolution
  - Served via pygbag with port forwarding
  - Clean browser tab closure
  
- **REQ-002**: Flap and gravity physics
  - Space bar applies upward velocity
  - Continuous gravity acceleration
  - Velocity clamping based on `config.py` constants
  
- **REQ-003**: Randomised obstacle generation
  - Variable spawn intervals (no fixed seed)
  - Random gap sizes and positions
  - Non-deterministic gameplay
  
- **REQ-004**: Collision detection
  - Player-obstacle collision
  - Screen boundary detection
  - Immediate game over on collision

- **REQ-005**: Score tracking
  - Score increments when passing obstacles
  - High score preserved across restarts
  - Score displayed on HUD

- **REQ-006**: Restart after game over
  - Press Space to restart after game over
  - Resets all game state without closing app
  - High score persists across restarts

- **REQ-007**: Mute toggle
  - Press M to toggle sound on/off
  - Sound state indicator on game over screen
  - Ready for sound file integration

- **REQ-008**: Quit shortcut
  - Press Esc or Q to quit at any time

- **REQ-009**: Async compatibility
  - Main game loop uses `async def` and `await asyncio.sleep(0)`
  - Full pygbag/WebAssembly support

### 🚧 TODO (Future Enhancements)

- **Sound Effects**: Add actual sound files (flap, score, crash)
  - Placeholder code ready in `game.py`
  - Sound file paths commented in `config.py`

## Project Structure

```
SDD_Demo/
├── specifications/
│   ├── requirements.md          # Functional requirements
│   └── acceptance_criteria.md   # Acceptance criteria (empty)
├── src/
│   ├── main.py                  # Entry point (REQ-001, REQ-008)
│   ├── game.py                  # Game loop and state (REQ-001 to REQ-004)
│   └── config.py                # Constants and configuration
├── tests/
│   ├── test_physics.py          # Tests for REQ-002
│   ├── test_random_spawns.py    # Tests for REQ-003
│   └── test_collision.py        # Tests for REQ-004
└── README.md
```

## Running the Game

### Prerequisites
- Python 3.12+
- PyGame
- pygbag (for web deployment)

### Installation
```bash
# Install dependencies (already done in virtual environment)
pip install pygame pygbag
```

### Launch Game in Browser (Recommended for Codespaces)
```bash
# From project root - serve on port 3496 (or any available port)
pygbag src/main.py --port 3496

# The game will be available at:
# http://localhost:3496
# Or via Codespaces port forwarding URL
```

### Launch Game Locally (Desktop)
```bash
# From project root
python src/main.py

# Or using the virtual environment
/workspaces/SDD_Demo/.venv/bin/python src/main.py
```

### Controls
- **Space**: Flap (apply upward velocity) / Restart after game over
- **Esc / Q**: Quit game
- **M**: Toggle mute (sound on/off)

## Running Tests

All tests for REQ-002 through REQ-007 are passing:

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_physics.py -v
pytest tests/test_random_spawns.py -v
pytest tests/test_collision.py -v
pytest tests/test_score.py -v
pytest tests/test_restart.py -v
pytest tests/test_mute.py -v
```

### Test Results
```
27 passed in 0.14s
```

## Configuration

All gameplay constants are defined in `src/config.py`:

- **Display**: `SCREEN_WIDTH`, `SCREEN_HEIGHT` (fixed for web compatibility)
- **Physics**: `G`, `V_FLAP`, `V_MAX_UP`, `V_MAX_DOWN`
- **Scrolling**: `SCROLL_SPEED`
- **Randomisation**: `GAP_SIZE_RANGE`, `SPAWN_INTERVAL_RANGE`
- **Rendering**: `EMOJI_SIZE`, `PLAYER_EMOJI`, `OBSTACLE_EMOJI`

## Requirements Mapping

| Requirement | File | Line/Class | Test File |
|-------------|------|------------|-----------|
| REQ-001 | `src/main.py`, `src/game.py`, `src/config.py` | `get_screen()`, `Game.__init__()` | Manual verification |
| REQ-002 | `src/game.py` | `Player` class | `test_physics.py` |
| REQ-003 | `src/game.py` | `Obstacle.__init__()`, `Game.spawnObstacle()` | `test_random_spawns.py` |
| REQ-004 | `src/game.py` | `Obstacle.checkCollision()`, `Game.update()` | `test_collision.py` |
| REQ-005 | `src/game.py` | `Game.score`, `Game.high_score`, `Game.draw()` | `test_score.py` |
| REQ-006 | `src/game.py` | `Game.restart()` | `test_restart.py` |
| REQ-007 | `src/game.py` | `Game.toggleMute()` | `test_mute.py` |
| REQ-008 | `src/game.py` | `Game.handleEvents()` | Manual verification |
| REQ-009 | `src/main.py`, `src/game.py` | `async def main()`, `async def run()` | Manual verification |

## Next Steps

To complete optional enhancements:

1. **Sound Effects**: Add actual audio files
   - Create `assets/sounds/` directory
   - Add flap.wav, score.wav, crash.wav
   - Uncomment sound code in `game.py`
2. **NFR-001**: Verify 60 FPS performance in browser
3. **NFR-002**: Measure and optimize input latency if needed
4. **NFR-003**: Test in multiple browsers (Chrome, Firefox, Safari)

## pygbag Deployment Notes

- Game runs in WebAssembly via pygbag
- Async/await pattern required for browser event loop
- Fixed resolution (800x600) for consistent web experience
- All assets embedded in WASM bundle
- Access via forwarded port in Codespaces or local browser

## License

Specification-Driven Development Demo Project

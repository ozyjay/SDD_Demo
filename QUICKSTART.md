# Quick Start Guide - Emoji Flappy (pygbag)

## ✅ Project is Ready!

The game has been updated for **pygbag** compatibility and can run in your browser.

## 🎮 Running the Game

### Option 1: Using the Run Script (Easiest)
```bash
./run_web.sh
```

### Option 2: Manual Command
```bash
# From project root
python -m pygbag --port 3496 src
```

### Option 3: Using Virtual Environment
```bash
/workspaces/SDD_Demo/.venv/bin/python -m pygbag --port 3496 src
```

## 🌐 Accessing the Game

1. **Server is currently running on port 3496**
2. In VS Code, look for the **PORTS** tab (next to Terminal)
3. Find port **3496** and click the **globe icon** or **Open in Browser** link
4. The game will load in your browser!

Alternatively, if you're in Codespaces:
- Click on the notification that says "Your application running on port 3496 is available"
- Or access via the forwarded URL shown in the PORTS panel

## 🎯 Controls

- **Space**: Flap (jump) / Restart after game over
- **Esc / Q**: Quit game
- **M**: Toggle mute (sound on/off)

## 📊 Current Status

✅ **Implemented:**
- REQ-001: Web-based display (pygbag compatible)
- REQ-002: Flap and gravity physics
- REQ-003: Randomised obstacle generation
- REQ-004: Collision detection
- REQ-005: Score tracking with high score
- REQ-006: Restart functionality
- REQ-007: Mute toggle
- REQ-008: Quit shortcuts
- REQ-009: Async/await compatibility

🚧 **Optional Enhancements:**
- Sound effects (code ready, need audio files)

## 🧪 Running Tests

```bash
pytest tests/ -v
```

All 27 tests passing! ✅

## 🛠 Troubleshooting

### Port 3496 not forwarding?
- Check the PORTS tab in VS Code
- Manually add port 3496 if not auto-detected
- Set visibility to "Public" if in Codespaces

### Game not loading?
- Wait for the build to complete (first run takes longer)
- Check browser console for errors
- Try refreshing the page

### Black/ffmpeg warnings?
- These are optional optimizations - the game works fine without them
- They don't affect gameplay

## 📁 Project Structure

```
src/
├── main.py       # Entry point (async)
├── game.py       # Game loop and logic
└── config.py     # All constants

tests/
├── test_physics.py
├── test_random_spawns.py
└── test_collision.py

specifications/
└── requirements.md
```

Enjoy playing! 🐤

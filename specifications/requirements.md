# Emoji Flappy (Fullscreen, Random) — Requirements

## 1. Overview
**Project:** Emoji Flappy (PyGame + pygbag)  
**Version:** 0.2
**Date:** 2025-10-30

**Summary:**  
A web-based PyGame clone of Flappy Bird using emojis, compatible with pygbag for browser deployment. The player controls 🐤 using keyboard or touch to flap upwards and avoid randomly generated emoji obstacles. Gameplay is entirely randomised — no fixed seed or deterministic sequence. Runs in GitHub Codespaces via web browser.

---

## 2. Functional Requirements
| ID | Requirement | Priority | Acceptance Criteria |
|----|-------------|-----------|---------------------|
| REQ-001 | Web-based display. | High | Game runs in browser at fixed resolution (800x600). Can be served via pygbag and accessed through forwarded port. Closing browser tab quits cleanly. |
| REQ-002 | Flap and gravity physics. | High | Space/tap applies upward velocity; gravity acts continuously; limits set by constants in `config.py`. |
| REQ-003 | Randomised obstacle generation. | High | Obstacles spawn at variable intervals, random gap size/position, with no deterministic seed. |
| REQ-004 | Collision detection. | High | Overlap between player emoji and any obstacle or screen boundary ends the run immediately. |
| REQ-005 | Score tracking. | Medium | Score increments when player passes an obstacle pair. |
| REQ-006 | Restart after game over. | Medium | After collision, a “Press Space to Restart” prompt appears; restarting resets state without closing the app. |
| REQ-007 | Mute toggle. | Low | Press "M" to toggle sounds (flap, score, crash). |
| REQ-008 | Quit shortcut. | High | Press Esc or Q to quit at any time (browser-compatible). |
| REQ-009 | Async compatibility. | High | Game loop uses async/await for pygbag compatibility. |
| REQ-010 | Emoji display support. | High | Game uses emoji-compatible system fonts (Noto Color Emoji, Apple Color Emoji, Segoe UI Emoji, etc.) to properly render emoji characters for player and obstacles. In pygbag/WebAssembly environment where system fonts aren't available, uses graphical fallbacks (colored shapes: yellow circle for player, green rectangles for obstacles). |

---

## 3. Non-Functional Requirements
| ID | Requirement | Category | Measurement |
|----|-------------|-----------|--------------|
| NFR-001 | Frame rate stability. | Performance | 60 FPS target on native display. |
| NFR-002 | Input latency. | Performance | Flap visible within ≤75 ms. |
| NFR-003 | Browser compatibility. | Reliability | Runs in modern browsers via pygbag/WebAssembly. |
| NFR-004 | Randomisation quality. | Gameplay | Each playthrough has unique obstacle timing and gaps. |
| NFR-005 | Graceful quit. | UX | Game releases all resources and closes without errors. |

---

## 4. Physics Constants (see `src/config.py`)
- `G`: gravity acceleration  
- `V_FLAP`: upward impulse  
- `V_MAX_UP`, `V_MAX_DOWN`: clamp limits  
- `SCROLL_SPEED`: obstacle speed  
- `GAP_SIZE_RANGE`: min–max tuple for random gap size  
- `SPAWN_INTERVAL_RANGE`: min–max tuple for random spawn timing  

---

## 5. Test Mapping
| Req | Test File | Description |
|------|------------|-------------|
| REQ-002 | `tests/test_physics.py` | Verify velocity updates correctly with gravity/flap over dt. |
| REQ-003 | `tests/test_random_spawns.py` | Ensure spawns vary across runs; no repeating sequences. |
| REQ-004 | `tests/test_collision.py` | Confirm collisions trigger game-over state. |
| REQ-005 | `tests/test_score.py` | Verify score increments when passing obstacles, high score tracking. |
| REQ-006 | `tests/test_restart.py` | Confirm restart resets state without closing app. |
| REQ-007 | `tests/test_mute.py` | Verify mute toggle functionality. |
| REQ-010 | `tests/test_emoji_rendering.py` | Verify emoji-compatible fonts load and render emoji characters properly. |

---

## 6. Revision History
| Ver | Date | Notes |
|------|------|-------|
| 0.1 | 2025-10-30 | Initial version (desktop fullscreen) |
| 0.2 | 2025-10-30 | Updated for pygbag/web browser compatibility |
| 0.3 | 2025-10-30 | Implemented REQ-005 to REQ-009 (score, restart, mute, quit, async) |
| 0.4 | 2025-11-13 | Added REQ-010 for emoji font rendering support |
| 0.5 | 2025-11-13 | Merged duplicate config files (removed config-pygbag.py) |

# ADR-001: Use Pygame as Game Engine for Desktop MVP

**Date:** 2025-11-15
**Status:** ✅ Accepted
**Deciders:** Development Team

## Context

Need game engine for educational WiFi security dashboard with:
- Character animations
- Real-time data visualization
- 60 FPS smooth experience
- Cross-platform (Linux/Win/macOS/Pi)
- Python integration (existing backend)

## Decision

Use **Pygame 2.5+** as primary game engine for desktop application.

## Rationale

1. **Python-native:** Zero impedance mismatch with existing plugins
2. **Mature:** 23+ years development, battle-tested
3. **Performance:** SDL2 backend, hardware acceleration
4. **Cross-platform:** Works on Raspberry Pi 3+
5. **Ecosystem:** Large community, extensive documentation
6. **Learning curve:** Gentle, well-documented

## Alternatives Considered

- **Godot + Python:** More powerful, but adds GDScript complexity
- **Unity + Python bridge:** Overkill, requires C# wrapper
- **Arcade library:** Similar but less mature than Pygame
- **Web Canvas first:** Requires FastAPI bridge, more complex

## Consequences

### Positive
- Rapid development (familiar Python)
- 70% code reuse from existing plugins
- Hardware acceleration via SDL2
- Easy sprite/audio management

### Negative
- 2D only (acceptable for our use case)
- Not native mobile (Phase 4: Web PWA handles this)
- Requires separate packaging per platform

### Neutral
- Performance adequate for our needs (tested on Pi 3)
- Asset pipeline standard (PNG sprites, OGG audio)

## Implementation Notes

```python
# Minimum viable Pygame loop
import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

while running:
    dt = clock.tick(60) / 1000.0  # 60 FPS
    # Update game logic
    # Render graphics
    pygame.display.flip()
```

## References

- [Pygame Documentation](https://www.pygame.org/docs/)
- [Real Python: Pygame Tutorial](https://realpython.com/pygame-a-primer/)
- ADR-002: Gamification Engine Layer

#!/usr/bin/env python3
"""
WiFi Security Education - Game Entry Point

This is the main entry point for the packaged application.

Author: Juan-Dev + AI Architect - Soli Deo Gloria ✝️
Date: 2025-11-15
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def main():
    """Main entry point for the game."""
    try:
        from presentation.pygame.game import WiFiSecurityGame

        print("🎮 WiFi Security Education - Starting...")
        print("📚 Educational WiFi Security Game")
        print("✝️ Soli Deo Gloria")
        print()

        game = WiFiSecurityGame()
        game.run()

    except ImportError as e:
        print(f"❌ Error importing game modules: {e}")
        print("Make sure all dependencies are installed:")
        print("  pip install pygame pyric scapy python-dotenv")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error starting game: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

"""
Base character class with state machine and behavior system.
All game characters (Guardian, Professor, Family, Threats) inherit from this.

Author: Juan-Dev + AI Architect - Soli Deo Gloria ✝️
Date: 2025-11-15
"""

from abc import ABC, abstractmethod
from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Optional, Dict, Any, Callable


class CharacterMood(Enum):
    """Character emotional states."""

    IDLE = auto()
    HAPPY = auto()
    ALERT = auto()
    WORRIED = auto()
    TEACHING = auto()
    CELEBRATING = auto()


@dataclass
class DialogLine:
    """A line of dialog from a character."""

    text: str
    mood: CharacterMood
    duration: float = 3.0  # seconds to display
    educational_note: Optional[str] = None
    sound_effect: Optional[str] = None


class Behavior(ABC):
    """
    Abstract behavior that can be attached to characters.
    Examples: IdleBehavior, DialogBehavior, MoveBehavior, etc.
    """

    @abstractmethod
    def should_activate(self, character: "Character") -> bool:
        """Check if this behavior should run."""
        pass

    @abstractmethod
    def execute(self, character: "Character", dt: float) -> None:
        """Execute behavior logic."""
        pass


class Character(ABC):
    """
    Base class for all game characters.

    Characters are autonomous agents that:
    - React to network events
    - Have moods and states
    - Speak dialog
    - Execute behaviors
    """

    def __init__(self, character_id: str, name: str, emoji: str = "👤"):
        """
        Initialize character.

        Args:
            character_id: Unique identifier (e.g., "guardian", "professor")
            name: Display name (e.g., "The Guardian")
            emoji: Visual emoji representation (default: generic person)
        """
        self.character_id = character_id
        self.name = name
        self.emoji = emoji

        # State
        self.mood = CharacterMood.IDLE
        self.health = 100.0
        self.position = (0, 0)

        # Dialog
        self.current_dialog: Optional[DialogLine] = None
        self.dialog_timer = 0.0
        self.dialog_queue: List[DialogLine] = []

        # Behaviors
        self.behaviors: List[Behavior] = []

        # Animation
        self.current_animation = "idle"
        self.animation_frame = 0
        self.animation_timer = 0.0

        # Events handled
        self.event_handlers: Dict[str, Callable] = {}

    def add_behavior(self, behavior: Behavior) -> None:
        """Add a behavior to this character."""
        self.behaviors.append(behavior)

    def register_event_handler(self, event_type: str, handler: Callable) -> None:
        """
        Register handler for specific event type.

        Args:
            event_type: e.g., "SIGNAL_WEAK", "ROGUE_AP_DETECTED"
            handler: Callable that takes (event_data: Dict) -> None
        """
        self.event_handlers[event_type] = handler

    def process_event(self, event_type: str, event_data: Dict[str, Any]) -> None:
        """
        Process a game event.

        Args:
            event_type: Type of event (e.g., "SIGNAL_WEAK")
            event_data: Event payload
        """
        if event_type in self.event_handlers:
            self.event_handlers[event_type](event_data)

    def speak(
        self,
        text: str,
        mood: Optional[CharacterMood] = None,
        educational_note: Optional[str] = None,
        duration: float = 3.0,
    ) -> None:
        """
        Queue dialog to be spoken.

        Args:
            text: What to say
            mood: Emotional state while speaking
            educational_note: Optional tooltip/explanation
            duration: How long to display (seconds)
        """
        dialog = DialogLine(
            text=text, mood=mood or self.mood, duration=duration, educational_note=educational_note
        )
        self.dialog_queue.append(dialog)

    def transition_to(self, new_mood: CharacterMood) -> None:
        """
        Change character mood/state.

        Args:
            new_mood: New emotional state
        """
        old_mood = self.mood
        self.mood = new_mood

        # Update animation
        if new_mood == CharacterMood.IDLE:
            self.current_animation = "idle"
        elif new_mood == CharacterMood.ALERT:
            self.current_animation = "alert"
        elif new_mood == CharacterMood.TEACHING:
            self.current_animation = "teaching"
        elif new_mood == CharacterMood.HAPPY:
            self.current_animation = "happy"
        elif new_mood == CharacterMood.WORRIED:
            self.current_animation = "worried"
        elif new_mood == CharacterMood.CELEBRATING:
            self.current_animation = "celebrating"

        self.on_mood_changed(old_mood, new_mood)

    def update(self, dt: float) -> None:
        """
        Update character logic.

        Args:
            dt: Delta time in seconds
        """
        # Update dialog
        if self.current_dialog:
            self.dialog_timer += dt
            if self.dialog_timer >= self.current_dialog.duration:
                self.current_dialog = None
                self.dialog_timer = 0.0

        # Pop next dialog from queue
        if not self.current_dialog and self.dialog_queue:
            self.current_dialog = self.dialog_queue.pop(0)
            self.dialog_timer = 0.0

        # Execute active behaviors
        for behavior in self.behaviors:
            if behavior.should_activate(self):
                behavior.execute(self, dt)

        # Character-specific update
        self.on_update(dt)

    @abstractmethod
    def on_update(self, dt: float) -> None:
        """Character-specific update logic (override in subclasses)."""
        pass

    def on_mood_changed(self, old_mood: CharacterMood, new_mood: CharacterMood) -> None:
        """Called when mood changes (can override)."""
        pass

    def get_sprite_id(self) -> str:
        """Get current sprite ID based on animation state."""
        return f"{self.character_id}_{self.current_animation}"

"""
Unit tests for base_character module.

Tests the Character base class, CharacterMood enum, and dialog system.

Author: Juan-Dev + AI Architect - Soli Deo Gloria ✝️
Date: 2025-11-15
"""

import pytest
from src.gamification.characters.base_character import (
    Character,
    CharacterMood,
    DialogLine,
    Behavior,
)


# Concrete Character implementation for testing
class MockCharacter(Character):
    """Mock character for unit testing."""

    def __init__(self):
        super().__init__(character_id="test_char", name="Test Character", emoji="🧪")
        self.update_called = False
        self.mood_changed_called = False
        self.old_mood = None
        self.new_mood = None

    def on_update(self, dt: float) -> None:
        """Track update calls."""
        self.update_called = True

    def on_mood_changed(self, old_mood: CharacterMood, new_mood: CharacterMood) -> None:
        """Track mood changes."""
        self.mood_changed_called = True
        self.old_mood = old_mood
        self.new_mood = new_mood


# Concrete Behavior implementation for testing
class MockBehavior(Behavior):
    """Test behavior for unit testing."""

    def __init__(self, should_activate: bool = True):
        self._should_activate = should_activate
        self.execute_called = False

    def should_activate(self, character: Character) -> bool:
        """Test activation condition."""
        return self._should_activate

    def execute(self, character: Character, dt: float) -> None:
        """Track execution calls."""
        self.execute_called = True


class TestCharacterMood:
    """Tests for CharacterMood enum."""

    def test_mood_values_exist(self):
        """Test that all mood values are defined."""
        assert CharacterMood.IDLE
        assert CharacterMood.HAPPY
        assert CharacterMood.ALERT
        assert CharacterMood.WORRIED
        assert CharacterMood.TEACHING
        assert CharacterMood.CELEBRATING

    def test_mood_unique(self):
        """Test that mood values are unique."""
        moods = [
            CharacterMood.IDLE,
            CharacterMood.HAPPY,
            CharacterMood.ALERT,
            CharacterMood.WORRIED,
            CharacterMood.TEACHING,
            CharacterMood.CELEBRATING,
        ]
        assert len(moods) == len(set(moods))


class TestDialogLine:
    """Tests for DialogLine dataclass."""

    def test_dialog_line_creation(self):
        """Test creating a dialog line."""
        dialog = DialogLine(
            text="Hello, world!",
            mood=CharacterMood.HAPPY,
            duration=5.0,
            educational_note="This is educational",
        )

        assert dialog.text == "Hello, world!"
        assert dialog.mood == CharacterMood.HAPPY
        assert dialog.duration == 5.0
        assert dialog.educational_note == "This is educational"

    def test_dialog_line_defaults(self):
        """Test dialog line default values."""
        dialog = DialogLine(text="Test", mood=CharacterMood.IDLE)

        assert dialog.duration == 3.0
        assert dialog.educational_note is None
        assert dialog.sound_effect is None


class TestCharacterInitialization:
    """Tests for Character initialization."""

    def test_character_init(self):
        """Test character initialization."""
        char = MockCharacter()

        assert char.character_id == "test_char"
        assert char.name == "Test Character"
        assert char.emoji == "🧪"
        assert char.mood == CharacterMood.IDLE
        assert char.health == 100.0
        assert char.position == (0, 0)

    def test_character_empty_queues(self):
        """Test character starts with empty queues."""
        char = MockCharacter()

        assert char.current_dialog is None
        assert char.dialog_timer == 0.0
        assert len(char.dialog_queue) == 0
        assert len(char.behaviors) == 0
        assert len(char.event_handlers) == 0


class TestCharacterDialog:
    """Tests for character dialog system."""

    def test_speak_adds_to_queue(self):
        """Test that speak() adds dialog to queue."""
        char = MockCharacter()
        char.speak("Hello!")

        assert len(char.dialog_queue) == 1
        assert char.dialog_queue[0].text == "Hello!"

    def test_speak_multiple_lines(self):
        """Test queueing multiple dialog lines."""
        char = MockCharacter()
        char.speak("Line 1")
        char.speak("Line 2")
        char.speak("Line 3")

        assert len(char.dialog_queue) == 3
        assert char.dialog_queue[0].text == "Line 1"
        assert char.dialog_queue[1].text == "Line 2"
        assert char.dialog_queue[2].text == "Line 3"

    def test_speak_with_custom_mood(self):
        """Test speak() with custom mood."""
        char = MockCharacter()
        char.speak("Happy text", mood=CharacterMood.HAPPY)

        assert char.dialog_queue[0].mood == CharacterMood.HAPPY

    def test_speak_with_educational_note(self):
        """Test speak() with educational note."""
        char = MockCharacter()
        char.speak("Text", educational_note="Educational content")

        assert char.dialog_queue[0].educational_note == "Educational content"

    def test_dialog_progression(self):
        """Test dialog advances through queue."""
        char = MockCharacter()
        char.speak("First", duration=1.0)
        char.speak("Second", duration=1.0)

        # First update should pop first dialog
        char.update(0.016)
        assert char.current_dialog is not None
        assert char.current_dialog.text == "First"

        # After duration expires, should move to second dialog
        char.update(1.5)
        assert char.current_dialog.text == "Second"

    def test_dialog_timer_reset(self):
        """Test dialog timer resets between lines."""
        char = MockCharacter()
        char.speak("Test", duration=2.0)

        # First update pops dialog and starts timer
        char.update(0.016)
        assert char.current_dialog is not None

        # Advance time within duration
        char.update(0.5)
        assert char.dialog_timer > 0

        # Complete first dialog
        char.update(3.0)
        assert char.current_dialog is None
        assert char.dialog_timer == 0.0


class TestCharacterMoodTransitions:
    """Tests for character mood transitions."""

    def test_transition_to_changes_mood(self):
        """Test transition_to() changes mood."""
        char = MockCharacter()
        assert char.mood == CharacterMood.IDLE

        char.transition_to(CharacterMood.HAPPY)
        assert char.mood == CharacterMood.HAPPY

    def test_transition_calls_on_mood_changed(self):
        """Test transition_to() calls on_mood_changed hook."""
        char = MockCharacter()
        char.transition_to(CharacterMood.ALERT)

        assert char.mood_changed_called
        assert char.old_mood == CharacterMood.IDLE
        assert char.new_mood == CharacterMood.ALERT

    def test_transition_updates_animation(self):
        """Test transition_to() updates animation."""
        char = MockCharacter()

        transitions = [
            (CharacterMood.IDLE, "idle"),
            (CharacterMood.HAPPY, "happy"),
            (CharacterMood.ALERT, "alert"),
            (CharacterMood.WORRIED, "worried"),
            (CharacterMood.TEACHING, "teaching"),
            (CharacterMood.CELEBRATING, "celebrating"),
        ]

        for mood, expected_animation in transitions:
            char.transition_to(mood)
            assert char.current_animation == expected_animation


class TestCharacterBehaviors:
    """Tests for character behavior system."""

    def test_add_behavior(self):
        """Test adding behavior to character."""
        char = MockCharacter()
        behavior = MockBehavior()

        char.add_behavior(behavior)
        assert len(char.behaviors) == 1
        assert behavior in char.behaviors

    def test_behavior_executes_when_active(self):
        """Test behavior executes when should_activate returns True."""
        char = MockCharacter()
        behavior = MockBehavior(should_activate=True)
        char.add_behavior(behavior)

        char.update(0.016)
        assert behavior.execute_called

    def test_behavior_not_executes_when_inactive(self):
        """Test behavior doesn't execute when should_activate returns False."""
        char = MockCharacter()
        behavior = MockBehavior(should_activate=False)
        char.add_behavior(behavior)

        char.update(0.016)
        assert not behavior.execute_called

    def test_multiple_behaviors(self):
        """Test multiple behaviors can be added."""
        char = MockCharacter()
        b1 = MockBehavior(should_activate=True)
        b2 = MockBehavior(should_activate=True)
        b3 = MockBehavior(should_activate=False)

        char.add_behavior(b1)
        char.add_behavior(b2)
        char.add_behavior(b3)

        char.update(0.016)
        assert b1.execute_called
        assert b2.execute_called
        assert not b3.execute_called


class TestCharacterEvents:
    """Tests for character event handling."""

    def test_register_event_handler(self):
        """Test registering event handler."""
        char = MockCharacter()
        handler_called = [False]

        def test_handler(event_data):
            handler_called[0] = True

        char.register_event_handler("TEST_EVENT", test_handler)
        assert "TEST_EVENT" in char.event_handlers

    def test_process_event_calls_handler(self):
        """Test process_event() calls registered handler."""
        char = MockCharacter()
        received_data = [None]

        def test_handler(event_data):
            received_data[0] = event_data

        char.register_event_handler("TEST_EVENT", test_handler)
        char.process_event("TEST_EVENT", {"value": 42})

        assert received_data[0] is not None
        assert received_data[0]["value"] == 42

    def test_process_event_ignores_unregistered(self):
        """Test process_event() ignores unregistered events."""
        char = MockCharacter()
        # Should not raise error
        char.process_event("UNKNOWN_EVENT", {})


class TestCharacterUpdate:
    """Tests for character update loop."""

    def test_update_calls_on_update(self):
        """Test update() calls on_update hook."""
        char = MockCharacter()
        char.update(0.016)

        assert char.update_called

    def test_update_processes_dialog(self):
        """Test update() processes dialog queue."""
        char = MockCharacter()
        char.speak("Test", duration=0.5)

        # First update should activate dialog
        char.update(0.016)
        assert char.current_dialog is not None

        # After duration, dialog should clear
        char.update(1.0)
        assert char.current_dialog is None

    def test_update_executes_behaviors(self):
        """Test update() executes active behaviors."""
        char = MockCharacter()
        behavior = MockBehavior(should_activate=True)
        char.add_behavior(behavior)

        char.update(0.016)
        assert behavior.execute_called


class TestCharacterProperties:
    """Tests for character properties and state."""

    def test_initial_health(self):
        """Test character starts with 100 health."""
        char = MockCharacter()
        assert char.health == 100.0

    def test_initial_position(self):
        """Test character starts at (0, 0)."""
        char = MockCharacter()
        assert char.position == (0, 0)

    def test_animation_state(self):
        """Test animation state properties."""
        char = MockCharacter()
        assert char.current_animation == "idle"
        assert char.animation_frame == 0
        assert char.animation_timer == 0.0

    def test_get_sprite_id(self):
        """Test get_sprite_id() returns correct format."""
        char = MockCharacter()
        sprite_id = char.get_sprite_id()

        assert sprite_id == "test_char_idle"

        char.transition_to(CharacterMood.HAPPY)
        sprite_id = char.get_sprite_id()
        assert sprite_id == "test_char_happy"

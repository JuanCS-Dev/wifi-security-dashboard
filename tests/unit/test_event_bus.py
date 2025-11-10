"""
Unit tests for EventBus.

Author: Juan-Dev - Soli Deo Gloria ✝️
Date: 2025-11-09
"""

import pytest
from src.core.event_bus import EventBus, Event, EventType


class TestEvent:
    """Test Event dataclass"""

    def test_event_creation(self):
        """Test creating event"""
        event = Event(
            type=EventType.COMPONENT_UPDATED.value,
            source="test_component",
            data={"value": 42}
        )

        assert event.type == EventType.COMPONENT_UPDATED.value
        assert event.source == "test_component"
        assert event.data == {"value": 42}
        assert event.timestamp > 0

    def test_event_repr(self):
        """Test event string representation"""
        event = Event(
            type="test.event",
            source="tester"
        )
        repr_str = repr(event)
        assert "test.event" in repr_str
        assert "tester" in repr_str


class TestEventBus:
    """Test EventBus publish-subscribe system"""

    def test_eventbus_initialization(self):
        """Test EventBus initializes correctly"""
        bus = EventBus()
        assert bus.get_subscriber_count(EventType.COMPONENT_UPDATED) == 0
        assert len(bus.get_history()) == 0

    def test_subscribe_and_publish(self):
        """Test basic subscribe and publish"""
        bus = EventBus()
        received_events = []

        def handler(event: Event):
            received_events.append(event)

        # Subscribe
        bus.subscribe(EventType.COMPONENT_UPDATED, handler)

        # Publish
        event = Event(
            type=EventType.COMPONENT_UPDATED.value,
            source="test",
            data={"value": 123}
        )
        bus.publish(event)

        # Assert handler was called
        assert len(received_events) == 1
        assert received_events[0].data == {"value": 123}

    def test_multiple_handlers(self):
        """Test multiple handlers for same event type"""
        bus = EventBus()
        call_count = {"handler1": 0, "handler2": 0}

        def handler1(event: Event):
            call_count["handler1"] += 1

        def handler2(event: Event):
            call_count["handler2"] += 1

        bus.subscribe(EventType.COMPONENT_UPDATED, handler1)
        bus.subscribe(EventType.COMPONENT_UPDATED, handler2)

        # Publish
        bus.publish(Event(
            type=EventType.COMPONENT_UPDATED.value,
            source="test"
        ))

        # Both handlers called
        assert call_count["handler1"] == 1
        assert call_count["handler2"] == 1

    def test_unsubscribe(self):
        """Test unsubscribing handler"""
        bus = EventBus()
        call_count = 0

        def handler(event: Event):
            nonlocal call_count
            call_count += 1

        # Subscribe then unsubscribe
        bus.subscribe(EventType.COMPONENT_UPDATED, handler)
        bus.unsubscribe(EventType.COMPONENT_UPDATED, handler)

        # Publish - handler should NOT be called
        bus.publish(Event(
            type=EventType.COMPONENT_UPDATED.value,
            source="test"
        ))

        assert call_count == 0

    def test_unsubscribe_nonexistent_raises_error(self):
        """Test unsubscribing handler that doesn't exist raises ValueError"""
        bus = EventBus()

        def handler(event: Event):
            pass

        with pytest.raises(ValueError, match="Handler not found"):
            bus.unsubscribe(EventType.COMPONENT_UPDATED, handler)

    def test_handler_exception_doesnt_break_others(self):
        """Test that exception in one handler doesn't prevent others from running"""
        bus = EventBus()
        results = []

        def bad_handler(event: Event):
            raise RuntimeError("Handler failed!")

        def good_handler(event: Event):
            results.append("success")

        bus.subscribe(EventType.COMPONENT_UPDATED, bad_handler)
        bus.subscribe(EventType.COMPONENT_UPDATED, good_handler)

        # Publish - should not raise exception
        bus.publish(Event(
            type=EventType.COMPONENT_UPDATED.value,
            source="test"
        ))

        # Good handler was still called
        assert results == ["success"]

    def test_event_history(self):
        """Test event history tracking"""
        bus = EventBus()

        # Publish multiple events
        for i in range(5):
            bus.publish(Event(
                type=EventType.COMPONENT_UPDATED.value,
                source=f"comp_{i}",
                data={"value": i}
            ))

        history = bus.get_history()
        assert len(history) == 5
        assert history[0].data["value"] == 0
        assert history[-1].data["value"] == 4

    def test_event_history_limit(self):
        """Test event history respects limit"""
        bus = EventBus()

        # Publish many events
        for i in range(20):
            bus.publish(Event(
                type=EventType.COMPONENT_UPDATED.value,
                source="test",
                data={"i": i}
            ))

        # Get limited history
        history = bus.get_history(limit=5)
        assert len(history) == 5
        # Should be most recent 5
        assert history[-1].data["i"] == 19

    def test_event_history_filter_by_type(self):
        """Test filtering history by event type"""
        bus = EventBus()

        # Publish different event types
        bus.publish(Event(type=EventType.COMPONENT_UPDATED.value, source="c1"))
        bus.publish(Event(type=EventType.PLUGIN_LOADED.value, source="p1"))
        bus.publish(Event(type=EventType.COMPONENT_UPDATED.value, source="c2"))

        # Filter by type
        updates = bus.get_history(event_type=EventType.COMPONENT_UPDATED)
        assert len(updates) == 2

        plugin_events = bus.get_history(event_type=EventType.PLUGIN_LOADED)
        assert len(plugin_events) == 1

    def test_clear_history(self):
        """Test clearing event history"""
        bus = EventBus()

        bus.publish(Event(type=EventType.COMPONENT_UPDATED.value, source="test"))
        assert len(bus.get_history()) == 1

        bus.clear_history()
        assert len(bus.get_history()) == 0

    def test_get_subscriber_count(self):
        """Test getting subscriber count"""
        bus = EventBus()

        def handler1(e): pass
        def handler2(e): pass

        assert bus.get_subscriber_count(EventType.COMPONENT_UPDATED) == 0

        bus.subscribe(EventType.COMPONENT_UPDATED, handler1)
        assert bus.get_subscriber_count(EventType.COMPONENT_UPDATED) == 1

        bus.subscribe(EventType.COMPONENT_UPDATED, handler2)
        assert bus.get_subscriber_count(EventType.COMPONENT_UPDATED) == 2

    def test_custom_max_history(self):
        """Test EventBus with custom max_history parameter"""
        # Create bus with custom limit of 5 events
        bus = EventBus(max_history=5)

        # Publish 10 events
        for i in range(10):
            bus.publish(Event(
                type=EventType.COMPONENT_UPDATED.value,
                source=f"component_{i}",
                data={"index": i}
            ))

        # Should only keep last 5 events
        history = bus.get_history(limit=100)
        assert len(history) == 5

        # Verify it's the last 5 (indices 5-9)
        for i, event in enumerate(history):
            assert event.data["index"] == i + 5

    def test_default_max_history(self):
        """Test EventBus default max_history is 100"""
        bus = EventBus()

        # Publish 150 events
        for i in range(150):
            bus.publish(Event(
                type=EventType.COMPONENT_UPDATED.value,
                source=f"component_{i}",
                data={"index": i}
            ))

        # Should keep exactly 100 events (the default)
        history = bus.get_history(limit=200)
        assert len(history) == 100

        # Verify it's the last 100 (indices 50-149)
        for i, event in enumerate(history):
            assert event.data["index"] == i + 50

    def test_eventbus_repr(self):
        """Test EventBus string representation"""
        bus = EventBus()

        def handler(e): pass
        bus.subscribe(EventType.COMPONENT_UPDATED, handler)
        bus.publish(Event(type=EventType.COMPONENT_UPDATED.value, source="test"))

        repr_str = repr(bus)
        assert "EventBus" in repr_str
        assert "handlers=1" in repr_str
        assert "history=1" in repr_str

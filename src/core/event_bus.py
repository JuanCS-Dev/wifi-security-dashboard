"""
Event bus for decoupled communication between system components.

This module provides a simple publish-subscribe event system for
components, plugins, and triggers to communicate without tight coupling.

Author: Juan-Dev - Soli Deo Gloria ✝️
Date: 2025-11-09
"""

from typing import Callable, Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
import time
from collections import defaultdict


class EventType(Enum):
    """Built-in event types"""
    # Component events
    COMPONENT_UPDATED = "component.updated"
    COMPONENT_TRIGGERED = "component.triggered"
    COMPONENT_ERROR = "component.error"

    # Plugin events
    PLUGIN_LOADED = "plugin.loaded"
    PLUGIN_DATA_READY = "plugin.data_ready"
    PLUGIN_DATA_COLLECTED = "plugin.data_collected"
    PLUGIN_STOPPED = "plugin.stopped"
    PLUGIN_ERROR = "plugin.error"

    # Dashboard events
    DASHBOARD_STARTED = "dashboard.started"
    DASHBOARD_STOPPED = "dashboard.stopped"
    DASHBOARD_PAUSED = "dashboard.paused"
    DASHBOARD_RESUMED = "dashboard.resumed"

    # User interaction events
    KEY_PRESSED = "user.key_pressed"
    MOUSE_CLICKED = "user.mouse_clicked"

    # Educational events
    TIP_SHOWN = "educational.tip_shown"
    HELP_REQUESTED = "educational.help_requested"


@dataclass
class Event:
    """
    Event data structure.

    Attributes:
        type: Event type (EventType or custom string)
        source: Source component/plugin identifier
        data: Event payload (any data relevant to the event)
        timestamp: Event creation timestamp (milliseconds)
    """
    type: str
    source: str
    data: Any = None
    timestamp: float = field(default_factory=lambda: time.time() * 1000)

    def __repr__(self) -> str:
        return f"Event(type='{self.type}', source='{self.source}', timestamp={self.timestamp:.0f})"


# Type alias for event handlers
EventHandler = Callable[[Event], None]


class EventBus:
    """
    Publish-subscribe event bus.

    Allows components to communicate without knowing about each other.
    Follows the Observer pattern for loose coupling.

    Example:
        >>> bus = EventBus()
        >>>
        >>> def on_component_update(event: Event):
        ...     print(f"Component {event.source} updated: {event.data}")
        >>>
        >>> bus.subscribe(EventType.COMPONENT_UPDATED, on_component_update)
        >>> bus.publish(Event(
        ...     type=EventType.COMPONENT_UPDATED.value,
        ...     source="wifi_chart",
        ...     data={"signal": -45}
        ... ))
    """

    def __init__(self, max_history: int = 100):
        """
        Initialize event bus.

        Args:
            max_history: Maximum number of events to keep in history (default: 100)
        """
        # Dict mapping event types to list of handlers
        self._handlers: Dict[str, List[EventHandler]] = defaultdict(list)

        # Event history (for debugging)
        self._history: List[Event] = []
        self._max_history: int = max_history

    def subscribe(self, event_type: str | EventType, handler: EventHandler) -> None:
        """
        Subscribe to events of a specific type.

        Args:
            event_type: Type of event to listen for (EventType or string)
            handler: Callback function to invoke when event occurs

        Example:
            >>> def my_handler(event: Event):
            ...     print(f"Received: {event}")
            >>> bus.subscribe(EventType.COMPONENT_UPDATED, my_handler)
        """
        if isinstance(event_type, EventType):
            event_type = event_type.value

        if handler not in self._handlers[event_type]:
            self._handlers[event_type].append(handler)

    def unsubscribe(self, event_type: str | EventType, handler: EventHandler) -> None:
        """
        Unsubscribe from events.

        Args:
            event_type: Event type to unsubscribe from
            handler: Handler to remove

        Raises:
            ValueError: If handler not found
        """
        if isinstance(event_type, EventType):
            event_type = event_type.value

        if handler in self._handlers[event_type]:
            self._handlers[event_type].remove(handler)
        else:
            raise ValueError(f"Handler not found for event type '{event_type}'")

    def publish(self, event: Event) -> None:
        """
        Publish an event to all subscribers.

        Args:
            event: Event to publish

        Note:
            Handlers are called synchronously in the order they were registered.
            If a handler raises an exception, it will be caught and logged,
            but other handlers will still be called.
        """
        # Add to history
        self._history.append(event)
        if len(self._history) > self._max_history:
            self._history.pop(0)

        # Call all registered handlers
        handlers = self._handlers.get(event.type, [])
        for handler in handlers:
            try:
                handler(event)
            except Exception as e:
                # Log error but continue with other handlers
                error_event = Event(
                    type=EventType.COMPONENT_ERROR.value,
                    source="event_bus",
                    data={
                        'original_event': event,
                        'handler': handler.__name__,
                        'error': str(e)
                    }
                )
                # Avoid infinite loop - don't publish error events recursively
                if event.type != EventType.COMPONENT_ERROR.value:
                    self._history.append(error_event)

    def get_history(self, event_type: Optional[str | EventType] = None,
                    limit: int = 10) -> List[Event]:
        """
        Get recent event history.

        Args:
            event_type: Filter by event type (None = all events)
            limit: Maximum number of events to return

        Returns:
            List of recent events (most recent last)
        """
        if event_type is not None:
            if isinstance(event_type, EventType):
                event_type = event_type.value
            events = [e for e in self._history if e.type == event_type]
        else:
            events = self._history

        return events[-limit:]

    def clear_history(self) -> None:
        """Clear event history"""
        self._history.clear()

    def get_subscriber_count(self, event_type: str | EventType) -> int:
        """
        Get number of subscribers for an event type.

        Args:
            event_type: Event type to check

        Returns:
            Number of registered handlers
        """
        if isinstance(event_type, EventType):
            event_type = event_type.value

        return len(self._handlers.get(event_type, []))

    def __repr__(self) -> str:
        total_handlers = sum(len(handlers) for handlers in self._handlers.values())
        return f"EventBus(handlers={total_handlers}, history={len(self._history)})"

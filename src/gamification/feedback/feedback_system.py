"""
Feedback and telemetry system for beta testing.

Collects anonymous usage data and user feedback (with explicit consent).
All data collection is OPT-IN and transparent.

Author: Juan-Dev + AI Architect - Soli Deo Gloria ✝️
Date: 2025-11-15
"""

import json
import time
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional
from datetime import datetime


@dataclass
class FeedbackEvent:
    """A single feedback/telemetry event."""

    event_type: str  # e.g., "game_start", "scenario_complete", "bug_report"
    timestamp: float = field(default_factory=time.time)
    session_id: str = ""
    data: Dict = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class BugReport:
    """User-submitted bug report."""

    title: str
    description: str
    steps_to_reproduce: str
    expected_behavior: str
    actual_behavior: str
    timestamp: float = field(default_factory=time.time)
    severity: str = "medium"  # low, medium, high, critical
    category: str = "general"  # gameplay, performance, ui, audio, other
    system_info: Dict = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class UserFeedback:
    """General user feedback."""

    rating: int  # 1-5 stars
    comments: str
    what_liked: str = ""
    what_disliked: str = ""
    suggestions: str = ""
    timestamp: float = field(default_factory=time.time)
    age_group: str = "not_specified"  # 9-12, 13-16, 17+, teacher, parent

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return asdict(self)


class FeedbackSystem:
    """
    Manages feedback collection and telemetry.

    All data collection is:
    - OPT-IN (disabled by default)
    - ANONYMOUS (no personal data)
    - TRANSPARENT (user knows what's collected)
    - LOCAL-FIRST (stored locally, optional upload)
    """

    def __init__(self, data_dir: Optional[Path] = None):
        """
        Initialize feedback system.

        Args:
            data_dir: Directory to store feedback data (default: ~/.wifi_security_game/)
        """
        if data_dir is None:
            data_dir = Path.home() / ".wifi_security_game"

        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

        self.feedback_file = self.data_dir / "feedback.json"
        self.bugs_file = self.data_dir / "bugs.json"
        self.events_file = self.data_dir / "events.json"
        self.consent_file = self.data_dir / "consent.json"

        # Session tracking
        self.session_id = self._generate_session_id()
        self.session_start = time.time()

        # Consent (opt-in)
        self.telemetry_enabled = self._load_consent()

        # Event buffer
        self.event_buffer: List[FeedbackEvent] = []

    def _generate_session_id(self) -> str:
        """Generate anonymous session ID."""
        import hashlib
        import uuid

        # Anonymous session ID (not tied to user)
        random_uuid = str(uuid.uuid4())
        return hashlib.sha256(random_uuid.encode()).hexdigest()[:16]

    def _load_consent(self) -> bool:
        """Load user consent for telemetry."""
        if not self.consent_file.exists():
            return False  # Default: disabled

        try:
            with open(self.consent_file, "r") as f:
                consent_data = json.load(f)
                return consent_data.get("telemetry_enabled", False)
        except Exception:
            return False

    def set_telemetry_consent(self, enabled: bool) -> None:
        """
        Set user consent for telemetry.

        Args:
            enabled: True to enable telemetry, False to disable
        """
        self.telemetry_enabled = enabled

        consent_data = {
            "telemetry_enabled": enabled,
            "consent_timestamp": time.time(),
            "consent_version": "1.0.0",
        }

        with open(self.consent_file, "w") as f:
            json.dump(consent_data, f, indent=2)

    def log_event(self, event_type: str, data: Optional[Dict] = None) -> None:
        """
        Log a telemetry event (only if consent given).

        Args:
            event_type: Type of event (e.g., "game_start", "scenario_complete")
            data: Optional event data
        """
        if not self.telemetry_enabled:
            return

        event = FeedbackEvent(
            event_type=event_type,
            session_id=self.session_id,
            data=data or {},
        )

        self.event_buffer.append(event)

        # Write to file (append mode)
        self._append_to_file(self.events_file, event.to_dict())

    def submit_bug_report(self, bug: BugReport) -> None:
        """
        Submit a bug report.

        Bug reports are always saved (not affected by telemetry consent).

        Args:
            bug: BugReport instance
        """
        # Add system info
        bug.system_info = self._get_system_info()

        # Save to file
        self._append_to_file(self.bugs_file, bug.to_dict())

    def submit_feedback(self, feedback: UserFeedback) -> None:
        """
        Submit general user feedback.

        Feedback is always saved (not affected by telemetry consent).

        Args:
            feedback: UserFeedback instance
        """
        # Save to file
        self._append_to_file(self.feedback_file, feedback.to_dict())

    def _append_to_file(self, filepath: Path, data: Dict) -> None:
        """Append data to JSON file."""
        # Load existing data
        if filepath.exists():
            try:
                with open(filepath, "r") as f:
                    existing = json.load(f)
            except Exception:
                existing = []
        else:
            existing = []

        # Append new data
        existing.append(data)

        # Write back
        with open(filepath, "w") as f:
            json.dump(existing, f, indent=2)

    def _get_system_info(self) -> Dict:
        """Get anonymous system information."""
        import platform
        import sys

        return {
            "os": platform.system(),
            "os_version": platform.version(),
            "python_version": sys.version,
            "architecture": platform.machine(),
        }

    def get_session_stats(self) -> Dict:
        """Get current session statistics."""
        return {
            "session_id": self.session_id,
            "session_duration": time.time() - self.session_start,
            "events_logged": len(self.event_buffer),
            "telemetry_enabled": self.telemetry_enabled,
        }

    def export_feedback_report(self, output_file: Path) -> None:
        """
        Export all feedback to a single report file.

        Args:
            output_file: Output filepath
        """
        report = {
            "export_date": datetime.now().isoformat(),
            "bugs": self._load_json_file(self.bugs_file),
            "feedback": self._load_json_file(self.feedback_file),
            "events": self._load_json_file(self.events_file) if self.telemetry_enabled else [],
            "consent": self._load_json_file(self.consent_file),
        }

        with open(output_file, "w") as f:
            json.dump(report, f, indent=2)

    def _load_json_file(self, filepath: Path) -> List:
        """Load JSON file or return empty list."""
        if not filepath.exists():
            return []

        try:
            with open(filepath, "r") as f:
                return json.load(f)
        except Exception:
            return []

    def clear_all_data(self) -> None:
        """Clear all collected data (for privacy)."""
        for file in [self.feedback_file, self.bugs_file, self.events_file]:
            if file.exists():
                file.unlink()

        self.event_buffer.clear()

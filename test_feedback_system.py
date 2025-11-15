#!/usr/bin/env python3
"""
Quick test script for feedback system.

Tests basic functionality without running the full game.

Author: Juan-Dev + AI Architect - Soli Deo Gloria ✝️
Date: 2025-11-15
"""

import sys
from pathlib import Path
import tempfile
import json

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.gamification.feedback.feedback_system import (
    FeedbackSystem,
    BugReport,
    UserFeedback,
    FeedbackEvent,
)


def test_feedback_system():
    """Test FeedbackSystem basic functionality."""
    print("=" * 70)
    print("Testing Feedback System")
    print("=" * 70)
    print()

    # Create temp directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        print(f"📁 Test directory: {temp_path}")
        print()

        # Test 1: Initialization
        print("Test 1: FeedbackSystem initialization...")
        fs = FeedbackSystem(temp_path)
        assert fs.data_dir == temp_path
        assert fs.telemetry_enabled is False  # Default: disabled
        assert len(fs.event_buffer) == 0
        print("✅ Initialization OK")
        print()

        # Test 2: Set consent
        print("Test 2: Telemetry consent...")
        fs.set_telemetry_consent(True)
        assert fs.telemetry_enabled is True
        assert fs.consent_file.exists()

        # Load consent from file
        with open(fs.consent_file, "r") as f:
            consent_data = json.load(f)
            assert consent_data["telemetry_enabled"] is True
        print("✅ Consent management OK")
        print()

        # Test 3: Log event (with telemetry enabled)
        print("Test 3: Event logging (telemetry ON)...")
        fs.log_event("test_event", {"foo": "bar", "count": 42})
        assert len(fs.event_buffer) == 1
        assert fs.events_file.exists()

        # Load events from file
        with open(fs.events_file, "r") as f:
            events = json.load(f)
            assert len(events) == 1
            assert events[0]["event_type"] == "test_event"
            assert events[0]["data"]["foo"] == "bar"
        print("✅ Event logging OK")
        print()

        # Test 4: Log event (with telemetry disabled)
        print("Test 4: Event logging (telemetry OFF)...")
        fs.set_telemetry_consent(False)
        fs.log_event("ignored_event", {"should": "not_appear"})
        # Event buffer shouldn't grow when telemetry disabled
        assert len(fs.event_buffer) == 1  # Still 1 from before
        print("✅ Telemetry opt-out OK")
        print()

        # Test 5: Submit bug report
        print("Test 5: Bug report submission...")
        bug = BugReport(
            title="Test Bug",
            description="This is a test bug",
            steps_to_reproduce="1. Do this\n2. Do that",
            expected_behavior="Expected result",
            actual_behavior="Actual result",
            severity="medium",
            category="gameplay",
        )
        fs.submit_bug_report(bug)
        assert fs.bugs_file.exists()

        # Load bugs from file
        with open(fs.bugs_file, "r") as f:
            bugs = json.load(f)
            assert len(bugs) == 1
            assert bugs[0]["title"] == "Test Bug"
            assert bugs[0]["severity"] == "medium"
            assert "system_info" in bugs[0]
            assert "os" in bugs[0]["system_info"]
        print("✅ Bug report submission OK")
        print()

        # Test 6: Submit user feedback
        print("Test 6: User feedback submission...")
        feedback = UserFeedback(
            rating=5,
            comments="Great game!",
            what_liked="Everything",
            what_disliked="Nothing",
            suggestions="Add more levels",
            age_group="13-16",
        )
        fs.submit_feedback(feedback)
        assert fs.feedback_file.exists()

        # Load feedback from file
        with open(fs.feedback_file, "r") as f:
            feedbacks = json.load(f)
            assert len(feedbacks) == 1
            assert feedbacks[0]["rating"] == 5
            assert feedbacks[0]["age_group"] == "13-16"
        print("✅ User feedback submission OK")
        print()

        # Test 7: Session stats
        print("Test 7: Session statistics...")
        stats = fs.get_session_stats()
        assert "session_id" in stats
        assert "session_duration" in stats
        assert "events_logged" in stats
        assert "telemetry_enabled" in stats
        assert len(stats["session_id"]) == 16  # SHA256 hash truncated to 16 chars
        print(f"   Session ID: {stats['session_id']}")
        print(f"   Duration: {stats['session_duration']:.2f}s")
        print(f"   Events: {stats['events_logged']}")
        print(f"   Telemetry: {stats['telemetry_enabled']}")
        print("✅ Session statistics OK")
        print()

        # Test 8: Export feedback report
        print("Test 8: Export feedback report...")
        export_file = temp_path / "export.json"
        fs.export_feedback_report(export_file)
        assert export_file.exists()

        with open(export_file, "r") as f:
            report = json.load(f)
            assert "export_date" in report
            assert "bugs" in report
            assert "feedback" in report
            assert "events" in report
            assert "consent" in report
            assert len(report["bugs"]) == 1
            assert len(report["feedback"]) == 1
        print("✅ Export feedback report OK")
        print()

        # Test 9: Clear all data
        print("Test 9: Clear all data...")
        fs.clear_all_data()
        assert not fs.feedback_file.exists()
        assert not fs.bugs_file.exists()
        assert not fs.events_file.exists()
        assert len(fs.event_buffer) == 0
        print("✅ Clear data OK")
        print()

    print("=" * 70)
    print("🎉 All tests PASSED!")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test_feedback_system()
    except AssertionError as e:
        print(f"\n❌ Test FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)

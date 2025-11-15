"""
Feedback UI components for beta testing.

Simple text-based UI for collecting feedback during beta testing.
Can be upgraded to graphical UI in future versions.

Author: Juan-Dev + AI Architect - Soli Deo Gloria ✝️
Date: 2025-11-15
"""

from typing import Optional
from src.gamification.feedback.feedback_system import BugReport, UserFeedback


def show_telemetry_consent_dialog() -> bool:
    """
    Show telemetry consent dialog (console-based).

    Returns:
        True if user consents, False otherwise
    """
    print("\n" + "=" * 70)
    print("📊 TELEMETRY CONSENT")
    print("=" * 70)
    print("\nWiFi Security Education would like to collect anonymous usage data")
    print("to improve the game for students like you!")
    print("\n🔒 Privacy Promise:")
    print("  • 100% ANONYMOUS - No personal information collected")
    print("  • OPT-IN - Disabled by default, you choose")
    print("  • TRANSPARENT - You know exactly what's collected")
    print("  • LOCAL-FIRST - Data stored on your computer")
    print("\n📈 What we collect (if you say YES):")
    print("  • Which scenarios you complete")
    print("  • How long you play")
    print("  • Game performance (FPS)")
    print("  • What features you use")
    print("\n❌ What we DON'T collect:")
    print("  • Your name or email")
    print("  • Your location")
    print("  • Your WiFi password or network details")
    print("  • Any personal information")
    print("\n💡 Why it helps:")
    print("  • Makes the game better for future students")
    print("  • Helps us fix bugs faster")
    print("  • Shows us which scenarios are most fun")
    print("\nYou can change this anytime by pressing F2 during the game.")
    print("\n" + "=" * 70)

    while True:
        response = input("\nEnable anonymous telemetry? (yes/no): ").strip().lower()
        if response in ["yes", "y"]:
            print("\n✅ Thank you! Telemetry ENABLED.")
            print("   Your contribution helps students worldwide! 🌍")
            return True
        elif response in ["no", "n"]:
            print("\n👍 No problem! Telemetry DISABLED.")
            print("   You can enable it anytime by pressing F2.")
            return False
        else:
            print("❌ Please enter 'yes' or 'no'")


def show_bug_report_dialog() -> Optional[BugReport]:
    """
    Show bug report dialog (console-based).

    Returns:
        BugReport if user submits, None if cancelled
    """
    print("\n" + "=" * 70)
    print("🐛 BUG REPORT")
    print("=" * 70)
    print("\nThank you for helping us improve the game!")
    print("Please describe the bug you encountered.")
    print("(Press Ctrl+C or type 'cancel' to abort)\n")

    try:
        # Title
        title = input("Bug title (short summary): ").strip()
        if title.lower() == "cancel" or not title:
            print("❌ Bug report cancelled")
            return None

        # Description
        description = input("\nWhat happened? (detailed description): ").strip()
        if description.lower() == "cancel" or not description:
            print("❌ Bug report cancelled")
            return None

        # Steps to reproduce
        print("\nSteps to reproduce (enter each step, empty line to finish):")
        steps = []
        step_num = 1
        while True:
            step = input(f"  {step_num}. ").strip()
            if not step:
                break
            if step.lower() == "cancel":
                print("❌ Bug report cancelled")
                return None
            steps.append(step)
            step_num += 1

        steps_to_reproduce = "\n".join(f"{i+1}. {s}" for i, s in enumerate(steps))
        if not steps_to_reproduce:
            steps_to_reproduce = "(No steps provided)"

        # Expected behavior
        expected = input("\nWhat did you EXPECT to happen? ").strip()
        if expected.lower() == "cancel":
            print("❌ Bug report cancelled")
            return None
        if not expected:
            expected = "(Not specified)"

        # Actual behavior
        actual = input("\nWhat ACTUALLY happened? ").strip()
        if actual.lower() == "cancel":
            print("❌ Bug report cancelled")
            return None
        if not actual:
            actual = description  # Use description if not specified

        # Severity
        print("\nSeverity:")
        print("  1. Low - Minor annoyance")
        print("  2. Medium - Affects gameplay")
        print("  3. High - Major problem")
        print("  4. Critical - Game-breaking")

        severity_map = {"1": "low", "2": "medium", "3": "high", "4": "critical"}
        severity_input = input("Select (1-4): ").strip()
        severity = severity_map.get(severity_input, "medium")

        # Category
        print("\nCategory:")
        print("  1. Gameplay")
        print("  2. Performance")
        print("  3. UI/Graphics")
        print("  4. Audio")
        print("  5. Other")

        category_map = {
            "1": "gameplay",
            "2": "performance",
            "3": "ui",
            "4": "audio",
            "5": "other",
        }
        category_input = input("Select (1-5): ").strip()
        category = category_map.get(category_input, "general")

        # Create bug report
        bug = BugReport(
            title=title,
            description=description,
            steps_to_reproduce=steps_to_reproduce,
            expected_behavior=expected,
            actual_behavior=actual,
            severity=severity,
            category=category,
        )

        # Confirm
        print("\n" + "-" * 70)
        print("Bug Report Summary:")
        print(f"  Title: {bug.title}")
        print(f"  Severity: {bug.severity.upper()}")
        print(f"  Category: {bug.category}")
        print("-" * 70)

        confirm = input("\nSubmit this bug report? (yes/no): ").strip().lower()
        if confirm in ["yes", "y"]:
            print("\n✅ Bug report submitted! Thank you for your help! 🙏")
            print("   Your report will help us fix this issue.")
            return bug
        else:
            print("❌ Bug report cancelled")
            return None

    except KeyboardInterrupt:
        print("\n\n❌ Bug report cancelled")
        return None


def show_feedback_dialog() -> Optional[UserFeedback]:
    """
    Show user feedback dialog (console-based).

    Returns:
        UserFeedback if user submits, None if cancelled
    """
    print("\n" + "=" * 70)
    print("💬 USER FEEDBACK")
    print("=" * 70)
    print("\nWe'd love to hear what you think about the game!")
    print("(Press Ctrl+C or type 'cancel' to abort)\n")

    try:
        # Rating
        print("How would you rate the game overall?")
        rating_input = input("Rating (1-5 stars): ").strip()
        if rating_input.lower() == "cancel":
            print("❌ Feedback cancelled")
            return None

        try:
            rating = int(rating_input)
            rating = max(1, min(5, rating))  # Clamp to 1-5
        except ValueError:
            rating = 3  # Default to 3 if invalid

        # Comments
        comments = input("\nGeneral comments: ").strip()
        if comments.lower() == "cancel":
            print("❌ Feedback cancelled")
            return None
        if not comments:
            comments = "(No comments)"

        # What liked
        what_liked = input("\nWhat did you LIKE? ").strip()
        if what_liked.lower() == "cancel":
            print("❌ Feedback cancelled")
            return None

        # What disliked
        what_disliked = input("\nWhat did you DISLIKE? ").strip()
        if what_disliked.lower() == "cancel":
            print("❌ Feedback cancelled")
            return None

        # Suggestions
        suggestions = input("\nSuggestions for improvement: ").strip()
        if suggestions.lower() == "cancel":
            print("❌ Feedback cancelled")
            return None

        # Age group
        print("\nAge group (optional, helps us improve for your age):")
        print("  1. 9-12 years")
        print("  2. 13-16 years")
        print("  3. 17+ years")
        print("  4. Teacher")
        print("  5. Parent")
        print("  6. Prefer not to say")

        age_map = {
            "1": "9-12",
            "2": "13-16",
            "3": "17+",
            "4": "teacher",
            "5": "parent",
            "6": "not_specified",
        }
        age_input = input("Select (1-6): ").strip()
        age_group = age_map.get(age_input, "not_specified")

        # Create feedback
        feedback = UserFeedback(
            rating=rating,
            comments=comments,
            what_liked=what_liked,
            what_disliked=what_disliked,
            suggestions=suggestions,
            age_group=age_group,
        )

        # Confirm
        print("\n" + "-" * 70)
        print("Feedback Summary:")
        print(f"  Rating: {'⭐' * rating} ({rating}/5)")
        print(f"  Age Group: {age_group}")
        print("-" * 70)

        confirm = input("\nSubmit this feedback? (yes/no): ").strip().lower()
        if confirm in ["yes", "y"]:
            print("\n✅ Feedback submitted! Thank you so much! 💖")
            print("   Your input helps us make the game better!")
            return feedback
        else:
            print("❌ Feedback cancelled")
            return None

    except KeyboardInterrupt:
        print("\n\n❌ Feedback cancelled")
        return None


def show_help_message() -> None:
    """Show feedback system help message."""
    print("\n" + "=" * 70)
    print("📊 FEEDBACK SYSTEM - HELP")
    print("=" * 70)
    print("\nKeyboard Shortcuts:")
    print("  F1  - Report a bug")
    print("  F2  - Toggle telemetry (ON/OFF)")
    print("  F12 - Submit general feedback")
    print("\n💡 About Telemetry:")
    print("  • Telemetry is 100% anonymous and optional")
    print("  • Helps us improve the game")
    print("  • Can be toggled ON/OFF anytime (F2)")
    print("\n🐛 Bug Reports:")
    print("  • Always saved (even if telemetry is OFF)")
    print("  • Help us fix problems faster")
    print("  • Include steps to reproduce")
    print("\n💬 General Feedback:")
    print("  • Tell us what you like/dislike")
    print("  • Suggest improvements")
    print("  • Help shape future updates")
    print("\n🔒 Privacy:")
    print("  • NO personal data collected")
    print("  • NO network passwords stored")
    print("  • Data stored locally on your computer")
    print("  • You can delete all data anytime")
    print("=" * 70)

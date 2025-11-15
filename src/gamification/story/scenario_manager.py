"""
Scenario manager - orchestrates scenario execution and progression.

Author: Juan-Dev + AI Architect - Soli Deo Gloria ✝️
Date: 2025-11-15
"""
from typing import Optional, List
from .scenario import Scenario, Quest, QuestObjective, ObjectiveStatus
from .progression import PlayerProgress, Badge
from .scenarios_library import ALL_SCENARIOS, get_scenario_by_id


class ScenarioManager:
    """
    Manages scenario execution, progression, and state.

    Responsibilities:
    - Load and track current scenario
    - Update quest progress
    - Award XP and badges
    - Handle scenario completion
    - Persist player progress
    """

    def __init__(self, player_progress: PlayerProgress):
        """
        Initialize scenario manager.

        Args:
            player_progress: Player progression state
        """
        self.player_progress = player_progress
        self.current_scenario: Optional[Scenario] = None
        self.available_scenarios = ALL_SCENARIOS.copy()

    def start_scenario(self, scenario_id: str) -> Scenario:
        """
        Start a scenario.

        Args:
            scenario_id: ID of scenario to start

        Returns:
            Started scenario

        Raises:
            ValueError: If scenario not found or already completed
        """
        scenario = get_scenario_by_id(scenario_id)

        # Check if already completed
        if scenario_id in self.player_progress.scenarios_completed:
            print(f"⚠️ Scenario '{scenario_id}' already completed. Replaying...")

        self.current_scenario = scenario
        scenario.start()

        print(f"🎬 Starting scenario: {scenario.name}")
        print(f"   Difficulty: {scenario.difficulty.name}")
        print(f"   Duration: {scenario.duration_minutes} minutes")

        return scenario

    def update_objective(self, objective_id: str, progress: int = 1) -> None:
        """
        Update a quest objective progress.

        Args:
            objective_id: Objective ID to update
            progress: Progress amount to add (default: 1)
        """
        if not self.current_scenario:
            print("⚠️ No active scenario")
            return

        # Find and update objective
        for quest in self.current_scenario.quests:
            for objective in quest.objectives:
                if objective.objective_id == objective_id:
                    old_status = objective.status
                    objective.update_progress(progress)

                    if objective.status == ObjectiveStatus.COMPLETED and old_status != ObjectiveStatus.COMPLETED:
                        print(f"✅ Objective completed: {objective.description}")
                        if objective.educational_tip:
                            print(f"   💡 {objective.educational_tip}")

                        # Check if quest is complete
                        self._check_quest_completion(quest)

                    return

        print(f"⚠️ Objective not found: {objective_id}")

    def _check_quest_completion(self, quest: Quest) -> None:
        """
        Check if quest is complete and award rewards.

        Args:
            quest: Quest to check
        """
        if not quest.is_complete():
            return

        if quest.status == ObjectiveStatus.COMPLETED:
            return  # Already processed

        quest.status = ObjectiveStatus.COMPLETED
        print(f"🎉 Quest completed: {quest.name}")

        # Award XP
        leveled_up = self.player_progress.add_xp(quest.xp_reward)
        print(f"   +{quest.xp_reward} XP")

        if leveled_up:
            print(f"   🆙 LEVEL UP! You are now level {self.player_progress.level}!")

        # Award badge
        if quest.badge_reward:
            self._award_badge(quest.badge_reward)

        # Increment quest counter
        self.player_progress.quests_completed += 1

        # Check if scenario is complete
        self._check_scenario_completion()

    def _award_badge(self, badge_id: str) -> None:
        """
        Award a badge to the player.

        Args:
            badge_id: Badge ID to award
        """
        # Import badge definitions
        from .progression import (
            BADGE_FIRST_EXPLORER,
            BADGE_SECURITY_DETECTIVE,
            BADGE_CRYPTO_DEFENDER,
            BADGE_NETWORK_GUARDIAN,
            BADGE_WIFI_MASTER
        )

        badge_map = {
            "first_explorer": BADGE_FIRST_EXPLORER,
            "security_detective": BADGE_SECURITY_DETECTIVE,
            "crypto_defender": BADGE_CRYPTO_DEFENDER,
            "network_guardian": BADGE_NETWORK_GUARDIAN,
            "wifi_master": BADGE_WIFI_MASTER,
        }

        badge = badge_map.get(badge_id)
        if not badge:
            print(f"⚠️ Badge not found: {badge_id}")
            return

        if self.player_progress.has_badge(badge_id):
            print(f"   Badge already earned: {badge.name}")
            return

        self.player_progress.earn_badge(badge)
        print(f"   🏅 Badge earned: {badge.name}")
        print(f"      {badge.description}")
        print(f"      Rarity: {badge.rarity.name}")

    def _check_scenario_completion(self) -> None:
        """Check if current scenario is complete."""
        if not self.current_scenario:
            return

        if not self.current_scenario.is_complete():
            return

        if self.current_scenario.status == ObjectiveStatus.COMPLETED:
            return  # Already processed

        self.current_scenario.complete()

        # Add to completed scenarios
        if self.current_scenario.scenario_id not in self.player_progress.scenarios_completed:
            self.player_progress.scenarios_completed.append(self.current_scenario.scenario_id)

        print(f"\n{'='*60}")
        print(f"🎊 SCENARIO COMPLETE: {self.current_scenario.name}")
        print(f"{'='*60}")
        print(f"Total XP earned: {self.current_scenario.get_total_xp()}")
        print(f"Completion: {self.current_scenario.get_progress_percent():.1f}%")
        print(f"\nScenarios completed: {len(self.player_progress.scenarios_completed)}/{len(ALL_SCENARIOS)}")

        # Show outro dialog
        if self.current_scenario.outro_dialog:
            print(f"\n--- Outro ---")
            for line in self.current_scenario.outro_dialog:
                print(f"📖 {line}")

        # Check for Network Guardian badge (all scenarios complete)
        if len(self.player_progress.scenarios_completed) == len(ALL_SCENARIOS):
            self._award_badge("network_guardian")

    def get_next_objective(self) -> Optional[QuestObjective]:
        """
        Get the next pending objective.

        Returns:
            Next objective or None if all complete
        """
        if not self.current_scenario:
            return None

        for quest in self.current_scenario.quests:
            for objective in quest.objectives:
                if objective.status != ObjectiveStatus.COMPLETED:
                    return objective

        return None

    def get_progress_summary(self) -> dict:
        """
        Get detailed progress summary.

        Returns:
            Progress summary dict
        """
        summary = self.player_progress.get_progress_summary()

        if self.current_scenario:
            summary['current_scenario'] = {
                'name': self.current_scenario.name,
                'progress': self.current_scenario.get_progress_percent(),
                'quests_complete': sum(1 for q in self.current_scenario.quests if q.is_complete()),
                'quests_total': len(self.current_scenario.quests),
            }

        return summary

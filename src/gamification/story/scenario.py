"""
Scenario system - educational scenarios with quests and objectives.

Author: Juan-Dev + AI Architect - Soli Deo Gloria ✝️
Date: 2025-11-15
"""
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Dict, Any, Optional, Callable


class ScenarioDifficulty(Enum):
    """Scenario difficulty levels."""
    BEGINNER = auto()
    INTERMEDIATE = auto()
    ADVANCED = auto()
    EXPERT = auto()


class ObjectiveStatus(Enum):
    """Quest objective status."""
    PENDING = auto()
    IN_PROGRESS = auto()
    COMPLETED = auto()
    FAILED = auto()


@dataclass
class QuestObjective:
    """A single quest objective."""
    objective_id: str
    description: str
    status: ObjectiveStatus = ObjectiveStatus.PENDING
    progress: int = 0
    target: int = 1
    educational_tip: Optional[str] = None

    def is_complete(self) -> bool:
        """Check if objective is complete."""
        return self.progress >= self.target or self.status == ObjectiveStatus.COMPLETED

    def update_progress(self, amount: int = 1) -> None:
        """Update objective progress."""
        self.progress += amount
        if self.progress >= self.target:
            self.status = ObjectiveStatus.COMPLETED


@dataclass
class Quest:
    """A quest with objectives."""
    quest_id: str
    name: str
    description: str
    objectives: List[QuestObjective] = field(default_factory=list)
    xp_reward: int = 100
    badge_reward: Optional[str] = None
    status: ObjectiveStatus = ObjectiveStatus.PENDING

    def is_complete(self) -> bool:
        """Check if all objectives are complete."""
        return all(obj.is_complete() for obj in self.objectives)

    def get_progress(self) -> tuple:
        """Get quest progress (completed, total)."""
        completed = sum(1 for obj in self.objectives if obj.is_complete())
        return (completed, len(self.objectives))


@dataclass
class Scenario:
    """An educational scenario with narrative and quests."""
    scenario_id: str
    name: str
    description: str
    difficulty: ScenarioDifficulty
    duration_minutes: int
    age_range: str

    # Learning objectives
    learning_objectives: List[str] = field(default_factory=list)

    # Narrative
    intro_dialog: List[str] = field(default_factory=list)
    outro_dialog: List[str] = field(default_factory=list)

    # Quests
    quests: List[Quest] = field(default_factory=list)

    # Progression
    status: ObjectiveStatus = ObjectiveStatus.PENDING
    completed_at: Optional[float] = None

    # Callbacks for dynamic behavior
    on_start: Optional[Callable] = None
    on_complete: Optional[Callable] = None
    on_objective_complete: Optional[Callable] = None

    def start(self) -> None:
        """Start the scenario."""
        self.status = ObjectiveStatus.IN_PROGRESS
        if self.on_start:
            self.on_start(self)

    def complete(self) -> None:
        """Complete the scenario."""
        import time
        self.status = ObjectiveStatus.COMPLETED
        self.completed_at = time.time()
        if self.on_complete:
            self.on_complete(self)

    def is_complete(self) -> bool:
        """Check if all quests are complete."""
        return all(quest.is_complete() for quest in self.quests)

    def get_total_xp(self) -> int:
        """Get total XP reward."""
        return sum(quest.xp_reward for quest in self.quests)

    def get_progress_percent(self) -> float:
        """Get overall completion percentage."""
        if not self.quests:
            return 0.0

        total_objectives = sum(len(quest.objectives) for quest in self.quests)
        completed_objectives = sum(
            sum(1 for obj in quest.objectives if obj.is_complete())
            for quest in self.quests
        )

        if total_objectives == 0:
            return 0.0

        return (completed_objectives / total_objectives) * 100

"""
Player progression system - XP, levels, badges, achievements.

Author: Juan-Dev + AI Architect - Soli Deo Gloria ✝️
Date: 2025-11-15
"""
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum, auto


class BadgeRarity(Enum):
    """Badge rarity levels."""
    COMMON = auto()
    UNCOMMON = auto()
    RARE = auto()
    EPIC = auto()
    LEGENDARY = auto()


@dataclass
class Badge:
    """A badge/achievement earned by the player."""
    badge_id: str
    name: str
    description: str
    rarity: BadgeRarity
    icon: Optional[str] = None
    earned_at: Optional[float] = None

    def is_earned(self) -> bool:
        """Check if badge has been earned."""
        return self.earned_at is not None


@dataclass
class PlayerProgress:
    """Player progression state."""
    # XP and levels
    total_xp: int = 0
    level: int = 1
    xp_to_next_level: int = 100

    # Badges and achievements
    badges_earned: List[Badge] = field(default_factory=list)
    scenarios_completed: List[str] = field(default_factory=list)

    # Statistics
    total_playtime_seconds: float = 0.0
    quests_completed: int = 0
    threats_detected: int = 0
    concepts_learned: int = 0

    def add_xp(self, amount: int) -> bool:
        """
        Add XP and check for level up.

        Args:
            amount: XP to add

        Returns:
            True if leveled up, False otherwise
        """
        self.total_xp += amount
        leveled_up = False

        while self.total_xp >= self.xp_to_next_level:
            self.total_xp -= self.xp_to_next_level
            self.level += 1
            self.xp_to_next_level = self._calculate_xp_for_next_level()
            leveled_up = True

        return leveled_up

    def _calculate_xp_for_next_level(self) -> int:
        """Calculate XP required for next level (exponential curve)."""
        base_xp = 100
        growth_rate = 1.5
        return int(base_xp * (growth_rate ** (self.level - 1)))

    def earn_badge(self, badge: Badge) -> None:
        """
        Earn a badge.

        Args:
            badge: Badge to earn
        """
        import time
        if badge not in self.badges_earned:
            badge.earned_at = time.time()
            self.badges_earned.append(badge)

    def has_badge(self, badge_id: str) -> bool:
        """
        Check if player has a specific badge.

        Args:
            badge_id: Badge ID to check

        Returns:
            True if badge is earned, False otherwise
        """
        return any(badge.badge_id == badge_id for badge in self.badges_earned)

    def get_progress_summary(self) -> Dict:
        """Get progress summary for display."""
        return {
            'level': self.level,
            'total_xp': self.total_xp,
            'xp_to_next_level': self.xp_to_next_level,
            'xp_progress_percent': (self.total_xp / self.xp_to_next_level) * 100,
            'badges_earned': len(self.badges_earned),
            'scenarios_completed': len(self.scenarios_completed),
            'quests_completed': self.quests_completed,
            'playtime_hours': self.total_playtime_seconds / 3600,
        }


# Predefined badges
BADGE_FIRST_EXPLORER = Badge(
    badge_id="first_explorer",
    name="First Explorer",
    description="Complete your first scenario",
    rarity=BadgeRarity.COMMON
)

BADGE_SECURITY_DETECTIVE = Badge(
    badge_id="security_detective",
    name="Security Detective",
    description="Identify a rogue AP",
    rarity=BadgeRarity.UNCOMMON
)

BADGE_CRYPTO_DEFENDER = Badge(
    badge_id="crypto_defender",
    name="Crypto Defender",
    description="Identify 5 insecure connections",
    rarity=BadgeRarity.RARE
)

BADGE_NETWORK_GUARDIAN = Badge(
    badge_id="network_guardian",
    name="Network Guardian",
    description="Complete all scenarios",
    rarity=BadgeRarity.EPIC
)

BADGE_WIFI_MASTER = Badge(
    badge_id="wifi_master",
    name="WiFi Master",
    description="Reach level 10",
    rarity=BadgeRarity.LEGENDARY
)

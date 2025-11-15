"""
Library of predefined educational scenarios.
Each scenario teaches specific WiFi security concepts.

Author: Juan-Dev + AI Architect - Soli Deo Gloria ✝️
Date: 2025-11-15
"""

from .scenario import Scenario, Quest, QuestObjective, ScenarioDifficulty


def create_scenario_1_first_day_online() -> Scenario:
    """
    Scenario 1: "First Day Online"

    Difficulty: Beginner
    Duration: 10 minutes
    Age: 7-12 years

    Learning Objectives:
    - What is WiFi?
    - How to identify your network (SSID)
    - What signal strength means
    """
    # Quest: Network Explorer
    quest = Quest(
        quest_id="network_explorer",
        name="Network Explorer",
        description="Discover 3 devices on your network",
        xp_reward=100,
        badge_reward="first_explorer",
        objectives=[
            QuestObjective(
                objective_id="observe_guardian",
                description="Observe the Guardian's health",
                target=1,
                educational_tip="The Guardian's health shows WiFi signal strength!",
            ),
            QuestObjective(
                objective_id="identify_ssid",
                description="Learn your network name (SSID)",
                target=1,
                educational_tip="SSID is like your WiFi's name tag - it identifies your network.",
            ),
            QuestObjective(
                objective_id="understand_signal",
                description="Understand signal strength categories",
                target=1,
                educational_tip="Strong signal (above -50 dBm) = healthy Guardian!",
            ),
        ],
    )

    scenario = Scenario(
        scenario_id="first_day_online",
        name="First Day Online",
        description="Welcome to the WiFi Kingdom! Learn the basics of WiFi networks.",
        difficulty=ScenarioDifficulty.BEGINNER,
        duration_minutes=10,
        age_range="7-12 years",
        learning_objectives=[
            "What is WiFi?",
            "How to identify your network (SSID)",
            "What signal strength means",
            "Meet the Guardian (your router)",
        ],
        intro_dialog=[
            "Welcome to the WiFi Kingdom! I'm Professor Packet, your guide.",
            "Today you'll meet the Guardian - they protect our kingdom.",
            "The Guardian's health shows how strong your WiFi signal is.",
            "Let's explore the kingdom together!",
        ],
        outro_dialog=[
            "Excellent work, young explorer!",
            "You've learned the basics of WiFi networks.",
            "The Guardian is proud of you!",
            "Ready for your next adventure?",
        ],
        quests=[quest],
    )

    return scenario


def create_scenario_2_the_impostor() -> Scenario:
    """
    Scenario 2: "The Impostor"

    Difficulty: Intermediate
    Duration: 15 minutes
    Age: 9-14 years

    Learning Objectives:
    - What are Rogue Access Points (Evil Twins)
    - How to identify fake WiFi networks
    - Dangers of connecting to unknown networks
    """
    quest = Quest(
        quest_id="impostor_hunter",
        name="Impostor Hunter",
        description="Identify and avoid the Rogue AP",
        xp_reward=250,
        badge_reward="security_detective",
        objectives=[
            QuestObjective(
                objective_id="detect_rogue_ap",
                description="Detect the impostor network",
                target=1,
                educational_tip=(
                    "Rogue APs pretend to be your real network. Always check carefully!"
                ),
            ),
            QuestObjective(
                objective_id="learn_evil_twin",
                description="Learn about Evil Twin attacks",
                target=1,
                educational_tip=(
                    "Evil Twins copy your network name to trick you. Very dangerous!"
                ),
            ),
            QuestObjective(
                objective_id="avoid_connection",
                description="Don't connect to the fake network",
                target=1,
                educational_tip=(
                    "Never connect to networks you don't recognize, "
                    "even if they look familiar."
                ),
            ),
        ],
    )

    scenario = Scenario(
        scenario_id="the_impostor",
        name="The Impostor",
        description="A fake WiFi network appears! Can you spot the impostor?",
        difficulty=ScenarioDifficulty.INTERMEDIATE,
        duration_minutes=15,
        age_range="9-14 years",
        learning_objectives=[
            "What are Rogue Access Points?",
            "How to identify fake WiFi",
            "Dangers of unknown networks",
            "Evil Twin attack explained",
        ],
        intro_dialog=[
            "⚠️ Alert! The Guardian detects something suspicious!",
            "There's a new WiFi network that looks just like ours...",
            "But it's not ours! It's an IMPOSTOR trying to trick us!",
            "This is called an 'Evil Twin' attack. Very dangerous!",
            "Help the Guardian identify and avoid this threat!",
        ],
        outro_dialog=[
            "🎉 Excellent detective work!",
            "You successfully identified the Rogue AP!",
            "Evil Twins are one of the most common WiFi attacks.",
            "Always double-check network names before connecting!",
            "The Guardian is grateful for your vigilance!",
        ],
        quests=[quest],
    )

    return scenario


def create_scenario_3_invisible_listener() -> Scenario:
    """
    Scenario 3: "Invisible Listener"

    Difficulty: Intermediate
    Duration: 15 minutes
    Age: 10-16 years

    Learning Objectives:
    - Difference between HTTP and HTTPS
    - What is packet sniffing?
    - Why encryption matters
    """
    quest = Quest(
        quest_id="encryption_guardian",
        name="Encryption Guardian",
        description="Identify 5 insecure connections (HTTP)",
        xp_reward=300,
        badge_reward="crypto_defender",
        objectives=[
            QuestObjective(
                objective_id="detect_sniffer",
                description="Detect the Eavesdropper (packet sniffer)",
                target=1,
                educational_tip="Packet sniffers can read unencrypted data flying through the air!",
            ),
            QuestObjective(
                objective_id="identify_http",
                description="Identify 5 insecure HTTP connections",
                target=5,
                educational_tip="HTTP = Open letter. HTTPS = Sealed envelope with lock!",
            ),
            QuestObjective(
                objective_id="learn_encryption",
                description="Learn why HTTPS is important",
                target=1,
                educational_tip="Always look for the padlock 🔒 in your browser. That's HTTPS!",
            ),
        ],
    )

    scenario = Scenario(
        scenario_id="invisible_listener",
        name="Invisible Listener",
        description="An eavesdropper is watching! Learn about encryption.",
        difficulty=ScenarioDifficulty.INTERMEDIATE,
        duration_minutes=15,
        age_range="10-16 years",
        learning_objectives=[
            "HTTP vs HTTPS difference",
            "What is packet sniffing?",
            "Why encryption protects you",
            "How to spot secure connections",
        ],
        intro_dialog=[
            "👀 Something strange is happening...",
            "The Guardian sees someone watching our network traffic!",
            "It's the Eavesdropper - they can see unencrypted data!",
            "Watch how packets travel: HTTP (open) vs HTTPS (sealed)",
            "Let's learn to spot insecure connections!",
        ],
        outro_dialog=[
            "🛡️ Amazing work, Crypto Defender!",
            "You've learned the difference between HTTP and HTTPS!",
            "Remember: Always look for HTTPS and the padlock 🔒",
            "Encrypted data = Safe data. The Eavesdropper can't read it!",
            "You're becoming a true network security expert!",
        ],
        quests=[quest],
    )

    return scenario


# Library of all scenarios
ALL_SCENARIOS = [
    create_scenario_1_first_day_online(),
    create_scenario_2_the_impostor(),
    create_scenario_3_invisible_listener(),
]


def get_scenario_by_id(scenario_id: str) -> Scenario:
    """
    Get scenario by ID.

    Args:
        scenario_id: Scenario ID

    Returns:
        Scenario instance

    Raises:
        ValueError: If scenario not found
    """
    for scenario in ALL_SCENARIOS:
        if scenario.scenario_id == scenario_id:
            return scenario
    raise ValueError(f"Scenario not found: {scenario_id}")

#!/usr/bin/env python3
"""
Shadowlands RPG - Dynamic Quest Generation and Narrative System
Advanced algorithms for character-driven quest creation and narrative branching
"""

import random
import uuid
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
import json

# Import the core quest engine
from quest_engine_core import (
    QuestTemplate, QuestType, QuestComplexity, ObjectiveType, 
    ChoiceConsequenceType, QuestEngine
)

class NarrativeTheme(Enum):
    """Narrative themes for dynamic quest generation"""
    CORRUPTION = "corruption"           # Dark magic, tainted lands, moral decay
    DISCOVERY = "discovery"             # Ancient secrets, lost knowledge, exploration
    BETRAYAL = "betrayal"              # Trust broken, allies turned enemies
    REDEMPTION = "redemption"          # Second chances, making amends, healing
    SACRIFICE = "sacrifice"            # Noble loss, difficult choices, greater good
    POWER = "power"                    # Ambition, control, dominance
    MYSTERY = "mystery"                # Puzzles, hidden truths, investigation
    REVENGE = "revenge"                # Justice, retribution, settling scores
    PROTECTION = "protection"          # Defending others, safeguarding values
    TRANSFORMATION = "transformation"   # Change, growth, evolution

class CharacterArchetype(Enum):
    """Character archetypes that influence quest generation"""
    WARRIOR = "warrior"                # Might-focused, direct action, combat solutions
    SCHOLAR = "scholar"                # Intellect-focused, knowledge seeking, research
    MYSTIC = "mystic"                  # Will-focused, spiritual, magical solutions
    SHADOW_WALKER = "shadow_walker"    # Shadow-focused, stealth, manipulation
    BALANCED = "balanced"              # No dominant attribute, versatile approach

class QuestTrigger(Enum):
    """Types of triggers that can generate dynamic quests"""
    CHARACTER_CHOICE = "character_choice"       # Based on previous decisions
    LOCATION_DISCOVERY = "location_discovery"   # Triggered by exploring areas
    NPC_INTERACTION = "npc_interaction"        # Initiated by character encounters
    ITEM_ACQUISITION = "item_acquisition"      # Triggered by finding items
    FACTION_STANDING = "faction_standing"      # Based on reputation changes
    TIME_BASED = "time_based"                  # Scheduled or timed events
    RANDOM_ENCOUNTER = "random_encounter"      # Procedural generation
    STORY_PROGRESSION = "story_progression"    # Main narrative advancement

@dataclass
class NarrativeContext:
    """Tracks character narrative progression and context"""
    character_id: str
    character_archetype: CharacterArchetype
    moral_alignment: Dict[str, float] = field(default_factory=lambda: {
        "order_chaos": 0.0,      # -1.0 (chaos) to 1.0 (order)
        "good_evil": 0.0,        # -1.0 (evil) to 1.0 (good)
        "selfless_selfish": 0.0  # -1.0 (selfish) to 1.0 (selfless)
    })
    choice_history: List[Dict[str, Any]] = field(default_factory=list)
    faction_standings: Dict[str, int] = field(default_factory=dict)
    completed_themes: List[NarrativeTheme] = field(default_factory=list)
    theme_affinity: Dict[NarrativeTheme, float] = field(default_factory=dict)
    narrative_flags: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Initialize theme affinity based on character archetype"""
        if not self.theme_affinity:
            self.theme_affinity = self._calculate_initial_theme_affinity()
    
    def _calculate_initial_theme_affinity(self) -> Dict[NarrativeTheme, float]:
        """Calculate initial theme preferences based on character archetype"""
        base_affinity = {theme: 0.5 for theme in NarrativeTheme}
        
        # Archetype-specific theme preferences
        archetype_preferences = {
            CharacterArchetype.WARRIOR: {
                NarrativeTheme.PROTECTION: 0.8,
                NarrativeTheme.SACRIFICE: 0.7,
                NarrativeTheme.POWER: 0.6,
                NarrativeTheme.CORRUPTION: 0.3,
                NarrativeTheme.MYSTERY: 0.4
            },
            CharacterArchetype.SCHOLAR: {
                NarrativeTheme.DISCOVERY: 0.9,
                NarrativeTheme.MYSTERY: 0.8,
                NarrativeTheme.TRANSFORMATION: 0.6,
                NarrativeTheme.POWER: 0.4,
                NarrativeTheme.SACRIFICE: 0.3
            },
            CharacterArchetype.MYSTIC: {
                NarrativeTheme.TRANSFORMATION: 0.8,
                NarrativeTheme.REDEMPTION: 0.7,
                NarrativeTheme.CORRUPTION: 0.6,
                NarrativeTheme.DISCOVERY: 0.6,
                NarrativeTheme.BETRAYAL: 0.3
            },
            CharacterArchetype.SHADOW_WALKER: {
                NarrativeTheme.BETRAYAL: 0.8,
                NarrativeTheme.REVENGE: 0.7,
                NarrativeTheme.MYSTERY: 0.7,
                NarrativeTheme.CORRUPTION: 0.6,
                NarrativeTheme.PROTECTION: 0.2
            },
            CharacterArchetype.BALANCED: {
                # Balanced characters have moderate affinity for all themes
                theme: 0.5 for theme in NarrativeTheme
            }
        }
        
        # Apply archetype preferences
        preferences = archetype_preferences.get(self.character_archetype, {})
        for theme, preference in preferences.items():
            base_affinity[theme] = preference
        
        return base_affinity
    
    def update_theme_affinity(self, theme: NarrativeTheme, change: float):
        """Update theme affinity based on quest completion or choices"""
        current = self.theme_affinity.get(theme, 0.5)
        # Clamp between 0.0 and 1.0
        self.theme_affinity[theme] = max(0.0, min(1.0, current + change))
    
    def add_choice_to_history(self, quest_id: str, choice_description: str, 
                             consequences: List[Dict[str, Any]], theme: NarrativeTheme):
        """Add a choice to the character's narrative history"""
        choice_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "quest_id": quest_id,
            "choice": choice_description,
            "consequences": consequences,
            "theme": theme.value,
            "moral_impact": self._calculate_moral_impact(consequences)
        }
        self.choice_history.append(choice_record)
        
        # Update moral alignment based on choice
        moral_impact = choice_record["moral_impact"]
        for axis, change in moral_impact.items():
            if axis in self.moral_alignment:
                current = self.moral_alignment[axis]
                self.moral_alignment[axis] = max(-1.0, min(1.0, current + change))
    
    def _calculate_moral_impact(self, consequences: List[Dict[str, Any]]) -> Dict[str, float]:
        """Calculate moral alignment impact from choice consequences"""
        impact = {"order_chaos": 0.0, "good_evil": 0.0, "selfless_selfish": 0.0}
        
        for consequence in consequences:
            action = consequence.get("action", "")
            
            # Analyze consequence type for moral impact
            if "help" in action.lower() or "protect" in action.lower():
                impact["good_evil"] += 0.1
                impact["selfless_selfish"] += 0.1
            elif "harm" in action.lower() or "destroy" in action.lower():
                impact["good_evil"] -= 0.1
                impact["selfless_selfish"] -= 0.05
            
            if "law" in action.lower() or "order" in action.lower():
                impact["order_chaos"] += 0.1
            elif "chaos" in action.lower() or "rebel" in action.lower():
                impact["order_chaos"] -= 0.1
        
        return impact

class DynamicQuestGenerator:
    """Advanced quest generation system with character-driven adaptation"""
    
    def __init__(self, quest_engine: QuestEngine):
        self.quest_engine = quest_engine
        self.narrative_contexts: Dict[str, NarrativeContext] = {}
        
        # Theme-based quest generation templates
        self.theme_templates = self._initialize_theme_templates()
        
        # Location-based quest triggers
        self.location_triggers = self._initialize_location_triggers()
        
        # Character archetype quest modifications
        self.archetype_modifiers = self._initialize_archetype_modifiers()
    
    def get_or_create_narrative_context(self, character_data: Dict[str, Any]) -> NarrativeContext:
        """Get existing narrative context or create new one for character"""
        character_id = character_data.get("character_id")
        
        if character_id not in self.narrative_contexts:
            # Determine character archetype from attributes
            archetype = self._determine_character_archetype(character_data)
            
            self.narrative_contexts[character_id] = NarrativeContext(
                character_id=character_id,
                character_archetype=archetype
            )
        
        return self.narrative_contexts[character_id]
    
    def _determine_character_archetype(self, character_data: Dict[str, Any]) -> CharacterArchetype:
        """Determine character archetype based on attributes"""
        attributes = character_data.get("attributes", {})
        might = attributes.get("might", 10)
        intellect = attributes.get("intellect", 10)
        will = attributes.get("will", 10)
        shadow = attributes.get("shadow", 10)
        
        # Find dominant attribute
        attr_values = {"might": might, "intellect": intellect, "will": will, "shadow": shadow}
        max_attr = max(attr_values, key=attr_values.get)
        max_value = attr_values[max_attr]
        
        # Check if there's a clear dominant attribute (at least 2 points higher)
        other_values = [v for k, v in attr_values.items() if k != max_attr]
        if max_value - max(other_values) >= 2:
            archetype_map = {
                "might": CharacterArchetype.WARRIOR,
                "intellect": CharacterArchetype.SCHOLAR,
                "will": CharacterArchetype.MYSTIC,
                "shadow": CharacterArchetype.SHADOW_WALKER
            }
            return archetype_map[max_attr]
        else:
            return CharacterArchetype.BALANCED
    
    def generate_dynamic_quest(self, character_data: Dict[str, Any], 
                              trigger: QuestTrigger = QuestTrigger.RANDOM_ENCOUNTER,
                              location_context: Optional[str] = None) -> Optional[QuestTemplate]:
        """Generate a dynamic quest based on character context and trigger"""
        
        # Get character narrative context
        narrative_context = self.get_or_create_narrative_context(character_data)
        
        # Select appropriate theme based on character affinity and context
        selected_theme = self._select_theme_for_character(narrative_context, trigger)
        
        # Generate quest template based on theme and character
        quest_template = self._generate_quest_from_theme(
            selected_theme, narrative_context, character_data, location_context
        )
        
        # Apply character archetype modifications
        if quest_template:
            quest_template = self._apply_archetype_modifications(
                quest_template, narrative_context.character_archetype
            )
        
        return quest_template
    
    def _select_theme_for_character(self, narrative_context: NarrativeContext, 
                                   trigger: QuestTrigger) -> NarrativeTheme:
        """Select narrative theme based on character affinity and trigger context"""
        
        # Get theme affinities
        affinities = narrative_context.theme_affinity.copy()
        
        # Reduce affinity for recently completed themes to encourage variety
        for completed_theme in narrative_context.completed_themes[-3:]:  # Last 3 themes
            if completed_theme in affinities:
                affinities[completed_theme] *= 0.7
        
        # Trigger-specific theme preferences
        trigger_preferences = {
            QuestTrigger.CHARACTER_CHOICE: [NarrativeTheme.BETRAYAL, NarrativeTheme.REDEMPTION],
            QuestTrigger.LOCATION_DISCOVERY: [NarrativeTheme.DISCOVERY, NarrativeTheme.MYSTERY],
            QuestTrigger.NPC_INTERACTION: [NarrativeTheme.PROTECTION, NarrativeTheme.BETRAYAL],
            QuestTrigger.FACTION_STANDING: [NarrativeTheme.POWER, NarrativeTheme.SACRIFICE],
            QuestTrigger.RANDOM_ENCOUNTER: list(NarrativeTheme)  # Any theme
        }
        
        # Filter themes based on trigger
        eligible_themes = trigger_preferences.get(trigger, list(NarrativeTheme))
        
        # Create weighted selection based on affinities
        weights = []
        themes = []
        for theme in eligible_themes:
            if theme in affinities:
                themes.append(theme)
                weights.append(affinities[theme])
        
        # Weighted random selection
        if themes and weights:
            return random.choices(themes, weights=weights)[0]
        else:
            return random.choice(list(NarrativeTheme))
    
    def _generate_quest_from_theme(self, theme: NarrativeTheme, 
                                  narrative_context: NarrativeContext,
                                  character_data: Dict[str, Any],
                                  location_context: Optional[str] = None) -> QuestTemplate:
        """Generate a quest template based on the selected theme"""
        
        # Get theme template
        theme_template = self.theme_templates.get(theme, {})
        
        # Generate unique quest ID
        template_id = f"dynamic_{theme.value}_{str(uuid.uuid4())[:8]}"
        
        # Determine quest complexity based on character level
        character_level = character_data.get("level", 1)
        if character_level >= 5:
            complexity = QuestComplexity.EPIC
        elif character_level >= 3:
            complexity = QuestComplexity.STANDARD
        else:
            complexity = QuestComplexity.QUICK
        
        # Create quest template
        quest_template = QuestTemplate(template_id, QuestType.DYNAMIC_GENERATED, complexity)
        
        # Generate contextual title and description
        quest_template.title = self._generate_contextual_title(theme, narrative_context, location_context)
        quest_template.description = self._generate_contextual_description(theme, narrative_context, character_data)
        
        # Generate objectives based on theme
        quest_template.objectives_templates = self._generate_theme_objectives(theme, complexity)
        
        # Generate choices based on theme and character archetype
        quest_template.choices_templates = self._generate_theme_choices(theme, narrative_context.character_archetype)
        
        # Generate appropriate rewards
        quest_template.rewards_templates = self._generate_theme_rewards(theme, complexity, character_level)
        
        return quest_template


    
    def _generate_contextual_title(self, theme: NarrativeTheme, 
                                  narrative_context: NarrativeContext,
                                  location_context: Optional[str] = None) -> str:
        """Generate a contextual quest title based on theme and character"""
        
        archetype = narrative_context.character_archetype
        
        # Theme-based title templates with archetype variations
        title_templates = {
            NarrativeTheme.CORRUPTION: {
                CharacterArchetype.WARRIOR: ["Cleansing the Tainted Lands", "Battle Against Corruption", "Purging the Darkness"],
                CharacterArchetype.SCHOLAR: ["Studying the Source of Corruption", "Research into Dark Magic", "Understanding the Taint"],
                CharacterArchetype.MYSTIC: ["Healing the Corrupted Spirits", "Spiritual Cleansing Ritual", "Restoring Sacred Balance"],
                CharacterArchetype.SHADOW_WALKER: ["Infiltrating Corrupt Networks", "Shadow Investigation", "Corruption from Within"],
                CharacterArchetype.BALANCED: ["Confronting the Corruption", "Dealing with Dark Forces", "Corruption's Challenge"]
            },
            NarrativeTheme.DISCOVERY: {
                CharacterArchetype.WARRIOR: ["Uncovering Ancient Battlegrounds", "Lost Warrior's Legacy", "Forgotten Military Secrets"],
                CharacterArchetype.SCHOLAR: ["Archaeological Expedition", "Lost Knowledge Recovery", "Ancient Texts Discovery"],
                CharacterArchetype.MYSTIC: ["Mystical Revelation Quest", "Spiritual Discovery Journey", "Sacred Knowledge Unveiled"],
                CharacterArchetype.SHADOW_WALKER: ["Hidden Secrets Investigation", "Covert Discovery Mission", "Uncovering Hidden Truths"],
                CharacterArchetype.BALANCED: ["Journey of Discovery", "Uncovering the Past", "Lost Secrets Found"]
            },
            NarrativeTheme.BETRAYAL: {
                CharacterArchetype.WARRIOR: ["Honor Betrayed", "Fallen Comrade's Truth", "Loyalty Tested"],
                CharacterArchetype.SCHOLAR: ["Academic Conspiracy", "Betrayal of Trust", "False Knowledge Exposed"],
                CharacterArchetype.MYSTIC: ["Spiritual Betrayal", "Sacred Trust Broken", "Divine Deception"],
                CharacterArchetype.SHADOW_WALKER: ["Double Agent Revealed", "Betrayal in the Shadows", "Trust No One"],
                CharacterArchetype.BALANCED: ["Broken Trust", "Betrayal Uncovered", "False Friends"]
            },
            NarrativeTheme.REDEMPTION: {
                CharacterArchetype.WARRIOR: ["Path to Honor", "Warrior's Redemption", "Second Chance at Glory"],
                CharacterArchetype.SCHOLAR: ["Knowledge Redeemed", "Academic Atonement", "Wisdom Through Failure"],
                CharacterArchetype.MYSTIC: ["Spiritual Redemption", "Soul's Second Chance", "Divine Forgiveness"],
                CharacterArchetype.SHADOW_WALKER: ["Emerging from Shadows", "Redemption in Darkness", "Light After Shadow"],
                CharacterArchetype.BALANCED: ["Second Chances", "Path to Redemption", "Making Amends"]
            },
            NarrativeTheme.MYSTERY: {
                CharacterArchetype.WARRIOR: ["The Warrior's Riddle", "Military Mystery", "Battle's Hidden Truth"],
                CharacterArchetype.SCHOLAR: ["Academic Enigma", "Scholarly Investigation", "Intellectual Puzzle"],
                CharacterArchetype.MYSTIC: ["Mystical Mystery", "Spiritual Enigma", "Divine Puzzle"],
                CharacterArchetype.SHADOW_WALKER: ["Shadow Investigation", "Hidden Truth Quest", "Covert Mystery"],
                CharacterArchetype.BALANCED: ["Unsolved Mystery", "Hidden Truth", "Enigmatic Quest"]
            }
        }
        
        # Get appropriate titles for theme and archetype
        theme_titles = title_templates.get(theme, {})
        archetype_titles = theme_titles.get(archetype, ["Dynamic Quest", "Adventure Awaits", "New Challenge"])
        
        # Select random title from appropriate list
        base_title = random.choice(archetype_titles)
        
        # Add location context if provided
        if location_context:
            base_title += f" in {location_context}"
        
        return base_title
    
    def _generate_contextual_description(self, theme: NarrativeTheme, 
                                        narrative_context: NarrativeContext,
                                        character_data: Dict[str, Any]) -> str:
        """Generate contextual quest description"""
        
        character_name = character_data.get("name", "Drifter")
        archetype = narrative_context.character_archetype
        
        # Theme-based description templates
        description_templates = {
            NarrativeTheme.CORRUPTION: f"Dark forces have begun to spread their influence across the land. As a {archetype.value}, {character_name} must confront this growing threat before it consumes everything in its path.",
            
            NarrativeTheme.DISCOVERY: f"Ancient secrets lie hidden, waiting to be uncovered. {character_name}'s {archetype.value} nature makes them uniquely suited to unravel these mysteries and bring lost knowledge to light.",
            
            NarrativeTheme.BETRAYAL: f"Trust has been shattered, and {character_name} must navigate a web of deception. Their {archetype.value} perspective will be crucial in determining who can truly be trusted.",
            
            NarrativeTheme.REDEMPTION: f"Past mistakes cast long shadows, but redemption is possible. {character_name} has the opportunity to make amends and forge a new path forward.",
            
            NarrativeTheme.MYSTERY: f"Strange events have been occurring, and answers are needed. {character_name}'s {archetype.value} approach may be the key to solving this enigmatic puzzle."
        }
        
        return description_templates.get(theme, f"{character_name} faces a new challenge that will test their resolve and {archetype.value} nature.")
    
    def _generate_theme_objectives(self, theme: NarrativeTheme, complexity: QuestComplexity) -> List[Dict[str, Any]]:
        """Generate objectives based on theme and complexity"""
        
        # Base objectives per theme
        theme_objectives = {
            NarrativeTheme.CORRUPTION: [
                {"type": "reach_location", "description": "Investigate the source of corruption", "target_value": 1, "metadata": {"location": "corruption_source"}},
                {"type": "collect_item", "description": "Gather corrupted samples for analysis", "target_value": 3, "metadata": {"item_type": "corrupted_sample"}},
                {"type": "kill_target", "description": "Eliminate corrupted creatures", "target_value": 5, "metadata": {"enemy_type": "corrupted"}}
            ],
            NarrativeTheme.DISCOVERY: [
                {"type": "reach_location", "description": "Explore the ancient site", "target_value": 1, "metadata": {"location": "ancient_ruins"}},
                {"type": "solve_puzzle", "description": "Decipher ancient inscriptions", "target_value": 1, "metadata": {"puzzle_type": "ancient_text"}},
                {"type": "collect_item", "description": "Recover lost artifacts", "target_value": 2, "metadata": {"item_type": "ancient_artifact"}}
            ],
            NarrativeTheme.BETRAYAL: [
                {"type": "interact_npc", "description": "Confront the suspected traitor", "target_value": 1, "metadata": {"npc_id": "suspected_traitor"}},
                {"type": "collect_item", "description": "Gather evidence of betrayal", "target_value": 3, "metadata": {"item_type": "evidence"}},
                {"type": "make_choice", "description": "Decide the traitor's fate", "target_value": 1, "metadata": {"choice_type": "justice"}}
            ],
            NarrativeTheme.REDEMPTION: [
                {"type": "interact_npc", "description": "Seek forgiveness from those wronged", "target_value": 2, "metadata": {"npc_type": "wronged_party"}},
                {"type": "collect_item", "description": "Make restitution for past wrongs", "target_value": 1, "metadata": {"item_type": "restitution"}},
                {"type": "reach_location", "description": "Visit the site of past mistakes", "target_value": 1, "metadata": {"location": "mistake_site"}}
            ],
            NarrativeTheme.MYSTERY: [
                {"type": "collect_item", "description": "Gather clues about the mystery", "target_value": 4, "metadata": {"item_type": "clue"}},
                {"type": "interact_npc", "description": "Interview witnesses", "target_value": 3, "metadata": {"npc_type": "witness"}},
                {"type": "solve_puzzle", "description": "Piece together the evidence", "target_value": 1, "metadata": {"puzzle_type": "deduction"}}
            ]
        }
        
        base_objectives = theme_objectives.get(theme, [
            {"type": "reach_location", "description": "Complete the quest objective", "target_value": 1, "metadata": {}}
        ])
        
        # Adjust objectives based on complexity
        if complexity == QuestComplexity.QUICK:
            return base_objectives[:2]  # Fewer objectives for quick quests
        elif complexity == QuestComplexity.EPIC:
            # Add additional objectives for epic quests
            additional_objectives = [
                {"type": "survive_time", "description": "Endure the challenges ahead", "target_value": 300, "metadata": {"duration": 300}}
            ]
            return base_objectives + additional_objectives
        else:
            return base_objectives
    
    def _generate_theme_choices(self, theme: NarrativeTheme, archetype: CharacterArchetype) -> List[Dict[str, Any]]:
        """Generate choices based on theme and character archetype"""
        
        # Theme-based choice templates
        theme_choices = {
            NarrativeTheme.CORRUPTION: [
                {
                    "description": "Purge the corruption with force",
                    "consequences": [
                        {"type": "immediate", "action": "add_objective", "objective_type": "kill_target", "description": "Destroy corrupted entities", "target_value": 3}
                    ]
                },
                {
                    "description": "Study the corruption to understand it",
                    "consequences": [
                        {"type": "intermediate", "action": "reputation_change", "faction": "scholars", "value": 10},
                        {"type": "immediate", "action": "add_objective", "objective_type": "collect_item", "description": "Gather research samples", "target_value": 5}
                    ]
                }
            ],
            NarrativeTheme.BETRAYAL: [
                {
                    "description": "Confront the betrayer directly",
                    "consequences": [
                        {"type": "immediate", "action": "moral_alignment", "axis": "order_chaos", "value": 0.1}
                    ]
                },
                {
                    "description": "Gather more evidence before acting",
                    "consequences": [
                        {"type": "intermediate", "action": "add_objective", "objective_type": "collect_item", "description": "Find additional proof", "target_value": 2}
                    ]
                }
            ],
            NarrativeTheme.REDEMPTION: [
                {
                    "description": "Accept full responsibility for past actions",
                    "consequences": [
                        {"type": "immediate", "action": "moral_alignment", "axis": "good_evil", "value": 0.2}
                    ]
                },
                {
                    "description": "Seek to make practical amends",
                    "consequences": [
                        {"type": "immediate", "action": "add_objective", "objective_type": "collect_item", "description": "Provide restitution", "target_value": 1}
                    ]
                }
            ]
        }
        
        return theme_choices.get(theme, [])
    
    def _generate_theme_rewards(self, theme: NarrativeTheme, complexity: QuestComplexity, character_level: int) -> List[Dict[str, Any]]:
        """Generate appropriate rewards based on theme and complexity"""
        
        # Base experience based on complexity and level
        base_exp = {
            QuestComplexity.QUICK: 100 * character_level,
            QuestComplexity.STANDARD: 200 * character_level,
            QuestComplexity.EPIC: 400 * character_level
        }
        
        experience_reward = {
            "type": "experience",
            "value": base_exp.get(complexity, 100),
            "description": "Quest completion experience"
        }
        
        # Theme-specific rewards
        theme_rewards = {
            NarrativeTheme.CORRUPTION: {
                "type": "item",
                "value": "purification_charm",
                "description": "Charm that protects against corruption"
            },
            NarrativeTheme.DISCOVERY: {
                "type": "item",
                "value": "ancient_knowledge",
                "description": "Ancient knowledge that enhances understanding"
            },
            NarrativeTheme.BETRAYAL: {
                "type": "skill",
                "value": "insight",
                "description": "Enhanced ability to detect deception"
            },
            NarrativeTheme.REDEMPTION: {
                "type": "reputation",
                "value": {"faction": "general", "amount": 15},
                "description": "Improved standing with various groups"
            },
            NarrativeTheme.MYSTERY: {
                "type": "item",
                "value": "investigation_tools",
                "description": "Tools that aid in solving mysteries"
            }
        }
        
        theme_reward = theme_rewards.get(theme, {
            "type": "item",
            "value": "generic_reward",
            "description": "Reward for completing the quest"
        })
        
        return [experience_reward, theme_reward]
    
    def _apply_archetype_modifications(self, quest_template: QuestTemplate, archetype: CharacterArchetype) -> QuestTemplate:
        """Apply character archetype-specific modifications to quest template"""
        
        # Archetype-specific objective modifications
        archetype_mods = {
            CharacterArchetype.WARRIOR: {
                "objective_preference": ["kill_target", "reach_location"],
                "description_modifier": "through strength and valor"
            },
            CharacterArchetype.SCHOLAR: {
                "objective_preference": ["solve_puzzle", "collect_item"],
                "description_modifier": "through knowledge and research"
            },
            CharacterArchetype.MYSTIC: {
                "objective_preference": ["interact_npc", "solve_puzzle"],
                "description_modifier": "through spiritual insight"
            },
            CharacterArchetype.SHADOW_WALKER: {
                "objective_preference": ["collect_item", "interact_npc"],
                "description_modifier": "through stealth and cunning"
            }
        }
        
        mods = archetype_mods.get(archetype, {})
        
        # Modify description to reflect archetype approach
        if "description_modifier" in mods:
            quest_template.description += f" This challenge must be approached {mods['description_modifier']}."
        
        return quest_template
    
    def _initialize_theme_templates(self) -> Dict[NarrativeTheme, Dict[str, Any]]:
        """Initialize theme-based quest generation templates"""
        return {
            theme: {
                "base_complexity": QuestComplexity.STANDARD,
                "preferred_objectives": ["reach_location", "collect_item", "interact_npc"],
                "narrative_weight": 1.0
            }
            for theme in NarrativeTheme
        }
    
    def _initialize_location_triggers(self) -> Dict[str, List[NarrativeTheme]]:
        """Initialize location-based quest triggers"""
        return {
            "corrupted_forest": [NarrativeTheme.CORRUPTION, NarrativeTheme.MYSTERY],
            "ancient_ruins": [NarrativeTheme.DISCOVERY, NarrativeTheme.MYSTERY],
            "abandoned_village": [NarrativeTheme.BETRAYAL, NarrativeTheme.REDEMPTION],
            "sacred_temple": [NarrativeTheme.REDEMPTION, NarrativeTheme.TRANSFORMATION],
            "shadow_district": [NarrativeTheme.BETRAYAL, NarrativeTheme.CORRUPTION]
        }
    
    def _initialize_archetype_modifiers(self) -> Dict[CharacterArchetype, Dict[str, Any]]:
        """Initialize character archetype quest modifiers"""
        return {
            CharacterArchetype.WARRIOR: {
                "combat_bonus": 1.2,
                "preferred_solutions": ["direct_action", "combat"],
                "dialogue_style": "direct"
            },
            CharacterArchetype.SCHOLAR: {
                "research_bonus": 1.2,
                "preferred_solutions": ["investigation", "knowledge"],
                "dialogue_style": "analytical"
            },
            CharacterArchetype.MYSTIC: {
                "spiritual_bonus": 1.2,
                "preferred_solutions": ["spiritual", "mystical"],
                "dialogue_style": "mystical"
            },
            CharacterArchetype.SHADOW_WALKER: {
                "stealth_bonus": 1.2,
                "preferred_solutions": ["stealth", "manipulation"],
                "dialogue_style": "subtle"
            },
            CharacterArchetype.BALANCED: {
                "versatility_bonus": 1.1,
                "preferred_solutions": ["adaptive", "flexible"],
                "dialogue_style": "balanced"
            }
        }

# Integration function for the quest engine
def integrate_dynamic_generation(quest_engine: QuestEngine) -> DynamicQuestGenerator:
    """Integrate dynamic quest generation with existing quest engine"""
    return DynamicQuestGenerator(quest_engine)

# Test function
def test_dynamic_generation():
    """Test the dynamic quest generation system"""
    from quest_engine_core import QuestEngine
    
    # Create quest engine and dynamic generator
    engine = QuestEngine()
    dynamic_generator = integrate_dynamic_generation(engine)
    
    # Test character data
    test_character = {
        "character_id": "test_dynamic_001",
        "name": "Dynamic Test Character",
        "level": 4,
        "attributes": {"might": 15, "intellect": 8, "will": 10, "shadow": 7}
    }
    
    print("🎮 Dynamic Quest Generation Test")
    print("=" * 40)
    
    # Test archetype determination
    context = dynamic_generator.get_or_create_narrative_context(test_character)
    print(f"Character Archetype: {context.character_archetype.value}")
    print(f"Theme Affinities: {len(context.theme_affinity)} themes")
    
    # Generate a dynamic quest
    dynamic_quest = dynamic_generator.generate_dynamic_quest(
        test_character, 
        QuestTrigger.RANDOM_ENCOUNTER
    )
    
    if dynamic_quest:
        print(f"✅ Generated Quest: {dynamic_quest.title}")
        print(f"   Type: {dynamic_quest.quest_type.value}")
        print(f"   Complexity: {dynamic_quest.complexity.value}")
        print(f"   Objectives: {len(dynamic_quest.objectives_templates)}")
        print(f"   Choices: {len(dynamic_quest.choices_templates)}")
        print("✅ Dynamic quest generation working!")
    else:
        print("❌ Failed to generate dynamic quest")
    
    return dynamic_quest is not None

if __name__ == "__main__":
    success = test_dynamic_generation()
    if success:
        print("\n🎉 Dynamic Quest Generation System Ready!")
    else:
        print("\n❌ Dynamic Quest Generation System Failed!")


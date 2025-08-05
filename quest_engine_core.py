#!/usr/bin/env python3
"""
Shadowlands RPG - Core Quest Engine Implementation
Comprehensive quest system with dynamic narrative branching and state management
"""

import json
import uuid
import time
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from abc import ABC, abstractmethod

class QuestType(Enum):
    """Quest classification types based on architecture specification"""
    MAIN_CAMPAIGN = "main_campaign"
    CHARACTER_PERSONAL = "character_personal"
    FACTION_POLITICAL = "faction_political"
    EXPLORATION_DISCOVERY = "exploration_discovery"
    DYNAMIC_GENERATED = "dynamic_generated"

class QuestComplexity(Enum):
    """Quest complexity and scope classifications"""
    EPIC = "epic"           # Multi-session, complex narrative
    STANDARD = "standard"   # Substantial content, reasonable timeframe
    QUICK = "quick"         # Time-efficient, immediate gratification

class QuestStatus(Enum):
    """Quest progression status tracking"""
    AVAILABLE = "available"         # Quest can be started
    ACTIVE = "active"              # Quest is in progress
    COMPLETED = "completed"        # Quest successfully finished
    FAILED = "failed"              # Quest failed or abandoned
    LOCKED = "locked"              # Prerequisites not met
    EXPIRED = "expired"            # Time-limited quest expired

class ObjectiveType(Enum):
    """Types of quest objectives"""
    KILL_TARGET = "kill_target"
    COLLECT_ITEM = "collect_item"
    REACH_LOCATION = "reach_location"
    INTERACT_NPC = "interact_npc"
    SOLVE_PUZZLE = "solve_puzzle"
    MAKE_CHOICE = "make_choice"
    CRAFT_ITEM = "craft_item"
    SURVIVE_TIME = "survive_time"

class ChoiceConsequenceType(Enum):
    """Types of choice consequences"""
    IMMEDIATE = "immediate"         # Affects current quest
    INTERMEDIATE = "intermediate"   # Affects faction/relationships
    LONG_TERM = "long_term"        # Affects major story developments

@dataclass
class QuestObjective:
    """Individual quest objective with tracking and validation"""
    objective_id: str
    objective_type: ObjectiveType
    description: str
    target_value: int = 1
    current_value: int = 0
    is_completed: bool = False
    is_optional: bool = False
    completion_timestamp: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def update_progress(self, increment: int = 1) -> bool:
        """Update objective progress and check completion"""
        if self.is_completed:
            return False
        
        self.current_value = min(self.current_value + increment, self.target_value)
        
        if self.current_value >= self.target_value:
            self.is_completed = True
            self.completion_timestamp = datetime.utcnow()
            return True
        
        return False
    
    def get_progress_percentage(self) -> float:
        """Get completion percentage for progress display"""
        if self.target_value == 0:
            return 100.0 if self.is_completed else 0.0
        return (self.current_value / self.target_value) * 100.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert objective to dictionary for serialization"""
        return {
            "objective_id": self.objective_id,
            "objective_type": self.objective_type.value,
            "description": self.description,
            "target_value": self.target_value,
            "current_value": self.current_value,
            "is_completed": self.is_completed,
            "is_optional": self.is_optional,
            "completion_timestamp": self.completion_timestamp.isoformat() if self.completion_timestamp else None,
            "progress_percentage": self.get_progress_percentage(),
            "metadata": self.metadata
        }

@dataclass
class QuestChoice:
    """Represents a choice point in quest narrative"""
    choice_id: str
    description: str
    consequences: List[Dict[str, Any]] = field(default_factory=list)
    requirements: Dict[str, Any] = field(default_factory=dict)
    is_available: bool = True
    choice_made: bool = False
    choice_timestamp: Optional[datetime] = None
    
    def make_choice(self) -> bool:
        """Record that this choice was made"""
        if not self.is_available or self.choice_made:
            return False
        
        self.choice_made = True
        self.choice_timestamp = datetime.utcnow()
        return True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert choice to dictionary for serialization"""
        return {
            "choice_id": self.choice_id,
            "description": self.description,
            "consequences": self.consequences,
            "requirements": self.requirements,
            "is_available": self.is_available,
            "choice_made": self.choice_made,
            "choice_timestamp": self.choice_timestamp.isoformat() if self.choice_timestamp else None
        }

@dataclass
class QuestReward:
    """Quest completion rewards"""
    reward_id: str
    reward_type: str  # "experience", "item", "skill", "reputation", etc.
    reward_value: Union[int, str, Dict[str, Any]]
    description: str
    is_claimed: bool = False
    claim_timestamp: Optional[datetime] = None
    
    def claim_reward(self) -> bool:
        """Mark reward as claimed"""
        if self.is_claimed:
            return False
        
        self.is_claimed = True
        self.claim_timestamp = datetime.utcnow()
        return True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert reward to dictionary for serialization"""
        return {
            "reward_id": self.reward_id,
            "reward_type": self.reward_type,
            "reward_value": self.reward_value,
            "description": self.description,
            "is_claimed": self.is_claimed,
            "claim_timestamp": self.claim_timestamp.isoformat() if self.claim_timestamp else None
        }

class QuestTemplate:
    """Template for quest generation and instantiation"""
    
    def __init__(self, template_id: str, quest_type: QuestType, complexity: QuestComplexity):
        self.template_id = template_id
        self.quest_type = quest_type
        self.complexity = complexity
        self.title = ""
        self.description = ""
        self.narrative_content = {}
        self.objectives_templates = []
        self.choices_templates = []
        self.rewards_templates = []
        self.prerequisites = {}
        self.time_limit = None
        self.level_requirement = 1
        self.faction_requirements = {}
        self.branching_logic = {}
        self.metadata = {}
    
    def create_quest_instance(self, character_data: Dict[str, Any]) -> 'Quest':
        """Create a quest instance from this template"""
        quest_id = str(uuid.uuid4())
        
        # Create objectives from templates
        objectives = []
        for obj_template in self.objectives_templates:
            objective = QuestObjective(
                objective_id=str(uuid.uuid4()),
                objective_type=ObjectiveType(obj_template["type"]),
                description=obj_template["description"],
                target_value=obj_template.get("target_value", 1),
                is_optional=obj_template.get("is_optional", False),
                metadata=obj_template.get("metadata", {})
            )
            objectives.append(objective)
        
        # Create choices from templates
        choices = []
        for choice_template in self.choices_templates:
            choice = QuestChoice(
                choice_id=str(uuid.uuid4()),
                description=choice_template["description"],
                consequences=choice_template.get("consequences", []),
                requirements=choice_template.get("requirements", {})
            )
            choices.append(choice)
        
        # Create rewards from templates
        rewards = []
        for reward_template in self.rewards_templates:
            reward = QuestReward(
                reward_id=str(uuid.uuid4()),
                reward_type=reward_template["type"],
                reward_value=reward_template["value"],
                description=reward_template["description"]
            )
            rewards.append(reward)
        
        # Create quest instance
        quest = Quest(
            quest_id=quest_id,
            template_id=self.template_id,
            quest_type=self.quest_type,
            complexity=self.complexity,
            title=self.title,
            description=self.description,
            objectives=objectives,
            choices=choices,
            rewards=rewards
        )
        
        return quest

class Quest:
    """Core quest instance with state management and progression tracking"""
    
    def __init__(self, quest_id: str, template_id: str, quest_type: QuestType, 
                 complexity: QuestComplexity, title: str, description: str,
                 objectives: List[QuestObjective] = None, 
                 choices: List[QuestChoice] = None,
                 rewards: List[QuestReward] = None):
        
        self.quest_id = quest_id
        self.template_id = template_id
        self.quest_type = quest_type
        self.complexity = complexity
        self.title = title
        self.description = description
        self.status = QuestStatus.AVAILABLE
        
        self.objectives = objectives or []
        self.choices = choices or []
        self.rewards = rewards or []
        
        self.start_timestamp = None
        self.completion_timestamp = None
        self.last_update_timestamp = datetime.utcnow()
        
        self.character_id = None
        self.choice_history = []
        self.progress_data = {}
        self.metadata = {}
    
    def start_quest(self, character_id: str) -> bool:
        """Start the quest for a character"""
        if self.status != QuestStatus.AVAILABLE:
            return False
        
        self.status = QuestStatus.ACTIVE
        self.character_id = character_id
        self.start_timestamp = datetime.utcnow()
        self.last_update_timestamp = datetime.utcnow()
        
        return True
    
    def update_objective_progress(self, objective_id: str, increment: int = 1) -> Dict[str, Any]:
        """Update progress for a specific objective"""
        for objective in self.objectives:
            if objective.objective_id == objective_id:
                was_completed = objective.is_completed
                progress_updated = objective.update_progress(increment)
                
                if progress_updated and not was_completed:
                    # Objective just completed
                    self.last_update_timestamp = datetime.utcnow()
                    self._check_quest_completion()
                    
                    return {
                        "success": True,
                        "objective_completed": True,
                        "quest_completed": self.status == QuestStatus.COMPLETED,
                        "progress": objective.get_progress_percentage()
                    }
                
                elif increment > 0:
                    # Progress updated but not completed
                    self.last_update_timestamp = datetime.utcnow()
                    
                    return {
                        "success": True,
                        "objective_completed": False,
                        "quest_completed": False,
                        "progress": objective.get_progress_percentage()
                    }
        
        return {"success": False, "error": "Objective not found"}
    
    def make_choice(self, choice_id: str) -> Dict[str, Any]:
        """Make a choice in the quest"""
        for choice in self.choices:
            if choice.choice_id == choice_id:
                if choice.make_choice():
                    self.choice_history.append({
                        "choice_id": choice_id,
                        "description": choice.description,
                        "timestamp": choice.choice_timestamp.isoformat(),
                        "consequences": choice.consequences
                    })
                    
                    self.last_update_timestamp = datetime.utcnow()
                    
                    # Apply choice consequences
                    self._apply_choice_consequences(choice.consequences)
                    
                    return {
                        "success": True,
                        "choice_made": True,
                        "consequences": choice.consequences
                    }
                else:
                    return {"success": False, "error": "Choice not available or already made"}
        
        return {"success": False, "error": "Choice not found"}
    
    def _check_quest_completion(self):
        """Check if quest is completed based on objectives"""
        required_objectives = [obj for obj in self.objectives if not obj.is_optional]
        completed_required = [obj for obj in required_objectives if obj.is_completed]
        
        if len(completed_required) == len(required_objectives):
            self.status = QuestStatus.COMPLETED
            self.completion_timestamp = datetime.utcnow()
    
    def _apply_choice_consequences(self, consequences: List[Dict[str, Any]]):
        """Apply consequences of choices made"""
        for consequence in consequences:
            consequence_type = ChoiceConsequenceType(consequence.get("type", "immediate"))
            
            if consequence_type == ChoiceConsequenceType.IMMEDIATE:
                # Apply immediate consequences to current quest
                if consequence.get("action") == "complete_objective":
                    obj_id = consequence.get("objective_id")
                    self.update_objective_progress(obj_id, 999)  # Force completion
                
                elif consequence.get("action") == "add_objective":
                    # Add new objective dynamically
                    new_objective = QuestObjective(
                        objective_id=str(uuid.uuid4()),
                        objective_type=ObjectiveType(consequence.get("objective_type", "interact_npc")),
                        description=consequence.get("description", "New objective"),
                        target_value=consequence.get("target_value", 1)
                    )
                    self.objectives.append(new_objective)
            
            # Store consequence for later processing by other systems
            self.progress_data[f"consequence_{len(self.choice_history)}"] = consequence
    
    def get_completion_percentage(self) -> float:
        """Get overall quest completion percentage"""
        if not self.objectives:
            return 100.0 if self.status == QuestStatus.COMPLETED else 0.0
        
        required_objectives = [obj for obj in self.objectives if not obj.is_optional]
        if not required_objectives:
            return 100.0
        
        total_progress = sum(obj.get_progress_percentage() for obj in required_objectives)
        return total_progress / len(required_objectives)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert quest to dictionary for serialization"""
        return {
            "quest_id": self.quest_id,
            "template_id": self.template_id,
            "quest_type": self.quest_type.value,
            "complexity": self.complexity.value,
            "title": self.title,
            "description": self.description,
            "status": self.status.value,
            "completion_percentage": self.get_completion_percentage(),
            
            "objectives": [obj.to_dict() for obj in self.objectives],
            "choices": [choice.to_dict() for choice in self.choices],
            "rewards": [reward.to_dict() for reward in self.rewards],
            
            "start_timestamp": self.start_timestamp.isoformat() if self.start_timestamp else None,
            "completion_timestamp": self.completion_timestamp.isoformat() if self.completion_timestamp else None,
            "last_update_timestamp": self.last_update_timestamp.isoformat(),
            
            "character_id": self.character_id,
            "choice_history": self.choice_history,
            "progress_data": self.progress_data,
            "metadata": self.metadata
        }

class QuestEngine:
    """Core quest engine managing quest instances and progression"""
    
    def __init__(self):
        self.active_quests: Dict[str, Quest] = {}  # character_id -> List[Quest]
        self.quest_templates: Dict[str, QuestTemplate] = {}
        self.completed_quests: Dict[str, List[Quest]] = {}
        self.quest_dependencies: Dict[str, List[str]] = {}
        
        # Initialize with sample quest templates
        self._initialize_sample_templates()
    
    def _initialize_sample_templates(self):
        """Initialize the engine with sample quest templates"""
        # Main Campaign Quest Template
        main_template = QuestTemplate("main_001", QuestType.MAIN_CAMPAIGN, QuestComplexity.EPIC)
        main_template.title = "Into the Corrupted Forest"
        main_template.description = "Investigate the source of corruption spreading through the ancient forest."
        main_template.objectives_templates = [
            {
                "type": "reach_location",
                "description": "Enter the Corrupted Forest",
                "target_value": 1,
                "metadata": {"location": "corrupted_forest_entrance"}
            },
            {
                "type": "interact_npc",
                "description": "Speak with the Forest Guardian",
                "target_value": 1,
                "metadata": {"npc_id": "forest_guardian"}
            },
            {
                "type": "collect_item",
                "description": "Gather corrupted samples",
                "target_value": 5,
                "metadata": {"item_type": "corrupted_sample"}
            }
        ]
        main_template.choices_templates = [
            {
                "description": "Approach the corruption directly",
                "consequences": [
                    {
                        "type": "immediate",
                        "action": "add_objective",
                        "objective_type": "kill_target",
                        "description": "Defeat corrupted creatures",
                        "target_value": 3
                    }
                ]
            },
            {
                "description": "Seek the Guardian's wisdom first",
                "consequences": [
                    {
                        "type": "intermediate",
                        "action": "reputation_change",
                        "faction": "forest_guardians",
                        "value": 10
                    }
                ]
            }
        ]
        main_template.rewards_templates = [
            {"type": "experience", "value": 500, "description": "Quest completion experience"},
            {"type": "item", "value": "guardian_blessing", "description": "Blessing of the Forest Guardian"}
        ]
        
        self.quest_templates[main_template.template_id] = main_template
        
        # Personal Quest Template
        personal_template = QuestTemplate("personal_001", QuestType.CHARACTER_PERSONAL, QuestComplexity.STANDARD)
        personal_template.title = "Echoes of the Past"
        personal_template.description = "Uncover memories from your character's mysterious past."
        personal_template.objectives_templates = [
            {
                "type": "reach_location",
                "description": "Visit your childhood home",
                "target_value": 1,
                "metadata": {"location": "character_home"}
            },
            {
                "type": "solve_puzzle",
                "description": "Decipher the old journal",
                "target_value": 1,
                "metadata": {"puzzle_type": "memory_fragments"}
            }
        ]
        personal_template.rewards_templates = [
            {"type": "skill", "value": "insight", "description": "Gained insight into your past"},
            {"type": "experience", "value": 250, "description": "Personal growth experience"}
        ]
        
        self.quest_templates[personal_template.template_id] = personal_template
    
    def create_quest_for_character(self, template_id: str, character_id: str, character_data: Dict[str, Any]) -> Optional[Quest]:
        """Create a new quest instance for a character"""
        if template_id not in self.quest_templates:
            return None
        
        template = self.quest_templates[template_id]
        quest = template.create_quest_instance(character_data)
        
        # Start the quest immediately
        if quest.start_quest(character_id):
            if character_id not in self.active_quests:
                self.active_quests[character_id] = []
            self.active_quests[character_id].append(quest)
            
            return quest
        
        return None
    
    def get_character_quests(self, character_id: str, status_filter: Optional[QuestStatus] = None) -> List[Quest]:
        """Get all quests for a character, optionally filtered by status"""
        character_quests = self.active_quests.get(character_id, [])
        
        if status_filter:
            return [quest for quest in character_quests if quest.status == status_filter]
        
        return character_quests
    
    def update_quest_objective(self, character_id: str, quest_id: str, objective_id: str, increment: int = 1) -> Dict[str, Any]:
        """Update quest objective progress"""
        character_quests = self.active_quests.get(character_id, [])
        
        for quest in character_quests:
            if quest.quest_id == quest_id:
                result = quest.update_objective_progress(objective_id, increment)
                
                # Move completed quests to completed list
                if quest.status == QuestStatus.COMPLETED:
                    if character_id not in self.completed_quests:
                        self.completed_quests[character_id] = []
                    self.completed_quests[character_id].append(quest)
                    self.active_quests[character_id].remove(quest)
                
                return result
        
        return {"success": False, "error": "Quest not found"}
    
    def make_quest_choice(self, character_id: str, quest_id: str, choice_id: str) -> Dict[str, Any]:
        """Make a choice in a quest"""
        character_quests = self.active_quests.get(character_id, [])
        
        for quest in character_quests:
            if quest.quest_id == quest_id:
                return quest.make_choice(choice_id)
        
        return {"success": False, "error": "Quest not found"}
    
    def get_available_quest_templates(self, character_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get quest templates available for a character"""
        available_templates = []
        
        for template_id, template in self.quest_templates.items():
            # Check level requirements
            character_level = character_data.get("level", 1)
            if character_level >= template.level_requirement:
                
                # Check if character already has this quest
                character_id = character_data.get("character_id", "")
                character_quests = self.active_quests.get(character_id, [])
                has_quest = any(quest.template_id == template_id for quest in character_quests)
                
                if not has_quest:
                    available_templates.append({
                        "template_id": template_id,
                        "quest_type": template.quest_type.value,
                        "complexity": template.complexity.value,
                        "title": template.title,
                        "description": template.description,
                        "level_requirement": template.level_requirement
                    })
        
        return available_templates
    
    def get_engine_statistics(self) -> Dict[str, Any]:
        """Get quest engine statistics"""
        total_active_quests = sum(len(quests) for quests in self.active_quests.values())
        total_completed_quests = sum(len(quests) for quests in self.completed_quests.values())
        
        return {
            "total_templates": len(self.quest_templates),
            "active_characters": len(self.active_quests),
            "total_active_quests": total_active_quests,
            "total_completed_quests": total_completed_quests,
            "templates_by_type": {
                quest_type.value: len([t for t in self.quest_templates.values() if t.quest_type == quest_type])
                for quest_type in QuestType
            }
        }

# Example usage and testing
if __name__ == "__main__":
    # Initialize quest engine
    engine = QuestEngine()
    
    # Sample character data
    character_data = {
        "character_id": "char_001",
        "level": 5,
        "name": "Test Drifter",
        "attributes": {"might": 12, "intellect": 10, "will": 14, "shadow": 8}
    }
    
    print("🎮 Shadowlands Quest Engine - Core Implementation Test")
    print("=" * 60)
    
    # Get available quests
    available_quests = engine.get_available_quest_templates(character_data)
    print(f"Available quest templates: {len(available_quests)}")
    
    for template in available_quests:
        print(f"  • {template['title']} ({template['quest_type']}, {template['complexity']})")
    
    # Create a quest
    if available_quests:
        template_id = available_quests[0]["template_id"]
        quest = engine.create_quest_for_character(template_id, character_data["character_id"], character_data)
        
        if quest:
            print(f"\\nCreated quest: {quest.title}")
            print(f"Quest ID: {quest.quest_id}")
            print(f"Status: {quest.status.value}")
            print(f"Objectives: {len(quest.objectives)}")
            
            # Test objective progress
            if quest.objectives:
                obj_id = quest.objectives[0].objective_id
                result = engine.update_quest_objective(character_data["character_id"], quest.quest_id, obj_id)
                print(f"\\nObjective update result: {result}")
            
            # Test choice making
            if quest.choices:
                choice_id = quest.choices[0].choice_id
                choice_result = engine.make_quest_choice(character_data["character_id"], quest.quest_id, choice_id)
                print(f"Choice result: {choice_result}")
    
    # Engine statistics
    stats = engine.get_engine_statistics()
    print(f"\\nEngine Statistics:")
    print(f"  Templates: {stats['total_templates']}")
    print(f"  Active Characters: {stats['active_characters']}")
    print(f"  Active Quests: {stats['total_active_quests']}")
    print(f"  Completed Quests: {stats['total_completed_quests']}")
    
    print("\\n✅ Core Quest Engine implementation completed successfully!")


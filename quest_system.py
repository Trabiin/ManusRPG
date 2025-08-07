from datetime import datetime
from enum import Enum
import json

class QuestStatus(Enum):
    NOT_STARTED = "not_started"
    AVAILABLE = "available"
    ACTIVE = "active"
    COMPLETED = "completed"
    FAILED = "failed"
    LOCKED = "locked"

class ObjectiveType(Enum):
    TALK_TO_NPC = "talk_to_npc"
    VISIT_LOCATION = "visit_location"
    COLLECT_ITEM = "collect_item"
    DEFEAT_ENEMY = "defeat_enemy"
    REACH_CORRUPTION_LEVEL = "reach_corruption_level"
    COMPLETE_ACTION = "complete_action"
    MAKE_CHOICE = "make_choice"
    DISCOVER_LORE = "discover_lore"

class Quest:
    def __init__(self, quest_id, title, description, location_id=None, npc_giver=None):
        self.quest_id = quest_id
        self.title = title
        self.description = description
        self.location_id = location_id
        self.npc_giver = npc_giver
        self.objectives = []
        self.prerequisites = []
        self.rewards = []
        self.status = QuestStatus.NOT_STARTED
        self.is_main_quest = False
        self.is_repeatable = False
        self.faction_requirements = {}
        self.corruption_requirements = {"min": 0, "max": 100}
        self.level_requirements = {"min": 1, "max": 25}
        self.completion_date = None
        self.choices_made = {}
        
    def add_objective(self, objective_id, description, objective_type, target=None, quantity=1, optional=False):
        objective = {
            "id": objective_id,
            "description": description,
            "type": objective_type,
            "target": target,
            "quantity": quantity,
            "current_progress": 0,
            "completed": False,
            "optional": optional
        }
        self.objectives.append(objective)
        
    def add_prerequisite(self, prerequisite_type, target, value=None):
        prerequisite = {
            "type": prerequisite_type,
            "target": target,
            "value": value
        }
        self.prerequisites.append(prerequisite)
        
    def add_reward(self, reward_type, target, quantity=1, description=None):
        reward = {
            "type": reward_type,
            "target": target,
            "quantity": quantity,
            "description": description
        }
        self.rewards.append(reward)
        
    def to_dict(self):
        return {
            "quest_id": self.quest_id,
            "title": self.title,
            "description": self.description,
            "location_id": self.location_id,
            "npc_giver": self.npc_giver,
            "objectives": self.objectives,
            "prerequisites": self.prerequisites,
            "rewards": self.rewards,
            "status": self.status.value,
            "is_main_quest": self.is_main_quest,
            "is_repeatable": self.is_repeatable,
            "faction_requirements": self.faction_requirements,
            "corruption_requirements": self.corruption_requirements,
            "level_requirements": self.level_requirements,
            "completion_date": self.completion_date.isoformat() if self.completion_date else None,
            "choices_made": self.choices_made
        }

class QuestManager:
    def __init__(self):
        self.quests = {}
        self.character_quest_states = {}
        
    def register_quest(self, quest):
        """Register a quest in the system"""
        self.quests[quest.quest_id] = quest
        
    def get_available_quests(self, character_data):
        """Get all quests available to a character based on their current state"""
        available_quests = []
        
        for quest_id, quest in self.quests.items():
            if self.check_quest_availability(quest, character_data):
                available_quests.append(quest)
                
        return available_quests
        
    def check_quest_availability(self, quest, character_data):
        """Check if a quest is available to a character"""
        character_id = character_data.get("character_id")
        quest_state = self.get_character_quest_state(character_id, quest.quest_id)
        
        # Check if quest is already completed and not repeatable
        if quest_state["status"] == QuestStatus.COMPLETED.value and not quest.is_repeatable:
            return False
            
        # Check if quest is already active
        if quest_state["status"] == QuestStatus.ACTIVE.value:
            return False
            
        # Check level requirements
        character_level = character_data.get("level", 1)
        if character_level < quest.level_requirements["min"] or character_level > quest.level_requirements["max"]:
            return False
            
        # Check corruption requirements
        corruption_level = character_data.get("corruption", 0)
        if corruption_level < quest.corruption_requirements["min"] or corruption_level > quest.corruption_requirements["max"]:
            return False
            
        # Check faction requirements
        character_factions = character_data.get("faction_standings", {})
        for faction, required_standing in quest.faction_requirements.items():
            if character_factions.get(faction, 0) < required_standing:
                return False
                
        # Check prerequisites
        for prerequisite in quest.prerequisites:
            if not self.check_prerequisite(prerequisite, character_data):
                return False
                
        return True
        
    def check_prerequisite(self, prerequisite, character_data):
        """Check if a specific prerequisite is met"""
        prereq_type = prerequisite["type"]
        target = prerequisite["target"]
        value = prerequisite.get("value")
        
        if prereq_type == "quest_completed":
            character_id = character_data.get("character_id")
            target_quest_state = self.get_character_quest_state(character_id, target)
            return target_quest_state["status"] == QuestStatus.COMPLETED.value
            
        elif prereq_type == "location_visited":
            visited_locations = character_data.get("visited_locations", [])
            return target in visited_locations
            
        elif prereq_type == "npc_relationship":
            npc_relationships = character_data.get("npc_relationships", {})
            return npc_relationships.get(target, 0) >= value
            
        elif prereq_type == "item_owned":
            inventory = character_data.get("inventory", [])
            return any(item["id"] == target for item in inventory)
            
        elif prereq_type == "skill_level":
            skills = character_data.get("skills", {})
            return skills.get(target, 0) >= value
            
        return True
        
    def start_quest(self, character_id, quest_id):
        """Start a quest for a character"""
        if quest_id not in self.quests:
            return {"success": False, "error": "Quest not found"}
            
        quest_state = self.get_character_quest_state(character_id, quest_id)
        quest_state["status"] = QuestStatus.ACTIVE.value
        quest_state["start_date"] = datetime.now().isoformat()
        
        # Initialize objective progress
        quest = self.quests[quest_id]
        for objective in quest.objectives:
            quest_state["objectives"][objective["id"]] = {
                "progress": 0,
                "completed": False
            }
            
        self.save_character_quest_state(character_id, quest_id, quest_state)
        
        return {"success": True, "quest": quest.to_dict(), "state": quest_state}
        
    def update_objective_progress(self, character_id, quest_id, objective_id, progress_increment=1):
        """Update progress on a specific quest objective"""
        quest_state = self.get_character_quest_state(character_id, quest_id)
        
        if quest_state["status"] != QuestStatus.ACTIVE.value:
            return {"success": False, "error": "Quest is not active"}
            
        if objective_id not in quest_state["objectives"]:
            return {"success": False, "error": "Objective not found"}
            
        quest = self.quests[quest_id]
        objective = next((obj for obj in quest.objectives if obj["id"] == objective_id), None)
        
        if not objective:
            return {"success": False, "error": "Objective definition not found"}
            
        # Update progress
        current_progress = quest_state["objectives"][objective_id]["progress"]
        new_progress = min(current_progress + progress_increment, objective["quantity"])
        quest_state["objectives"][objective_id]["progress"] = new_progress
        
        # Check if objective is completed
        if new_progress >= objective["quantity"]:
            quest_state["objectives"][objective_id]["completed"] = True
            
        # Check if all required objectives are completed
        all_required_completed = True
        for obj in quest.objectives:
            if not obj["optional"] and not quest_state["objectives"][obj["id"]]["completed"]:
                all_required_completed = False
                break
                
        # Complete quest if all required objectives are done
        if all_required_completed:
            return self.complete_quest(character_id, quest_id)
            
        self.save_character_quest_state(character_id, quest_id, quest_state)
        
        return {"success": True, "objective_completed": quest_state["objectives"][objective_id]["completed"]}
        
    def complete_quest(self, character_id, quest_id):
        """Complete a quest and distribute rewards"""
        quest_state = self.get_character_quest_state(character_id, quest_id)
        quest = self.quests[quest_id]
        
        quest_state["status"] = QuestStatus.COMPLETED.value
        quest_state["completion_date"] = datetime.now().isoformat()
        
        # Distribute rewards
        rewards_given = []
        for reward in quest.rewards:
            reward_result = self.distribute_reward(character_id, reward)
            rewards_given.append(reward_result)
            
        self.save_character_quest_state(character_id, quest_id, quest_state)
        
        return {
            "success": True,
            "quest_completed": True,
            "rewards": rewards_given
        }
        
    def distribute_reward(self, character_id, reward):
        """Distribute a specific reward to a character"""
        reward_type = reward["type"]
        target = reward["target"]
        quantity = reward["quantity"]
        
        # This would integrate with the character system to actually give rewards
        # For now, we'll return the reward information
        return {
            "type": reward_type,
            "target": target,
            "quantity": quantity,
            "description": reward.get("description", f"Received {quantity} {target}")
        }
        
    def get_character_quest_state(self, character_id, quest_id):
        """Get the current state of a quest for a character"""
        if character_id not in self.character_quest_states:
            self.character_quest_states[character_id] = {}
            
        if quest_id not in self.character_quest_states[character_id]:
            # Initialize quest state
            quest = self.quests.get(quest_id)
            if quest:
                self.character_quest_states[character_id][quest_id] = {
                    "status": QuestStatus.NOT_STARTED.value,
                    "start_date": None,
                    "completion_date": None,
                    "objectives": {},
                    "choices_made": {}
                }
                
        return self.character_quest_states[character_id].get(quest_id, {})
        
    def save_character_quest_state(self, character_id, quest_id, quest_state):
        """Save quest state for a character"""
        if character_id not in self.character_quest_states:
            self.character_quest_states[character_id] = {}
            
        self.character_quest_states[character_id][quest_id] = quest_state
        
    def get_character_active_quests(self, character_id):
        """Get all active quests for a character"""
        if character_id not in self.character_quest_states:
            return []
            
        active_quests = []
        for quest_id, quest_state in self.character_quest_states[character_id].items():
            if quest_state["status"] == QuestStatus.ACTIVE.value:
                quest = self.quests.get(quest_id)
                if quest:
                    quest_data = quest.to_dict()
                    quest_data["state"] = quest_state
                    active_quests.append(quest_data)
                    
        return active_quests
        
    def make_quest_choice(self, character_id, quest_id, choice_id, choice_value):
        """Record a choice made during a quest"""
        quest_state = self.get_character_quest_state(character_id, quest_id)
        quest_state["choices_made"][choice_id] = choice_value
        self.save_character_quest_state(character_id, quest_id, quest_state)
        
        return {"success": True, "choice_recorded": True}

# Initialize the global quest manager
quest_manager = QuestManager()

def initialize_quests():
    """Initialize all quests in the system"""
    
    # Main Quest: The Drifter's Arrival
    main_quest_1 = Quest(
        "main_drifters_arrival",
        "The Drifter's Arrival",
        "You have arrived at Haven's Rest seeking shelter and purpose. Learn about this community and the world they inhabit.",
        location_id="havens_rest",
        npc_giver="elder_marta"
    )
    main_quest_1.is_main_quest = True
    main_quest_1.add_objective("talk_to_marta", "Speak with Elder Marta", ObjectiveType.TALK_TO_NPC, "elder_marta")
    main_quest_1.add_objective("talk_to_sarah", "Meet Captain Sarah", ObjectiveType.TALK_TO_NPC, "captain_sarah")
    main_quest_1.add_objective("talk_to_thomas", "Speak with Brother Thomas", ObjectiveType.TALK_TO_NPC, "brother_thomas")
    main_quest_1.add_objective("rest_at_inn", "Rest at the village inn", ObjectiveType.COMPLETE_ACTION, "rest")
    main_quest_1.add_reward("experience", "general", 100, "Experience for completing your first quest")
    main_quest_1.add_reward("reputation", "havens_rest", 10, "Improved standing with Haven's Rest")
    quest_manager.register_quest(main_quest_1)
    
    # Side Quest: The Missing Merchant
    side_quest_1 = Quest(
        "side_missing_merchant",
        "The Missing Merchant",
        "Gareth Ironfoot has failed to arrive for his scheduled visit. Investigate his disappearance.",
        location_id="havens_rest",
        npc_giver="elder_marta"
    )
    side_quest_1.add_prerequisite("quest_completed", "main_drifters_arrival")
    side_quest_1.add_objective("investigate_route", "Investigate Gareth's usual route", ObjectiveType.VISIT_LOCATION, "trade_route")
    side_quest_1.add_objective("find_gareth", "Locate Gareth Ironfoot", ObjectiveType.COMPLETE_ACTION, "find_merchant")
    side_quest_1.add_objective("resolve_situation", "Resolve the bandit situation", ObjectiveType.MAKE_CHOICE, "bandit_resolution")
    side_quest_1.add_reward("experience", "general", 150)
    side_quest_1.add_reward("reputation", "havens_rest", 15)
    side_quest_1.add_reward("item", "merchants_blessing", 1, "A token of gratitude from Gareth")
    quest_manager.register_quest(side_quest_1)
    
    # Side Quest: The Corrupted Well
    side_quest_2 = Quest(
        "side_corrupted_well",
        "The Corrupted Well",
        "One of Haven's Rest's wells is showing signs of corruption. Investigate and determine the best course of action.",
        location_id="havens_rest",
        npc_giver="captain_sarah"
    )
    side_quest_2.add_prerequisite("quest_completed", "main_drifters_arrival")
    side_quest_2.add_objective("examine_well", "Examine the corrupted well", ObjectiveType.COMPLETE_ACTION, "examine_well")
    side_quest_2.add_objective("consult_experts", "Consult with Brother Thomas and the Hermit", ObjectiveType.TALK_TO_NPC, "multiple_npcs")
    side_quest_2.add_objective("make_recommendation", "Make a recommendation to the village council", ObjectiveType.MAKE_CHOICE, "well_decision")
    side_quest_2.add_reward("experience", "general", 120)
    side_quest_2.add_reward("skill", "corruption_knowledge", 1)
    quest_manager.register_quest(side_quest_2)
    
    # Shadowmere Woods Quest: The Lost Child
    woods_quest_1 = Quest(
        "woods_lost_child",
        "The Lost Child",
        "Young Lily has wandered into Shadowmere Woods and become lost. Find her and ensure her safety.",
        location_id="shadowmere_woods",
        npc_giver="lilys_mother"
    )
    woods_quest_1.add_prerequisite("location_visited", "shadowmere_woods")
    woods_quest_1.add_objective("search_woods", "Search Shadowmere Woods for Lily", ObjectiveType.VISIT_LOCATION, "deep_woods")
    woods_quest_1.add_objective("find_lily", "Locate Lily", ObjectiveType.COMPLETE_ACTION, "find_child")
    woods_quest_1.add_objective("decide_lilys_fate", "Decide what to do about Lily's situation", ObjectiveType.MAKE_CHOICE, "child_decision")
    woods_quest_1.add_reward("experience", "general", 180)
    woods_quest_1.add_reward("corruption", "shadow", 5, "Exposure to transformation magic")
    quest_manager.register_quest(woods_quest_1)
    
    # Character Quest: Elder Marta's Legacy
    character_quest_1 = Quest(
        "character_martas_burden",
        "The Burden of Leadership",
        "Elder Marta is struggling with the weight of leadership. Help her work through her doubts and decisions.",
        location_id="havens_rest",
        npc_giver="elder_marta"
    )
    character_quest_1.add_prerequisite("npc_relationship", "elder_marta", 25)
    character_quest_1.add_objective("listen_to_concerns", "Listen to Marta's concerns", ObjectiveType.TALK_TO_NPC, "elder_marta")
    character_quest_1.add_objective("review_decisions", "Review past leadership decisions", ObjectiveType.COMPLETE_ACTION, "review_history")
    character_quest_1.add_objective("provide_counsel", "Provide counsel on leadership approach", ObjectiveType.MAKE_CHOICE, "leadership_advice")
    character_quest_1.add_reward("experience", "general", 200)
    character_quest_1.add_reward("skill", "leadership", 2)
    character_quest_1.add_reward("reputation", "havens_rest", 25)
    quest_manager.register_quest(character_quest_1)
    
    # Faction Quest: Luminous Order Trials
    faction_quest_1 = Quest(
        "faction_luminous_trials",
        "Trials of Purification",
        "Undergo the formal trials to become a member of the Luminous Order.",
        location_id="purification_temple",
        npc_giver="high_priestess_seraphina"
    )
    faction_quest_1.faction_requirements = {"luminous_order": 50}
    faction_quest_1.corruption_requirements = {"min": 0, "max": 25}
    faction_quest_1.add_objective("trial_artifact", "Complete the Artifact Purification Trial", ObjectiveType.COMPLETE_ACTION, "purify_artifact")
    faction_quest_1.add_objective("trial_community", "Complete the Community Consent Trial", ObjectiveType.COMPLETE_ACTION, "community_trial")
    faction_quest_1.add_objective("trial_compassion", "Complete the Compassion Trial", ObjectiveType.COMPLETE_ACTION, "compassion_trial")
    faction_quest_1.add_objective("trial_resistance", "Complete the Corruption Resistance Trial", ObjectiveType.COMPLETE_ACTION, "resistance_trial")
    faction_quest_1.add_reward("experience", "general", 300)
    faction_quest_1.add_reward("faction_rank", "luminous_order", 1)
    faction_quest_1.add_reward("skill", "purification_mastery", 3)
    quest_manager.register_quest(faction_quest_1)

# Initialize all quests when the module is imported
initialize_quests()


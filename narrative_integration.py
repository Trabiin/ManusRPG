from datetime import datetime
import json
from quest_system import quest_manager, QuestStatus

class NarrativeIntegration:
    """
    System for integrating narrative elements with game mechanics.
    Handles the connection between quests, character progression, corruption,
    faction relationships, and world state changes.
    """
    
    def __init__(self):
        self.character_narrative_states = {}
        self.world_state_changes = {}
        self.faction_relationship_modifiers = {}
        self.corruption_narrative_thresholds = [10, 25, 50, 75, 90]
        
    def process_quest_completion(self, character_id, quest_id, choices_made):
        """
        Process the narrative consequences of completing a quest.
        This includes character development, faction changes, and world state updates.
        """
        quest = quest_manager.quests.get(quest_id)
        if not quest:
            return {"error": "Quest not found"}
            
        consequences = {
            "character_changes": {},
            "faction_changes": {},
            "world_changes": {},
            "corruption_effects": {},
            "narrative_flags": [],
            "unlocked_content": []
        }
        
        # Process quest-specific consequences
        if quest_id == "main_drifters_arrival":
            consequences.update(self._process_drifters_arrival(character_id, choices_made))
        elif quest_id == "side_missing_merchant":
            consequences.update(self._process_missing_merchant(character_id, choices_made))
        elif quest_id == "side_corrupted_well":
            consequences.update(self._process_corrupted_well(character_id, choices_made))
        elif quest_id == "woods_lost_child":
            consequences.update(self._process_lost_child(character_id, choices_made))
        elif quest_id == "character_martas_burden":
            consequences.update(self._process_martas_burden(character_id, choices_made))
        elif quest_id == "faction_luminous_trials":
            consequences.update(self._process_luminous_trials(character_id, choices_made))
            
        # Apply consequences to character
        self._apply_consequences_to_character(character_id, consequences)
        
        # Update narrative state
        self._update_character_narrative_state(character_id, quest_id, consequences)
        
        return consequences
        
    def _process_drifters_arrival(self, character_id, choices_made):
        """Process consequences of The Drifter's Arrival main quest"""
        consequences = {
            "character_changes": {
                "experience": 100,
                "corruption_resistance": 5  # Initial exposure builds slight resistance
            },
            "faction_changes": {
                "havens_rest": 15  # Basic positive relationship with starting community
            },
            "narrative_flags": [
                "drifter_accepted_by_havens_rest",
                "corruption_exposure_begun"
            ]
        }
        
        # Check how the player interacted with different NPCs
        if choices_made.get("marta_conversation_style") == "respectful":
            consequences["faction_changes"]["havens_rest"] += 5
            consequences["narrative_flags"].append("marta_impressed")
            
        if choices_made.get("thomas_spiritual_discussion") == "open_minded":
            consequences["character_changes"]["corruption_knowledge"] = 1
            consequences["narrative_flags"].append("thomas_spiritual_connection")
            
        if choices_made.get("sarah_combat_training") == "participated":
            consequences["character_changes"]["combat_experience"] = 10
            consequences["narrative_flags"].append("sarah_combat_training")
            
        return consequences
        
    def _process_missing_merchant(self, character_id, choices_made):
        """Process consequences of The Missing Merchant side quest"""
        consequences = {
            "character_changes": {},
            "faction_changes": {},
            "narrative_flags": []
        }
        
        resolution = choices_made.get("bandit_resolution")
        
        if resolution == "negotiate":
            consequences["character_changes"]["diplomacy_skill"] = 1
            consequences["faction_changes"]["havens_rest"] = 20
            consequences["narrative_flags"].extend([
                "merchant_saved_peacefully",
                "bandits_reformed",
                "diplomatic_reputation_growing"
            ])
            # Unlock future diplomatic options
            consequences["unlocked_content"] = ["diplomatic_solutions_enhanced"]
            
        elif resolution == "combat":
            consequences["character_changes"]["combat_experience"] = 15
            consequences["faction_changes"]["havens_rest"] = 10
            consequences["narrative_flags"].extend([
                "merchant_saved_by_force",
                "bandits_defeated",
                "combat_reputation_growing"
            ])
            # Some villagers question violent methods
            consequences["character_changes"]["moral_complexity_exposure"] = 1
            
        elif resolution == "corruption_intimidation":
            consequences["character_changes"]["corruption"] = 5
            consequences["character_changes"]["shadow_skill"] = 1
            consequences["faction_changes"]["havens_rest"] = 5  # Mixed reaction
            consequences["narrative_flags"].extend([
                "merchant_saved_through_corruption",
                "corruption_power_demonstrated",
                "villagers_wary_of_player"
            ])
            # Unlock shadow-based solutions but create social tension
            consequences["unlocked_content"] = ["shadow_intimidation_options"]
            consequences["world_changes"]["havens_rest_corruption_awareness"] = True
            
        return consequences
        
    def _process_corrupted_well(self, character_id, choices_made):
        """Process consequences of The Corrupted Well side quest"""
        consequences = {
            "character_changes": {},
            "faction_changes": {},
            "world_changes": {},
            "narrative_flags": []
        }
        
        decision = choices_made.get("well_decision")
        
        if decision == "purify_completely":
            consequences["character_changes"]["purification_skill"] = 2
            consequences["faction_changes"]["luminous_order"] = 15
            consequences["world_changes"]["havens_rest_well_status"] = "purified"
            consequences["narrative_flags"].extend([
                "well_purified_completely",
                "traditional_solution_chosen",
                "purification_expertise_demonstrated"
            ])
            
        elif decision == "controlled_integration":
            consequences["character_changes"]["corruption_knowledge"] = 2
            consequences["character_changes"]["innovation_reputation"] = 1
            consequences["faction_changes"]["scholarly_circle"] = 20
            consequences["world_changes"]["havens_rest_well_status"] = "integrated"
            consequences["narrative_flags"].extend([
                "well_corruption_integrated",
                "innovative_solution_found",
                "corruption_benefits_demonstrated"
            ])
            # This creates a model for other communities
            consequences["unlocked_content"] = ["integration_consultation_requests"]
            
        elif decision == "seal_and_monitor":
            consequences["character_changes"]["caution_reputation"] = 1
            consequences["faction_changes"]["havens_rest"] = 10
            consequences["world_changes"]["havens_rest_well_status"] = "sealed"
            consequences["narrative_flags"].extend([
                "well_sealed_safely",
                "cautious_approach_taken",
                "long_term_thinking_demonstrated"
            ])
            
        return consequences
        
    def _process_lost_child(self, character_id, choices_made):
        """Process consequences of The Lost Child quest"""
        consequences = {
            "character_changes": {},
            "faction_changes": {},
            "corruption_effects": {},
            "narrative_flags": []
        }
        
        decision = choices_made.get("child_decision")
        
        if decision == "return_unchanged":
            consequences["faction_changes"]["havens_rest"] = 15
            consequences["narrative_flags"].extend([
                "lily_returned_safely",
                "family_reunited",
                "protective_instincts_honored"
            ])
            
        elif decision == "help_adapt_to_changes":
            consequences["character_changes"]["corruption_knowledge"] = 1
            consequences["character_changes"]["empathy_skill"] = 1
            consequences["corruption_effects"]["controlled_exposure"] = 3
            consequences["narrative_flags"].extend([
                "lily_helped_to_adapt",
                "transformation_guidance_provided",
                "child_welfare_prioritized"
            ])
            # This creates a precedent for helping others adapt
            consequences["unlocked_content"] = ["transformation_counseling_options"]
            
        elif decision == "study_the_transformation":
            consequences["character_changes"]["corruption_knowledge"] = 3
            consequences["character_changes"]["research_reputation"] = 1
            consequences["faction_changes"]["scholarly_circle"] = 25
            consequences["corruption_effects"]["research_exposure"] = 5
            consequences["narrative_flags"].extend([
                "lily_transformation_studied",
                "scientific_approach_taken",
                "knowledge_prioritized_over_emotion"
            ])
            # Some question the ethics of this choice
            consequences["character_changes"]["moral_complexity_exposure"] = 2
            
        return consequences
        
    def _process_martas_burden(self, character_id, choices_made):
        """Process consequences of Elder Marta's character quest"""
        consequences = {
            "character_changes": {},
            "faction_changes": {},
            "narrative_flags": []
        }
        
        advice = choices_made.get("leadership_advice")
        
        if advice == "maintain_traditional_values":
            consequences["character_changes"]["traditional_wisdom"] = 2
            consequences["faction_changes"]["havens_rest"] = 25
            consequences["faction_changes"]["luminous_order"] = 10
            consequences["narrative_flags"].extend([
                "marta_traditional_guidance",
                "community_stability_reinforced",
                "conservative_leadership_supported"
            ])
            
        elif advice == "adapt_while_preserving_core":
            consequences["character_changes"]["balanced_wisdom"] = 2
            consequences["character_changes"]["leadership_skill"] = 1
            consequences["faction_changes"]["havens_rest"] = 30
            consequences["narrative_flags"].extend([
                "marta_balanced_guidance",
                "adaptive_leadership_encouraged",
                "community_resilience_enhanced"
            ])
            # This approach becomes a model for other communities
            consequences["unlocked_content"] = ["leadership_consultation_requests"]
            
        elif advice == "embrace_necessary_change":
            consequences["character_changes"]["progressive_wisdom"] = 2
            consequences["faction_changes"]["havens_rest"] = 20
            consequences["faction_changes"]["shadow_court"] = 15
            consequences["narrative_flags"].extend([
                "marta_progressive_guidance",
                "transformative_leadership_encouraged",
                "community_evolution_supported"
            ])
            
        return consequences
        
    def _process_luminous_trials(self, character_id, choices_made):
        """Process consequences of Luminous Order faction quest"""
        consequences = {
            "character_changes": {},
            "faction_changes": {},
            "narrative_flags": []
        }
        
        # This is a major faction quest with significant consequences
        consequences["character_changes"]["purification_mastery"] = 3
        consequences["character_changes"]["corruption_resistance"] = 10
        consequences["faction_changes"]["luminous_order"] = 50
        consequences["narrative_flags"].extend([
            "luminous_order_member",
            "purification_master",
            "corruption_resistance_enhanced"
        ])
        
        # Check performance in individual trials
        if choices_made.get("artifact_trial_method") == "innovative":
            consequences["character_changes"]["innovation_reputation"] = 1
            consequences["narrative_flags"].append("innovative_purification_techniques")
            
        if choices_made.get("community_trial_approach") == "respectful":
            consequences["character_changes"]["diplomacy_skill"] = 1
            consequences["narrative_flags"].append("respectful_purification_advocate")
            
        if choices_made.get("compassion_trial_choice") == "mercy":
            consequences["character_changes"]["empathy_skill"] = 2
            consequences["narrative_flags"].append("compassionate_purifier")
            
        # Unlock advanced Luminous Order content
        consequences["unlocked_content"] = [
            "advanced_purification_techniques",
            "luminous_order_inner_circle",
            "purification_research_projects"
        ]
        
        return consequences
        
    def _apply_consequences_to_character(self, character_id, consequences):
        """Apply narrative consequences to the character's actual game state"""
        from flask import session
        
        character_data = session.get('character')
        if not character_data:
            return
            
        # Apply character changes
        char_changes = consequences.get("character_changes", {})
        for attribute, value in char_changes.items():
            if attribute == "experience":
                character_data["experience"] = character_data.get("experience", 0) + value
            elif attribute == "corruption":
                character_data["corruption"] = max(0, min(100, character_data.get("corruption", 0) + value))
            elif attribute == "corruption_resistance":
                character_data["corruption_resistance"] = character_data.get("corruption_resistance", 0) + value
            elif attribute.endswith("_skill"):
                skills = character_data.get("skills", {})
                skill_name = attribute.replace("_skill", "")
                skills[skill_name] = skills.get(skill_name, 0) + value
                character_data["skills"] = skills
            elif attribute.endswith("_experience"):
                character_data[attribute] = character_data.get(attribute, 0) + value
                
        # Apply faction changes
        faction_changes = consequences.get("faction_changes", {})
        faction_standings = character_data.get("faction_standings", {})
        for faction, value in faction_changes.items():
            faction_standings[faction] = faction_standings.get(faction, 0) + value
        character_data["faction_standings"] = faction_standings
        
        # Apply corruption effects
        corruption_effects = consequences.get("corruption_effects", {})
        for effect_type, value in corruption_effects.items():
            if effect_type in ["controlled_exposure", "research_exposure"]:
                # These provide corruption with some resistance
                character_data["corruption"] = min(100, character_data.get("corruption", 0) + value)
                character_data["corruption_resistance"] = character_data.get("corruption_resistance", 0) + (value // 2)
                
        # Store narrative flags
        narrative_flags = character_data.get("narrative_flags", [])
        narrative_flags.extend(consequences.get("narrative_flags", []))
        character_data["narrative_flags"] = list(set(narrative_flags))  # Remove duplicates
        
        # Store unlocked content
        unlocked_content = character_data.get("unlocked_content", [])
        unlocked_content.extend(consequences.get("unlocked_content", []))
        character_data["unlocked_content"] = list(set(unlocked_content))
        
        # Update session
        session['character'] = character_data
        
    def _update_character_narrative_state(self, character_id, quest_id, consequences):
        """Update the character's narrative state tracking"""
        if character_id not in self.character_narrative_states:
            self.character_narrative_states[character_id] = {
                "completed_quests": [],
                "major_choices": {},
                "reputation_modifiers": {},
                "corruption_milestones": [],
                "faction_relationships": {},
                "world_impact": []
            }
            
        state = self.character_narrative_states[character_id]
        
        # Track quest completion
        if quest_id not in state["completed_quests"]:
            state["completed_quests"].append(quest_id)
            
        # Track major choices
        quest = quest_manager.quests.get(quest_id)
        if quest:
            quest_state = quest_manager.get_character_quest_state(character_id, quest_id)
            choices = quest_state.get("choices_made", {})
            state["major_choices"][quest_id] = choices
            
        # Track world impact
        world_changes = consequences.get("world_changes", {})
        for change, value in world_changes.items():
            state["world_impact"].append({
                "quest": quest_id,
                "change": change,
                "value": value,
                "timestamp": datetime.now().isoformat()
            })
            
    def check_corruption_narrative_triggers(self, character_id, current_corruption):
        """Check if corruption level changes trigger narrative events"""
        triggers = []
        
        for threshold in self.corruption_narrative_thresholds:
            if current_corruption >= threshold:
                trigger_key = f"corruption_threshold_{threshold}"
                
                # Check if this threshold hasn't been triggered before
                character_data = self._get_character_narrative_state(character_id)
                if trigger_key not in character_data.get("corruption_milestones", []):
                    triggers.append(self._create_corruption_trigger(threshold))
                    character_data.setdefault("corruption_milestones", []).append(trigger_key)
                    
        return triggers
        
    def _create_corruption_trigger(self, threshold):
        """Create narrative triggers for corruption thresholds"""
        triggers = {
            10: {
                "type": "corruption_awareness",
                "title": "First Shadows",
                "description": "You begin to notice subtle changes in how you perceive the world. Colors seem slightly different, and you catch glimpses of movement in your peripheral vision.",
                "effects": ["shadow_sight_level_1"],
                "dialogue_changes": ["corruption_awareness_dialogue"]
            },
            25: {
                "type": "corruption_adaptation",
                "title": "Embracing Change",
                "description": "The corruption no longer feels entirely foreign. You find yourself understanding things that once seemed incomprehensible.",
                "effects": ["corruption_understanding", "shadow_magic_access"],
                "dialogue_changes": ["corruption_adaptation_dialogue"],
                "npc_reactions": ["some_npcs_wary", "shadow_beings_friendly"]
            },
            50: {
                "type": "corruption_transformation",
                "title": "Threshold Crossed",
                "description": "You have crossed a significant threshold. Your very nature is changing, and there may be no going back.",
                "effects": ["major_transformation", "shadow_realm_access"],
                "dialogue_changes": ["major_corruption_dialogue"],
                "npc_reactions": ["traditional_npcs_hostile", "transformed_beings_accepting"],
                "quest_unlocks": ["shadow_realm_quests"]
            },
            75: {
                "type": "corruption_mastery",
                "title": "Power and Price",
                "description": "You wield corruption like a tool, but the line between user and used grows ever thinner.",
                "effects": ["corruption_mastery", "advanced_shadow_magic"],
                "dialogue_changes": ["corruption_master_dialogue"],
                "npc_reactions": ["fear_and_respect", "shadow_lord_attention"],
                "quest_unlocks": ["shadow_court_advancement"]
            },
            90: {
                "type": "corruption_transcendence",
                "title": "Beyond Human",
                "description": "You are no longer entirely human. The question is whether you retain enough of your original self to remember why that matters.",
                "effects": ["transcendent_corruption", "reality_manipulation"],
                "dialogue_changes": ["transcendent_being_dialogue"],
                "npc_reactions": ["awe_and_terror", "shadow_lord_peer"],
                "quest_unlocks": ["transcendence_questline"]
            }
        }
        
        return triggers.get(threshold, {})
        
    def get_available_dialogue_options(self, character_id, npc_id, base_options):
        """Modify dialogue options based on character's narrative state"""
        character_state = self._get_character_narrative_state(character_id)
        narrative_flags = character_state.get("narrative_flags", [])
        
        modified_options = base_options.copy()
        
        # Add corruption-based dialogue options
        from flask import session
        character_data = session.get('character', {})
        corruption = character_data.get('corruption', 0)
        
        if corruption >= 25:
            modified_options.append({
                "id": "corruption_insight",
                "text": "I understand the nature of transformation...",
                "requires": ["corruption_adaptation_dialogue"],
                "corruption_cost": 0
            })
            
        if corruption >= 50:
            modified_options.append({
                "id": "shadow_intimidation",
                "text": "[Shadow Power] Your resistance is futile.",
                "requires": ["major_corruption_dialogue"],
                "corruption_cost": 2
            })
            
        # Add faction-based dialogue options
        faction_standings = character_data.get('faction_standings', {})
        
        if faction_standings.get('luminous_order', 0) >= 25:
            modified_options.append({
                "id": "purification_offer",
                "text": "I can help purify this corruption.",
                "requires": ["luminous_order_member"],
                "corruption_cost": -5
            })
            
        # Add quest-completion-based options
        if "marta_impressed" in narrative_flags:
            modified_options.append({
                "id": "marta_reference",
                "text": "Elder Marta spoke highly of your community.",
                "requires": ["marta_impressed"]
            })
            
        return modified_options
        
    def _get_character_narrative_state(self, character_id):
        """Get the narrative state for a character"""
        return self.character_narrative_states.get(character_id, {})
        
    def get_character_reputation_summary(self, character_id):
        """Get a summary of the character's reputation and standing"""
        from flask import session
        character_data = session.get('character', {})
        
        if not character_data:
            return {}
            
        faction_standings = character_data.get('faction_standings', {})
        narrative_flags = character_data.get('narrative_flags', [])
        corruption = character_data.get('corruption', 0)
        
        reputation_summary = {
            "overall_alignment": self._determine_overall_alignment(faction_standings, corruption, narrative_flags),
            "faction_relationships": self._categorize_faction_relationships(faction_standings),
            "corruption_status": self._get_corruption_status(corruption),
            "notable_achievements": self._get_notable_achievements(narrative_flags),
            "world_impact": self._assess_world_impact(character_id)
        }
        
        return reputation_summary
        
    def _determine_overall_alignment(self, faction_standings, corruption, narrative_flags):
        """Determine the character's overall moral/philosophical alignment"""
        luminous_standing = faction_standings.get('luminous_order', 0)
        shadow_standing = faction_standings.get('shadow_court', 0)
        
        if corruption < 25 and luminous_standing > shadow_standing:
            return "Purifier"
        elif corruption > 50 and shadow_standing > luminous_standing:
            return "Transformed"
        elif "balanced_wisdom" in narrative_flags or "adaptive_leadership" in narrative_flags:
            return "Integrator"
        elif corruption < 10:
            return "Traditional"
        else:
            return "Seeker"
            
    def _categorize_faction_relationships(self, faction_standings):
        """Categorize relationships with different factions"""
        relationships = {}
        
        for faction, standing in faction_standings.items():
            if standing >= 50:
                relationships[faction] = "Allied"
            elif standing >= 25:
                relationships[faction] = "Friendly"
            elif standing >= 0:
                relationships[faction] = "Neutral"
            elif standing >= -25:
                relationships[faction] = "Wary"
            else:
                relationships[faction] = "Hostile"
                
        return relationships
        
    def _get_corruption_status(self, corruption):
        """Get a descriptive status for the character's corruption level"""
        if corruption < 10:
            return "Pure"
        elif corruption < 25:
            return "Touched"
        elif corruption < 50:
            return "Adapted"
        elif corruption < 75:
            return "Transformed"
        else:
            return "Transcendent"
            
    def _get_notable_achievements(self, narrative_flags):
        """Extract notable achievements from narrative flags"""
        achievements = []
        
        achievement_mapping = {
            "marta_impressed": "Earned Elder Marta's Respect",
            "diplomatic_reputation_growing": "Known for Diplomatic Solutions",
            "combat_reputation_growing": "Feared in Combat",
            "corruption_power_demonstrated": "Wielder of Shadow Power",
            "innovative_solution_found": "Creative Problem Solver",
            "luminous_order_member": "Member of the Luminous Order",
            "compassionate_purifier": "Compassionate Healer",
            "transformation_guidance_provided": "Guide for the Transformed"
        }
        
        for flag in narrative_flags:
            if flag in achievement_mapping:
                achievements.append(achievement_mapping[flag])
                
        return achievements
        
    def _assess_world_impact(self, character_id):
        """Assess the character's impact on the world"""
        character_state = self._get_character_narrative_state(character_id)
        world_impacts = character_state.get("world_impact", [])
        
        impact_summary = {
            "communities_helped": 0,
            "conflicts_resolved": 0,
            "innovations_introduced": 0,
            "people_transformed": 0
        }
        
        for impact in world_impacts:
            change = impact.get("change", "")
            if "well_status" in change or "community" in change:
                impact_summary["communities_helped"] += 1
            if "conflict" in change or "resolution" in change:
                impact_summary["conflicts_resolved"] += 1
            if "integration" in change or "innovation" in change:
                impact_summary["innovations_introduced"] += 1
            if "transformation" in change:
                impact_summary["people_transformed"] += 1
                
        return impact_summary

# Initialize the global narrative integration system
narrative_integration = NarrativeIntegration()


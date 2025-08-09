"""
Shadowlands RPG - Dynamic Quest Generation API Routes
RESTful API endpoints for dynamic quest generation and narrative management
"""

from flask import Blueprint, request, jsonify, session
from typing import Dict, Any, List, Optional
import sys
import os

# Add the parent directory to the path to import dynamic quest generation
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
from dynamic_quest_generation import (
    DynamicQuestGenerator, NarrativeTheme, CharacterArchetype, 
    QuestTrigger, integrate_dynamic_generation
)
from quest_engine_core import QuestEngine

# Import shared quest engine
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from shared_quest_engine import get_quest_engine, get_dynamic_generator

# Create Blueprint
dynamic_quests_bp = Blueprint('dynamic_quests', __name__)

# Use shared instances
def get_quest_engine_instance():
    return get_quest_engine()

def get_dynamic_generator_instance():
    return get_dynamic_generator()

def create_standardized_response(success: bool, data: Any = None, message: str = "", error_code: str = None) -> Dict[str, Any]:
    """Create standardized API response format"""
    response = {
        "success": success,
        "message": message,
        "timestamp": "2025-07-31T12:00:00Z",
        "data": data if data is not None else {}
    }
    
    if error_code:
        response["error_code"] = error_code
    
    return response

def get_character_data_from_session() -> Optional[Dict[str, Any]]:
    """Get character data from session"""
    if 'character' not in session:
        return None
    
    character = session['character']
    return {
        "character_id": character.get("character_id", "default_character"),
        "level": character.get("level", 1),
        "name": character.get("name", "Unknown Drifter"),
        "attributes": character.get("attributes", {"might": 10, "intellect": 10, "will": 10, "shadow": 10})
    }

@dynamic_quests_bp.route('/narrative-context', methods=['GET'])
def get_narrative_context():
    """Get character's narrative context and progression"""
    try:
        character_data = get_character_data_from_session()
        if not character_data:
            return jsonify(create_standardized_response(
                False, message="No character data found in session", error_code="NO_CHARACTER_DATA"
            )), 400
        
        # Get or create narrative context
        narrative_context = get_dynamic_generator_instance().get_or_create_narrative_context(character_data)
        
        # Convert to serializable format
        context_data = {
            "character_id": narrative_context.character_id,
            "character_archetype": narrative_context.character_archetype.value,
            "moral_alignment": narrative_context.moral_alignment,
            "theme_affinity": {theme.value: affinity for theme, affinity in narrative_context.theme_affinity.items()},
            "completed_themes": [theme.value for theme in narrative_context.completed_themes],
            "choice_history_count": len(narrative_context.choice_history),
            "faction_standings": narrative_context.faction_standings,
            "narrative_flags": narrative_context.narrative_flags
        }
        
        return jsonify(create_standardized_response(
            True, 
            data={"narrative_context": context_data},
            message="Narrative context retrieved successfully"
        ))
        
    except Exception as e:
        return jsonify(create_standardized_response(
            False, message=f"Failed to retrieve narrative context: {str(e)}", error_code="CONTEXT_ERROR"
        )), 500

@dynamic_quests_bp.route('/generate', methods=['POST'])
def generate_dynamic_quest():
    """Generate a dynamic quest based on character context and trigger"""
    try:
        character_data = get_character_data_from_session()
        if not character_data:
            return jsonify(create_standardized_response(
                False, message="No character data found in session", error_code="NO_CHARACTER_DATA"
            )), 400
        
        # Get request parameters
        request_data = request.get_json() or {}
        trigger_str = request_data.get("trigger", "random_encounter")
        location_context = request_data.get("location_context")
        
        # Convert trigger string to enum
        try:
            trigger = QuestTrigger(trigger_str)
        except ValueError:
            trigger = QuestTrigger.RANDOM_ENCOUNTER
        
        # Generate dynamic quest
        quest_template = get_dynamic_generator_instance().generate_dynamic_quest(
            character_data, trigger, location_context
        )
        
        if not quest_template:
            return jsonify(create_standardized_response(
                False, message="Failed to generate dynamic quest", error_code="GENERATION_FAILED"
            )), 500
        
        # Convert quest template to serializable format
        quest_data = {
            "template_id": quest_template.template_id,
            "quest_type": quest_template.quest_type.value,
            "complexity": quest_template.complexity.value,
            "title": quest_template.title,
            "description": quest_template.description,
            "objectives_count": len(quest_template.objectives_templates),
            "choices_count": len(quest_template.choices_templates),
            "rewards_count": len(quest_template.rewards_templates),
            "level_requirement": quest_template.level_requirement,
            "objectives": quest_template.objectives_templates,
            "choices": quest_template.choices_templates,
            "rewards": quest_template.rewards_templates
        }
        
        # Add the template to the quest engine for future use
        get_quest_engine_instance().quest_templates[quest_template.template_id] = quest_template
        
        return jsonify(create_standardized_response(
            True,
            data={"generated_quest": quest_data},
            message=f"Successfully generated dynamic quest: {quest_template.title}"
        ))
        
    except Exception as e:
        return jsonify(create_standardized_response(
            False, message=f"Failed to generate dynamic quest: {str(e)}", error_code="GENERATION_ERROR"
        )), 500

@dynamic_quests_bp.route('/themes', methods=['GET'])
def get_available_themes():
    """Get available narrative themes and their descriptions"""
    try:
        character_data = get_character_data_from_session()
        if character_data:
            narrative_context = get_dynamic_generator_instance().get_or_create_narrative_context(character_data)
            theme_affinities = {theme.value: affinity for theme, affinity in narrative_context.theme_affinity.items()}
        else:
            theme_affinities = {}
        
        # Theme descriptions
        theme_descriptions = {
            "corruption": "Dark magic, tainted lands, and moral decay challenge the character",
            "discovery": "Ancient secrets, lost knowledge, and exploration await",
            "betrayal": "Trust is broken, allies become enemies, and deception runs deep",
            "redemption": "Second chances, making amends, and healing past wounds",
            "sacrifice": "Noble loss, difficult choices, and serving the greater good",
            "power": "Ambition, control, and the pursuit of dominance",
            "mystery": "Puzzles, hidden truths, and investigations to uncover",
            "revenge": "Justice, retribution, and settling old scores",
            "protection": "Defending others, safeguarding values, and standing guard",
            "transformation": "Change, growth, and personal evolution"
        }
        
        themes_data = []
        for theme in NarrativeTheme:
            theme_info = {
                "theme": theme.value,
                "description": theme_descriptions.get(theme.value, "A narrative theme"),
                "affinity": theme_affinities.get(theme.value, 0.5)
            }
            themes_data.append(theme_info)
        
        return jsonify(create_standardized_response(
            True,
            data={"themes": themes_data, "total_themes": len(themes_data)},
            message="Retrieved available narrative themes"
        ))
        
    except Exception as e:
        return jsonify(create_standardized_response(
            False, message=f"Failed to retrieve themes: {str(e)}", error_code="THEMES_ERROR"
        )), 500

@dynamic_quests_bp.route('/archetypes', methods=['GET'])
def get_character_archetypes():
    """Get available character archetypes and their descriptions"""
    try:
        archetype_descriptions = {
            "warrior": "Might-focused characters who prefer direct action and combat solutions",
            "scholar": "Intellect-focused characters who seek knowledge and research-based approaches",
            "mystic": "Will-focused characters who use spiritual insight and magical solutions",
            "shadow_walker": "Shadow-focused characters who employ stealth and manipulation",
            "balanced": "Versatile characters with no dominant attribute, adaptable to any situation"
        }
        
        archetypes_data = []
        for archetype in CharacterArchetype:
            archetype_info = {
                "archetype": archetype.value,
                "description": archetype_descriptions.get(archetype.value, "A character archetype")
            }
            archetypes_data.append(archetype_info)
        
        # Get current character's archetype if available
        current_archetype = None
        character_data = get_character_data_from_session()
        if character_data:
            narrative_context = get_dynamic_generator_instance().get_or_create_narrative_context(character_data)
            current_archetype = narrative_context.character_archetype.value
        
        return jsonify(create_standardized_response(
            True,
            data={
                "archetypes": archetypes_data, 
                "total_archetypes": len(archetypes_data),
                "current_archetype": current_archetype
            },
            message="Retrieved character archetypes"
        ))
        
    except Exception as e:
        return jsonify(create_standardized_response(
            False, message=f"Failed to retrieve archetypes: {str(e)}", error_code="ARCHETYPES_ERROR"
        )), 500

@dynamic_quests_bp.route('/triggers', methods=['GET'])
def get_quest_triggers():
    """Get available quest triggers and their descriptions"""
    try:
        trigger_descriptions = {
            "character_choice": "Quests generated based on previous character decisions",
            "location_discovery": "Quests triggered by exploring new areas",
            "npc_interaction": "Quests initiated through character encounters",
            "item_acquisition": "Quests triggered by finding specific items",
            "faction_standing": "Quests based on reputation changes with factions",
            "time_based": "Scheduled or timed quest events",
            "random_encounter": "Procedurally generated quest opportunities",
            "story_progression": "Quests that advance the main narrative"
        }
        
        triggers_data = []
        for trigger in QuestTrigger:
            trigger_info = {
                "trigger": trigger.value,
                "description": trigger_descriptions.get(trigger.value, "A quest trigger type")
            }
            triggers_data.append(trigger_info)
        
        return jsonify(create_standardized_response(
            True,
            data={"triggers": triggers_data, "total_triggers": len(triggers_data)},
            message="Retrieved quest trigger types"
        ))
        
    except Exception as e:
        return jsonify(create_standardized_response(
            False, message=f"Failed to retrieve triggers: {str(e)}", error_code="TRIGGERS_ERROR"
        )), 500

@dynamic_quests_bp.route('/statistics', methods=['GET'])
def get_dynamic_quest_statistics():
    """Get statistics about dynamic quest generation"""
    try:
        character_data = get_character_data_from_session()
        
        # Global statistics
        total_contexts = len(get_dynamic_generator_instance().narrative_contexts)
        
        # Character-specific statistics
        character_stats = {}
        if character_data:
            character_id = character_data["character_id"]
            if character_id in get_dynamic_generator_instance().narrative_contexts:
                context = get_dynamic_generator_instance().narrative_contexts[character_id]
                character_stats = {
                    "character_archetype": context.character_archetype.value,
                    "choices_made": len(context.choice_history),
                    "completed_themes": len(context.completed_themes),
                    "faction_relationships": len(context.faction_standings),
                    "narrative_flags": len(context.narrative_flags),
                    "moral_alignment": context.moral_alignment
                }
        
        # System statistics
        system_stats = {
            "total_narrative_contexts": total_contexts,
            "available_themes": len(list(NarrativeTheme)),
            "available_archetypes": len(list(CharacterArchetype)),
            "available_triggers": len(list(QuestTrigger))
        }
        
        return jsonify(create_standardized_response(
            True,
            data={
                "character_statistics": character_stats,
                "system_statistics": system_stats
            },
            message="Dynamic quest statistics retrieved successfully"
        ))
        
    except Exception as e:
        return jsonify(create_standardized_response(
            False, message=f"Failed to retrieve statistics: {str(e)}", error_code="STATISTICS_ERROR"
        )), 500


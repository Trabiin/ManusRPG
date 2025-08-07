"""
Shadowlands RPG - Quest System API Routes
RESTful API endpoints for quest management and progression
"""

from flask import Blueprint, request, jsonify, session
from typing import Dict, Any, List, Optional
import sys
import os

# Add the parent directory to the path to import quest engine
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
from quest_engine_core import QuestEngine, QuestStatus, QuestType, QuestComplexity

# Import shared quest engine
from src.shared_quest_engine import get_quest_engine

# Create Blueprint
quests_bp = Blueprint('quests', __name__)

# Use shared quest engine instance
def get_quest_engine_instance():
    return get_quest_engine()

def create_standardized_response(success: bool, data: Any = None, message: str = "", error_code: str = None) -> Dict[str, Any]:
    """Create standardized API response format"""
    response = {
        "success": success,
        "message": message,
        "timestamp": "2025-07-26T12:00:00Z",
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

@quests_bp.route('/available', methods=['GET'])
def get_available_quests():
    """Get available quest templates for the current character"""
    try:
        character_data = get_character_data_from_session()
        if not character_data:
            return jsonify(create_standardized_response(
                success=False,
                message="No character data found in session",
                error_code="NO_CHARACTER_DATA"
            )), 400
        
        available_quests = quest_engine.get_available_quest_templates(character_data)
        
        return jsonify(create_standardized_response(
            success=True,
            data={
                "available_quests": available_quests,
                "character_level": character_data["level"],
                "total_available": len(available_quests)
            },
            message=f"Found {len(available_quests)} available quest templates"
        ))
        
    except Exception as e:
        return jsonify(create_standardized_response(
            success=False,
            message=f"Error retrieving available quests: {str(e)}",
            error_code="QUEST_RETRIEVAL_ERROR"
        )), 500

@quests_bp.route('/start', methods=['POST'])
def start_quest():
    """Start a new quest for the current character"""
    try:
        character_data = get_character_data_from_session()
        if not character_data:
            return jsonify(create_standardized_response(
                success=False,
                message="No character data found in session",
                error_code="NO_CHARACTER_DATA"
            )), 400
        
        data = request.get_json()
        if not data or 'template_id' not in data:
            return jsonify(create_standardized_response(
                success=False,
                message="Template ID is required",
                error_code="MISSING_TEMPLATE_ID"
            )), 400
        
        template_id = data['template_id']
        quest = quest_engine.create_quest_for_character(template_id, character_data["character_id"], character_data)
        
        if quest:
            return jsonify(create_standardized_response(
                success=True,
                data={
                    "quest": quest.to_dict(),
                    "started": True
                },
                message=f"Successfully started quest: {quest.title}"
            ))
        else:
            return jsonify(create_standardized_response(
                success=False,
                message="Failed to create quest. Template may not exist or character may not meet requirements.",
                error_code="QUEST_CREATION_FAILED"
            )), 400
        
    except Exception as e:
        return jsonify(create_standardized_response(
            success=False,
            message=f"Error starting quest: {str(e)}",
            error_code="QUEST_START_ERROR"
        )), 500

@quests_bp.route('/active', methods=['GET'])
def get_active_quests():
    """Get all active quests for the current character"""
    try:
        character_data = get_character_data_from_session()
        if not character_data:
            return jsonify(create_standardized_response(
                success=False,
                message="No character data found in session",
                error_code="NO_CHARACTER_DATA"
            )), 400
        
        active_quests = quest_engine.get_character_quests(character_data["character_id"], QuestStatus.ACTIVE)
        
        return jsonify(create_standardized_response(
            success=True,
            data={
                "active_quests": [quest.to_dict() for quest in active_quests],
                "total_active": len(active_quests)
            },
            message=f"Retrieved {len(active_quests)} active quests"
        ))
        
    except Exception as e:
        return jsonify(create_standardized_response(
            success=False,
            message=f"Error retrieving active quests: {str(e)}",
            error_code="QUEST_RETRIEVAL_ERROR"
        )), 500

@quests_bp.route('/completed', methods=['GET'])
def get_completed_quests():
    """Get all completed quests for the current character"""
    try:
        character_data = get_character_data_from_session()
        if not character_data:
            return jsonify(create_standardized_response(
                success=False,
                message="No character data found in session",
                error_code="NO_CHARACTER_DATA"
            )), 400
        
        completed_quests = quest_engine.get_character_quests(character_data["character_id"], QuestStatus.COMPLETED)
        
        return jsonify(create_standardized_response(
            success=True,
            data={
                "completed_quests": [quest.to_dict() for quest in completed_quests],
                "total_completed": len(completed_quests)
            },
            message=f"Retrieved {len(completed_quests)} completed quests"
        ))
        
    except Exception as e:
        return jsonify(create_standardized_response(
            success=False,
            message=f"Error retrieving completed quests: {str(e)}",
            error_code="QUEST_RETRIEVAL_ERROR"
        )), 500

@quests_bp.route('/<quest_id>', methods=['GET'])
def get_quest_details(quest_id: str):
    """Get detailed information about a specific quest"""
    try:
        character_data = get_character_data_from_session()
        if not character_data:
            return jsonify(create_standardized_response(
                success=False,
                message="No character data found in session",
                error_code="NO_CHARACTER_DATA"
            )), 400
        
        character_quests = quest_engine.get_character_quests(character_data["character_id"])
        
        for quest in character_quests:
            if quest.quest_id == quest_id:
                return jsonify(create_standardized_response(
                    success=True,
                    data={"quest": quest.to_dict()},
                    message=f"Retrieved quest details for: {quest.title}"
                ))
        
        return jsonify(create_standardized_response(
            success=False,
            message="Quest not found",
            error_code="QUEST_NOT_FOUND"
        )), 404
        
    except Exception as e:
        return jsonify(create_standardized_response(
            success=False,
            message=f"Error retrieving quest details: {str(e)}",
            error_code="QUEST_RETRIEVAL_ERROR"
        )), 500

@quests_bp.route('/<quest_id>/objective/<objective_id>/progress', methods=['POST'])
def update_objective_progress(quest_id: str, objective_id: str):
    """Update progress for a specific quest objective"""
    try:
        character_data = get_character_data_from_session()
        if not character_data:
            return jsonify(create_standardized_response(
                success=False,
                message="No character data found in session",
                error_code="NO_CHARACTER_DATA"
            )), 400
        
        data = request.get_json() or {}
        increment = data.get('increment', 1)
        
        result = quest_engine.update_quest_objective(
            character_data["character_id"], 
            quest_id, 
            objective_id, 
            increment
        )
        
        if result["success"]:
            return jsonify(create_standardized_response(
                success=True,
                data=result,
                message="Objective progress updated successfully"
            ))
        else:
            return jsonify(create_standardized_response(
                success=False,
                message=result.get("error", "Failed to update objective progress"),
                error_code="OBJECTIVE_UPDATE_FAILED"
            )), 400
        
    except Exception as e:
        return jsonify(create_standardized_response(
            success=False,
            message=f"Error updating objective progress: {str(e)}",
            error_code="OBJECTIVE_UPDATE_ERROR"
        )), 500

@quests_bp.route('/<quest_id>/choice/<choice_id>', methods=['POST'])
def make_quest_choice(quest_id: str, choice_id: str):
    """Make a choice in a quest"""
    try:
        character_data = get_character_data_from_session()
        if not character_data:
            return jsonify(create_standardized_response(
                success=False,
                message="No character data found in session",
                error_code="NO_CHARACTER_DATA"
            )), 400
        
        result = quest_engine.make_quest_choice(character_data["character_id"], quest_id, choice_id)
        
        if result["success"]:
            return jsonify(create_standardized_response(
                success=True,
                data=result,
                message="Quest choice made successfully"
            ))
        else:
            return jsonify(create_standardized_response(
                success=False,
                message=result.get("error", "Failed to make quest choice"),
                error_code="CHOICE_FAILED"
            )), 400
        
    except Exception as e:
        return jsonify(create_standardized_response(
            success=False,
            message=f"Error making quest choice: {str(e)}",
            error_code="CHOICE_ERROR"
        )), 500

@quests_bp.route('/statistics', methods=['GET'])
def get_quest_statistics():
    """Get quest engine statistics"""
    try:
        character_data = get_character_data_from_session()
        if not character_data:
            return jsonify(create_standardized_response(
                success=False,
                message="No character data found in session",
                error_code="NO_CHARACTER_DATA"
            )), 400
        
        engine_stats = quest_engine.get_engine_statistics()
        
        # Get character-specific statistics
        character_id = character_data["character_id"]
        active_quests = quest_engine.get_character_quests(character_id, QuestStatus.ACTIVE)
        completed_quests = quest_engine.get_character_quests(character_id, QuestStatus.COMPLETED)
        
        character_stats = {
            "character_active_quests": len(active_quests),
            "character_completed_quests": len(completed_quests),
            "character_total_quests": len(active_quests) + len(completed_quests),
            "character_level": character_data["level"],
            "character_name": character_data["name"]
        }
        
        return jsonify(create_standardized_response(
            success=True,
            data={
                "engine_statistics": engine_stats,
                "character_statistics": character_stats
            },
            message="Quest statistics retrieved successfully"
        ))
        
    except Exception as e:
        return jsonify(create_standardized_response(
            success=False,
            message=f"Error retrieving quest statistics: {str(e)}",
            error_code="STATISTICS_ERROR"
        )), 500

@quests_bp.route('/templates', methods=['GET'])
def get_quest_templates():
    """Get all available quest templates (admin/debug endpoint)"""
    try:
        templates = []
        for template_id, template in quest_engine.quest_templates.items():
            templates.append({
                "template_id": template_id,
                "quest_type": template.quest_type.value,
                "complexity": template.complexity.value,
                "title": template.title,
                "description": template.description,
                "level_requirement": template.level_requirement,
                "objectives_count": len(template.objectives_templates),
                "choices_count": len(template.choices_templates),
                "rewards_count": len(template.rewards_templates)
            })
        
        return jsonify(create_standardized_response(
            success=True,
            data={
                "templates": templates,
                "total_templates": len(templates)
            },
            message=f"Retrieved {len(templates)} quest templates"
        ))
        
    except Exception as e:
        return jsonify(create_standardized_response(
            success=False,
            message=f"Error retrieving quest templates: {str(e)}",
            error_code="TEMPLATE_RETRIEVAL_ERROR"
        )), 500

# Error handlers for the blueprint
@quests_bp.errorhandler(404)
def quest_not_found(error):
    return jsonify(create_standardized_response(
        success=False,
        message="Quest endpoint not found",
        error_code="ENDPOINT_NOT_FOUND"
    )), 404

@quests_bp.errorhandler(405)
def method_not_allowed(error):
    return jsonify(create_standardized_response(
        success=False,
        message="HTTP method not allowed for this quest endpoint",
        error_code="METHOD_NOT_ALLOWED"
    )), 405

@quests_bp.errorhandler(500)
def internal_server_error(error):
    return jsonify(create_standardized_response(
        success=False,
        message="Internal server error in quest system",
        error_code="INTERNAL_SERVER_ERROR"
    )), 500


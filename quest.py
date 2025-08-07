from flask import Blueprint, jsonify, request, session
from quest_system import quest_manager, QuestStatus

quest_bp = Blueprint('quest', __name__)

@quest_bp.route('/api/quests/available', methods=['GET'])
def get_available_quests():
    """Get all quests available to the current character"""
    try:
        character_data = session.get('character')
        if not character_data:
            return jsonify({"error": "No character selected"}), 400
            
        character_id = character_data.get('character_id')
        
        # Get character data for quest availability checking
        quest_character_data = get_character_data(character_id)
        if not quest_character_data:
            return jsonify({"error": "Character data not found"}), 404
            
        available_quests = quest_manager.get_available_quests(quest_character_data)
        
        quest_list = []
        for quest in available_quests:
            quest_dict = quest.to_dict()
            quest_dict["state"] = quest_manager.get_character_quest_state(character_id, quest.quest_id)
            quest_list.append(quest_dict)
            
        return jsonify({
            "success": True,
            "available_quests": quest_list,
            "count": len(quest_list)
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@quest_bp.route('/api/quests/active', methods=['GET'])
def get_active_quests():
    """Get all active quests for the current character"""
    try:
        character_id = session.get('character_id')
        if not character_id:
            return jsonify({"error": "No character selected"}), 400
            
        active_quests = quest_manager.get_character_active_quests(character_id)
        
        return jsonify({
            "success": True,
            "active_quests": active_quests,
            "count": len(active_quests)
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@quest_bp.route('/api/quests/<quest_id>/start', methods=['POST'])
def start_quest(quest_id):
    """Start a specific quest"""
    try:
        character_id = session.get('character_id')
        if not character_id:
            return jsonify({"error": "No character selected"}), 400
            
        # Check if quest exists
        if quest_id not in quest_manager.quests:
            return jsonify({"error": "Quest not found"}), 404
            
        # Get character data to check availability
        character_data = get_character_data(character_id)
        quest = quest_manager.quests[quest_id]
        
        if not quest_manager.check_quest_availability(quest, character_data):
            return jsonify({"error": "Quest not available"}), 400
            
        result = quest_manager.start_quest(character_id, quest_id)
        
        if result["success"]:
            return jsonify({
                "success": True,
                "message": f"Quest '{quest.title}' started successfully",
                "quest": result["quest"],
                "state": result["state"]
            })
        else:
            return jsonify({"error": result["error"]}), 400
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@quest_bp.route('/api/quests/<quest_id>/progress', methods=['POST'])
def update_quest_progress():
    """Update progress on a quest objective"""
    try:
        character_id = session.get('character_id')
        if not character_id:
            return jsonify({"error": "No character selected"}), 400
            
        data = request.get_json()
        quest_id = data.get('quest_id')
        objective_id = data.get('objective_id')
        progress_increment = data.get('progress_increment', 1)
        
        if not quest_id or not objective_id:
            return jsonify({"error": "Missing quest_id or objective_id"}), 400
            
        result = quest_manager.update_objective_progress(
            character_id, quest_id, objective_id, progress_increment
        )
        
        if result["success"]:
            response_data = {
                "success": True,
                "objective_completed": result.get("objective_completed", False)
            }
            
            if result.get("quest_completed"):
                response_data["quest_completed"] = True
                response_data["rewards"] = result.get("rewards", [])
                
            return jsonify(response_data)
        else:
            return jsonify({"error": result["error"]}), 400
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@quest_bp.route('/api/quests/<quest_id>/choice', methods=['POST'])
def make_quest_choice(quest_id):
    """Make a choice during a quest"""
    try:
        character_id = session.get('character_id')
        if not character_id:
            return jsonify({"error": "No character selected"}), 400
            
        data = request.get_json()
        choice_id = data.get('choice_id')
        choice_value = data.get('choice_value')
        
        if not choice_id or choice_value is None:
            return jsonify({"error": "Missing choice_id or choice_value"}), 400
            
        result = quest_manager.make_quest_choice(character_id, quest_id, choice_id, choice_value)
        
        # Process any immediate consequences of the choice
        consequences = process_quest_choice_consequences(character_id, quest_id, choice_id, choice_value)
        
        return jsonify({
            "success": True,
            "choice_recorded": True,
            "consequences": consequences
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@quest_bp.route('/api/quests/<quest_id>', methods=['GET'])
def get_quest_details(quest_id):
    """Get detailed information about a specific quest"""
    try:
        character_id = session.get('character_id')
        if not character_id:
            return jsonify({"error": "No character selected"}), 400
            
        if quest_id not in quest_manager.quests:
            return jsonify({"error": "Quest not found"}), 404
            
        quest = quest_manager.quests[quest_id]
        quest_state = quest_manager.get_character_quest_state(character_id, quest_id)
        
        quest_data = quest.to_dict()
        quest_data["state"] = quest_state
        
        return jsonify({
            "success": True,
            "quest": quest_data
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@quest_bp.route('/api/quests/trigger', methods=['POST'])
def trigger_quest_event():
    """Trigger a quest-related event (used by other systems)"""
    try:
        character_id = session.get('character_id')
        if not character_id:
            return jsonify({"error": "No character selected"}), 400
            
        data = request.get_json()
        event_type = data.get('event_type')
        event_data = data.get('event_data', {})
        
        # Process different types of quest events
        results = []
        
        if event_type == "npc_interaction":
            results = handle_npc_interaction_events(character_id, event_data)
        elif event_type == "location_visit":
            results = handle_location_visit_events(character_id, event_data)
        elif event_type == "item_collection":
            results = handle_item_collection_events(character_id, event_data)
        elif event_type == "combat_victory":
            results = handle_combat_victory_events(character_id, event_data)
        elif event_type == "action_completion":
            results = handle_action_completion_events(character_id, event_data)
        
        return jsonify({
            "success": True,
            "events_processed": len(results),
            "results": results
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@quest_bp.route('/api/quests/journal', methods=['GET'])
def get_quest_journal():
    """Get the complete quest journal for a character"""
    try:
        character_id = session.get('character_id')
        if not character_id:
            return jsonify({"error": "No character selected"}), 400
            
        # Get all quest states for the character
        character_quest_states = quest_manager.character_quest_states.get(character_id, {})
        
        journal = {
            "active_quests": [],
            "completed_quests": [],
            "failed_quests": [],
            "available_quests": []
        }
        
        # Get character data for availability checking
        character_data = get_character_data(character_id)
        
        for quest_id, quest_state in character_quest_states.items():
            quest = quest_manager.quests.get(quest_id)
            if not quest:
                continue
                
            quest_data = quest.to_dict()
            quest_data["state"] = quest_state
            
            if quest_state["status"] == QuestStatus.ACTIVE.value:
                journal["active_quests"].append(quest_data)
            elif quest_state["status"] == QuestStatus.COMPLETED.value:
                journal["completed_quests"].append(quest_data)
            elif quest_state["status"] == QuestStatus.FAILED.value:
                journal["failed_quests"].append(quest_data)
                
        # Add available quests
        available_quests = quest_manager.get_available_quests(character_data)
        for quest in available_quests:
            quest_data = quest.to_dict()
            quest_data["state"] = quest_manager.get_character_quest_state(character_id, quest.quest_id)
            journal["available_quests"].append(quest_data)
            
        return jsonify({
            "success": True,
            "journal": journal,
            "statistics": {
                "active_count": len(journal["active_quests"]),
                "completed_count": len(journal["completed_quests"]),
                "failed_count": len(journal["failed_quests"]),
                "available_count": len(journal["available_quests"])
            }
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Helper functions

def get_character_data(character_id):
    """Get character data for quest availability checking"""
    from flask import session
    
    # Get character data from session
    character_data = session.get('character')
    if not character_data:
        return None
        
    # Convert to quest system format
    return {
        "character_id": character_data.get('character_id'),
        "level": character_data.get('level', 1),
        "corruption": character_data.get('corruption', 0),
        "faction_standings": character_data.get('faction_standings', {
            "havens_rest": 0,
            "luminous_order": 0,
            "shadow_court": 0
        }),
        "visited_locations": character_data.get('visited_locations', [character_data.get('current_location', 'havens_rest')]),
        "npc_relationships": character_data.get('npc_relationships', {}),
        "inventory": character_data.get('inventory', []),
        "skills": character_data.get('skills', {
            "combat": character_data.get('combat_experience', 0) // 10,
            "diplomacy": 1,
            "corruption_knowledge": min(character_data.get('corruption', 0) // 10, 5)
        })
    }

def process_quest_choice_consequences(character_id, quest_id, choice_id, choice_value):
    """Process the consequences of a quest choice"""
    consequences = []
    
    # This would contain the logic for different quest choices
    # For now, return basic consequence information
    if quest_id == "side_missing_merchant" and choice_id == "bandit_resolution":
        if choice_value == "negotiate":
            consequences.append({
                "type": "reputation_change",
                "target": "havens_rest",
                "value": 10,
                "description": "Your diplomatic approach impressed the villagers"
            })
        elif choice_value == "combat":
            consequences.append({
                "type": "reputation_change",
                "target": "havens_rest",
                "value": 5,
                "description": "You solved the problem, but some question your methods"
            })
            
    return consequences

def handle_npc_interaction_events(character_id, event_data):
    """Handle NPC interaction events for quest progression"""
    results = []
    npc_id = event_data.get('npc_id')
    
    # Check all active quests for NPC interaction objectives
    active_quests = quest_manager.get_character_active_quests(character_id)
    
    for quest_data in active_quests:
        quest_id = quest_data['quest_id']
        for objective in quest_data['objectives']:
            if (objective['type'] == 'talk_to_npc' and 
                objective['target'] == npc_id and 
                not quest_data['state']['objectives'][objective['id']]['completed']):
                
                result = quest_manager.update_objective_progress(character_id, quest_id, objective['id'])
                results.append(result)
                
    return results

def handle_location_visit_events(character_id, event_data):
    """Handle location visit events for quest progression"""
    results = []
    location_id = event_data.get('location_id')
    
    active_quests = quest_manager.get_character_active_quests(character_id)
    
    for quest_data in active_quests:
        quest_id = quest_data['quest_id']
        for objective in quest_data['objectives']:
            if (objective['type'] == 'visit_location' and 
                objective['target'] == location_id and 
                not quest_data['state']['objectives'][objective['id']]['completed']):
                
                result = quest_manager.update_objective_progress(character_id, quest_id, objective['id'])
                results.append(result)
                
    return results

def handle_item_collection_events(character_id, event_data):
    """Handle item collection events for quest progression"""
    results = []
    item_id = event_data.get('item_id')
    quantity = event_data.get('quantity', 1)
    
    active_quests = quest_manager.get_character_active_quests(character_id)
    
    for quest_data in active_quests:
        quest_id = quest_data['quest_id']
        for objective in quest_data['objectives']:
            if (objective['type'] == 'collect_item' and 
                objective['target'] == item_id and 
                not quest_data['state']['objectives'][objective['id']]['completed']):
                
                result = quest_manager.update_objective_progress(character_id, quest_id, objective['id'], quantity)
                results.append(result)
                
    return results

def handle_combat_victory_events(character_id, event_data):
    """Handle combat victory events for quest progression"""
    results = []
    enemy_type = event_data.get('enemy_type')
    
    active_quests = quest_manager.get_character_active_quests(character_id)
    
    for quest_data in active_quests:
        quest_id = quest_data['quest_id']
        for objective in quest_data['objectives']:
            if (objective['type'] == 'defeat_enemy' and 
                objective['target'] == enemy_type and 
                not quest_data['state']['objectives'][objective['id']]['completed']):
                
                result = quest_manager.update_objective_progress(character_id, quest_id, objective['id'])
                results.append(result)
                
    return results

def handle_action_completion_events(character_id, event_data):
    """Handle action completion events for quest progression"""
    results = []
    action_id = event_data.get('action_id')
    
    active_quests = quest_manager.get_character_active_quests(character_id)
    
    for quest_data in active_quests:
        quest_id = quest_data['quest_id']
        for objective in quest_data['objectives']:
            if (objective['type'] == 'complete_action' and 
                objective['target'] == action_id and 
                not quest_data['state']['objectives'][objective['id']]['completed']):
                
                result = quest_manager.update_objective_progress(character_id, quest_id, objective['id'])
                results.append(result)
                
    return results


from flask import Blueprint, jsonify, session, request
from narrative_integration import narrative_integration

narrative_bp = Blueprint('narrative', __name__)

@narrative_bp.route('/api/narrative/character-status', methods=['GET'])
def get_character_narrative_status():
    """Get the character's current narrative status and reputation"""
    try:
        character_data = session.get('character')
        if not character_data:
            return jsonify({"error": "No character selected"}), 400
            
        character_id = character_data.get('character_id')
        
        # Get comprehensive narrative status
        reputation_summary = narrative_integration.get_character_reputation_summary(character_id)
        
        # Get corruption narrative triggers
        corruption = character_data.get('corruption', 0)
        corruption_triggers = narrative_integration.check_corruption_narrative_triggers(character_id, corruption)
        
        # Get narrative flags and unlocked content
        narrative_flags = character_data.get('narrative_flags', [])
        unlocked_content = character_data.get('unlocked_content', [])
        
        return jsonify({
            "character_id": character_id,
            "reputation_summary": reputation_summary,
            "corruption_triggers": corruption_triggers,
            "narrative_flags": narrative_flags,
            "unlocked_content": unlocked_content,
            "corruption_level": corruption
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@narrative_bp.route('/api/narrative/dialogue-options/<npc_id>', methods=['GET'])
def get_enhanced_dialogue_options(npc_id):
    """Get dialogue options enhanced by narrative state"""
    try:
        character_data = session.get('character')
        if not character_data:
            return jsonify({"error": "No character selected"}), 400
            
        character_id = character_data.get('character_id')
        
        # Base dialogue options (would normally come from NPC system)
        base_options = get_base_dialogue_options(npc_id)
        
        # Enhance with narrative state
        enhanced_options = narrative_integration.get_available_dialogue_options(
            character_id, npc_id, base_options
        )
        
        return jsonify({
            "npc_id": npc_id,
            "dialogue_options": enhanced_options
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@narrative_bp.route('/api/narrative/process-quest-completion', methods=['POST'])
def process_quest_completion():
    """Process narrative consequences of quest completion"""
    try:
        character_data = session.get('character')
        if not character_data:
            return jsonify({"error": "No character selected"}), 400
            
        character_id = character_data.get('character_id')
        
        data = request.get_json()
        quest_id = data.get('quest_id')
        choices_made = data.get('choices_made', {})
        
        if not quest_id:
            return jsonify({"error": "Quest ID required"}), 400
            
        # Process narrative consequences
        consequences = narrative_integration.process_quest_completion(
            character_id, quest_id, choices_made
        )
        
        return jsonify({
            "quest_id": quest_id,
            "consequences": consequences,
            "message": "Quest consequences processed successfully"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@narrative_bp.route('/api/narrative/corruption-check', methods=['POST'])
def check_corruption_triggers():
    """Check for corruption-based narrative triggers"""
    try:
        character_data = session.get('character')
        if not character_data:
            return jsonify({"error": "No character selected"}), 400
            
        character_id = character_data.get('character_id')
        corruption = character_data.get('corruption', 0)
        
        # Check for new triggers
        triggers = narrative_integration.check_corruption_narrative_triggers(character_id, corruption)
        
        return jsonify({
            "character_id": character_id,
            "current_corruption": corruption,
            "new_triggers": triggers
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@narrative_bp.route('/api/narrative/world-state', methods=['GET'])
def get_world_state():
    """Get the current state of the world based on player actions"""
    try:
        character_data = session.get('character')
        if not character_data:
            return jsonify({"error": "No character selected"}), 400
            
        character_id = character_data.get('character_id')
        
        # Get character's impact on the world
        character_state = narrative_integration._get_character_narrative_state(character_id)
        world_impacts = character_state.get("world_impact", [])
        
        # Organize world state by location
        world_state = {
            "havens_rest": {
                "well_status": "normal",
                "community_mood": "cautious",
                "leadership_style": "traditional"
            },
            "shadowmere_woods": {
                "exploration_level": "minimal",
                "corruption_understanding": "basic"
            },
            "ancient_ruins": {
                "research_progress": "beginning",
                "artifact_status": "undisturbed"
            }
        }
        
        # Apply world impacts
        for impact in world_impacts:
            location_key = None
            if "havens_rest" in impact.get("change", ""):
                location_key = "havens_rest"
            elif "woods" in impact.get("change", ""):
                location_key = "shadowmere_woods"
            elif "ruins" in impact.get("change", ""):
                location_key = "ancient_ruins"
                
            if location_key and location_key in world_state:
                change_key = impact.get("change", "").split("_")[-1]
                world_state[location_key][change_key] = impact.get("value")
        
        return jsonify({
            "world_state": world_state,
            "total_impacts": len(world_impacts),
            "character_influence": narrative_integration._assess_world_impact(character_id)
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_base_dialogue_options(npc_id):
    """Get base dialogue options for an NPC (placeholder function)"""
    # This would normally integrate with the NPC system
    base_options = {
        "elder_marta": [
            {"id": "greeting", "text": "Hello, Elder Marta."},
            {"id": "village_status", "text": "How is the village faring?"},
            {"id": "advice", "text": "I could use your wisdom."}
        ],
        "captain_sarah": [
            {"id": "greeting", "text": "Captain Sarah."},
            {"id": "training", "text": "I'd like some combat training."},
            {"id": "threats", "text": "What threats face the village?"}
        ],
        "brother_thomas": [
            {"id": "greeting", "text": "Greetings, Brother Thomas."},
            {"id": "spiritual_guidance", "text": "I seek spiritual guidance."},
            {"id": "corruption_help", "text": "I'm concerned about corruption."}
        ]
    }
    
    return base_options.get(npc_id, [
        {"id": "greeting", "text": "Hello."},
        {"id": "general", "text": "How are you?"}
    ])


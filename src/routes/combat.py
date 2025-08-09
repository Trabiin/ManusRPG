"""
Combat API Routes for Shadowlands RPG Backend
Provides comprehensive REST API for the advanced combat system
"""

from flask import Blueprint, request, jsonify, session
from functools import wraps
import sys
import os
import traceback
from datetime import datetime

# Add the parent directory to the path to import our combat systems
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from integrated_combat_system import IntegratedCombatSystem
from abilities_and_status_effects import AbilityRegistry
from combat_ai_system import AIPersonality

# Create blueprint
combat_bp = Blueprint('combat', __name__, url_prefix='/api/combat')

# Global combat system instance
combat_system = IntegratedCombatSystem()
ability_registry = AbilityRegistry()

def require_session(f):
    """Decorator to require active session"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'character_id' not in session:
            return jsonify({'error': 'No active session'}), 401
        return f(*args, **kwargs)
    return decorated_function

def handle_api_error(f):
    """Decorator to handle API errors gracefully"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            print(f"API Error in {f.__name__}: {str(e)}")
            print(traceback.format_exc())
            return jsonify({
                'error': 'Internal server error',
                'message': str(e),
                'timestamp': datetime.utcnow().isoformat()
            }), 500
    return decorated_function

# ============================================================================
# ENCOUNTER MANAGEMENT ENDPOINTS
# ============================================================================

@combat_bp.route('/encounters', methods=['POST'])
@require_session
@handle_api_error
def create_encounter():
    """Create a new combat encounter"""
    data = request.get_json()
    
    # Validate required fields
    if not data or 'encounter_template' not in data:
        return jsonify({'error': 'encounter_template is required'}), 400
    
    encounter_template = data['encounter_template']
    difficulty_override = data.get('difficulty_override')
    
    # Get player characters from session or request
    player_characters = data.get('player_characters', [])
    if not player_characters:
        # Create default player character from session
        character_id = session.get('character_id')
        if character_id:
            # This would normally fetch from database
            player_characters = [{
                'character_id': character_id,
                'name': session.get('character_name', 'Player'),
                'attributes': session.get('character_attributes', {
                    'might': 12, 'intellect': 12, 'will': 12, 'shadow': 0
                }),
                'derived_attributes': {
                    'health': 150, 'mana': 100, 'action_points': 4
                },
                'level': session.get('character_level', 1),
                'corruption': {'points': session.get('corruption_points', 0)}
            }]
    
    if not player_characters:
        return jsonify({'error': 'No player characters available'}), 400
    
    # Create encounter
    encounter_id = combat_system.create_encounter(
        encounter_template, 
        player_characters, 
        difficulty_override
    )
    
    return jsonify({
        'encounter_id': encounter_id,
        'status': 'created',
        'encounter_template': encounter_template,
        'player_count': len(player_characters),
        'timestamp': datetime.utcnow().isoformat()
    }), 201

@combat_bp.route('/encounters/<encounter_id>/start', methods=['POST'])
@require_session
@handle_api_error
def start_encounter(encounter_id):
    """Start a combat encounter"""
    result = combat_system.start_encounter(encounter_id)
    
    if 'error' in result:
        return jsonify(result), 404
    
    return jsonify({
        'encounter_id': encounter_id,
        'combat_started': True,
        'turn_order': result.get('turn_order', []),
        'current_participant': result.get('current_participant'),
        'round_number': result.get('round_number', 1),
        'timestamp': datetime.utcnow().isoformat()
    })

@combat_bp.route('/encounters/<encounter_id>/state', methods=['GET'])
@require_session
@handle_api_error
def get_encounter_state(encounter_id):
    """Get the current state of a combat encounter"""
    state = combat_system.get_encounter_state(encounter_id)
    
    if 'error' in state:
        return jsonify(state), 404
    
    return jsonify(state)

@combat_bp.route('/encounters/<encounter_id>/end', methods=['POST'])
@require_session
@handle_api_error
def end_encounter(encounter_id):
    """End a combat encounter"""
    result = combat_system.end_encounter(encounter_id)
    
    if 'error' in result:
        return jsonify(result), 404
    
    return jsonify(result)

# ============================================================================
# COMBAT ACTION ENDPOINTS
# ============================================================================

@combat_bp.route('/encounters/<encounter_id>/actions/player', methods=['POST'])
@require_session
@handle_api_error
def process_player_action(encounter_id):
    """Process a player action in combat"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Action data is required'}), 400
    
    # Validate action data
    required_fields = ['actor_id', 'action_type']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400
    
    # Process the action
    result = combat_system.process_player_action(encounter_id, data)
    
    if not result.get('success', False):
        return jsonify(result), 400
    
    return jsonify({
        'action_processed': True,
        'encounter_id': encounter_id,
        'result': result,
        'timestamp': datetime.utcnow().isoformat()
    })

@combat_bp.route('/encounters/<encounter_id>/actions/ai/<participant_id>', methods=['POST'])
@require_session
@handle_api_error
def process_ai_action(encounter_id, participant_id):
    """Process an AI participant's action"""
    result = combat_system.process_ai_turn(encounter_id, participant_id)
    
    if not result.get('success', False):
        return jsonify(result), 400
    
    return jsonify({
        'ai_action_processed': True,
        'encounter_id': encounter_id,
        'participant_id': participant_id,
        'result': result,
        'timestamp': datetime.utcnow().isoformat()
    })

@combat_bp.route('/encounters/<encounter_id>/turn/advance', methods=['POST'])
@require_session
@handle_api_error
def advance_turn(encounter_id):
    """Advance to the next turn in combat"""
    result = combat_system.advance_turn(encounter_id)
    
    if 'error' in result:
        return jsonify(result), 400
    
    return jsonify({
        'turn_advanced': True,
        'encounter_id': encounter_id,
        'round_number': result.get('round_number'),
        'current_participant': result.get('current_participant'),
        'timestamp': datetime.utcnow().isoformat()
    })

# ============================================================================
# ABILITIES AND STATUS EFFECTS ENDPOINTS
# ============================================================================

@combat_bp.route('/abilities', methods=['GET'])
@handle_api_error
def get_abilities():
    """Get all available abilities"""
    abilities = {}
    for ability_id, ability in ability_registry.abilities.items():
        abilities[ability_id] = {
            'ability_id': ability.ability_id,
            'name': ability.name,
            'description': ability.description,
            'ability_type': ability.ability_type.value,
            'target_type': ability.target_type.value,
            'action_cost': ability.action_cost,
            'mana_cost': ability.mana_cost,
            'corruption_cost': ability.corruption_cost,
            'level_requirement': ability.level_requirement,
            'attribute_requirements': ability.attribute_requirements,
            'corruption_requirement': ability.corruption_requirement,
            'range_value': ability.range_value,
            'area_size': ability.area_size,
            'cooldown': ability.cooldown
        }
    
    return jsonify({
        'abilities': abilities,
        'total_count': len(abilities)
    })

@combat_bp.route('/abilities/<ability_id>', methods=['GET'])
@handle_api_error
def get_ability_details(ability_id):
    """Get detailed information about a specific ability"""
    ability = ability_registry.get_ability(ability_id)
    
    if not ability:
        return jsonify({'error': 'Ability not found'}), 404
    
    # Convert effects to serializable format
    effects = []
    for effect in ability.effects:
        effect_data = {
            'effect_type': effect.effect_type,
            'value': effect.value,
            'duration': effect.duration,
            'scaling_attribute': effect.scaling_attribute,
            'scaling_factor': effect.scaling_factor,
            'conditions': effect.conditions
        }
        if effect.damage_type:
            effect_data['damage_type'] = effect.damage_type.value
        effects.append(effect_data)
    
    return jsonify({
        'ability_id': ability.ability_id,
        'name': ability.name,
        'description': ability.description,
        'ability_type': ability.ability_type.value,
        'target_type': ability.target_type.value,
        'effects': effects,
        'action_cost': ability.action_cost,
        'mana_cost': ability.mana_cost,
        'corruption_cost': ability.corruption_cost,
        'health_cost': ability.health_cost,
        'level_requirement': ability.level_requirement,
        'attribute_requirements': ability.attribute_requirements,
        'corruption_requirement': ability.corruption_requirement,
        'range_value': ability.range_value,
        'area_size': ability.area_size,
        'cooldown': ability.cooldown,
        'cast_time': ability.cast_time,
        'scaling_attributes': ability.scaling_attributes,
        'critical_chance': ability.critical_chance,
        'critical_multiplier': ability.critical_multiplier
    })

@combat_bp.route('/abilities/available', methods=['POST'])
@require_session
@handle_api_error
def get_available_abilities():
    """Get abilities available to a character"""
    data = request.get_json()
    
    # Use session data if not provided
    character_attributes = data.get('attributes', session.get('character_attributes', {}))
    character_level = data.get('level', session.get('character_level', 1))
    corruption_points = data.get('corruption_points', session.get('corruption_points', 0))
    
    available_abilities = ability_registry.get_available_abilities(
        character_attributes, character_level, corruption_points
    )
    
    # Get detailed info for available abilities
    abilities_details = {}
    for ability_id in available_abilities:
        ability = ability_registry.get_ability(ability_id)
        if ability:
            abilities_details[ability_id] = {
                'name': ability.name,
                'description': ability.description,
                'ability_type': ability.ability_type.value,
                'action_cost': ability.action_cost,
                'mana_cost': ability.mana_cost,
                'corruption_cost': ability.corruption_cost
            }
    
    return jsonify({
        'available_abilities': available_abilities,
        'abilities_details': abilities_details,
        'character_level': character_level,
        'corruption_points': corruption_points
    })

@combat_bp.route('/status-effects', methods=['GET'])
@handle_api_error
def get_status_effects():
    """Get all status effects"""
    status_effects = {}
    for effect_id, effect in ability_registry.status_effects.items():
        status_effects[effect_id] = {
            'effect_id': effect.effect_id,
            'name': effect.name,
            'description': effect.description,
            'effect_type': effect.effect_type.value,
            'duration': effect.duration,
            'damage_per_turn': effect.damage_per_turn,
            'healing_per_turn': effect.healing_per_turn,
            'attribute_modifiers': effect.attribute_modifiers,
            'damage_modifiers': effect.damage_modifiers,
            'stacks': effect.stacks,
            'max_stacks': effect.max_stacks,
            'dispellable': effect.dispellable,
            'visual_effect': effect.visual_effect
        }
    
    return jsonify({
        'status_effects': status_effects,
        'total_count': len(status_effects)
    })

# ============================================================================
# COMBAT STATISTICS AND ANALYTICS ENDPOINTS
# ============================================================================

@combat_bp.route('/statistics', methods=['GET'])
@handle_api_error
def get_combat_statistics():
    """Get comprehensive combat system statistics"""
    stats = combat_system.get_system_statistics()
    return jsonify(stats)

@combat_bp.route('/encounters/<encounter_id>/statistics', methods=['GET'])
@require_session
@handle_api_error
def get_encounter_statistics(encounter_id):
    """Get statistics for a specific encounter"""
    encounter = combat_system.active_encounters.get(encounter_id)
    if not encounter:
        return jsonify({'error': 'Encounter not found'}), 404
    
    stats = encounter.get_encounter_statistics()
    return jsonify(stats)

@combat_bp.route('/ai/personalities', methods=['GET'])
@handle_api_error
def get_ai_personalities():
    """Get available AI personality types"""
    personalities = {}
    for personality in AIPersonality:
        personalities[personality.value] = {
            'name': personality.value.title(),
            'description': f"AI with {personality.value} behavior patterns"
        }
    
    return jsonify({
        'personalities': personalities,
        'total_count': len(personalities)
    })

# ============================================================================
# ENCOUNTER TEMPLATES ENDPOINTS
# ============================================================================

@combat_bp.route('/templates', methods=['GET'])
@handle_api_error
def get_encounter_templates():
    """Get available encounter templates"""
    templates = {
        'basic_bandits': {
            'name': 'Basic Bandits',
            'description': 'A group of common bandits',
            'difficulty': 'Easy',
            'enemy_count': '2-3',
            'recommended_level': '1-3'
        },
        'corrupted_guards': {
            'name': 'Corrupted Guards',
            'description': 'Former guards consumed by shadow',
            'difficulty': 'Medium',
            'enemy_count': '2-4',
            'recommended_level': '3-5'
        },
        'shadow_cultists': {
            'name': 'Shadow Cultists',
            'description': 'Cultists wielding dark magic',
            'difficulty': 'Hard',
            'enemy_count': '3-5',
            'recommended_level': '5-8'
        },
        'ancient_beast': {
            'name': 'Ancient Beast',
            'description': 'A powerful corrupted creature',
            'difficulty': 'Boss',
            'enemy_count': '1',
            'recommended_level': '8-10'
        }
    }
    
    return jsonify({
        'templates': templates,
        'total_count': len(templates)
    })

# ============================================================================
# COMBAT VALIDATION AND TESTING ENDPOINTS
# ============================================================================

@combat_bp.route('/validate', methods=['POST'])
@handle_api_error
def validate_combat_action():
    """Validate a combat action without executing it"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Validation data is required'}), 400
    
    # Basic validation logic
    action_type = data.get('action_type')
    actor_id = data.get('actor_id')
    
    validation_result = {
        'valid': True,
        'errors': [],
        'warnings': []
    }
    
    # Validate action type
    valid_actions = ['attack', 'ability', 'move', 'defend', 'wait']
    if action_type not in valid_actions:
        validation_result['valid'] = False
        validation_result['errors'].append(f'Invalid action type: {action_type}')
    
    # Validate ability if specified
    if action_type == 'ability':
        ability_id = data.get('ability_id')
        if not ability_id:
            validation_result['valid'] = False
            validation_result['errors'].append('ability_id is required for ability actions')
        elif not ability_registry.get_ability(ability_id):
            validation_result['valid'] = False
            validation_result['errors'].append(f'Unknown ability: {ability_id}')
    
    return jsonify(validation_result)

@combat_bp.route('/test/encounter', methods=['POST'])
@handle_api_error
def test_encounter():
    """Create and run a test encounter for validation"""
    data = request.get_json() or {}
    
    # Create test player character
    test_player = {
        'name': 'Test Character',
        'attributes': {'might': 14, 'intellect': 12, 'will': 10, 'shadow': 0},
        'derived_attributes': {'health': 150, 'mana': 100, 'action_points': 4},
        'level': 3,
        'corruption': {'points': 0}
    }
    
    # Create test encounter
    template = data.get('template', 'basic_bandits')
    encounter_id = combat_system.create_encounter(template, [test_player])
    
    # Start combat
    start_result = combat_system.start_encounter(encounter_id)
    
    # Get initial state
    initial_state = combat_system.get_encounter_state(encounter_id)
    
    # End encounter
    end_result = combat_system.end_encounter(encounter_id)
    
    return jsonify({
        'test_completed': True,
        'encounter_id': encounter_id,
        'start_result': start_result,
        'initial_state': {
            'participant_count': len(initial_state.get('participants', {})),
            'round_number': initial_state.get('round_number'),
            'current_participant': initial_state.get('current_participant')
        },
        'end_result': end_result,
        'timestamp': datetime.utcnow().isoformat()
    })

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@combat_bp.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Combat endpoint not found'}), 404

@combat_bp.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'error': 'Method not allowed for this combat endpoint'}), 405

@combat_bp.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal combat system error'}), 500

# ============================================================================
# HEALTH CHECK ENDPOINT
# ============================================================================

@combat_bp.route('/health', methods=['GET'])
def health_check():
    """Health check for combat system"""
    try:
        # Test basic functionality
        stats = combat_system.get_system_statistics()
        ability_count = len(ability_registry.abilities)
        
        return jsonify({
            'status': 'healthy',
            'combat_system': 'operational',
            'active_encounters': stats.get('active_encounters', 0),
            'total_abilities': ability_count,
            'timestamp': datetime.utcnow().isoformat()
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500


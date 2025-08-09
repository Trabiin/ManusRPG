"""
ManusRPG Location Routes
Flask blueprint for location and world management endpoints.
"""

from flask import Blueprint, request, jsonify, session
from datetime import datetime

# Create Blueprint
location_bp = Blueprint('location', __name__, url_prefix='/api/location')

# Sample location data (in a real app, this would come from a database)
SAMPLE_LOCATIONS = {
    'shadowlands_entrance': {
        'id': 'shadowlands_entrance',
        'name': 'Shadowlands Entrance',
        'description': 'A mysterious portal leading to the dark realm of shadows.',
        'type': 'portal',
        'coordinates': {'x': 0, 'y': 0},
        'available_actions': ['enter', 'examine', 'rest']
    },
    'shadow_forest': {
        'id': 'shadow_forest',
        'name': 'Shadow Forest',
        'description': 'A dark forest where shadows move independently of their sources.',
        'type': 'wilderness',
        'coordinates': {'x': 1, 'y': 0},
        'available_actions': ['explore', 'hunt', 'gather', 'rest']
    },
    'abandoned_village': {
        'id': 'abandoned_village',
        'name': 'Abandoned Village',
        'description': 'Once a thriving settlement, now empty and haunted.',
        'type': 'settlement',
        'coordinates': {'x': 0, 'y': 1},
        'available_actions': ['search', 'investigate', 'rest', 'trade']
    }
}

@location_bp.route('/list', methods=['GET'])
def get_locations():
    """Get list of all available locations."""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'No user session found'}), 401
        
        return jsonify({
            'success': True,
            'locations': list(SAMPLE_LOCATIONS.values())
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to get locations: {str(e)}'}), 500

@location_bp.route('/<location_id>', methods=['GET'])
def get_location(location_id):
    """Get details for a specific location."""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'No user session found'}), 401
        
        location = SAMPLE_LOCATIONS.get(location_id)
        if not location:
            return jsonify({'error': 'Location not found'}), 404
        
        return jsonify({
            'success': True,
            'location': location
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to get location: {str(e)}'}), 500

@location_bp.route('/current', methods=['GET'])
def get_current_location():
    """Get the player's current location."""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'No user session found'}), 401
        
        # TODO: Implement actual current location tracking
        # This is a placeholder implementation
        current_location_id = session.get('current_location', 'shadowlands_entrance')
        location = SAMPLE_LOCATIONS.get(current_location_id)
        
        return jsonify({
            'success': True,
            'current_location': location
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to get current location: {str(e)}'}), 500

@location_bp.route('/move', methods=['POST'])
def move_to_location():
    """Move player to a new location."""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'No user session found'}), 401
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        location_id = data.get('location_id')
        if not location_id:
            return jsonify({'error': 'Location ID is required'}), 400
        
        location = SAMPLE_LOCATIONS.get(location_id)
        if not location:
            return jsonify({'error': 'Location not found'}), 404
        
        # TODO: Implement movement validation (distance, requirements, etc.)
        session['current_location'] = location_id
        
        return jsonify({
            'success': True,
            'message': f'Moved to {location["name"]}',
            'new_location': location
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to move to location: {str(e)}'}), 500

@location_bp.route('/action', methods=['POST'])
def perform_location_action():
    """Perform an action at the current location."""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'No user session found'}), 401
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        action = data.get('action')
        if not action:
            return jsonify({'error': 'Action is required'}), 400
        
        current_location_id = session.get('current_location', 'shadowlands_entrance')
        location = SAMPLE_LOCATIONS.get(current_location_id)
        
        if not location:
            return jsonify({'error': 'Current location not found'}), 404
        
        if action not in location['available_actions']:
            return jsonify({'error': f'Action "{action}" not available at this location'}), 400
        
        # TODO: Implement actual action logic
        # This is a placeholder implementation
        result_message = f'You performed "{action}" at {location["name"]}'
        
        return jsonify({
            'success': True,
            'message': result_message,
            'action': action,
            'location': location
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to perform action: {str(e)}'}), 500


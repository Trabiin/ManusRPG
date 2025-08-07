#!/usr/bin/env python3
"""
Shadowlands RPG - Simplified Flask App for Quest Testing
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from datetime import datetime, timedelta
import secrets
from flask import Flask, jsonify, request, session
from flask_cors import CORS
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'shadowlands_rpg_secret_key_2025'
app.config['PERMANENT_SESSION_LIFETIME'] = 1800  # 30 minutes
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = False

# Enable CORS for all routes
CORS(app, supports_credentials=True)

# Import quest routes
from src.routes.quests import quests_bp

# Register quest blueprint
app.register_blueprint(quests_bp, url_prefix='/api/quests')

@app.route('/api/session/init', methods=['GET'])
def init_session():
    """Initialize session with default character data"""
    try:
        default_character = {
            "character_id": "default_character_001",
            "name": "Test Drifter",
            "level": 3,
            "might": 12,
            "intellect": 10,
            "will": 14,
            "shadow": 8,
            "corruption": 0,
            "gold": 100,
            "materials": {"iron": 5, "wood": 10, "leather": 3},
            "faction_standing": {},
            "equipped_items": {},
            "inventory": []
        }
        
        # Initialize session with character data
        session['character'] = default_character
        session['character_id'] = default_character['character_id']
        session['level'] = default_character['level']
        session.permanent = True
        
        return jsonify({
            "success": True,
            "message": "Session initialized successfully",
            "character_data": default_character
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Session Initialization Error",
            "message": f"Failed to initialize session: {str(e)}",
            "status_code": 500
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "success": True,
        "message": "Quest API server is running",
        "timestamp": datetime.utcnow().isoformat()
    })

if __name__ == '__main__':
    print("🎮 Starting Shadowlands Quest API Server...")
    print("📍 Server will be available at: http://localhost:5002")
    print("🔗 Quest endpoints: /api/quests/*")
    print("🔗 Health check: /api/health")
    app.run(debug=True, host='0.0.0.0', port=5002, threaded=True)


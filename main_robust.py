#!/usr/bin/env python3
"""
Shadowlands RPG - Robust Flask App for Quest System
Enhanced with better error handling and logging
"""

import os
import sys
import logging
import traceback
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from datetime import datetime, timedelta
import secrets
from flask import Flask, jsonify, request, session
from flask_cors import CORS
import uuid

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'shadowlands_rpg_secret_key_2025'
app.config['PERMANENT_SESSION_LIFETIME'] = 1800  # 30 minutes
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = False

# Enable CORS for all routes
CORS(app, supports_credentials=True)

# Global error handler
@app.errorhandler(Exception)
def handle_exception(e):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {str(e)}")
    logger.error(traceback.format_exc())
    
    return jsonify({
        "success": False,
        "error": "Internal Server Error",
        "message": "An unexpected error occurred",
        "timestamp": datetime.utcnow().isoformat()
    }), 500

# Import quest routes with error handling
try:
    from src.routes.quests import quests_bp
    app.register_blueprint(quests_bp, url_prefix='/api/quests')
    logger.info("Quest routes registered successfully")
except Exception as e:
    logger.error(f"Failed to import quest routes: {str(e)}")
    logger.error(traceback.format_exc())

# Import dynamic quest routes with error handling
try:
    from src.routes.dynamic_quests import dynamic_quests_bp
    app.register_blueprint(dynamic_quests_bp, url_prefix='/api/dynamic-quests')
    logger.info("Dynamic quest routes registered successfully")
except Exception as e:
    logger.error(f"Failed to import dynamic quest routes: {str(e)}")
    logger.error(traceback.format_exc())

@app.route('/api/session/init', methods=['GET'])
def init_session():
    """Initialize session with default character data"""
    try:
        logger.info("Initializing session")
        
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
        
        logger.info(f"Session initialized for character: {default_character['name']}")
        
        return jsonify({
            "success": True,
            "message": "Session initialized successfully",
            "character_data": default_character,
            "timestamp": datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Session initialization failed: {str(e)}")
        return jsonify({
            "success": False,
            "error": "Session Initialization Error",
            "message": f"Failed to initialize session: {str(e)}",
            "timestamp": datetime.utcnow().isoformat()
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint with detailed status"""
    try:
        # Test quest engine import
        quest_engine_status = "unknown"
        try:
            sys.path.append('/home/ubuntu')
            from quest_engine_core import QuestEngine
            engine = QuestEngine()
            quest_engine_status = f"working ({len(engine.quest_templates)} templates)"
        except Exception as e:
            quest_engine_status = f"error: {str(e)}"
        
        return jsonify({
            "success": True,
            "message": "Quest API server is running",
            "status": {
                "server": "running",
                "quest_engine": quest_engine_status,
                "session_support": "enabled",
                "cors": "enabled"
            },
            "timestamp": datetime.utcnow().isoformat()
        })
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            "success": False,
            "error": "Health Check Error",
            "message": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }), 500

@app.route('/api/debug/session', methods=['GET'])
def debug_session():
    """Debug endpoint to check session data"""
    try:
        return jsonify({
            "success": True,
            "session_data": dict(session),
            "session_id": request.cookies.get('session'),
            "timestamp": datetime.utcnow().isoformat()
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }), 500

if __name__ == '__main__':
    logger.info("🎮 Starting Shadowlands Quest API Server (Robust Version)...")
    logger.info("📍 Server will be available at: http://localhost:5002")
    logger.info("🔗 Quest endpoints: /api/quests/*")
    logger.info("🔗 Health check: /api/health")
    logger.info("🔗 Debug session: /api/debug/session")
    
    try:
        app.run(debug=False, host='0.0.0.0', port=5002, threaded=True, use_reloader=False)
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        logger.error(traceback.format_exc())


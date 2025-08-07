import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from datetime import datetime, timedelta
import secrets
from flask import Flask, send_from_directory, jsonify, request, session
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import uuid

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'shadowlands_rpg_secret_key_2025'
app.config['PERMANENT_SESSION_LIFETIME'] = 1800  # 30 minutes
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS

# Enable CORS for all routes
CORS(app, supports_credentials=True)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 10,
    'pool_recycle': 300,
    'pool_pre_ping': True,
    'max_overflow': 20
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# User model
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.String(100), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Character model
class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    level = db.Column(db.Integer, default=1)
    experience = db.Column(db.Integer, default=0)
    might = db.Column(db.Integer, default=10)
    intellect = db.Column(db.Integer, default=10)
    will = db.Column(db.Integer, default=10)
    shadow = db.Column(db.Integer, default=0)
    health = db.Column(db.Integer, default=100)
    max_health = db.Column(db.Integer, default=100)
    mana = db.Column(db.Integer, default=50)
    max_mana = db.Column(db.Integer, default=50)
    corruption = db.Column(db.Integer, default=0)
    combat_experience = db.Column(db.Integer, default=0)
    
    def to_dict(self):
        return {
            'character_id': str(self.id),
            'user_id': self.user_id,
            'name': self.name,
            'level': self.level,
            'experience': self.experience,
            'might': self.might,
            'intellect': self.intellect,
            'will': self.will,
            'shadow': self.shadow,
            'health': self.health,
            'max_health': self.max_health,
            'mana': self.mana,
            'max_mana': self.max_mana,
            'corruption': self.corruption,
            'combat_experience': self.combat_experience,
            'faction_standings': {
                'luminous_order': 0,
                'shadow_courts': 0,
                'neutral_traders': 0
            }
        }

# GameSession model
class GameSession(db.Model):
    __tablename__ = 'game_sessions'
    
    id = db.Column(db.String(64), primary_key=True)
    user_id = db.Column(db.String(100), nullable=False)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    
    def __init__(self, user_id, character_id=None):
        self.id = secrets.token_urlsafe(32)
        self.user_id = user_id
        self.character_id = character_id
        self.expires_at = datetime.utcnow() + timedelta(minutes=30)
    
    def is_expired(self):
        return datetime.utcnow() > self.expires_at

# Session helper functions
def create_session(user_id, character_id=None):
    try:
        game_session = GameSession(user_id=user_id, character_id=character_id)
        db.session.add(game_session)
        db.session.commit()
        
        session['session_id'] = game_session.id
        session['user_id'] = user_id
        session['character_id'] = character_id
        session.permanent = True
        
        return game_session
    except Exception as e:
        db.session.rollback()
        return None

def get_session():
    try:
        session_id = session.get('session_id')
        if not session_id:
            return None
        
        game_session = GameSession.query.filter_by(id=session_id, is_active=True).first()
        if not game_session or game_session.is_expired():
            return None
        
        return game_session
    except Exception:
        return None

# Import routes after models are defined
from src.routes.user import user_bp
from src.routes.location import location_bp
from src.routes.quest import quest_bp
from src.routes.narrative import narrative_bp
from src.routes.equipment import equipment_bp
from src.routes.combat import combat_bp

# Register blueprints
app.register_blueprint(user_bp)
app.register_blueprint(location_bp)
app.register_blueprint(quest_bp)
app.register_blueprint(narrative_bp)
app.register_blueprint(equipment_bp)
app.register_blueprint(combat_bp)

# Character routes
@app.route('/api/characters', methods=['GET'])
def get_characters():
    """Get all characters for the current user."""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'No user session found'}), 400
    
    characters = Character.query.filter_by(user_id=user_id).all()
    return jsonify([char.to_dict() for char in characters])

@app.route('/api/characters', methods=['POST'])
def create_character():
    """Create a new character."""
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
    
    data = request.json
    character = Character(
        user_id=session['user_id'],
        name=data.get('name', 'Unnamed Drifter')
    )
    
    db.session.add(character)
    db.session.commit()
    
    # Store character in session for easy access
    session['character'] = character.to_dict()
    
    return jsonify({
        'success': True,
        'message': 'Character created successfully',
        'data': character.to_dict()
    }), 201

@app.route('/api/character/<int:character_id>/select', methods=['POST'])
def select_character(character_id):
    """Select a character as the active character."""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'No user session found'}), 400
    
    character = Character.query.filter_by(id=character_id, user_id=user_id).first()
    if not character:
        return jsonify({'error': 'Character not found'}), 404
    
    # Store character in session
    session['character'] = character.to_dict()
    
    return jsonify({
        'success': True,
        'message': f'Selected character: {character.name}',
        'data': character.to_dict()
    })

@app.route('/api/character/current', methods=['GET'])
def get_current_character():
    """Get the currently selected character."""
    character_data = session.get('character')
    if not character_data:
        return jsonify({'error': 'No character selected'}), 400
    
    return jsonify({
        'success': True,
        'data': character_data
    })

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return {
        'status': 'healthy',
        'message': 'Shadowlands RPG Backend is running',
        'version': '1.0.0'
    }

# Session initialization endpoint
@app.route('/api/session/init', methods=['POST'])
def initialize_session():
    """Initialize a session with default character data for testing"""
    try:
        # Create default character data
        default_character = {
            "character_id": "test_character_001",
            "level": 5,
            "might": 12,
            "intellect": 10,
            "will": 8,
            "shadow": 2,
            "corruption": 15,
            "gold": 1000,
            "materials": ["iron_ingot", "leather", "enchanting_dust"],
            "faction_standing": {},
            "equipped_items": {
                "weapon_main": None,
                "weapon_off": None,
                "armor_head": None,
                "armor_chest": None,
                "armor_legs": None,
                "armor_feet": None,
                "armor_hands": None,
                "accessory_ring1": None,
                "accessory_ring2": None,
                "accessory_amulet": None
            },
            "inventory": []
        }
        
        # Initialize session with character data
        session['character_id'] = default_character['character_id']
        session['level'] = default_character['level']
        session['might'] = default_character['might']
        session['intellect'] = default_character['intellect']
        session['will'] = default_character['will']
        session['shadow'] = default_character['shadow']
        session['corruption'] = default_character['corruption']
        session['gold'] = default_character['gold']
        session['materials'] = default_character['materials']
        session['faction_standing'] = default_character['faction_standing']
        session['equipped_items'] = default_character['equipped_items']
        session['inventory'] = default_character['inventory']
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

# Database initialization
with app.app_context():
    db.create_all()

# Static file serving
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5001, threaded=True)

"""
ManusRPG Routes Package
Contains all Flask blueprint route definitions for the ManusRPG application.
"""

# Import all blueprints for easy access
try:
    from .user import user_bp
except ImportError:
    user_bp = None

try:
    from .location import location_bp
except ImportError:
    location_bp = None

try:
    from .quest import quest_bp
except ImportError:
    quest_bp = None

try:
    from .narrative import narrative_bp
except ImportError:
    narrative_bp = None

try:
    from .equipment import equipment_bp
except ImportError:
    equipment_bp = None

try:
    from .combat import combat_bp
except ImportError:
    combat_bp = None

try:
    from .quests import quests_bp
except ImportError:
    quests_bp = None

try:
    from .dynamic_quests import dynamic_quests_bp
except ImportError:
    dynamic_quests_bp = None

__all__ = [
    'user_bp',
    'location_bp', 
    'quest_bp',
    'narrative_bp',
    'equipment_bp',
    'combat_bp',
    'quests_bp',
    'dynamic_quests_bp'
]


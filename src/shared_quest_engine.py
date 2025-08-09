"""
Shadowlands RPG - Shared Quest Engine Instance
Provides a single quest engine instance for all API routes
"""

import sys
import os

# Add the parent directory to the path to import quest engine
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from quest_engine_core import QuestEngine
from dynamic_quest_generation import integrate_dynamic_generation

# Create single shared quest engine instance
_quest_engine = None
_dynamic_generator = None

def get_quest_engine():
    """Get the shared quest engine instance"""
    global _quest_engine
    if _quest_engine is None:
        _quest_engine = QuestEngine()
    return _quest_engine

def get_dynamic_generator():
    """Get the shared dynamic quest generator instance"""
    global _dynamic_generator
    if _dynamic_generator is None:
        quest_engine = get_quest_engine()
        _dynamic_generator = integrate_dynamic_generation(quest_engine)
    return _dynamic_generator


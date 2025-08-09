"""
ManusRPG Equipment System
Basic equipment management system for the ManusRPG application.
"""

from enum import Enum
from typing import Dict, List, Optional, Any
import json

class EquipmentSlot(Enum):
    """Equipment slot types."""
    WEAPON = "weapon"
    ARMOR = "armor"
    HELMET = "helmet"
    BOOTS = "boots"
    GLOVES = "gloves"
    RING = "ring"
    AMULET = "amulet"
    SHIELD = "shield"

class Equipment:
    """Represents a piece of equipment."""
    
    def __init__(self, item_id: str, name: str, slot: EquipmentSlot, 
                 stats: Dict[str, int] = None, description: str = ""):
        self.item_id = item_id
        self.name = name
        self.slot = slot
        self.stats = stats or {}
        self.description = description
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert equipment to dictionary."""
        return {
            'item_id': self.item_id,
            'name': self.name,
            'slot': self.slot.value,
            'stats': self.stats,
            'description': self.description
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Equipment':
        """Create equipment from dictionary."""
        return cls(
            item_id=data['item_id'],
            name=data['name'],
            slot=EquipmentSlot(data['slot']),
            stats=data.get('stats', {}),
            description=data.get('description', '')
        )

class EquipmentManager:
    """Manages equipment for characters."""
    
    def __init__(self):
        self.equipment_database = self._initialize_equipment_database()
        self.character_equipment = {}  # character_id -> {slot: equipment}
    
    def _initialize_equipment_database(self) -> Dict[str, Equipment]:
        """Initialize the equipment database with sample items."""
        items = {
            'iron_sword': Equipment(
                'iron_sword', 'Iron Sword', EquipmentSlot.WEAPON,
                {'attack': 10, 'durability': 100}, 'A sturdy iron sword.'
            ),
            'leather_armor': Equipment(
                'leather_armor', 'Leather Armor', EquipmentSlot.ARMOR,
                {'defense': 5, 'durability': 80}, 'Basic leather armor.'
            ),
            'iron_helmet': Equipment(
                'iron_helmet', 'Iron Helmet', EquipmentSlot.HELMET,
                {'defense': 3, 'durability': 60}, 'An iron helmet for protection.'
            ),
            'leather_boots': Equipment(
                'leather_boots', 'Leather Boots', EquipmentSlot.BOOTS,
                {'defense': 2, 'speed': 1}, 'Comfortable leather boots.'
            ),
            'magic_ring': Equipment(
                'magic_ring', 'Magic Ring', EquipmentSlot.RING,
                {'magic': 5, 'mana': 20}, 'A ring imbued with magical energy.'
            )
        }
        return items
    
    def get_equipment(self, item_id: str) -> Optional[Equipment]:
        """Get equipment by ID."""
        return self.equipment_database.get(item_id)
    
    def get_all_equipment(self) -> List[Equipment]:
        """Get all available equipment."""
        return list(self.equipment_database.values())
    
    def equip_item(self, character_id: str, item_id: str) -> bool:
        """Equip an item to a character."""
        equipment = self.get_equipment(item_id)
        if not equipment:
            return False
        
        if character_id not in self.character_equipment:
            self.character_equipment[character_id] = {}
        
        self.character_equipment[character_id][equipment.slot] = equipment
        return True
    
    def unequip_item(self, character_id: str, slot: EquipmentSlot) -> bool:
        """Unequip an item from a character."""
        if character_id not in self.character_equipment:
            return False
        
        if slot in self.character_equipment[character_id]:
            del self.character_equipment[character_id][slot]
            return True
        
        return False
    
    def get_character_equipment(self, character_id: str) -> Dict[str, Equipment]:
        """Get all equipment for a character."""
        if character_id not in self.character_equipment:
            return {}
        
        return {slot.value: equipment for slot, equipment in 
                self.character_equipment[character_id].items()}
    
    def get_character_stats(self, character_id: str) -> Dict[str, int]:
        """Calculate total stats from equipped items."""
        equipment = self.character_equipment.get(character_id, {})
        total_stats = {}
        
        for item in equipment.values():
            for stat, value in item.stats.items():
                total_stats[stat] = total_stats.get(stat, 0) + value
        
        return total_stats

# Global equipment manager instance
equipment_manager = EquipmentManager()


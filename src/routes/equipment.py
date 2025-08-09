
from flask import Blueprint, jsonify, request, session
import sys
import os
# Add the parent directory to the path to import equipment_system
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from equipment_system import equipment_manager, EquipmentSlot
import json

equipment_bp = Blueprint('equipment', __name__)

def get_character_data():
    """Get character data from session with proper error handling"""
    try:
        # Check if we have a session
        if not session:
            return None, "No session found"
        
        character_id = session.get('character_id')
        if not character_id:
            # Create a default character for testing
            default_character = {
                "character_id": "default_test_char",
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
                    EquipmentSlot.WEAPON_MAIN: None,
                    EquipmentSlot.WEAPON_OFF: None,
                    EquipmentSlot.ARMOR_HEAD: None,
                    EquipmentSlot.ARMOR_CHEST: None,
                    EquipmentSlot.ARMOR_LEGS: None,
                    EquipmentSlot.ARMOR_FEET: None,
                    EquipmentSlot.ARMOR_HANDS: None,
                    EquipmentSlot.ACCESSORY_RING1: None,
                    EquipmentSlot.ACCESSORY_RING2: None,
                    EquipmentSlot.ACCESSORY_AMULET: None
                },
                "inventory": []
            }
            return default_character, None
        
        # Get character data from session
        character_data = {
            "character_id": character_id,
            "level": session.get('level', 1),
            "might": session.get('might', 10),
            "intellect": session.get('intellect', 10),
            "will": session.get('will', 10),
            "shadow": session.get('shadow', 0),
            "corruption": session.get('corruption', 0),
            "gold": session.get('gold', 1000),
            "materials": session.get('materials', ["iron_ingot", "leather", "enchanting_dust"]),
            "faction_standing": session.get('faction_standing', {}),
            "equipped_items": session.get('equipped_items', {
                EquipmentSlot.WEAPON_MAIN: None,
                EquipmentSlot.WEAPON_OFF: None,
                EquipmentSlot.ARMOR_HEAD: None,
                EquipmentSlot.ARMOR_CHEST: None,
                EquipmentSlot.ARMOR_LEGS: None,
                EquipmentSlot.ARMOR_FEET: None,
                EquipmentSlot.ARMOR_HANDS: None,
                EquipmentSlot.ACCESSORY_RING1: None,
                EquipmentSlot.ACCESSORY_RING2: None,
                EquipmentSlot.ACCESSORY_AMULET: None
            }),
            "inventory": session.get('inventory', [])
        }
        
        return character_data, None
        
    except Exception as e:
        return None, f"Error getting character data: {str(e)}"

@equipment_bp.route('/api/equipment/available', methods=['GET'])
def get_available_equipment():
    """Get equipment available to the current character with proper error handling"""
    try:
        character_data, error = get_character_data()
        if error:
            return jsonify({
                "success": False,
                "error": "Character Data Error",
                "message": error,
                "status_code": 400
            }), 400
        
        if not character_data:
            return jsonify({
                "success": False,
                "error": "No Character Found",
                "message": "No character data available",
                "status_code": 400
            }), 400
        
        # Get filter parameters
        item_type = request.args.get('type')
        slot = request.args.get('slot')
        
        # Get available equipment
        available_equipment = equipment_manager.get_equipment_for_character(
            character_data, item_type, slot
        )
        
        equipment_list = [eq.to_dict() for eq in available_equipment]
        
        return jsonify({
            "success": True,
            "equipment": equipment_list,
            "total_count": len(equipment_list),
            "character_level": character_data["level"],
            "character_corruption": character_data["corruption"],
            "message": "Equipment retrieved successfully"
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Server Error",
            "message": f"Failed to get available equipment: {str(e)}",
            "status_code": 500
        }), 500

@equipment_bp.route('/api/equipment/equipped', methods=['GET'])
def get_equipped_items():
    """Get all currently equipped items and their bonuses with proper error handling"""
    try:
        character_data, error = get_character_data()
        if error:
            return jsonify({
                "success": False,
                "error": "Character Data Error",
                "message": error,
                "status_code": 400
            }), 400
        
        if not character_data:
            return jsonify({
                "success": False,
                "error": "No Character Found",
                "message": "No character data available",
                "status_code": 400
            }), 400
        
        equipped_items = character_data["equipped_items"]
        equipped_details = {}
        
        for slot, item_id in equipped_items.items():
            if item_id:
                equipment = equipment_manager.get_equipment(item_id)
                if equipment:
                    equipped_details[slot] = equipment.to_dict()
                else:
                    equipped_details[slot] = None
            else:
                equipped_details[slot] = None
        
        # Calculate total bonuses
        bonuses = equipment_manager.calculate_equipment_bonuses(equipped_items, character_data)
        
        return jsonify({
            "success": True,
            "equipped_items": equipped_details,
            "total_bonuses": bonuses,
            "equipment_slots": EquipmentSlot.ALL_SLOTS,
            "message": "Equipped items retrieved successfully"
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Server Error",
            "message": f"Failed to get equipped items: {str(e)}",
            "status_code": 500
        }), 500

@equipment_bp.route('/api/equipment/equip', methods=['POST'])
def equip_item():
    """Equip an item to a specific slot with proper error handling"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "success": False,
                "error": "Invalid Request",
                "message": "No JSON data provided",
                "status_code": 400
            }), 400
        
        item_id = data.get('item_id')
        slot = data.get('slot')
        
        if not item_id or not slot:
            return jsonify({
                "success": False,
                "error": "Missing Parameters",
                "message": "Missing item_id or slot",
                "status_code": 400
            }), 400
        
        character_data, error = get_character_data()
        if error:
            return jsonify({
                "success": False,
                "error": "Character Data Error",
                "message": error,
                "status_code": 400
            }), 400
        
        if not character_data:
            return jsonify({
                "success": False,
                "error": "No Character Found",
                "message": "No character data available",
                "status_code": 400
            }), 400
        
        equipment = equipment_manager.get_equipment(item_id)
        if not equipment:
            return jsonify({
                "success": False,
                "error": "Equipment Not Found",
                "message": f"Equipment with ID {item_id} not found",
                "status_code": 404
            }), 404
        
        # Check if character can equip
        can_equip, reason = equipment.can_be_equipped_by(character_data)
        if not can_equip:
            return jsonify({
                "success": False,
                "error": "Cannot Equip",
                "message": f"Cannot equip: {reason}",
                "status_code": 400
            }), 400
        
        # Check if slot is valid for this equipment
        if equipment.slot != slot and not (equipment.slot == EquipmentSlot.ACCESSORY_RING1 and slot == EquipmentSlot.ACCESSORY_RING2):
            return jsonify({
                "success": False,
                "error": "Invalid Slot",
                "message": "Invalid slot for this equipment",
                "status_code": 400
            }), 400
        
        # Equip the item
        equipped_items = character_data["equipped_items"]
        previously_equipped = equipped_items.get(slot)
        equipped_items[slot] = item_id
        
        # Update session
        session['equipped_items'] = equipped_items
        
        # Calculate new bonuses
        bonuses = equipment_manager.calculate_equipment_bonuses(equipped_items, character_data)
        
        return jsonify({
            "success": True,
            "message": f"Equipped {equipment.get_display_name()}",
            "previously_equipped": previously_equipped,
            "new_bonuses": bonuses,
            "item_id": item_id,
            "slot": slot
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Server Error",
            "message": f"Failed to equip item: {str(e)}",
            "status_code": 500
        }), 500

@equipment_bp.route('/api/equipment/unequip', methods=['POST'])
def unequip_item():
    """Unequip an item from a specific slot with proper error handling"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "success": False,
                "error": "Invalid Request",
                "message": "No JSON data provided",
                "status_code": 400
            }), 400
        
        slot = data.get('slot')
        
        if not slot:
            return jsonify({
                "success": False,
                "error": "Missing Parameters",
                "message": "Missing slot parameter",
                "status_code": 400
            }), 400
        
        character_data, error = get_character_data()
        if error:
            return jsonify({
                "success": False,
                "error": "Character Data Error",
                "message": error,
                "status_code": 400
            }), 400
        
        if not character_data:
            return jsonify({
                "success": False,
                "error": "No Character Found",
                "message": "No character data available",
                "status_code": 400
            }), 400
        
        # Check if there's an item equipped in that slot
        equipped_items = character_data["equipped_items"]
        currently_equipped = equipped_items.get(slot)
        
        if not currently_equipped:
            return jsonify({
                "success": False,
                "error": "No Item Equipped",
                "message": f"No item equipped in slot {slot}",
                "status_code": 400
            }), 400
        
        # Get equipment details for response
        equipment = equipment_manager.get_equipment(currently_equipped)
        equipment_name = equipment.get_display_name() if equipment else currently_equipped
        
        # Unequip the item
        equipped_items[slot] = None
        
        # Update session
        session['equipped_items'] = equipped_items
        
        # Calculate new bonuses
        bonuses = equipment_manager.calculate_equipment_bonuses(equipped_items, character_data)
        
        return jsonify({
            "success": True,
            "message": f"Unequipped {equipment_name}",
            "unequipped_item": currently_equipped,
            "new_bonuses": bonuses,
            "slot": slot
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Server Error",
            "message": f"Failed to unequip item: {str(e)}",
            "status_code": 500
        }), 500

@equipment_bp.route('/api/equipment/test', methods=['GET'])
def test_equipment_system():
    """Test equipment system functionality"""
    try:
        # Test basic functionality
        total_items = len(equipment_manager.equipment_database)
        weapons = len(equipment_manager.get_equipment_by_type("weapon"))
        armor = len(equipment_manager.get_equipment_by_type("armor"))
        accessories = len(equipment_manager.get_equipment_by_type("accessory"))
        
        # Test character data
        character_data, error = get_character_data()
        
        result = {
            "success": True,
            "message": "Equipment system test completed",
            "system_status": {
                "total_items": total_items,
                "weapons": weapons,
                "armor": armor,
                "accessories": accessories
            },
            "character_status": {
                "has_character": character_data is not None,
                "error": error
            }
        }
        
        if character_data:
            available_equipment = equipment_manager.get_equipment_for_character(character_data)
            result["character_status"]["available_items"] = len(available_equipment)
            result["character_status"]["level"] = character_data["level"]
            result["character_status"]["corruption"] = character_data["corruption"]
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Server Error",
            "message": f"Equipment system test failed: {str(e)}",
            "status_code": 500
        }), 500

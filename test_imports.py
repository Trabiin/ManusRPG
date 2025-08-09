#!/usr/bin/env python3
"""
Test script to verify that all blueprint imports work correctly.
This tests the fix for issue #9.
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

def test_blueprint_imports():
    """Test that all blueprint imports work correctly."""
    print("Testing blueprint imports...")
    
    try:
        # Test individual blueprint imports
        from src.routes.user import user_bp
        print("✓ user_bp imported successfully")
        
        from src.routes.location import location_bp
        print("✓ location_bp imported successfully")
        
        from src.routes.quest import quest_bp
        print("✓ quest_bp imported successfully")
        
        from src.routes.narrative import narrative_bp
        print("✓ narrative_bp imported successfully")
        
        from src.routes.equipment import equipment_bp
        print("✓ equipment_bp imported successfully")
        
        from src.routes.combat import combat_bp
        print("✓ combat_bp imported successfully")
        
        from src.routes.quests import quests_bp
        print("✓ quests_bp imported successfully")
        
        from src.routes.dynamic_quests import dynamic_quests_bp
        print("✓ dynamic_quests_bp imported successfully")
        
        # Test that blueprints are properly configured
        blueprints = [
            ('user_bp', user_bp),
            ('location_bp', location_bp),
            ('quest_bp', quest_bp),
            ('narrative_bp', narrative_bp),
            ('equipment_bp', equipment_bp),
            ('combat_bp', combat_bp),
            ('quests_bp', quests_bp),
            ('dynamic_quests_bp', dynamic_quests_bp)
        ]
        
        print("\nValidating blueprint configurations...")
        for name, bp in blueprints:
            if hasattr(bp, 'name'):
                print(f"✓ {name} has name: {bp.name}")
            else:
                print(f"✗ {name} missing name attribute")
                return False
        
        print("\n✅ All blueprint imports successful!")
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False

def test_main_file_imports():
    """Test that main files can import blueprints correctly."""
    print("\nTesting main file import patterns...")
    
    try:
        # Test the import pattern used in main_clean.py
        from src.routes.user import user_bp
        from src.routes.location import location_bp
        from src.routes.quest import quest_bp
        from src.routes.narrative import narrative_bp
        from src.routes.equipment import equipment_bp
        from src.routes.combat import combat_bp
        
        print("✓ Main file import pattern works")
        
        # Test the import pattern used in main_robust.py
        from src.routes.quests import quests_bp
        from src.routes.dynamic_quests import dynamic_quests_bp
        
        print("✓ Quest-specific import pattern works")
        
        return True
        
    except ImportError as e:
        print(f"✗ Main file import error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error in main file imports: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("ManusRPG Issue #9 Fix - Import Test")
    print("=" * 50)
    
    success = True
    
    success &= test_blueprint_imports()
    success &= test_main_file_imports()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 ALL TESTS PASSED! Issue #9 fix is working correctly.")
        sys.exit(0)
    else:
        print("❌ TESTS FAILED! Issue #9 fix needs more work.")
        sys.exit(1)


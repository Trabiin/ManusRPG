#!/usr/bin/env python3
"""
Test script to verify that the main file blueprint imports work correctly.
This specifically tests the fix for issue #9 in the context of main files.
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

def test_main_clean_blueprint_imports():
    """Test that main_clean.py can import all required blueprints."""
    print("Testing main_clean.py blueprint imports...")
    
    try:
        # Test the exact import pattern used in main_clean.py
        from src.routes.user import user_bp
        from src.routes.location import location_bp
        from src.routes.quest import quest_bp
        from src.routes.narrative import narrative_bp
        from src.routes.equipment import equipment_bp
        from src.routes.combat import combat_bp
        
        print("✓ All main_clean.py blueprint imports successful")
        
        # Verify blueprints are properly configured
        blueprints = [
            ('user_bp', user_bp),
            ('location_bp', location_bp),
            ('quest_bp', quest_bp),
            ('narrative_bp', narrative_bp),
            ('equipment_bp', equipment_bp),
            ('combat_bp', combat_bp)
        ]
        
        for name, bp in blueprints:
            if hasattr(bp, 'name'):
                print(f"✓ {name} ready for registration: {bp.name}")
            else:
                print(f"✗ {name} missing name attribute")
                return False
        
        return True
        
    except ImportError as e:
        print(f"✗ Blueprint import error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False

def test_main_robust_blueprint_imports():
    """Test that main_robust.py can import all required blueprints."""
    print("\nTesting main_robust.py blueprint imports...")
    
    try:
        # Test the exact import pattern used in main_robust.py
        from src.routes.quests import quests_bp
        from src.routes.dynamic_quests import dynamic_quests_bp
        
        print("✓ All main_robust.py blueprint imports successful")
        
        # Verify blueprints are properly configured
        blueprints = [
            ('quests_bp', quests_bp),
            ('dynamic_quests_bp', dynamic_quests_bp)
        ]
        
        for name, bp in blueprints:
            if hasattr(bp, 'name'):
                print(f"✓ {name} ready for registration: {bp.name}")
            else:
                print(f"✗ {name} missing name attribute")
                return False
        
        return True
        
    except ImportError as e:
        print(f"✗ Blueprint import error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False

def test_flask_server_fixes_imports():
    """Test that flask_server_fixes.py can import all required blueprints."""
    print("\nTesting flask_server_fixes.py blueprint imports...")
    
    try:
        # Test the exact import pattern used in flask_server_fixes.py
        from src.routes.user import user_bp
        from src.routes.location import location_bp
        from src.routes.quest import quest_bp
        from src.routes.narrative import narrative_bp
        from src.routes.equipment import equipment_bp
        from src.routes.combat import combat_bp
        
        print("✓ All flask_server_fixes.py blueprint imports successful")
        return True
        
    except ImportError as e:
        print(f"✗ Blueprint import error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("ManusRPG Issue #9 Fix - Main File Import Test")
    print("=" * 60)
    
    success = True
    
    success &= test_main_clean_blueprint_imports()
    success &= test_main_robust_blueprint_imports()
    success &= test_flask_server_fixes_imports()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 ALL MAIN FILE IMPORTS WORKING! Issue #9 fix is complete.")
        print("The src/ directory structure is properly created and functional.")
        sys.exit(0)
    else:
        print("❌ MAIN FILE IMPORT TESTS FAILED!")
        sys.exit(1)


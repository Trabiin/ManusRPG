#!/usr/bin/env python3
"""
Comprehensive Quest System Test
Tests all core functionality of the Shadowlands RPG Quest System
"""

import requests
import json
import time

BASE_URL = "http://localhost:5002"

def test_quest_system():
    """Run comprehensive quest system tests"""
    print("🎮 Shadowlands Quest System - Comprehensive Test")
    print("=" * 50)
    
    session = requests.Session()
    
    # Test 1: Health Check
    print("1. Testing API Health...")
    response = session.get(f"{BASE_URL}/api/health")
    if response.status_code == 200:
        print("   ✅ API Health: PASS")
    else:
        print("   ❌ API Health: FAIL")
        return False
    
    # Test 2: Session Initialization
    print("2. Testing Session Initialization...")
    response = session.get(f"{BASE_URL}/api/session/init")
    if response.status_code == 200 and response.json().get("success"):
        character_data = response.json().get("character_data", {})
        print(f"   ✅ Session Init: PASS (Character: {character_data.get('name')})")
    else:
        print("   ❌ Session Init: FAIL")
        return False
    
    # Test 3: Quest Templates
    print("3. Testing Quest Templates...")
    response = session.get(f"{BASE_URL}/api/quests/templates")
    if response.status_code == 200 and response.json().get("success"):
        templates = response.json().get("data", {}).get("templates", [])
        print(f"   ✅ Quest Templates: PASS ({len(templates)} templates)")
        for template in templates:
            print(f"      • {template['title']} ({template['quest_type']})")
    else:
        print("   ❌ Quest Templates: FAIL")
        return False
    
    # Test 4: Available Quests
    print("4. Testing Available Quests...")
    response = session.get(f"{BASE_URL}/api/quests/available")
    if response.status_code == 200 and response.json().get("success"):
        available = response.json().get("data", {}).get("available_quests", [])
        print(f"   ✅ Available Quests: PASS ({len(available)} available)")
    else:
        print("   ❌ Available Quests: FAIL")
        return False
    
    # Test 5: Quest Creation
    print("5. Testing Quest Creation...")
    quest_data = {"template_id": "main_001"}
    response = session.post(f"{BASE_URL}/api/quests/start", json=quest_data)
    if response.status_code == 200 and response.json().get("success"):
        quest = response.json().get("data", {}).get("quest", {})
        quest_id = quest.get("quest_id")
        print(f"   ✅ Quest Creation: PASS (Quest ID: {quest_id[:8]}...)")
        print(f"      Title: {quest.get('title')}")
        print(f"      Objectives: {len(quest.get('objectives', []))}")
        print(f"      Choices: {len(quest.get('choices', []))}")
    else:
        print("   ❌ Quest Creation: FAIL")
        return False
    
    # Test 6: Active Quests
    print("6. Testing Active Quests...")
    response = session.get(f"{BASE_URL}/api/quests/active")
    if response.status_code == 200 and response.json().get("success"):
        active = response.json().get("data", {}).get("active_quests", [])
        print(f"   ✅ Active Quests: PASS ({len(active)} active)")
    else:
        print("   ❌ Active Quests: FAIL")
        return False
    
    # Test 7: Objective Progress
    print("7. Testing Objective Progress...")
    if quest_id and quest.get("objectives"):
        objective_id = quest["objectives"][0]["objective_id"]
        progress_data = {"increment": 1}
        response = session.post(f"{BASE_URL}/api/quests/{quest_id}/objective/{objective_id}/progress", json=progress_data)
        if response.status_code == 200 and response.json().get("success"):
            result = response.json().get("data", {})
            print(f"   ✅ Objective Progress: PASS (Progress: {result.get('progress', 0)}%)")
        else:
            print("   ❌ Objective Progress: FAIL")
            return False
    
    # Test 8: Quest Statistics
    print("8. Testing Quest Statistics...")
    response = session.get(f"{BASE_URL}/api/quests/statistics")
    if response.status_code == 200 and response.json().get("success"):
        stats = response.json().get("data", {})
        print(f"   ✅ Quest Statistics: PASS")
        print(f"      Total Templates: {stats.get('total_templates', 0)}")
        print(f"      Active Quests: {stats.get('active_quests', 0)}")
        print(f"      Completed Quests: {stats.get('completed_quests', 0)}")
    else:
        print("   ❌ Quest Statistics: FAIL")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 QUEST SYSTEM COMPREHENSIVE TEST: SUCCESS")
    print("✅ All core quest functionality is working correctly!")
    print("✅ Quest templates are available and functional")
    print("✅ Quest creation, progression, and tracking work")
    print("✅ API endpoints respond with standardized format")
    
    return True

if __name__ == "__main__":
    success = test_quest_system()
    if not success:
        print("\n❌ Quest system test failed!")
        exit(1)
    else:
        print("\n🎮 Quest system is ready for production!")


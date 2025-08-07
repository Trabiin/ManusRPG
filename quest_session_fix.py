#!/usr/bin/env python3
"""
Quest API Session Fix and Test
Simple test to verify quest API functionality with proper session setup
"""

import requests
import json

def test_quest_api_with_session():
    """Test quest API with proper session initialization"""
    base_url = "http://localhost:5002"
    session = requests.Session()
    
    print("🎮 Testing Quest API with Session Initialization")
    print("=" * 50)
    
    # Step 1: Initialize session with character data
    print("1. Initializing session...")
    init_response = session.get(f"{base_url}/api/session/init")
    if init_response.status_code == 200:
        print("✅ Session initialized")
        print(f"   Response: {init_response.json()}")
    else:
        print(f"❌ Session initialization failed: {init_response.status_code}")
        return False
    
    # Step 2: Get quest templates
    print("\\n2. Getting quest templates...")
    templates_response = session.get(f"{base_url}/api/quests/templates")
    if templates_response.status_code == 200:
        templates_data = templates_response.json()
        templates = templates_data.get("data", {}).get("templates", [])
        print(f"✅ Retrieved {len(templates)} quest templates")
        for template in templates:
            print(f"   • {template['title']} ({template['quest_type']})")
    else:
        print(f"❌ Failed to get templates: {templates_response.status_code}")
        return False
    
    # Step 3: Get available quests
    print("\\n3. Getting available quests...")
    available_response = session.get(f"{base_url}/api/quests/available")
    if available_response.status_code == 200:
        available_data = available_response.json()
        available_quests = available_data.get("data", {}).get("available_quests", [])
        print(f"✅ Found {len(available_quests)} available quests")
        for quest in available_quests:
            print(f"   • {quest['title']} (Level {quest['level_requirement']})")
    else:
        print(f"❌ Failed to get available quests: {available_response.status_code}")
        print(f"   Response: {available_response.json()}")
        return False
    
    # Step 4: Start a quest
    if available_quests:
        print("\\n4. Starting a quest...")
        template_id = available_quests[0]["template_id"]
        start_data = {"template_id": template_id}
        
        start_response = session.post(f"{base_url}/api/quests/start", json=start_data)
        if start_response.status_code == 200:
            start_data = start_response.json()
            quest = start_data.get("data", {}).get("quest", {})
            quest_id = quest.get("quest_id")
            print(f"✅ Started quest: {quest.get('title')} (ID: {quest_id})")
            print(f"   Objectives: {len(quest.get('objectives', []))}")
            print(f"   Choices: {len(quest.get('choices', []))}")
            
            # Step 5: Get active quests
            print("\\n5. Getting active quests...")
            active_response = session.get(f"{base_url}/api/quests/active")
            if active_response.status_code == 200:
                active_data = active_response.json()
                active_quests = active_data.get("data", {}).get("active_quests", [])
                print(f"✅ Retrieved {len(active_quests)} active quests")
            else:
                print(f"❌ Failed to get active quests: {active_response.status_code}")
            
            # Step 6: Update objective progress
            objectives = quest.get("objectives", [])
            if objectives:
                print("\\n6. Updating objective progress...")
                objective_id = objectives[0]["objective_id"]
                progress_data = {"increment": 1}
                
                progress_response = session.post(
                    f"{base_url}/api/quests/{quest_id}/objective/{objective_id}/progress",
                    json=progress_data
                )
                
                if progress_response.status_code == 200:
                    progress_result = progress_response.json()
                    result_data = progress_result.get("data", {})
                    print(f"✅ Updated objective progress")
                    print(f"   Objective completed: {result_data.get('objective_completed', False)}")
                    print(f"   Quest completed: {result_data.get('quest_completed', False)}")
                else:
                    print(f"❌ Failed to update objective: {progress_response.status_code}")
            
            # Step 7: Make a quest choice
            choices = quest.get("choices", [])
            if choices:
                print("\\n7. Making a quest choice...")
                choice_id = choices[0]["choice_id"]
                
                choice_response = session.post(f"{base_url}/api/quests/{quest_id}/choice/{choice_id}")
                if choice_response.status_code == 200:
                    choice_result = choice_response.json()
                    result_data = choice_result.get("data", {})
                    print(f"✅ Made quest choice")
                    print(f"   Consequences: {len(result_data.get('consequences', []))}")
                else:
                    print(f"❌ Failed to make choice: {choice_response.status_code}")
            
        else:
            print(f"❌ Failed to start quest: {start_response.status_code}")
            print(f"   Response: {start_response.json()}")
            return False
    
    # Step 8: Get quest statistics
    print("\\n8. Getting quest statistics...")
    stats_response = session.get(f"{base_url}/api/quests/statistics")
    if stats_response.status_code == 200:
        stats_data = stats_response.json()
        stats = stats_data.get("data", {})
        character_stats = stats.get("character_statistics", {})
        print(f"✅ Retrieved quest statistics")
        print(f"   Active quests: {character_stats.get('character_active_quests', 0)}")
        print(f"   Completed quests: {character_stats.get('character_completed_quests', 0)}")
        print(f"   Character level: {character_stats.get('character_level', 1)}")
    else:
        print(f"❌ Failed to get statistics: {stats_response.status_code}")
    
    print("\\n🎉 Quest API testing completed successfully!")
    return True

if __name__ == "__main__":
    success = test_quest_api_with_session()
    if success:
        print("\\n✅ All quest API endpoints are working correctly!")
    else:
        print("\\n❌ Some quest API endpoints failed.")


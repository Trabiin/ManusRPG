#!/usr/bin/env python3
"""
Comprehensive API Test for Core Mechanics
Tests all core mechanics endpoints directly
"""

import requests
import json
import time
from datetime import datetime

def test_core_mechanics_api():
    """Test core mechanics API endpoints"""
    
    print("🧪 Testing Core Mechanics API")
    print("=" * 50)
    
    base_url = "http://localhost:5001"
    test_results = {
        'timestamp': datetime.utcnow().isoformat(),
        'tests': {},
        'overall_status': 'UNKNOWN'
    }
    
    # Test 1: Health Check
    print("🔍 Test 1: Health Check")
    try:
        response = requests.get(f"{base_url}/api/health", timeout=5)
        if response.status_code == 200:
            print("   ✅ Health check passed")
            test_results['tests']['health_check'] = 'PASS'
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
            test_results['tests']['health_check'] = 'FAIL'
    except Exception as e:
        print(f"   ❌ Health check error: {e}")
        test_results['tests']['health_check'] = 'ERROR'
    
    # Test 2: Core Mechanics Test Endpoint
    print("\\n🔍 Test 2: Core Mechanics Test")
    try:
        response = requests.get(f"{base_url}/api/mechanics/test", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                print("   ✅ Core mechanics test passed")
                print(f"   Character Health: {data['test_results']['test_character']['derived_attributes']['health']}")
                print(f"   Combat Damage: {data['test_results']['combat_result']['damage_dealt']}")
                test_results['tests']['core_mechanics_test'] = 'PASS'
                test_results['test_data'] = data['test_results']
            else:
                print(f"   ❌ Core mechanics test failed: {data}")
                test_results['tests']['core_mechanics_test'] = 'FAIL'
        else:
            print(f"   ❌ Core mechanics test failed: {response.status_code}")
            test_results['tests']['core_mechanics_test'] = 'FAIL'
    except Exception as e:
        print(f"   ❌ Core mechanics test error: {e}")
        test_results['tests']['core_mechanics_test'] = 'ERROR'
    
    # Test 3: Character Creation
    print("\\n🔍 Test 3: Character Creation")
    try:
        character_data = {
            'attributes': {
                'might': 15,
                'intellect': 12,
                'will': 10,
                'shadow': 0
            }
        }
        response = requests.post(f"{base_url}/api/mechanics/character/create", 
                               json=character_data, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                print("   ✅ Character creation passed")
                character = data['character']
                print(f"   Health: {character['derived_attributes']['health']}")
                print(f"   Mana: {character['derived_attributes']['mana']}")
                test_results['tests']['character_creation'] = 'PASS'
                test_results['sample_character'] = character
            else:
                print(f"   ❌ Character creation failed: {data}")
                test_results['tests']['character_creation'] = 'FAIL'
        else:
            print(f"   ❌ Character creation failed: {response.status_code}")
            test_results['tests']['character_creation'] = 'FAIL'
    except Exception as e:
        print(f"   ❌ Character creation error: {e}")
        test_results['tests']['character_creation'] = 'ERROR'
    
    # Test 4: Attribute Calculation
    print("\\n🔍 Test 4: Attribute Calculation")
    try:
        attr_data = {
            'attributes': {'might': 15, 'intellect': 12, 'will': 10, 'shadow': 5},
            'level': 5
        }
        response = requests.post(f"{base_url}/api/mechanics/character/attributes", 
                               json=attr_data, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                print("   ✅ Attribute calculation passed")
                attrs = data['derived_attributes']
                print(f"   Health: {attrs['health']}, Mana: {attrs['mana']}")
                test_results['tests']['attribute_calculation'] = 'PASS'
            else:
                print(f"   ❌ Attribute calculation failed: {data}")
                test_results['tests']['attribute_calculation'] = 'FAIL'
        else:
            print(f"   ❌ Attribute calculation failed: {response.status_code}")
            test_results['tests']['attribute_calculation'] = 'FAIL'
    except Exception as e:
        print(f"   ❌ Attribute calculation error: {e}")
        test_results['tests']['attribute_calculation'] = 'ERROR'
    
    # Test 5: Combat Simulation
    print("\\n🔍 Test 5: Combat Simulation")
    try:
        combat_data = {
            'attacker_attributes': {'might': 15, 'intellect': 10, 'will': 12, 'shadow': 0},
            'defender_attributes': {'might': 12, 'intellect': 8, 'will': 10, 'shadow': 0},
            'weapon_damage': 15,
            'armor_value': 8
        }
        response = requests.post(f"{base_url}/api/mechanics/combat/simulate", 
                               json=combat_data, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                print("   ✅ Combat simulation passed")
                combat = data['combat_result']
                print(f"   Hit: {combat['hit_success']}, Damage: {combat['damage_dealt']}")
                test_results['tests']['combat_simulation'] = 'PASS'
            else:
                print(f"   ❌ Combat simulation failed: {data}")
                test_results['tests']['combat_simulation'] = 'FAIL'
        else:
            print(f"   ❌ Combat simulation failed: {response.status_code}")
            test_results['tests']['combat_simulation'] = 'FAIL'
    except Exception as e:
        print(f"   ❌ Combat simulation error: {e}")
        test_results['tests']['combat_simulation'] = 'ERROR'
    
    # Calculate overall status
    passed_tests = sum(1 for result in test_results['tests'].values() if result == 'PASS')
    total_tests = len(test_results['tests'])
    
    if passed_tests == total_tests:
        test_results['overall_status'] = 'SUCCESS'
        status_emoji = "✅"
    elif passed_tests > 0:
        test_results['overall_status'] = 'PARTIAL'
        status_emoji = "⚠️"
    else:
        test_results['overall_status'] = 'FAILURE'
        status_emoji = "❌"
    
    print(f"\\n📊 CORE MECHANICS API TEST RESULTS")
    print("=" * 50)
    print(f"{status_emoji} Overall Status: {test_results['overall_status']}")
    print(f"✅ Tests Passed: {passed_tests}/{total_tests}")
    
    if passed_tests == total_tests:
        print("🎉 All core mechanics systems operational!")
        print("🚀 Ready for frontend integration")
    
    # Save results
    with open('/home/ubuntu/core_mechanics_api_test_results.json', 'w') as f:
        json.dump(test_results, f, indent=2)
    
    print("💾 Results saved to: /home/ubuntu/core_mechanics_api_test_results.json")
    
    return test_results

if __name__ == "__main__":
    test_core_mechanics_api()


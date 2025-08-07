#!/usr/bin/env python3
"""
Session Initialization Fix
Adds proper session initialization for equipment API testing
"""

# Add session initialization route to main.py
session_init_route = '''
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
'''

def add_session_init_to_main():
    """Add session initialization route to main.py"""
    print("=== Adding Session Initialization Route ===")
    
    try:
        # Read current main.py
        with open('/home/ubuntu/shadowlands-backend/src/main.py', 'r') as f:
            main_content = f.read()
        
        # Find the position to insert the new route (before the final if __name__ == '__main__':)
        insert_position = main_content.rfind("if __name__ == '__main__':")
        
        if insert_position == -1:
            print("❌ Could not find insertion point in main.py")
            return False
        
        # Insert the session initialization route
        new_content = (
            main_content[:insert_position] + 
            session_init_route + 
            "\n\n" + 
            main_content[insert_position:]
        )
        
        # Write back to main.py
        with open('/home/ubuntu/shadowlands-backend/src/main.py', 'w') as f:
            f.write(new_content)
        
        print("✅ Session initialization route added to main.py")
        return True
        
    except Exception as e:
        print(f"❌ Failed to add session initialization route: {e}")
        return False

def create_updated_integration_test():
    """Create updated integration test with session initialization"""
    print("\n=== Creating Updated Integration Test ===")
    
    updated_test_code = '''#!/usr/bin/env python3
"""
Updated Equipment Integration Test
Tests equipment API with proper session initialization
"""

import requests
import json
import time
from datetime import datetime

class EquipmentIntegrationTester:
    def __init__(self, base_url="http://localhost:5001"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def initialize_session(self):
        """Initialize session with character data"""
        print("=== Initializing Session ===")
        try:
            response = self.session.post(f"{self.base_url}/api/session/init", timeout=10)
            if response.status_code == 200:
                print("✅ Session initialized successfully")
                return True
            else:
                print(f"❌ Session initialization failed: {response.status_code}")
                print(f"Response: {response.text[:200]}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ Session initialization request failed: {e}")
            return False
    
    def test_equipment_endpoints(self):
        """Test all equipment API endpoints"""
        print("\\n=== Testing Equipment Endpoints ===")
        
        endpoints_to_test = [
            ("GET", "/api/equipment/test", None, "Equipment system test"),
            ("GET", "/api/equipment/available", None, "Available equipment"),
            ("GET", "/api/equipment/equipped", None, "Equipped items"),
            ("GET", "/api/equipment/stats", None, "Equipment statistics")
        ]
        
        results = {}
        
        for method, endpoint, data, description in endpoints_to_test:
            print(f"Testing {description}...")
            try:
                if method == "GET":
                    response = self.session.get(f"{self.base_url}{endpoint}", timeout=10)
                else:
                    response = self.session.post(f"{self.base_url}{endpoint}", 
                                               json=data, timeout=10)
                
                print(f"  Status: {response.status_code}")
                results[endpoint] = {
                    "status_code": response.status_code,
                    "success": response.status_code == 200,
                    "description": description
                }
                
                if response.status_code == 200:
                    try:
                        json_data = response.json()
                        print(f"  ✅ Success - Response keys: {list(json_data.keys())}")
                        results[endpoint]["response_keys"] = list(json_data.keys())
                        results[endpoint]["response_data"] = json_data
                    except json.JSONDecodeError:
                        print(f"  ⚠️ Success but response not JSON")
                        results[endpoint]["response_keys"] = []
                else:
                    print(f"  ❌ Error {response.status_code} - Response: {response.text[:200]}")
                    results[endpoint]["error"] = response.text[:200]
                    
            except requests.exceptions.RequestException as e:
                print(f"  ❌ Request failed: {e}")
                results[endpoint] = {
                    "status_code": None,
                    "success": False,
                    "error": str(e),
                    "description": description
                }
        
        return results
    
    def test_equipment_operations(self):
        """Test equipment equip/unequip operations"""
        print("\\n=== Testing Equipment Operations ===")
        
        operations_results = {}
        
        try:
            # First get available equipment
            print("Getting available equipment...")
            response = self.session.get(f"{self.base_url}/api/equipment/available", timeout=10)
            if response.status_code != 200:
                print(f"❌ Cannot get available equipment: {response.status_code}")
                return {"error": "Cannot get available equipment"}
            
            equipment_data = response.json()
            if not equipment_data.get("equipment"):
                print("❌ No equipment available for testing")
                return {"error": "No equipment available"}
            
            test_item = equipment_data["equipment"][0]
            item_id = test_item["item_id"]
            slot = test_item["slot"]
            
            print(f"Testing with item: {test_item['name']} (ID: {item_id})")
            operations_results["test_item"] = {
                "name": test_item["name"],
                "item_id": item_id,
                "slot": slot
            }
            
            # Test equip operation
            print("Testing equip operation...")
            equip_data = {
                "item_id": item_id,
                "slot": slot
            }
            
            response = self.session.post(f"{self.base_url}/api/equipment/equip", 
                                       json=equip_data, timeout=10)
            print(f"Equip status: {response.status_code}")
            
            operations_results["equip"] = {
                "status_code": response.status_code,
                "success": response.status_code == 200
            }
            
            if response.status_code == 200:
                print("✅ Equip operation successful")
                try:
                    equip_result = response.json()
                    operations_results["equip"]["response"] = equip_result
                    print(f"  Message: {equip_result.get('message', 'No message')}")
                except json.JSONDecodeError:
                    print("  ⚠️ Equip successful but response not JSON")
                
                # Test unequip operation
                print("Testing unequip operation...")
                unequip_data = {"slot": slot}
                
                response = self.session.post(f"{self.base_url}/api/equipment/unequip", 
                                           json=unequip_data, timeout=10)
                print(f"Unequip status: {response.status_code}")
                
                operations_results["unequip"] = {
                    "status_code": response.status_code,
                    "success": response.status_code == 200
                }
                
                if response.status_code == 200:
                    print("✅ Unequip operation successful")
                    try:
                        unequip_result = response.json()
                        operations_results["unequip"]["response"] = unequip_result
                        print(f"  Message: {unequip_result.get('message', 'No message')}")
                    except json.JSONDecodeError:
                        print("  ⚠️ Unequip successful but response not JSON")
                else:
                    print(f"❌ Unequip failed: {response.status_code}")
                    print(f"Response: {response.text[:200]}")
                    operations_results["unequip"]["error"] = response.text[:200]
            else:
                print(f"❌ Equip failed: {response.status_code}")
                print(f"Response: {response.text[:200]}")
                operations_results["equip"]["error"] = response.text[:200]
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Equipment operations failed: {e}")
            operations_results["error"] = str(e)
        except json.JSONDecodeError as e:
            print(f"❌ JSON decode error: {e}")
            operations_results["json_error"] = str(e)
        
        return operations_results
    
    def run_comprehensive_test(self):
        """Run all tests and generate report"""
        print("="*60)
        print("UPDATED EQUIPMENT INTEGRATION TEST")
        print("="*60)
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Target: {self.base_url}")
        print()
        
        # Wait for server to be ready
        print("Waiting for server to be ready...")
        time.sleep(3)
        
        # Initialize session
        session_initialized = self.initialize_session()
        if not session_initialized:
            print("❌ Cannot initialize session - aborting tests")
            return False
        
        # Run tests
        results = {
            "session_initialized": session_initialized,
            "equipment_endpoints": self.test_equipment_endpoints(),
            "equipment_operations": self.test_equipment_operations()
        }
        
        print("\\n" + "="*60)
        print("TEST SUMMARY")
        print("="*60)
        
        # Analyze results
        endpoint_results = results["equipment_endpoints"]
        endpoint_passed = sum(1 for r in endpoint_results.values() if r.get("success", False))
        endpoint_total = len(endpoint_results)
        
        operations_success = results["equipment_operations"].get("equip", {}).get("success", False) and \\
                           results["equipment_operations"].get("unequip", {}).get("success", False)
        
        print(f"SESSION INITIALIZATION: {'✅ PASS' if session_initialized else '❌ FAIL'}")
        print(f"EQUIPMENT ENDPOINTS: {endpoint_passed}/{endpoint_total} passed")
        print(f"EQUIPMENT OPERATIONS: {'✅ PASS' if operations_success else '❌ FAIL'}")
        
        # Detailed endpoint results
        for endpoint, result in endpoint_results.items():
            status = "✅ PASS" if result.get("success", False) else "❌ FAIL"
            print(f"  {endpoint}: {status} - {result.get('description', '')}")
        
        # Overall assessment
        total_categories = 3
        passed_categories = sum([
            session_initialized,
            endpoint_passed == endpoint_total,
            operations_success
        ])
        
        print(f"\\nOVERALL: {passed_categories}/{total_categories} test categories passed")
        
        # Save detailed results
        with open('/home/ubuntu/equipment_integration_test_results_updated.json', 'w') as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "target_url": self.base_url,
                "results": results,
                "summary": {
                    "passed_categories": passed_categories,
                    "total_categories": total_categories,
                    "success_rate": passed_categories / total_categories * 100,
                    "endpoint_success_rate": endpoint_passed / endpoint_total * 100 if endpoint_total > 0 else 0
                }
            }, f, indent=2, default=str)
        
        print(f"\\nDetailed results saved to: /home/ubuntu/equipment_integration_test_results_updated.json")
        
        if passed_categories == total_categories:
            print("\\n🎉 All integration tests passed! Equipment API is fully functional.")
        else:
            print(f"\\n⚠️ {total_categories - passed_categories} test categories failed. Review details above.")
        
        return passed_categories == total_categories

def main():
    tester = EquipmentIntegrationTester()
    success = tester.run_comprehensive_test()
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())
'''
    
    try:
        with open('/home/ubuntu/equipment_integration_test_updated.py', 'w') as f:
            f.write(updated_test_code)
        
        print("✅ Updated integration test created")
        print("Saved to: /home/ubuntu/equipment_integration_test_updated.py")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create updated integration test: {e}")
        return False

def main():
    """Main function to apply all fixes"""
    print("="*60)
    print("SESSION INITIALIZATION FIX")
    print("="*60)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Add session initialization route
    main_fix_success = add_session_init_to_main()
    
    # Create updated integration test
    test_fix_success = create_updated_integration_test()
    
    print("\\n" + "="*60)
    print("FIX SUMMARY")
    print("="*60)
    
    print(f"Session Init Route Added: {'✅ PASS' if main_fix_success else '❌ FAIL'}")
    print(f"Updated Test Created: {'✅ PASS' if test_fix_success else '❌ FAIL'}")
    
    if main_fix_success and test_fix_success:
        print("\\n🎉 Session initialization fix completed successfully!")
        print("\\nNext steps:")
        print("1. Restart the Flask server")
        print("2. Run the updated integration test")
        print("3. Verify equipment API functionality")
    else:
        print("\\n⚠️ Some fixes failed. Review the errors above.")
    
    return main_fix_success and test_fix_success

if __name__ == "__main__":
    from datetime import datetime
    success = main()
    exit(0 if success else 1)


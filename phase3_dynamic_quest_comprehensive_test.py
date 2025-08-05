#!/usr/bin/env python3
"""
Phase 3: Dynamic Quest Generation - Comprehensive Test Suite
Tests all aspects of the dynamic quest generation and narrative system
"""

import requests
import json
import time
from typing import Dict, Any

class DynamicQuestSystemTester:
    """Comprehensive tester for the dynamic quest generation system"""
    
    def __init__(self, base_url: str = "http://localhost:5002"):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = []
    
    def log_test(self, test_name: str, success: bool, details: str = ""):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"   {status}: {test_name}")
        if details:
            print(f"      {details}")
        
        self.test_results.append({
            "test": test_name,
            "success": success,
            "details": details
        })
    
    def test_server_health(self) -> bool:
        """Test server health and basic connectivity"""
        try:
            response = self.session.get(f"{self.base_url}/api/health")
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and "quest_engine" in data.get("status", {}):
                    self.log_test("Server Health Check", True, f"Quest engine: {data['status']['quest_engine']}")
                    return True
            
            self.log_test("Server Health Check", False, f"Status: {response.status_code}")
            return False
        except Exception as e:
            self.log_test("Server Health Check", False, f"Error: {str(e)}")
            return False
    
    def test_session_initialization(self) -> bool:
        """Test session initialization"""
        try:
            response = self.session.get(f"{self.base_url}/api/session/init")
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and "character_data" in data:
                    character = data["character_data"]
                    self.log_test("Session Initialization", True, 
                                f"Character: {character.get('name', 'Unknown')}, Level: {character.get('level', 0)}")
                    return True
            
            self.log_test("Session Initialization", False, f"Status: {response.status_code}")
            return False
        except Exception as e:
            self.log_test("Session Initialization", False, f"Error: {str(e)}")
            return False
    
    def test_narrative_context(self) -> bool:
        """Test narrative context retrieval"""
        try:
            response = self.session.get(f"{self.base_url}/api/dynamic-quests/narrative-context")
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and "narrative_context" in data.get("data", {}):
                    context = data["data"]["narrative_context"]
                    archetype = context.get("character_archetype", "unknown")
                    themes = len(context.get("theme_affinity", {}))
                    self.log_test("Narrative Context", True, 
                                f"Archetype: {archetype}, Themes: {themes}")
                    return True
            
            self.log_test("Narrative Context", False, f"Status: {response.status_code}")
            return False
        except Exception as e:
            self.log_test("Narrative Context", False, f"Error: {str(e)}")
            return False
    
    def test_themes_endpoint(self) -> bool:
        """Test themes endpoint"""
        try:
            response = self.session.get(f"{self.base_url}/api/dynamic-quests/themes")
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and "themes" in data.get("data", {}):
                    themes = data["data"]["themes"]
                    total = data["data"].get("total_themes", 0)
                    self.log_test("Themes Endpoint", True, 
                                f"Retrieved {total} themes with descriptions and affinities")
                    return True
            
            self.log_test("Themes Endpoint", False, f"Status: {response.status_code}")
            return False
        except Exception as e:
            self.log_test("Themes Endpoint", False, f"Error: {str(e)}")
            return False
    
    def test_archetypes_endpoint(self) -> bool:
        """Test archetypes endpoint"""
        try:
            response = self.session.get(f"{self.base_url}/api/dynamic-quests/archetypes")
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and "archetypes" in data.get("data", {}):
                    archetypes = data["data"]["archetypes"]
                    current = data["data"].get("current_archetype", "unknown")
                    self.log_test("Archetypes Endpoint", True, 
                                f"Retrieved {len(archetypes)} archetypes, current: {current}")
                    return True
            
            self.log_test("Archetypes Endpoint", False, f"Status: {response.status_code}")
            return False
        except Exception as e:
            self.log_test("Archetypes Endpoint", False, f"Error: {str(e)}")
            return False
    
    def test_triggers_endpoint(self) -> bool:
        """Test triggers endpoint"""
        try:
            response = self.session.get(f"{self.base_url}/api/dynamic-quests/triggers")
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and "triggers" in data.get("data", {}):
                    triggers = data["data"]["triggers"]
                    self.log_test("Triggers Endpoint", True, 
                                f"Retrieved {len(triggers)} quest trigger types")
                    return True
            
            self.log_test("Triggers Endpoint", False, f"Status: {response.status_code}")
            return False
        except Exception as e:
            self.log_test("Triggers Endpoint", False, f"Error: {str(e)}")
            return False
    
    def test_dynamic_quest_generation(self) -> bool:
        """Test dynamic quest generation"""
        try:
            # Test different triggers and contexts
            test_cases = [
                {"trigger": "random_encounter", "location_context": "Ancient Ruins"},
                {"trigger": "location_discovery", "location_context": "Corrupted Forest"},
                {"trigger": "character_choice"},
                {"trigger": "npc_interaction", "location_context": "Village Square"}
            ]
            
            successful_generations = 0
            
            for i, test_case in enumerate(test_cases):
                response = self.session.post(
                    f"{self.base_url}/api/dynamic-quests/generate",
                    json=test_case,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("success") and "generated_quest" in data.get("data", {}):
                        quest = data["data"]["generated_quest"]
                        successful_generations += 1
                        
                        # Validate quest structure
                        required_fields = ["title", "description", "quest_type", "complexity", "objectives", "rewards"]
                        if all(field in quest for field in required_fields):
                            self.log_test(f"Dynamic Quest Generation #{i+1}", True, 
                                        f"Generated: {quest['title'][:50]}...")
                        else:
                            self.log_test(f"Dynamic Quest Generation #{i+1}", False, 
                                        "Missing required quest fields")
                    else:
                        self.log_test(f"Dynamic Quest Generation #{i+1}", False, 
                                    f"Invalid response structure")
                else:
                    self.log_test(f"Dynamic Quest Generation #{i+1}", False, 
                                f"Status: {response.status_code}")
            
            # Overall success if at least 75% of generations succeeded
            overall_success = successful_generations >= len(test_cases) * 0.75
            self.log_test("Dynamic Quest Generation Overall", overall_success, 
                        f"{successful_generations}/{len(test_cases)} successful generations")
            
            return overall_success
            
        except Exception as e:
            self.log_test("Dynamic Quest Generation", False, f"Error: {str(e)}")
            return False
    
    def test_statistics_endpoint(self) -> bool:
        """Test statistics endpoint"""
        try:
            response = self.session.get(f"{self.base_url}/api/dynamic-quests/statistics")
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    stats = data.get("data", {})
                    char_stats = stats.get("character_statistics", {})
                    sys_stats = stats.get("system_statistics", {})
                    
                    self.log_test("Statistics Endpoint", True, 
                                f"Character stats: {len(char_stats)} fields, System stats: {len(sys_stats)} fields")
                    return True
            
            self.log_test("Statistics Endpoint", False, f"Status: {response.status_code}")
            return False
        except Exception as e:
            self.log_test("Statistics Endpoint", False, f"Error: {str(e)}")
            return False
    
    def test_integration_with_core_system(self) -> bool:
        """Test integration with core quest system"""
        try:
            # Generate a dynamic quest
            response = self.session.post(
                f"{self.base_url}/api/dynamic-quests/generate",
                json={"trigger": "random_encounter"},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code != 200:
                self.log_test("Core System Integration", False, "Failed to generate dynamic quest")
                return False
            
            quest_data = response.json()
            if not quest_data.get("success"):
                self.log_test("Core System Integration", False, "Dynamic quest generation failed")
                return False
            
            # Try to start the generated quest using core system
            generated_quest = quest_data["data"]["generated_quest"]
            template_id = generated_quest["template_id"]
            
            start_response = self.session.post(
                f"{self.base_url}/api/quests/start",
                json={"template_id": template_id},
                headers={"Content-Type": "application/json"}
            )
            
            if start_response.status_code == 200:
                start_data = start_response.json()
                if start_data.get("success"):
                    self.log_test("Core System Integration", True, 
                                f"Successfully started dynamic quest: {template_id}")
                    return True
            
            self.log_test("Core System Integration", False, 
                        f"Failed to start dynamic quest: {start_response.status_code}")
            return False
            
        except Exception as e:
            self.log_test("Core System Integration", False, f"Error: {str(e)}")
            return False
    
    def run_comprehensive_test(self) -> Dict[str, Any]:
        """Run all tests and return results"""
        print("🎮 Phase 3: Dynamic Quest Generation - Comprehensive Test")
        print("=" * 60)
        
        # Run all tests
        tests = [
            ("1. Server Health", self.test_server_health),
            ("2. Session Initialization", self.test_session_initialization),
            ("3. Narrative Context", self.test_narrative_context),
            ("4. Themes Endpoint", self.test_themes_endpoint),
            ("5. Archetypes Endpoint", self.test_archetypes_endpoint),
            ("6. Triggers Endpoint", self.test_triggers_endpoint),
            ("7. Dynamic Quest Generation", self.test_dynamic_quest_generation),
            ("8. Statistics Endpoint", self.test_statistics_endpoint),
            ("9. Core System Integration", self.test_integration_with_core_system)
        ]
        
        passed_tests = 0
        total_tests = len(tests)
        
        for test_name, test_func in tests:
            print(f"\n{test_name}...")
            if test_func():
                passed_tests += 1
        
        # Calculate success rate
        success_rate = (passed_tests / total_tests) * 100
        
        print("\n" + "=" * 60)
        print(f"🎯 TEST RESULTS SUMMARY")
        print(f"   Passed: {passed_tests}/{total_tests} tests")
        print(f"   Success Rate: {success_rate:.1f}%")
        
        if success_rate >= 90:
            print("🎉 PHASE 3: DYNAMIC QUEST GENERATION - SUCCESS!")
            print("✅ All core dynamic quest functionality is working correctly!")
            print("✅ Narrative context and character archetypes functional")
            print("✅ Dynamic quest generation with multiple triggers working")
            print("✅ Integration with core quest system successful")
            print("🎮 Dynamic quest system is ready for production!")
        elif success_rate >= 75:
            print("⚠️  PHASE 3: DYNAMIC QUEST GENERATION - MOSTLY SUCCESSFUL")
            print("✅ Core functionality working with minor issues")
        else:
            print("❌ PHASE 3: DYNAMIC QUEST GENERATION - NEEDS ATTENTION")
            print("⚠️  Significant issues detected that need resolution")
        
        return {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "success_rate": success_rate,
            "test_results": self.test_results
        }

def main():
    """Main test execution"""
    tester = DynamicQuestSystemTester()
    results = tester.run_comprehensive_test()
    
    # Save results to file
    with open("/home/ubuntu/phase3_dynamic_quest_test_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    return results["success_rate"] >= 90

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)


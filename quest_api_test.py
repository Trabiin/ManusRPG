#!/usr/bin/env python3
"""
Shadowlands RPG - Quest API Testing Suite
Comprehensive testing of quest system API endpoints
"""

import requests
import json
import time
from typing import Dict, Any, List

class QuestAPITester:
    """Comprehensive quest API testing framework"""
    
    def __init__(self, base_url: str = "http://localhost:5002"):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = []
        
        # Enable session cookies for authentication
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def log_test(self, test_name: str, success: bool, details: str = "", response_data: Any = None):
        """Log test results"""
        result = {
            "test_name": test_name,
            "success": success,
            "details": details,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "response_data": response_data
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {details}")
        
        if response_data and not success:
            print(f"   Response: {json.dumps(response_data, indent=2)}")
    
    def setup_test_session(self) -> bool:
        """Set up test session with character data"""
        try:
            # Create a test character session
            character_data = {
                "name": "Test Drifter",
                "level": 5,
                "attributes": {
                    "might": 12,
                    "intellect": 10,
                    "will": 14,
                    "shadow": 8
                }
            }
            
            # Simulate session setup by making a request that creates session data
            response = self.session.get(f"{self.base_url}/api/quests/templates")
            
            if response.status_code == 200:
                self.log_test("Session Setup", True, "Test session established successfully")
                return True
            else:
                self.log_test("Session Setup", False, f"Failed to establish session: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Session Setup", False, f"Exception during session setup: {str(e)}")
            return False
    
    def test_get_quest_templates(self) -> bool:
        """Test retrieving quest templates"""
        try:
            response = self.session.get(f"{self.base_url}/api/quests/templates")
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and "templates" in data.get("data", {}):
                    templates = data["data"]["templates"]
                    self.log_test(
                        "Get Quest Templates", 
                        True, 
                        f"Retrieved {len(templates)} quest templates",
                        {"template_count": len(templates), "templates": templates}
                    )
                    return True
                else:
                    self.log_test("Get Quest Templates", False, "Invalid response format", data)
                    return False
            else:
                self.log_test("Get Quest Templates", False, f"HTTP {response.status_code}", response.json())
                return False
                
        except Exception as e:
            self.log_test("Get Quest Templates", False, f"Exception: {str(e)}")
            return False
    
    def test_get_available_quests(self) -> bool:
        """Test retrieving available quests for character"""
        try:
            response = self.session.get(f"{self.base_url}/api/quests/available")
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and "available_quests" in data.get("data", {}):
                    available_quests = data["data"]["available_quests"]
                    self.log_test(
                        "Get Available Quests", 
                        True, 
                        f"Found {len(available_quests)} available quests",
                        {"available_count": len(available_quests)}
                    )
                    return True
                else:
                    self.log_test("Get Available Quests", False, "Invalid response format", data)
                    return False
            else:
                self.log_test("Get Available Quests", False, f"HTTP {response.status_code}", response.json())
                return False
                
        except Exception as e:
            self.log_test("Get Available Quests", False, f"Exception: {str(e)}")
            return False
    
    def test_start_quest(self) -> str:
        """Test starting a quest and return quest ID"""
        try:
            # First get available quests
            response = self.session.get(f"{self.base_url}/api/quests/available")
            if response.status_code != 200:
                self.log_test("Start Quest - Get Available", False, "Failed to get available quests")
                return None
            
            available_data = response.json()
            available_quests = available_data.get("data", {}).get("available_quests", [])
            
            if not available_quests:
                self.log_test("Start Quest", False, "No available quests to start")
                return None
            
            # Start the first available quest
            template_id = available_quests[0]["template_id"]
            start_data = {"template_id": template_id}
            
            response = self.session.post(
                f"{self.base_url}/api/quests/start",
                json=start_data
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and "quest" in data.get("data", {}):
                    quest = data["data"]["quest"]
                    quest_id = quest["quest_id"]
                    self.log_test(
                        "Start Quest", 
                        True, 
                        f"Started quest: {quest['title']} (ID: {quest_id})",
                        {"quest_id": quest_id, "quest_title": quest["title"]}
                    )
                    return quest_id
                else:
                    self.log_test("Start Quest", False, "Invalid response format", data)
                    return None
            else:
                self.log_test("Start Quest", False, f"HTTP {response.status_code}", response.json())
                return None
                
        except Exception as e:
            self.log_test("Start Quest", False, f"Exception: {str(e)}")
            return None
    
    def test_get_active_quests(self) -> bool:
        """Test retrieving active quests"""
        try:
            response = self.session.get(f"{self.base_url}/api/quests/active")
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and "active_quests" in data.get("data", {}):
                    active_quests = data["data"]["active_quests"]
                    self.log_test(
                        "Get Active Quests", 
                        True, 
                        f"Retrieved {len(active_quests)} active quests",
                        {"active_count": len(active_quests)}
                    )
                    return True
                else:
                    self.log_test("Get Active Quests", False, "Invalid response format", data)
                    return False
            else:
                self.log_test("Get Active Quests", False, f"HTTP {response.status_code}", response.json())
                return False
                
        except Exception as e:
            self.log_test("Get Active Quests", False, f"Exception: {str(e)}")
            return False
    
    def test_quest_details(self, quest_id: str) -> bool:
        """Test retrieving quest details"""
        if not quest_id:
            self.log_test("Get Quest Details", False, "No quest ID provided")
            return False
        
        try:
            response = self.session.get(f"{self.base_url}/api/quests/{quest_id}")
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and "quest" in data.get("data", {}):
                    quest = data["data"]["quest"]
                    self.log_test(
                        "Get Quest Details", 
                        True, 
                        f"Retrieved details for quest: {quest['title']}",
                        {"quest_title": quest["title"], "objectives_count": len(quest.get("objectives", []))}
                    )
                    return True
                else:
                    self.log_test("Get Quest Details", False, "Invalid response format", data)
                    return False
            else:
                self.log_test("Get Quest Details", False, f"HTTP {response.status_code}", response.json())
                return False
                
        except Exception as e:
            self.log_test("Get Quest Details", False, f"Exception: {str(e)}")
            return False
    
    def test_objective_progress(self, quest_id: str) -> bool:
        """Test updating quest objective progress"""
        if not quest_id:
            self.log_test("Update Objective Progress", False, "No quest ID provided")
            return False
        
        try:
            # First get quest details to find an objective
            response = self.session.get(f"{self.base_url}/api/quests/{quest_id}")
            if response.status_code != 200:
                self.log_test("Update Objective Progress - Get Quest", False, "Failed to get quest details")
                return False
            
            quest_data = response.json()
            quest = quest_data.get("data", {}).get("quest", {})
            objectives = quest.get("objectives", [])
            
            if not objectives:
                self.log_test("Update Objective Progress", False, "No objectives found in quest")
                return False
            
            # Update progress for the first objective
            objective_id = objectives[0]["objective_id"]
            progress_data = {"increment": 1}
            
            response = self.session.post(
                f"{self.base_url}/api/quests/{quest_id}/objective/{objective_id}/progress",
                json=progress_data
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    result_data = data.get("data", {})
                    self.log_test(
                        "Update Objective Progress", 
                        True, 
                        f"Updated objective progress. Completed: {result_data.get('objective_completed', False)}",
                        result_data
                    )
                    return True
                else:
                    self.log_test("Update Objective Progress", False, "Update failed", data)
                    return False
            else:
                self.log_test("Update Objective Progress", False, f"HTTP {response.status_code}", response.json())
                return False
                
        except Exception as e:
            self.log_test("Update Objective Progress", False, f"Exception: {str(e)}")
            return False
    
    def test_quest_choice(self, quest_id: str) -> bool:
        """Test making a quest choice"""
        if not quest_id:
            self.log_test("Make Quest Choice", False, "No quest ID provided")
            return False
        
        try:
            # First get quest details to find a choice
            response = self.session.get(f"{self.base_url}/api/quests/{quest_id}")
            if response.status_code != 200:
                self.log_test("Make Quest Choice - Get Quest", False, "Failed to get quest details")
                return False
            
            quest_data = response.json()
            quest = quest_data.get("data", {}).get("quest", {})
            choices = quest.get("choices", [])
            
            if not choices:
                self.log_test("Make Quest Choice", False, "No choices found in quest")
                return False
            
            # Make the first available choice
            choice_id = choices[0]["choice_id"]
            
            response = self.session.post(f"{self.base_url}/api/quests/{quest_id}/choice/{choice_id}")
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    result_data = data.get("data", {})
                    self.log_test(
                        "Make Quest Choice", 
                        True, 
                        f"Made quest choice successfully. Consequences: {len(result_data.get('consequences', []))}",
                        result_data
                    )
                    return True
                else:
                    self.log_test("Make Quest Choice", False, "Choice failed", data)
                    return False
            else:
                self.log_test("Make Quest Choice", False, f"HTTP {response.status_code}", response.json())
                return False
                
        except Exception as e:
            self.log_test("Make Quest Choice", False, f"Exception: {str(e)}")
            return False
    
    def test_quest_statistics(self) -> bool:
        """Test retrieving quest statistics"""
        try:
            response = self.session.get(f"{self.base_url}/api/quests/statistics")
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    stats = data.get("data", {})
                    engine_stats = stats.get("engine_statistics", {})
                    character_stats = stats.get("character_statistics", {})
                    
                    self.log_test(
                        "Get Quest Statistics", 
                        True, 
                        f"Retrieved statistics. Active: {character_stats.get('character_active_quests', 0)}, Completed: {character_stats.get('character_completed_quests', 0)}",
                        stats
                    )
                    return True
                else:
                    self.log_test("Get Quest Statistics", False, "Invalid response format", data)
                    return False
            else:
                self.log_test("Get Quest Statistics", False, f"HTTP {response.status_code}", response.json())
                return False
                
        except Exception as e:
            self.log_test("Get Quest Statistics", False, f"Exception: {str(e)}")
            return False
    
    def run_comprehensive_test(self) -> Dict[str, Any]:
        """Run comprehensive quest API test suite"""
        print("🎮 Shadowlands Quest API - Comprehensive Test Suite")
        print("=" * 60)
        
        # Setup test session
        if not self.setup_test_session():
            print("❌ Failed to setup test session. Aborting tests.")
            return self.generate_test_report()
        
        # Run all tests
        self.test_get_quest_templates()
        self.test_get_available_quests()
        
        # Start a quest and get its ID for further testing
        quest_id = self.test_start_quest()
        
        self.test_get_active_quests()
        
        if quest_id:
            self.test_quest_details(quest_id)
            self.test_objective_progress(quest_id)
            self.test_quest_choice(quest_id)
        
        self.test_quest_statistics()
        
        return self.generate_test_report()
    
    def generate_test_report(self) -> Dict[str, Any]:
        """Generate comprehensive test report"""
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r["success"]])
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        report = {
            "test_summary": {
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "failed_tests": failed_tests,
                "success_rate": round(success_rate, 2)
            },
            "test_results": self.test_results,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        print("\\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {success_rate:.1f}%")
        
        if failed_tests > 0:
            print("\\n❌ FAILED TESTS:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"  • {result['test_name']}: {result['details']}")
        
        return report

def main():
    """Main test execution"""
    tester = QuestAPITester()
    
    try:
        report = tester.run_comprehensive_test()
        
        # Save test results
        with open('/home/ubuntu/quest_api_test_results.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\\n📄 Test results saved to: quest_api_test_results.json")
        
        return report["test_summary"]["success_rate"] > 80
        
    except Exception as e:
        print(f"\\n❌ Test suite failed with exception: {str(e)}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)


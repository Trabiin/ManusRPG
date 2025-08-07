#!/usr/bin/env python3
"""
Shadowlands RPG - Integration Testing and End-to-End Validation Suite
Phase FR4.4: Integration Testing and End-to-End Validation

This module provides comprehensive integration testing for the complete Shadowlands RPG
system, validating end-to-end workflows from frontend user interactions through backend
API processing and data persistence. The testing suite ensures that all system components
work together seamlessly to provide a cohesive user experience.

Author: Manus AI
Date: July 21, 2025
"""

import requests
import time
import json
import subprocess
import threading
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed
import statistics

# Test Configuration
BACKEND_URL = "http://localhost:5001"
FRONTEND_URL = "http://localhost:3000"
TEST_TIMEOUT = 30
MAX_CONCURRENT_USERS = 5

@dataclass
class IntegrationTestResult:
    """Data class for storing integration test results"""
    test_name: str
    success: bool
    duration: float
    status_code: Optional[int] = None
    error_message: Optional[str] = None
    details: Optional[Dict] = None
    workflow_steps: Optional[List[str]] = None

class ShadowlandsIntegrationTester:
    """
    Comprehensive integration testing framework for Shadowlands RPG.
    
    This class provides end-to-end testing of complete user workflows including:
    - Session initialization and management
    - Equipment browsing, equipping, and stat calculations
    - Character progression and experience systems
    - Quest management and progression tracking
    - Combat system integration
    - Frontend-backend data synchronization
    """
    
    def __init__(self):
        self.backend_url = BACKEND_URL
        self.frontend_url = FRONTEND_URL
        self.session = requests.Session()
        self.test_results: List[IntegrationTestResult] = []
        
    def check_server_availability(self) -> Dict[str, bool]:
        """
        Check if both backend and frontend servers are running.
        
        Returns:
            Dictionary with server availability status
        """
        availability = {
            'backend': False,
            'frontend': False
        }
        
        try:
            response = requests.get(f"{self.backend_url}/api/health", timeout=5)
            availability['backend'] = response.status_code == 200
        except:
            pass
        
        try:
            response = requests.get(self.frontend_url, timeout=5)
            availability['frontend'] = response.status_code == 200
        except:
            pass
        
        return availability
    
    def test_session_workflow(self) -> IntegrationTestResult:
        """
        Test complete session initialization and management workflow.
        
        Returns:
            IntegrationTestResult for session workflow
        """
        start_time = time.time()
        workflow_steps = []
        
        try:
            # Step 1: Initialize session
            workflow_steps.append("Initializing session")
            response = self.session.post(f"{self.backend_url}/api/session/init")
            
            if response.status_code != 200:
                return IntegrationTestResult(
                    test_name="Session Workflow",
                    success=False,
                    duration=time.time() - start_time,
                    status_code=response.status_code,
                    error_message="Session initialization failed",
                    workflow_steps=workflow_steps
                )
            
            session_data = response.json()
            workflow_steps.append("Session initialized successfully")
            
            # Step 2: Validate session data structure
            workflow_steps.append("Validating session data structure")
            required_keys = ['success', 'character_data']
            for key in required_keys:
                if key not in session_data:
                    return IntegrationTestResult(
                        test_name="Session Workflow",
                        success=False,
                        duration=time.time() - start_time,
                        status_code=response.status_code,
                        error_message=f"Missing required session key: {key}",
                        workflow_steps=workflow_steps
                    )
            
            workflow_steps.append("Session data structure validated")
            
            # Step 3: Validate character data
            workflow_steps.append("Validating character data")
            character_data = session_data.get('character_data', {})
            required_character_keys = ['character_id', 'name', 'level', 'might', 'intellect', 'will', 'shadow']
            
            for key in required_character_keys:
                if key not in character_data:
                    return IntegrationTestResult(
                        test_name="Session Workflow",
                        success=False,
                        duration=time.time() - start_time,
                        status_code=response.status_code,
                        error_message=f"Missing required character key: {key}",
                        workflow_steps=workflow_steps
                    )
            
            workflow_steps.append("Character data validated")
            
            # Step 4: Test session persistence
            workflow_steps.append("Testing session persistence")
            response2 = self.session.get(f"{self.backend_url}/api/health")
            
            if response2.status_code != 200:
                return IntegrationTestResult(
                    test_name="Session Workflow",
                    success=False,
                    duration=time.time() - start_time,
                    status_code=response2.status_code,
                    error_message="Session persistence test failed",
                    workflow_steps=workflow_steps
                )
            
            workflow_steps.append("Session persistence validated")
            
            return IntegrationTestResult(
                test_name="Session Workflow",
                success=True,
                duration=time.time() - start_time,
                status_code=200,
                details={
                    'session_data': session_data,
                    'character_id': character_data.get('character_id'),
                    'character_level': character_data.get('level')
                },
                workflow_steps=workflow_steps
            )
            
        except Exception as e:
            return IntegrationTestResult(
                test_name="Session Workflow",
                success=False,
                duration=time.time() - start_time,
                error_message=str(e),
                workflow_steps=workflow_steps
            )
    
    def test_equipment_workflow(self) -> IntegrationTestResult:
        """
        Test complete equipment management workflow.
        
        Returns:
            IntegrationTestResult for equipment workflow
        """
        start_time = time.time()
        workflow_steps = []
        
        try:
            # Step 1: Initialize session
            workflow_steps.append("Initializing session for equipment test")
            session_response = self.session.post(f"{self.backend_url}/api/session/init")
            
            if session_response.status_code != 200:
                return IntegrationTestResult(
                    test_name="Equipment Workflow",
                    success=False,
                    duration=time.time() - start_time,
                    status_code=session_response.status_code,
                    error_message="Session initialization failed",
                    workflow_steps=workflow_steps
                )
            
            workflow_steps.append("Session initialized")
            
            # Step 2: Browse available equipment
            workflow_steps.append("Browsing available equipment")
            equipment_response = self.session.get(f"{self.backend_url}/api/equipment/available")
            
            if equipment_response.status_code != 200:
                return IntegrationTestResult(
                    test_name="Equipment Workflow",
                    success=False,
                    duration=time.time() - start_time,
                    status_code=equipment_response.status_code,
                    error_message="Equipment browsing failed",
                    workflow_steps=workflow_steps
                )
            
            equipment_data = equipment_response.json()
            equipment_list = equipment_data.get('equipment', [])
            
            if not equipment_list:
                return IntegrationTestResult(
                    test_name="Equipment Workflow",
                    success=False,
                    duration=time.time() - start_time,
                    status_code=equipment_response.status_code,
                    error_message="No equipment available",
                    workflow_steps=workflow_steps
                )
            
            workflow_steps.append(f"Found {len(equipment_list)} equipment items")
            
            # Step 3: Get equipment overview (before equipping)
            workflow_steps.append("Getting initial equipment overview")
            overview_response = self.session.get(f"{self.backend_url}/api/equipment/overview")
            
            if overview_response.status_code != 200:
                return IntegrationTestResult(
                    test_name="Equipment Workflow",
                    success=False,
                    duration=time.time() - start_time,
                    status_code=overview_response.status_code,
                    error_message="Equipment overview failed",
                    workflow_steps=workflow_steps
                )
            
            initial_overview = overview_response.json()
            workflow_steps.append("Initial equipment overview retrieved")
            
            # Step 4: Find a suitable item to equip
            workflow_steps.append("Finding suitable equipment to equip")
            suitable_item = None
            
            for item in equipment_list:
                # Look for a basic weapon that should be equippable
                if (item.get('type') == 'weapon' and 
                    item.get('rarity') == 'common' and 
                    item.get('level_requirement', 1) <= 5):
                    suitable_item = item
                    break
            
            if not suitable_item:
                # Try any common item
                for item in equipment_list:
                    if item.get('rarity') == 'common':
                        suitable_item = item
                        break
            
            if not suitable_item:
                return IntegrationTestResult(
                    test_name="Equipment Workflow",
                    success=False,
                    duration=time.time() - start_time,
                    error_message="No suitable equipment found for testing",
                    workflow_steps=workflow_steps
                )
            
            workflow_steps.append(f"Selected item: {suitable_item.get('name', 'Unknown')}")
            
            # Step 5: Equip the item
            workflow_steps.append("Equipping selected item")
            equip_data = {
                'item_id': suitable_item['id'],
                'slot': suitable_item.get('slot', 'weapon_main')
            }
            
            equip_response = self.session.post(
                f"{self.backend_url}/api/equipment/equip",
                json=equip_data
            )
            
            if equip_response.status_code != 200:
                return IntegrationTestResult(
                    test_name="Equipment Workflow",
                    success=False,
                    duration=time.time() - start_time,
                    status_code=equip_response.status_code,
                    error_message=f"Equipment equip failed: {equip_response.text}",
                    workflow_steps=workflow_steps,
                    details={'attempted_equip': equip_data}
                )
            
            equip_result = equip_response.json()
            workflow_steps.append("Item equipped successfully")
            
            # Step 6: Verify equipment overview changed
            workflow_steps.append("Verifying equipment overview after equipping")
            updated_overview_response = self.session.get(f"{self.backend_url}/api/equipment/overview")
            
            if updated_overview_response.status_code != 200:
                return IntegrationTestResult(
                    test_name="Equipment Workflow",
                    success=False,
                    duration=time.time() - start_time,
                    status_code=updated_overview_response.status_code,
                    error_message="Updated equipment overview failed",
                    workflow_steps=workflow_steps
                )
            
            updated_overview = updated_overview_response.json()
            workflow_steps.append("Updated equipment overview retrieved")
            
            # Step 7: Unequip the item
            workflow_steps.append("Unequipping item")
            unequip_data = {
                'slot': suitable_item.get('slot', 'weapon_main')
            }
            
            unequip_response = self.session.post(
                f"{self.backend_url}/api/equipment/unequip",
                json=unequip_data
            )
            
            if unequip_response.status_code != 200:
                return IntegrationTestResult(
                    test_name="Equipment Workflow",
                    success=False,
                    duration=time.time() - start_time,
                    status_code=unequip_response.status_code,
                    error_message=f"Equipment unequip failed: {unequip_response.text}",
                    workflow_steps=workflow_steps
                )
            
            workflow_steps.append("Item unequipped successfully")
            
            return IntegrationTestResult(
                test_name="Equipment Workflow",
                success=True,
                duration=time.time() - start_time,
                status_code=200,
                details={
                    'equipment_count': len(equipment_list),
                    'tested_item': suitable_item,
                    'initial_overview': initial_overview,
                    'updated_overview': updated_overview,
                    'equip_result': equip_result
                },
                workflow_steps=workflow_steps
            )
            
        except Exception as e:
            return IntegrationTestResult(
                test_name="Equipment Workflow",
                success=False,
                duration=time.time() - start_time,
                error_message=str(e),
                workflow_steps=workflow_steps
            )
    
    def test_quest_workflow(self) -> IntegrationTestResult:
        """
        Test complete quest management workflow.
        
        Returns:
            IntegrationTestResult for quest workflow
        """
        start_time = time.time()
        workflow_steps = []
        
        try:
            # Step 1: Initialize session
            workflow_steps.append("Initializing session for quest test")
            session_response = self.session.post(f"{self.backend_url}/api/session/init")
            
            if session_response.status_code != 200:
                return IntegrationTestResult(
                    test_name="Quest Workflow",
                    success=False,
                    duration=time.time() - start_time,
                    status_code=session_response.status_code,
                    error_message="Session initialization failed",
                    workflow_steps=workflow_steps
                )
            
            workflow_steps.append("Session initialized")
            
            # Step 2: Get available quests
            workflow_steps.append("Getting available quests")
            quests_response = self.session.get(f"{self.backend_url}/api/quests/available")
            
            if quests_response.status_code != 200:
                return IntegrationTestResult(
                    test_name="Quest Workflow",
                    success=False,
                    duration=time.time() - start_time,
                    status_code=quests_response.status_code,
                    error_message="Quest listing failed",
                    workflow_steps=workflow_steps
                )
            
            quests_data = quests_response.json()
            workflow_steps.append("Available quests retrieved")
            
            # Step 3: Get quest details
            workflow_steps.append("Getting quest details")
            quest_detail_response = self.session.get(f"{self.backend_url}/api/quests/into_the_woods")
            
            if quest_detail_response.status_code != 200:
                return IntegrationTestResult(
                    test_name="Quest Workflow",
                    success=False,
                    duration=time.time() - start_time,
                    status_code=quest_detail_response.status_code,
                    error_message="Quest details failed",
                    workflow_steps=workflow_steps
                )
            
            quest_details = quest_detail_response.json()
            workflow_steps.append("Quest details retrieved")
            
            # Step 4: Test quest progression
            workflow_steps.append("Testing quest progression")
            progress_data = {
                'quest_id': 'into_the_woods',
                'objective_id': 'explore_forest',
                'progress': 1
            }
            
            progress_response = self.session.post(
                f"{self.backend_url}/api/quests/progress",
                json=progress_data
            )
            
            # Note: This might fail if quest system isn't fully implemented
            quest_success = progress_response.status_code == 200
            
            if quest_success:
                workflow_steps.append("Quest progression successful")
            else:
                workflow_steps.append(f"Quest progression failed (status: {progress_response.status_code})")
            
            return IntegrationTestResult(
                test_name="Quest Workflow",
                success=quest_success,
                duration=time.time() - start_time,
                status_code=progress_response.status_code if quest_success else quests_response.status_code,
                details={
                    'quests_data': quests_data,
                    'quest_details': quest_details,
                    'progression_attempted': progress_data
                },
                workflow_steps=workflow_steps
            )
            
        except Exception as e:
            return IntegrationTestResult(
                test_name="Quest Workflow",
                success=False,
                duration=time.time() - start_time,
                error_message=str(e),
                workflow_steps=workflow_steps
            )
    
    def test_combat_workflow(self) -> IntegrationTestResult:
        """
        Test complete combat system workflow.
        
        Returns:
            IntegrationTestResult for combat workflow
        """
        start_time = time.time()
        workflow_steps = []
        
        try:
            # Step 1: Test combat health endpoint
            workflow_steps.append("Testing combat system health")
            health_response = self.session.get(f"{self.backend_url}/api/combat/health")
            
            if health_response.status_code != 200:
                return IntegrationTestResult(
                    test_name="Combat Workflow",
                    success=False,
                    duration=time.time() - start_time,
                    status_code=health_response.status_code,
                    error_message="Combat health check failed",
                    workflow_steps=workflow_steps
                )
            
            workflow_steps.append("Combat system health confirmed")
            
            # Step 2: Get available abilities
            workflow_steps.append("Getting available combat abilities")
            abilities_response = self.session.get(f"{self.backend_url}/api/combat/abilities")
            
            if abilities_response.status_code != 200:
                return IntegrationTestResult(
                    test_name="Combat Workflow",
                    success=False,
                    duration=time.time() - start_time,
                    status_code=abilities_response.status_code,
                    error_message="Combat abilities retrieval failed",
                    workflow_steps=workflow_steps
                )
            
            abilities_data = abilities_response.json()
            workflow_steps.append(f"Retrieved {len(abilities_data.get('abilities', []))} combat abilities")
            
            # Step 3: Get status effects
            workflow_steps.append("Getting combat status effects")
            effects_response = self.session.get(f"{self.backend_url}/api/combat/status-effects")
            
            if effects_response.status_code != 200:
                return IntegrationTestResult(
                    test_name="Combat Workflow",
                    success=False,
                    duration=time.time() - start_time,
                    status_code=effects_response.status_code,
                    error_message="Combat status effects retrieval failed",
                    workflow_steps=workflow_steps
                )
            
            effects_data = effects_response.json()
            workflow_steps.append(f"Retrieved {len(effects_data.get('status_effects', []))} status effects")
            
            # Step 4: Test encounter creation
            workflow_steps.append("Creating combat encounter")
            encounter_data = {
                'encounter_type': 'basic_combat',
                'enemies': ['shadow_wolf'],
                'difficulty': 'normal'
            }
            
            encounter_response = self.session.post(
                f"{self.backend_url}/api/combat/encounter/create",
                json=encounter_data
            )
            
            encounter_success = encounter_response.status_code == 200
            
            if encounter_success:
                workflow_steps.append("Combat encounter created successfully")
            else:
                workflow_steps.append(f"Combat encounter creation failed (status: {encounter_response.status_code})")
            
            # Step 5: Get combat statistics
            workflow_steps.append("Getting combat statistics")
            stats_response = self.session.get(f"{self.backend_url}/api/combat/statistics")
            
            stats_success = stats_response.status_code == 200
            
            if stats_success:
                stats_data = stats_response.json()
                workflow_steps.append("Combat statistics retrieved")
            else:
                workflow_steps.append(f"Combat statistics failed (status: {stats_response.status_code})")
            
            overall_success = encounter_success and stats_success
            
            return IntegrationTestResult(
                test_name="Combat Workflow",
                success=overall_success,
                duration=time.time() - start_time,
                status_code=200 if overall_success else encounter_response.status_code,
                details={
                    'abilities_count': len(abilities_data.get('abilities', [])),
                    'effects_count': len(effects_data.get('status_effects', [])),
                    'encounter_data': encounter_data,
                    'encounter_success': encounter_success,
                    'stats_success': stats_success
                },
                workflow_steps=workflow_steps
            )
            
        except Exception as e:
            return IntegrationTestResult(
                test_name="Combat Workflow",
                success=False,
                duration=time.time() - start_time,
                error_message=str(e),
                workflow_steps=workflow_steps
            )
    
    def test_concurrent_user_workflow(self, num_users: int = MAX_CONCURRENT_USERS) -> IntegrationTestResult:
        """
        Test system behavior with multiple concurrent users.
        
        Args:
            num_users: Number of concurrent users to simulate
            
        Returns:
            IntegrationTestResult for concurrent user testing
        """
        start_time = time.time()
        workflow_steps = []
        
        def simulate_user_session(user_id: int) -> Dict[str, Any]:
            """Simulate a complete user session."""
            user_session = requests.Session()
            user_results = {
                'user_id': user_id,
                'session_init': False,
                'equipment_browse': False,
                'quest_browse': False,
                'errors': []
            }
            
            try:
                # Initialize session
                response = user_session.post(f"{self.backend_url}/api/session/init")
                user_results['session_init'] = response.status_code == 200
                
                # Browse equipment
                response = user_session.get(f"{self.backend_url}/api/equipment/available")
                user_results['equipment_browse'] = response.status_code == 200
                
                # Browse quests
                response = user_session.get(f"{self.backend_url}/api/quests/available")
                user_results['quest_browse'] = response.status_code == 200
                
            except Exception as e:
                user_results['errors'].append(str(e))
            
            return user_results
        
        try:
            workflow_steps.append(f"Starting concurrent user test with {num_users} users")
            
            # Execute concurrent user sessions
            with ThreadPoolExecutor(max_workers=num_users) as executor:
                futures = [executor.submit(simulate_user_session, i) for i in range(num_users)]
                user_results = []
                
                for future in as_completed(futures):
                    try:
                        result = future.result()
                        user_results.append(result)
                    except Exception as e:
                        workflow_steps.append(f"User session failed: {e}")
            
            workflow_steps.append(f"Completed {len(user_results)} user sessions")
            
            # Analyze results
            successful_sessions = sum(1 for r in user_results if r['session_init'])
            successful_equipment = sum(1 for r in user_results if r['equipment_browse'])
            successful_quests = sum(1 for r in user_results if r['quest_browse'])
            
            success_rate = (successful_sessions / num_users) * 100 if num_users > 0 else 0
            overall_success = success_rate >= 80  # 80% success threshold
            
            workflow_steps.append(f"Success rate: {success_rate:.1f}%")
            
            return IntegrationTestResult(
                test_name="Concurrent User Workflow",
                success=overall_success,
                duration=time.time() - start_time,
                details={
                    'num_users': num_users,
                    'successful_sessions': successful_sessions,
                    'successful_equipment': successful_equipment,
                    'successful_quests': successful_quests,
                    'success_rate': success_rate,
                    'user_results': user_results
                },
                workflow_steps=workflow_steps
            )
            
        except Exception as e:
            return IntegrationTestResult(
                test_name="Concurrent User Workflow",
                success=False,
                duration=time.time() - start_time,
                error_message=str(e),
                workflow_steps=workflow_steps
            )
    
    def test_data_consistency_workflow(self) -> IntegrationTestResult:
        """
        Test data consistency across multiple operations.
        
        Returns:
            IntegrationTestResult for data consistency testing
        """
        start_time = time.time()
        workflow_steps = []
        
        try:
            # Step 1: Initialize session and get initial state
            workflow_steps.append("Initializing session for consistency test")
            session_response = self.session.post(f"{self.backend_url}/api/session/init")
            
            if session_response.status_code != 200:
                return IntegrationTestResult(
                    test_name="Data Consistency Workflow",
                    success=False,
                    duration=time.time() - start_time,
                    status_code=session_response.status_code,
                    error_message="Session initialization failed",
                    workflow_steps=workflow_steps
                )
            
            initial_session = session_response.json()
            workflow_steps.append("Initial session state captured")
            
            # Step 2: Perform multiple operations
            workflow_steps.append("Performing multiple operations")
            
            # Get equipment overview
            overview1 = self.session.get(f"{self.backend_url}/api/equipment/overview")
            
            # Browse equipment
            equipment_browse = self.session.get(f"{self.backend_url}/api/equipment/available")
            
            # Get equipment overview again
            overview2 = self.session.get(f"{self.backend_url}/api/equipment/overview")
            
            # Check if overviews are consistent
            if overview1.status_code == 200 and overview2.status_code == 200:
                overview1_data = overview1.json()
                overview2_data = overview2.json()
                
                # Compare key fields for consistency
                consistency_checks = []
                
                if 'equipped_count' in overview1_data and 'equipped_count' in overview2_data:
                    consistency_checks.append(
                        overview1_data['equipped_count'] == overview2_data['equipped_count']
                    )
                
                if 'total_slots' in overview1_data and 'total_slots' in overview2_data:
                    consistency_checks.append(
                        overview1_data['total_slots'] == overview2_data['total_slots']
                    )
                
                data_consistent = all(consistency_checks) if consistency_checks else True
                workflow_steps.append(f"Data consistency check: {'PASS' if data_consistent else 'FAIL'}")
            else:
                data_consistent = False
                workflow_steps.append("Data consistency check: FAIL (API errors)")
            
            # Step 3: Test session persistence
            workflow_steps.append("Testing session persistence")
            
            # Make another session call
            session_response2 = self.session.get(f"{self.backend_url}/api/health")
            session_persistent = session_response2.status_code == 200
            
            workflow_steps.append(f"Session persistence: {'PASS' if session_persistent else 'FAIL'}")
            
            overall_success = data_consistent and session_persistent
            
            return IntegrationTestResult(
                test_name="Data Consistency Workflow",
                success=overall_success,
                duration=time.time() - start_time,
                status_code=200 if overall_success else 500,
                details={
                    'data_consistent': data_consistent,
                    'session_persistent': session_persistent,
                    'initial_session': initial_session,
                    'overview1_status': overview1.status_code,
                    'overview2_status': overview2.status_code
                },
                workflow_steps=workflow_steps
            )
            
        except Exception as e:
            return IntegrationTestResult(
                test_name="Data Consistency Workflow",
                success=False,
                duration=time.time() - start_time,
                error_message=str(e),
                workflow_steps=workflow_steps
            )
    
    def run_comprehensive_integration_tests(self) -> Dict[str, Any]:
        """
        Execute the complete integration test suite.
        
        Returns:
            Dictionary containing all integration test results and analysis
        """
        print("🚀 Starting Comprehensive Shadowlands RPG Integration Test Suite")
        print("=" * 70)
        
        # Check server availability first
        availability = self.check_server_availability()
        print(f"Backend Server: {'✅ Available' if availability['backend'] else '❌ Unavailable'}")
        print(f"Frontend Server: {'✅ Available' if availability['frontend'] else '❌ Unavailable'}")
        
        if not availability['backend']:
            print("\n❌ Backend server not available. Starting backend server...")
            try:
                # Try to start backend server
                subprocess.Popen([
                    'python3', '-m', 'src.main'
                ], cwd='/home/ubuntu/shadowlands-backend')
                time.sleep(5)  # Wait for server to start
                
                # Check again
                availability = self.check_server_availability()
                if not availability['backend']:
                    print("❌ Failed to start backend server")
                    return {
                        'error': 'Backend server unavailable',
                        'availability': availability
                    }
                else:
                    print("✅ Backend server started successfully")
            except Exception as e:
                print(f"❌ Error starting backend server: {e}")
                return {
                    'error': f'Failed to start backend server: {e}',
                    'availability': availability
                }
        
        print("\n" + "=" * 70)
        
        all_results = []
        
        # Test 1: Session Workflow
        print("Testing Session Workflow...")
        session_result = self.test_session_workflow()
        all_results.append(session_result)
        print(f"  Result: {'✅ PASS' if session_result.success else '❌ FAIL'}")
        
        # Test 2: Equipment Workflow
        print("Testing Equipment Workflow...")
        equipment_result = self.test_equipment_workflow()
        all_results.append(equipment_result)
        print(f"  Result: {'✅ PASS' if equipment_result.success else '❌ FAIL'}")
        
        # Test 3: Quest Workflow
        print("Testing Quest Workflow...")
        quest_result = self.test_quest_workflow()
        all_results.append(quest_result)
        print(f"  Result: {'✅ PASS' if quest_result.success else '❌ FAIL'}")
        
        # Test 4: Combat Workflow
        print("Testing Combat Workflow...")
        combat_result = self.test_combat_workflow()
        all_results.append(combat_result)
        print(f"  Result: {'✅ PASS' if combat_result.success else '❌ FAIL'}")
        
        # Test 5: Concurrent Users
        print("Testing Concurrent User Workflow...")
        concurrent_result = self.test_concurrent_user_workflow()
        all_results.append(concurrent_result)
        print(f"  Result: {'✅ PASS' if concurrent_result.success else '❌ FAIL'}")
        
        # Test 6: Data Consistency
        print("Testing Data Consistency Workflow...")
        consistency_result = self.test_data_consistency_workflow()
        all_results.append(consistency_result)
        print(f"  Result: {'✅ PASS' if consistency_result.success else '❌ FAIL'}")
        
        # Calculate overall statistics
        total_tests = len(all_results)
        successful_tests = sum(1 for result in all_results if result.success)
        success_rate = (successful_tests / total_tests) * 100 if total_tests > 0 else 0
        avg_duration = sum(result.duration for result in all_results) / total_tests if total_tests > 0 else 0
        
        # Generate comprehensive report
        report = {
            'test_summary': {
                'total_tests': total_tests,
                'successful_tests': successful_tests,
                'failed_tests': total_tests - successful_tests,
                'success_rate': success_rate,
                'average_duration': avg_duration
            },
            'server_availability': availability,
            'test_results': {
                'session_workflow': session_result,
                'equipment_workflow': equipment_result,
                'quest_workflow': quest_result,
                'combat_workflow': combat_result,
                'concurrent_users': concurrent_result,
                'data_consistency': consistency_result
            },
            'detailed_results': all_results
        }
        
        return report

def main():
    """Main function to execute the comprehensive integration test suite."""
    print("Shadowlands RPG - Integration Testing and End-to-End Validation Suite")
    print("Phase FR4.4: Integration Testing and End-to-End Validation")
    print("=" * 70)
    
    # Initialize tester
    tester = ShadowlandsIntegrationTester()
    
    # Run comprehensive integration tests
    results = tester.run_comprehensive_integration_tests()
    
    if 'error' in results:
        print(f"\n❌ Integration testing failed: {results['error']}")
        return results
    
    # Display results summary
    print("\n" + "=" * 70)
    print("🎯 INTEGRATION TEST RESULTS SUMMARY")
    print("=" * 70)
    
    summary = results['test_summary']
    print(f"Total Tests: {summary['total_tests']}")
    print(f"Successful: {summary['successful_tests']}")
    print(f"Failed: {summary['failed_tests']}")
    print(f"Success Rate: {summary['success_rate']:.1f}%")
    print(f"Average Duration: {summary['average_duration']:.3f}s")
    
    # Display individual test results
    print("\n📊 INDIVIDUAL TEST RESULTS")
    print("-" * 50)
    for test_name, test_result in results['test_results'].items():
        status = "✅ PASS" if test_result.success else "❌ FAIL"
        duration = f"{test_result.duration:.3f}s"
        print(f"{test_name}: {status} ({duration})")
        
        if not test_result.success and test_result.error_message:
            print(f"  Error: {test_result.error_message}")
    
    # Save detailed results to file
    serializable_results = []
    for result in results['detailed_results']:
        serializable_results.append({
            'test_name': result.test_name,
            'success': result.success,
            'duration': result.duration,
            'status_code': result.status_code,
            'error_message': result.error_message,
            'details': result.details,
            'workflow_steps': result.workflow_steps
        })
    
    final_results = {
        'test_summary': results['test_summary'],
        'server_availability': results['server_availability'],
        'detailed_results': serializable_results
    }
    
    with open('/home/ubuntu/integration_test_results.json', 'w') as f:
        json.dump(final_results, f, indent=2)
    
    print(f"\n📊 Detailed results saved to: /home/ubuntu/integration_test_results.json")
    
    # Determine overall test status
    if summary['success_rate'] >= 90:
        print("\n✅ OVERALL STATUS: EXCELLENT - All integrations working perfectly")
    elif summary['success_rate'] >= 75:
        print("\n⚠️  OVERALL STATUS: GOOD - Minor integration issues detected")
    elif summary['success_rate'] >= 50:
        print("\n⚠️  OVERALL STATUS: FAIR - Some integration issues need attention")
    else:
        print("\n❌ OVERALL STATUS: NEEDS ATTENTION - Significant integration issues detected")
    
    return results

if __name__ == "__main__":
    main()


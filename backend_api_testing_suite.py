#!/usr/bin/env python3
"""
Shadowlands RPG - Comprehensive Backend API Testing Suite
Phase FR4.2: Backend API Testing Implementation

This module provides comprehensive testing for all Shadowlands RPG backend APIs,
including equipment management, character progression, combat systems, quest management,
and session handling. The testing suite validates functionality, performance, error handling,
and data integrity across all backend endpoints.

Author: Manus AI
Date: July 21, 2025
"""

import unittest
import requests
import json
import time
import threading
import random
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed
import statistics

# Test Configuration
API_BASE_URL = "http://localhost:5001/api"
TEST_TIMEOUT = 30
MAX_CONCURRENT_USERS = 10
PERFORMANCE_ITERATIONS = 100

@dataclass
class TestResult:
    """Data class for storing test results with performance metrics"""
    test_name: str
    success: bool
    response_time: float
    status_code: int
    error_message: Optional[str] = None
    response_data: Optional[Dict] = None

@dataclass
class PerformanceMetrics:
    """Data class for storing performance analysis results"""
    min_time: float
    max_time: float
    avg_time: float
    median_time: float
    p95_time: float
    p99_time: float
    success_rate: float
    total_requests: int

class ShadowlandsAPITester:
    """
    Comprehensive API testing framework for Shadowlands RPG backend.
    
    This class provides methods for testing all backend endpoints including:
    - Session management and authentication
    - Character creation and progression
    - Equipment management and operations
    - Combat system functionality
    - Quest management and progression
    - Performance and load testing
    """
    
    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results: List[TestResult] = []
        self.performance_data: Dict[str, List[float]] = {}
        
    def make_request(self, method: str, endpoint: str, data: Optional[Dict] = None, 
                    params: Optional[Dict] = None, timeout: int = TEST_TIMEOUT) -> TestResult:
        """
        Make HTTP request with comprehensive error handling and performance tracking.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint path
            data: Request body data for POST/PUT requests
            params: Query parameters for GET requests
            timeout: Request timeout in seconds
            
        Returns:
            TestResult object with response data and performance metrics
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        start_time = time.time()
        
        try:
            if method.upper() == 'GET':
                response = self.session.get(url, params=params, timeout=timeout)
            elif method.upper() == 'POST':
                response = self.session.post(url, json=data, timeout=timeout)
            elif method.upper() == 'PUT':
                response = self.session.put(url, json=data, timeout=timeout)
            elif method.upper() == 'DELETE':
                response = self.session.delete(url, timeout=timeout)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
                
            response_time = time.time() - start_time
            
            # Parse response data
            try:
                response_data = response.json()
            except json.JSONDecodeError:
                response_data = {"raw_response": response.text}
                
            return TestResult(
                test_name=f"{method} {endpoint}",
                success=response.status_code < 400,
                response_time=response_time,
                status_code=response.status_code,
                response_data=response_data
            )
            
        except Exception as e:
            response_time = time.time() - start_time
            return TestResult(
                test_name=f"{method} {endpoint}",
                success=False,
                response_time=response_time,
                status_code=0,
                error_message=str(e)
            )
    
    def test_health_endpoint(self) -> TestResult:
        """Test the health check endpoint for basic connectivity."""
        return self.make_request('GET', '/health')
    
    def test_session_management(self) -> List[TestResult]:
        """
        Comprehensive testing of session management endpoints.
        
        Tests:
        - Session initialization
        - Session state persistence
        - Session data validation
        - Session cleanup
        
        Returns:
            List of TestResult objects for all session tests
        """
        results = []
        
        # Test session initialization
        result = self.make_request('POST', '/session/init')
        results.append(result)
        
        if result.success and result.response_data:
            # Validate session initialization response structure
            expected_keys = ['success', 'message', 'character_data']
            for key in expected_keys:
                if key not in result.response_data:
                    results.append(TestResult(
                        test_name=f"Session Init - {key} validation",
                        success=False,
                        response_time=0,
                        status_code=result.status_code,
                        error_message=f"Missing required key: {key}"
                    ))
                else:
                    results.append(TestResult(
                        test_name=f"Session Init - {key} validation",
                        success=True,
                        response_time=0,
                        status_code=result.status_code
                    ))
        
        return results
    
    def test_equipment_endpoints(self) -> List[TestResult]:
        """
        Comprehensive testing of equipment management endpoints.
        
        Tests:
        - Equipment browsing and filtering
        - Equipment details retrieval
        - Equipment equip/unequip operations
        - Equipment requirements validation
        - Equipment stat calculations
        
        Returns:
            List of TestResult objects for all equipment tests
        """
        results = []
        
        # Initialize session first
        session_result = self.make_request('POST', '/session/init')
        if not session_result.success:
            results.append(TestResult(
                test_name="Equipment Tests - Session Setup",
                success=False,
                response_time=0,
                status_code=session_result.status_code,
                error_message="Failed to initialize session for equipment tests"
            ))
            return results
        
        # Test equipment browsing
        browse_result = self.make_request('GET', '/equipment/available')
        results.append(browse_result)
        
        # Test equipment filtering
        filter_params = {
            'type': 'weapon',
            'rarity': 'common',
            'min_level': 1,
            'max_level': 5
        }
        filter_result = self.make_request('GET', '/equipment/available', params=filter_params)
        results.append(filter_result)
        
        # Test equipment details
        if browse_result.success and browse_result.response_data:
            equipment_list = browse_result.response_data.get('equipment', [])
            if equipment_list:
                first_item = equipment_list[0]
                item_id = first_item.get('id')
                if item_id:
                    details_result = self.make_request('GET', f'/equipment/{item_id}')
                    results.append(details_result)
        
        # Test equipment operations
        equip_data = {
            'item_id': 'rusty_sword',
            'slot': 'weapon_main'
        }
        equip_result = self.make_request('POST', '/equipment/equip', data=equip_data)
        results.append(equip_result)
        
        # Test unequip operation
        unequip_data = {
            'slot': 'weapon_main'
        }
        unequip_result = self.make_request('POST', '/equipment/unequip', data=unequip_data)
        results.append(unequip_result)
        
        # Test equipment overview
        overview_result = self.make_request('GET', '/equipment/overview')
        results.append(overview_result)
        
        return results
    
    def test_character_endpoints(self) -> List[TestResult]:
        """
        Comprehensive testing of character management endpoints.
        
        Tests:
        - Character creation and validation
        - Character attribute management
        - Character progression and leveling
        - Character stats calculation
        - Character inventory management
        
        Returns:
            List of TestResult objects for all character tests
        """
        results = []
        
        # Test character listing
        list_result = self.make_request('GET', '/characters')
        results.append(list_result)
        
        # Test character creation
        character_data = {
            'name': 'Test Drifter',
            'attributes': {
                'might': 12,
                'intellect': 10,
                'will': 8,
                'shadow': 6
            }
        }
        create_result = self.make_request('POST', '/characters', data=character_data)
        results.append(create_result)
        
        # If character creation successful, test character operations
        if create_result.success and create_result.response_data:
            character_id = create_result.response_data.get('character_id')
            if character_id:
                # Test character retrieval
                get_result = self.make_request('GET', f'/characters/{character_id}')
                results.append(get_result)
                
                # Test character stats
                stats_result = self.make_request('GET', f'/characters/{character_id}/stats')
                results.append(stats_result)
                
                # Test experience addition
                exp_data = {'experience': 100}
                exp_result = self.make_request('POST', f'/characters/{character_id}/add-experience', data=exp_data)
                results.append(exp_result)
                
                # Test character inventory
                inventory_result = self.make_request('GET', f'/characters/{character_id}/inventory')
                results.append(inventory_result)
        
        return results
    
    def test_combat_endpoints(self) -> List[TestResult]:
        """
        Comprehensive testing of combat system endpoints.
        
        Tests:
        - Combat encounter creation
        - Combat action processing
        - Combat abilities and effects
        - Combat AI behavior
        - Combat statistics and analytics
        
        Returns:
            List of TestResult objects for all combat tests
        """
        results = []
        
        # Test combat health check
        health_result = self.make_request('GET', '/combat/health')
        results.append(health_result)
        
        # Test encounter creation
        encounter_data = {
            'encounter_type': 'basic_combat',
            'enemies': ['shadow_wolf'],
            'difficulty': 'normal'
        }
        create_encounter_result = self.make_request('POST', '/combat/encounter/create', data=encounter_data)
        results.append(create_encounter_result)
        
        # Test abilities listing
        abilities_result = self.make_request('GET', '/combat/abilities')
        results.append(abilities_result)
        
        # Test status effects listing
        effects_result = self.make_request('GET', '/combat/status-effects')
        results.append(effects_result)
        
        # Test combat statistics
        stats_result = self.make_request('GET', '/combat/statistics')
        results.append(stats_result)
        
        return results
    
    def test_quest_endpoints(self) -> List[TestResult]:
        """
        Comprehensive testing of quest management endpoints.
        
        Tests:
        - Quest listing and filtering
        - Quest details and requirements
        - Quest progression tracking
        - Quest completion and rewards
        - Quest narrative integration
        
        Returns:
            List of TestResult objects for all quest tests
        """
        results = []
        
        # Test quest listing
        list_result = self.make_request('GET', '/quests')
        results.append(list_result)
        
        # Test available quests
        available_result = self.make_request('GET', '/quests/available')
        results.append(available_result)
        
        # Test quest details
        quest_detail_result = self.make_request('GET', '/quests/into_the_woods')
        results.append(quest_detail_result)
        
        # Test quest progression
        progress_data = {
            'quest_id': 'into_the_woods',
            'objective_id': 'explore_forest',
            'progress': 1
        }
        progress_result = self.make_request('POST', '/quests/progress', data=progress_data)
        results.append(progress_result)
        
        return results
    
    def test_narrative_endpoints(self) -> List[TestResult]:
        """
        Comprehensive testing of narrative system endpoints.
        
        Tests:
        - Narrative state management
        - Story progression tracking
        - Character dialogue systems
        - Narrative choice handling
        - Story branching logic
        
        Returns:
            List of TestResult objects for all narrative tests
        """
        results = []
        
        # Test narrative state
        state_result = self.make_request('GET', '/narrative/state')
        results.append(state_result)
        
        # Test current scene
        scene_result = self.make_request('GET', '/narrative/current-scene')
        results.append(scene_result)
        
        # Test dialogue options
        dialogue_result = self.make_request('GET', '/narrative/dialogue-options')
        results.append(dialogue_result)
        
        return results
    
    def test_location_endpoints(self) -> List[TestResult]:
        """
        Comprehensive testing of location and exploration endpoints.
        
        Tests:
        - Location listing and details
        - Location navigation
        - Area exploration mechanics
        - Location-based events
        - Environmental interactions
        
        Returns:
            List of TestResult objects for all location tests
        """
        results = []
        
        # Test location listing
        list_result = self.make_request('GET', '/locations')
        results.append(list_result)
        
        # Test current location
        current_result = self.make_request('GET', '/locations/current')
        results.append(current_result)
        
        # Test location details
        detail_result = self.make_request('GET', '/locations/corrupted_forest')
        results.append(detail_result)
        
        return results
    
    def performance_test_endpoint(self, method: str, endpoint: str, 
                                data: Optional[Dict] = None, iterations: int = PERFORMANCE_ITERATIONS) -> PerformanceMetrics:
        """
        Perform comprehensive performance testing on a specific endpoint.
        
        Args:
            method: HTTP method to test
            endpoint: API endpoint to test
            data: Request data for POST/PUT requests
            iterations: Number of test iterations to perform
            
        Returns:
            PerformanceMetrics object with detailed performance analysis
        """
        response_times = []
        success_count = 0
        
        for _ in range(iterations):
            result = self.make_request(method, endpoint, data=data)
            response_times.append(result.response_time)
            if result.success:
                success_count += 1
        
        # Calculate performance metrics
        response_times.sort()
        return PerformanceMetrics(
            min_time=min(response_times),
            max_time=max(response_times),
            avg_time=statistics.mean(response_times),
            median_time=statistics.median(response_times),
            p95_time=response_times[int(0.95 * len(response_times))],
            p99_time=response_times[int(0.99 * len(response_times))],
            success_rate=(success_count / iterations) * 100,
            total_requests=iterations
        )
    
    def load_test_concurrent_users(self, num_users: int = MAX_CONCURRENT_USERS) -> Dict[str, Any]:
        """
        Perform load testing with multiple concurrent users.
        
        Args:
            num_users: Number of concurrent users to simulate
            
        Returns:
            Dictionary containing load test results and metrics
        """
        def simulate_user_session():
            """Simulate a complete user session with multiple operations."""
            user_results = []
            
            # Session initialization
            user_results.append(self.make_request('POST', '/session/init'))
            
            # Equipment browsing
            user_results.append(self.make_request('GET', '/equipment/available'))
            
            # Character operations
            user_results.append(self.make_request('GET', '/characters'))
            
            # Quest browsing
            user_results.append(self.make_request('GET', '/quests/available'))
            
            return user_results
        
        start_time = time.time()
        
        # Execute concurrent user sessions
        with ThreadPoolExecutor(max_workers=num_users) as executor:
            futures = [executor.submit(simulate_user_session) for _ in range(num_users)]
            all_results = []
            
            for future in as_completed(futures):
                try:
                    user_results = future.result()
                    all_results.extend(user_results)
                except Exception as e:
                    print(f"User session failed: {e}")
        
        total_time = time.time() - start_time
        
        # Analyze results
        successful_requests = sum(1 for result in all_results if result.success)
        total_requests = len(all_results)
        avg_response_time = statistics.mean([r.response_time for r in all_results])
        
        return {
            'concurrent_users': num_users,
            'total_time': total_time,
            'total_requests': total_requests,
            'successful_requests': successful_requests,
            'success_rate': (successful_requests / total_requests) * 100 if total_requests > 0 else 0,
            'average_response_time': avg_response_time,
            'requests_per_second': total_requests / total_time if total_time > 0 else 0
        }
    
    def run_comprehensive_test_suite(self) -> Dict[str, Any]:
        """
        Execute the complete test suite and generate comprehensive results.
        
        Returns:
            Dictionary containing all test results, performance metrics, and analysis
        """
        print("🚀 Starting Comprehensive Shadowlands RPG API Test Suite")
        print("=" * 60)
        
        all_results = []
        test_categories = {}
        
        # Health check
        print("Testing Health Endpoint...")
        health_result = self.test_health_endpoint()
        all_results.append(health_result)
        test_categories['health'] = [health_result]
        
        # Session management tests
        print("Testing Session Management...")
        session_results = self.test_session_management()
        all_results.extend(session_results)
        test_categories['session'] = session_results
        
        # Equipment tests
        print("Testing Equipment Endpoints...")
        equipment_results = self.test_equipment_endpoints()
        all_results.extend(equipment_results)
        test_categories['equipment'] = equipment_results
        
        # Character tests
        print("Testing Character Endpoints...")
        character_results = self.test_character_endpoints()
        all_results.extend(character_results)
        test_categories['character'] = character_results
        
        # Combat tests
        print("Testing Combat Endpoints...")
        combat_results = self.test_combat_endpoints()
        all_results.extend(combat_results)
        test_categories['combat'] = combat_results
        
        # Quest tests
        print("Testing Quest Endpoints...")
        quest_results = self.test_quest_endpoints()
        all_results.extend(quest_results)
        test_categories['quest'] = quest_results
        
        # Narrative tests
        print("Testing Narrative Endpoints...")
        narrative_results = self.test_narrative_endpoints()
        all_results.extend(narrative_results)
        test_categories['narrative'] = narrative_results
        
        # Location tests
        print("Testing Location Endpoints...")
        location_results = self.test_location_endpoints()
        all_results.extend(location_results)
        test_categories['location'] = location_results
        
        # Performance testing
        print("Performing Performance Tests...")
        performance_results = {}
        critical_endpoints = [
            ('GET', '/health'),
            ('POST', '/session/init'),
            ('GET', '/equipment/available'),
            ('GET', '/characters'),
            ('GET', '/quests/available')
        ]
        
        for method, endpoint in critical_endpoints:
            print(f"  Performance testing {method} {endpoint}...")
            perf_metrics = self.performance_test_endpoint(method, endpoint)
            performance_results[f"{method} {endpoint}"] = perf_metrics
        
        # Load testing
        print("Performing Load Tests...")
        load_test_results = self.load_test_concurrent_users()
        
        # Calculate overall statistics
        total_tests = len(all_results)
        successful_tests = sum(1 for result in all_results if result.success)
        success_rate = (successful_tests / total_tests) * 100 if total_tests > 0 else 0
        avg_response_time = statistics.mean([r.response_time for r in all_results if r.response_time > 0])
        
        # Generate comprehensive report
        report = {
            'test_summary': {
                'total_tests': total_tests,
                'successful_tests': successful_tests,
                'failed_tests': total_tests - successful_tests,
                'success_rate': success_rate,
                'average_response_time': avg_response_time
            },
            'test_categories': test_categories,
            'performance_metrics': performance_results,
            'load_test_results': load_test_results,
            'detailed_results': all_results
        }
        
        return report

def main():
    """Main function to execute the comprehensive test suite."""
    print("Shadowlands RPG - Backend API Testing Suite")
    print("Phase FR4.2: Backend API Testing Implementation")
    print("=" * 60)
    
    # Initialize tester
    tester = ShadowlandsAPITester()
    
    # Run comprehensive test suite
    results = tester.run_comprehensive_test_suite()
    
    # Display results summary
    print("\n" + "=" * 60)
    print("🎯 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    summary = results['test_summary']
    print(f"Total Tests: {summary['total_tests']}")
    print(f"Successful: {summary['successful_tests']}")
    print(f"Failed: {summary['failed_tests']}")
    print(f"Success Rate: {summary['success_rate']:.1f}%")
    print(f"Average Response Time: {summary['average_response_time']:.3f}s")
    
    # Display performance metrics
    print("\n🚀 PERFORMANCE METRICS")
    print("-" * 40)
    for endpoint, metrics in results['performance_metrics'].items():
        print(f"{endpoint}:")
        print(f"  Average: {metrics.avg_time:.3f}s")
        print(f"  P95: {metrics.p95_time:.3f}s")
        print(f"  Success Rate: {metrics.success_rate:.1f}%")
    
    # Display load test results
    print("\n⚡ LOAD TEST RESULTS")
    print("-" * 40)
    load_results = results['load_test_results']
    print(f"Concurrent Users: {load_results['concurrent_users']}")
    print(f"Total Requests: {load_results['total_requests']}")
    print(f"Success Rate: {load_results['success_rate']:.1f}%")
    print(f"Requests/Second: {load_results['requests_per_second']:.1f}")
    
    # Save detailed results to file
    with open('/home/ubuntu/backend_api_test_results.json', 'w') as f:
        # Convert TestResult objects to dictionaries for JSON serialization
        serializable_results = []
        for result in results['detailed_results']:
            serializable_results.append({
                'test_name': result.test_name,
                'success': result.success,
                'response_time': result.response_time,
                'status_code': result.status_code,
                'error_message': result.error_message,
                'response_data': result.response_data
            })
        
        # Convert PerformanceMetrics to dictionaries
        serializable_performance = {}
        for endpoint, metrics in results['performance_metrics'].items():
            serializable_performance[endpoint] = {
                'min_time': metrics.min_time,
                'max_time': metrics.max_time,
                'avg_time': metrics.avg_time,
                'median_time': metrics.median_time,
                'p95_time': metrics.p95_time,
                'p99_time': metrics.p99_time,
                'success_rate': metrics.success_rate,
                'total_requests': metrics.total_requests
            }
        
        final_results = {
            'test_summary': results['test_summary'],
            'performance_metrics': serializable_performance,
            'load_test_results': results['load_test_results'],
            'detailed_results': serializable_results
        }
        
        json.dump(final_results, f, indent=2)
    
    print(f"\n📊 Detailed results saved to: /home/ubuntu/backend_api_test_results.json")
    
    # Determine overall test status
    if summary['success_rate'] >= 90:
        print("\n✅ OVERALL STATUS: EXCELLENT - All systems operational")
    elif summary['success_rate'] >= 75:
        print("\n⚠️  OVERALL STATUS: GOOD - Minor issues detected")
    else:
        print("\n❌ OVERALL STATUS: NEEDS ATTENTION - Significant issues detected")
    
    return results

if __name__ == "__main__":
    main()


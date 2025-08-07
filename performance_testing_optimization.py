#!/usr/bin/env python3
"""
Shadowlands RPG - Performance Testing and Optimization Suite
Phase FR4.5: Performance Testing and Optimization

This module provides comprehensive performance testing and optimization analysis
for the Shadowlands RPG system, including load testing, response time analysis,
memory usage monitoring, and performance optimization recommendations.

Author: Manus AI
Date: July 21, 2025
"""

import time
import requests
import threading
import psutil
import json
import statistics
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed
import subprocess

# Performance Test Configuration
BACKEND_URL = "http://localhost:5001"
PERFORMANCE_ITERATIONS = 100
LOAD_TEST_USERS = [1, 5, 10, 20, 50]
STRESS_TEST_DURATION = 60  # seconds
MEMORY_SAMPLE_INTERVAL = 1  # seconds

@dataclass
class PerformanceMetric:
    """Data class for storing performance metrics"""
    test_name: str
    min_time: float
    max_time: float
    avg_time: float
    median_time: float
    p95_time: float
    p99_time: float
    success_rate: float
    throughput: float
    total_requests: int

@dataclass
class LoadTestResult:
    """Data class for storing load test results"""
    concurrent_users: int
    total_requests: int
    successful_requests: int
    failed_requests: int
    success_rate: float
    avg_response_time: float
    throughput: float
    errors: List[str]

class ShadowlandsPerformanceTester:
    """
    Comprehensive performance testing framework for Shadowlands RPG.
    
    This class provides performance testing including:
    - Response time benchmarking
    - Load testing with varying user counts
    - Stress testing under sustained load
    - Memory usage monitoring
    - Performance optimization analysis
    """
    
    def __init__(self):
        self.backend_url = BACKEND_URL
        self.session = requests.Session()
        self.performance_data: Dict[str, List[float]] = {}
        
    def measure_response_time(self, method: str, endpoint: str, 
                            data: Optional[Dict] = None, iterations: int = PERFORMANCE_ITERATIONS) -> PerformanceMetric:
        """
        Measure response time performance for a specific endpoint.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint to test
            data: Request data for POST requests
            iterations: Number of test iterations
            
        Returns:
            PerformanceMetric object with detailed performance analysis
        """
        response_times = []
        success_count = 0
        errors = []
        
        print(f"  Testing {method} {endpoint} ({iterations} iterations)...")
        
        for i in range(iterations):
            start_time = time.time()
            
            try:
                if method.upper() == 'GET':
                    response = self.session.get(f"{self.backend_url}{endpoint}", timeout=10)
                elif method.upper() == 'POST':
                    response = self.session.post(f"{self.backend_url}{endpoint}", json=data, timeout=10)
                else:
                    raise ValueError(f"Unsupported method: {method}")
                
                response_time = time.time() - start_time
                response_times.append(response_time)
                
                if response.status_code < 400:
                    success_count += 1
                else:
                    errors.append(f"HTTP {response.status_code}")
                    
            except Exception as e:
                response_time = time.time() - start_time
                response_times.append(response_time)
                errors.append(str(e))
        
        # Calculate statistics
        if response_times:
            response_times.sort()
            return PerformanceMetric(
                test_name=f"{method} {endpoint}",
                min_time=min(response_times),
                max_time=max(response_times),
                avg_time=statistics.mean(response_times),
                median_time=statistics.median(response_times),
                p95_time=response_times[int(0.95 * len(response_times))],
                p99_time=response_times[int(0.99 * len(response_times))],
                success_rate=(success_count / iterations) * 100,
                throughput=success_count / sum(response_times) if sum(response_times) > 0 else 0,
                total_requests=iterations
            )
        else:
            return PerformanceMetric(
                test_name=f"{method} {endpoint}",
                min_time=0, max_time=0, avg_time=0, median_time=0,
                p95_time=0, p99_time=0, success_rate=0, throughput=0,
                total_requests=iterations
            )
    
    def run_load_test(self, concurrent_users: int, requests_per_user: int = 10) -> LoadTestResult:
        """
        Run load test with specified number of concurrent users.
        
        Args:
            concurrent_users: Number of concurrent users to simulate
            requests_per_user: Number of requests each user should make
            
        Returns:
            LoadTestResult object with load test analysis
        """
        print(f"  Load testing with {concurrent_users} concurrent users...")
        
        def user_session(user_id: int) -> Dict[str, Any]:
            """Simulate a user session with multiple requests."""
            user_session = requests.Session()
            user_results = {
                'user_id': user_id,
                'requests': [],
                'errors': []
            }
            
            # Define user workflow
            endpoints = [
                ('POST', '/api/session/init', None),
                ('GET', '/api/equipment/available', None),
                ('GET', '/api/equipment/overview', None),
                ('GET', '/api/quests/available', None),
                ('GET', '/api/combat/health', None)
            ]
            
            for _ in range(requests_per_user):
                for method, endpoint, data in endpoints:
                    start_time = time.time()
                    
                    try:
                        if method == 'GET':
                            response = user_session.get(f"{self.backend_url}{endpoint}", timeout=10)
                        else:
                            response = user_session.post(f"{self.backend_url}{endpoint}", json=data, timeout=10)
                        
                        response_time = time.time() - start_time
                        
                        user_results['requests'].append({
                            'endpoint': endpoint,
                            'method': method,
                            'response_time': response_time,
                            'status_code': response.status_code,
                            'success': response.status_code < 400
                        })
                        
                    except Exception as e:
                        response_time = time.time() - start_time
                        user_results['errors'].append({
                            'endpoint': endpoint,
                            'method': method,
                            'error': str(e),
                            'response_time': response_time
                        })
            
            return user_results
        
        start_time = time.time()
        
        # Execute concurrent user sessions
        with ThreadPoolExecutor(max_workers=concurrent_users) as executor:
            futures = [executor.submit(user_session, i) for i in range(concurrent_users)]
            all_user_results = []
            
            for future in as_completed(futures):
                try:
                    result = future.result()
                    all_user_results.append(result)
                except Exception as e:
                    print(f"User session failed: {e}")
        
        total_time = time.time() - start_time
        
        # Analyze results
        total_requests = 0
        successful_requests = 0
        failed_requests = 0
        all_response_times = []
        all_errors = []
        
        for user_result in all_user_results:
            for request in user_result['requests']:
                total_requests += 1
                all_response_times.append(request['response_time'])
                if request['success']:
                    successful_requests += 1
                else:
                    failed_requests += 1
            
            for error in user_result['errors']:
                failed_requests += 1
                all_errors.append(error['error'])
        
        success_rate = (successful_requests / total_requests) * 100 if total_requests > 0 else 0
        avg_response_time = statistics.mean(all_response_times) if all_response_times else 0
        throughput = total_requests / total_time if total_time > 0 else 0
        
        return LoadTestResult(
            concurrent_users=concurrent_users,
            total_requests=total_requests,
            successful_requests=successful_requests,
            failed_requests=failed_requests,
            success_rate=success_rate,
            avg_response_time=avg_response_time,
            throughput=throughput,
            errors=list(set(all_errors))  # Unique errors
        )
    
    def monitor_system_resources(self, duration: int = 60) -> Dict[str, Any]:
        """
        Monitor system resource usage during testing.
        
        Args:
            duration: Duration to monitor in seconds
            
        Returns:
            Dictionary with resource usage statistics
        """
        print(f"  Monitoring system resources for {duration} seconds...")
        
        cpu_samples = []
        memory_samples = []
        disk_samples = []
        network_samples = []
        
        start_time = time.time()
        
        while time.time() - start_time < duration:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_samples.append(cpu_percent)
            
            # Memory usage
            memory = psutil.virtual_memory()
            memory_samples.append({
                'percent': memory.percent,
                'available_gb': memory.available / (1024**3),
                'used_gb': memory.used / (1024**3)
            })
            
            # Disk usage
            disk = psutil.disk_usage('/')
            disk_samples.append({
                'percent': (disk.used / disk.total) * 100,
                'free_gb': disk.free / (1024**3),
                'used_gb': disk.used / (1024**3)
            })
            
            # Network I/O
            network = psutil.net_io_counters()
            network_samples.append({
                'bytes_sent': network.bytes_sent,
                'bytes_recv': network.bytes_recv,
                'packets_sent': network.packets_sent,
                'packets_recv': network.packets_recv
            })
        
        # Calculate statistics
        return {
            'duration': duration,
            'cpu': {
                'avg_percent': statistics.mean(cpu_samples),
                'max_percent': max(cpu_samples),
                'min_percent': min(cpu_samples)
            },
            'memory': {
                'avg_percent': statistics.mean([s['percent'] for s in memory_samples]),
                'max_percent': max([s['percent'] for s in memory_samples]),
                'avg_available_gb': statistics.mean([s['available_gb'] for s in memory_samples])
            },
            'disk': {
                'avg_percent': statistics.mean([s['percent'] for s in disk_samples]),
                'avg_free_gb': statistics.mean([s['free_gb'] for s in disk_samples])
            },
            'network': {
                'total_bytes_sent': network_samples[-1]['bytes_sent'] - network_samples[0]['bytes_sent'],
                'total_bytes_recv': network_samples[-1]['bytes_recv'] - network_samples[0]['bytes_recv'],
                'avg_bytes_per_sec': (network_samples[-1]['bytes_sent'] + network_samples[-1]['bytes_recv'] - 
                                    network_samples[0]['bytes_sent'] - network_samples[0]['bytes_recv']) / duration
            }
        }
    
    def analyze_performance_bottlenecks(self, performance_metrics: List[PerformanceMetric]) -> Dict[str, Any]:
        """
        Analyze performance metrics to identify bottlenecks.
        
        Args:
            performance_metrics: List of performance metrics to analyze
            
        Returns:
            Dictionary with bottleneck analysis and recommendations
        """
        print("  Analyzing performance bottlenecks...")
        
        # Performance thresholds
        thresholds = {
            'excellent': 0.010,  # 10ms
            'good': 0.050,       # 50ms
            'acceptable': 0.100,  # 100ms
            'poor': 0.500        # 500ms
        }
        
        analysis = {
            'endpoint_performance': {},
            'bottlenecks': [],
            'recommendations': [],
            'overall_rating': 'excellent'
        }
        
        for metric in performance_metrics:
            # Categorize performance
            if metric.avg_time <= thresholds['excellent']:
                rating = 'excellent'
            elif metric.avg_time <= thresholds['good']:
                rating = 'good'
            elif metric.avg_time <= thresholds['acceptable']:
                rating = 'acceptable'
            else:
                rating = 'poor'
            
            analysis['endpoint_performance'][metric.test_name] = {
                'avg_time': metric.avg_time,
                'p95_time': metric.p95_time,
                'success_rate': metric.success_rate,
                'throughput': metric.throughput,
                'rating': rating
            }
            
            # Identify bottlenecks
            if rating == 'poor':
                analysis['bottlenecks'].append({
                    'endpoint': metric.test_name,
                    'issue': 'High response time',
                    'avg_time': metric.avg_time,
                    'recommendation': 'Optimize database queries and caching'
                })
            
            if metric.success_rate < 95:
                analysis['bottlenecks'].append({
                    'endpoint': metric.test_name,
                    'issue': 'Low success rate',
                    'success_rate': metric.success_rate,
                    'recommendation': 'Improve error handling and stability'
                })
        
        # Overall rating
        avg_times = [m.avg_time for m in performance_metrics]
        if avg_times:
            overall_avg = statistics.mean(avg_times)
            if overall_avg <= thresholds['excellent']:
                analysis['overall_rating'] = 'excellent'
            elif overall_avg <= thresholds['good']:
                analysis['overall_rating'] = 'good'
            elif overall_avg <= thresholds['acceptable']:
                analysis['overall_rating'] = 'acceptable'
            else:
                analysis['overall_rating'] = 'poor'
        
        # Generate recommendations
        if analysis['overall_rating'] in ['poor', 'acceptable']:
            analysis['recommendations'].extend([
                'Implement response caching for frequently accessed data',
                'Optimize database queries and add appropriate indexes',
                'Consider implementing connection pooling',
                'Add performance monitoring and alerting'
            ])
        
        if any(m.success_rate < 95 for m in performance_metrics):
            analysis['recommendations'].extend([
                'Improve error handling and retry mechanisms',
                'Add comprehensive logging for debugging',
                'Implement circuit breaker patterns for external dependencies'
            ])
        
        return analysis
    
    def generate_optimization_recommendations(self, load_test_results: List[LoadTestResult], 
                                           resource_usage: Dict[str, Any]) -> List[str]:
        """
        Generate optimization recommendations based on test results.
        
        Args:
            load_test_results: Results from load testing
            resource_usage: System resource usage data
            
        Returns:
            List of optimization recommendations
        """
        recommendations = []
        
        # Analyze load test results
        for result in load_test_results:
            if result.success_rate < 90:
                recommendations.append(
                    f"System struggles with {result.concurrent_users} concurrent users "
                    f"({result.success_rate:.1f}% success rate). Consider horizontal scaling."
                )
            
            if result.avg_response_time > 0.5:
                recommendations.append(
                    f"High response times ({result.avg_response_time:.3f}s) with "
                    f"{result.concurrent_users} users. Optimize backend processing."
                )
        
        # Analyze resource usage
        if resource_usage['cpu']['avg_percent'] > 80:
            recommendations.append(
                f"High CPU usage ({resource_usage['cpu']['avg_percent']:.1f}%). "
                "Consider CPU optimization or scaling."
            )
        
        if resource_usage['memory']['avg_percent'] > 80:
            recommendations.append(
                f"High memory usage ({resource_usage['memory']['avg_percent']:.1f}%). "
                "Check for memory leaks and optimize memory allocation."
            )
        
        # General recommendations
        recommendations.extend([
            "Implement Redis caching for frequently accessed data",
            "Add database connection pooling",
            "Implement API rate limiting to prevent abuse",
            "Add comprehensive monitoring and alerting",
            "Consider implementing CDN for static assets",
            "Optimize database queries with proper indexing"
        ])
        
        return recommendations
    
    def run_comprehensive_performance_tests(self) -> Dict[str, Any]:
        """
        Execute the complete performance test suite.
        
        Returns:
            Dictionary containing all performance test results and analysis
        """
        print("🚀 Starting Comprehensive Shadowlands RPG Performance Test Suite")
        print("=" * 70)
        
        # Check if backend is available
        try:
            response = requests.get(f"{self.backend_url}/api/health", timeout=5)
            if response.status_code != 200:
                return {'error': 'Backend server not available'}
        except:
            return {'error': 'Backend server not available'}
        
        print("✅ Backend server available")
        print("=" * 70)
        
        # 1. Response Time Benchmarking
        print("1. Response Time Benchmarking")
        print("-" * 40)
        
        critical_endpoints = [
            ('GET', '/api/health'),
            ('POST', '/api/session/init'),
            ('GET', '/api/equipment/available'),
            ('GET', '/api/equipment/overview'),
            ('GET', '/api/quests/available'),
            ('GET', '/api/combat/health'),
            ('GET', '/api/combat/abilities')
        ]
        
        performance_metrics = []
        for method, endpoint in critical_endpoints:
            metric = self.measure_response_time(method, endpoint)
            performance_metrics.append(metric)
        
        # 2. Load Testing
        print("\n2. Load Testing")
        print("-" * 40)
        
        load_test_results = []
        for user_count in LOAD_TEST_USERS:
            result = self.run_load_test(user_count)
            load_test_results.append(result)
        
        # 3. System Resource Monitoring
        print("\n3. System Resource Monitoring")
        print("-" * 40)
        
        resource_usage = self.monitor_system_resources(30)  # 30 seconds
        
        # 4. Performance Analysis
        print("\n4. Performance Analysis")
        print("-" * 40)
        
        bottleneck_analysis = self.analyze_performance_bottlenecks(performance_metrics)
        optimization_recommendations = self.generate_optimization_recommendations(
            load_test_results, resource_usage
        )
        
        # Generate comprehensive report
        report = {
            'performance_metrics': performance_metrics,
            'load_test_results': load_test_results,
            'resource_usage': resource_usage,
            'bottleneck_analysis': bottleneck_analysis,
            'optimization_recommendations': optimization_recommendations,
            'summary': {
                'total_endpoints_tested': len(performance_metrics),
                'avg_response_time': statistics.mean([m.avg_time for m in performance_metrics]),
                'overall_success_rate': statistics.mean([m.success_rate for m in performance_metrics]),
                'max_concurrent_users_tested': max(LOAD_TEST_USERS),
                'overall_performance_rating': bottleneck_analysis['overall_rating']
            }
        }
        
        return report

def main():
    """Main function to execute the comprehensive performance test suite."""
    print("Shadowlands RPG - Performance Testing and Optimization Suite")
    print("Phase FR4.5: Performance Testing and Optimization")
    print("=" * 70)
    
    # Initialize tester
    tester = ShadowlandsPerformanceTester()
    
    # Run comprehensive performance tests
    results = tester.run_comprehensive_performance_tests()
    
    if 'error' in results:
        print(f"\n❌ Performance testing failed: {results['error']}")
        return results
    
    # Display results summary
    print("\n" + "=" * 70)
    print("🎯 PERFORMANCE TEST RESULTS SUMMARY")
    print("=" * 70)
    
    summary = results['summary']
    print(f"Endpoints Tested: {summary['total_endpoints_tested']}")
    print(f"Average Response Time: {summary['avg_response_time']:.3f}s")
    print(f"Overall Success Rate: {summary['overall_success_rate']:.1f}%")
    print(f"Max Concurrent Users: {summary['max_concurrent_users_tested']}")
    print(f"Performance Rating: {summary['overall_performance_rating'].upper()}")
    
    # Display performance metrics
    print("\n🚀 ENDPOINT PERFORMANCE METRICS")
    print("-" * 50)
    for metric in results['performance_metrics']:
        print(f"{metric.test_name}:")
        print(f"  Avg: {metric.avg_time:.3f}s | P95: {metric.p95_time:.3f}s | Success: {metric.success_rate:.1f}%")
    
    # Display load test results
    print("\n⚡ LOAD TEST RESULTS")
    print("-" * 50)
    for result in results['load_test_results']:
        print(f"{result.concurrent_users} users: {result.success_rate:.1f}% success, "
              f"{result.avg_response_time:.3f}s avg, {result.throughput:.1f} req/s")
    
    # Display resource usage
    print("\n💻 SYSTEM RESOURCE USAGE")
    print("-" * 50)
    resource = results['resource_usage']
    print(f"CPU: {resource['cpu']['avg_percent']:.1f}% avg, {resource['cpu']['max_percent']:.1f}% max")
    print(f"Memory: {resource['memory']['avg_percent']:.1f}% avg, "
          f"{resource['memory']['avg_available_gb']:.1f}GB available")
    print(f"Network: {resource['network']['avg_bytes_per_sec']/1024:.1f} KB/s avg")
    
    # Display bottlenecks
    print("\n⚠️  PERFORMANCE BOTTLENECKS")
    print("-" * 50)
    bottlenecks = results['bottleneck_analysis']['bottlenecks']
    if bottlenecks:
        for bottleneck in bottlenecks:
            print(f"• {bottleneck['endpoint']}: {bottleneck['issue']}")
    else:
        print("✅ No significant bottlenecks detected")
    
    # Display top recommendations
    print("\n💡 TOP OPTIMIZATION RECOMMENDATIONS")
    print("-" * 50)
    for i, rec in enumerate(results['optimization_recommendations'][:5], 1):
        print(f"{i}. {rec}")
    
    # Save detailed results to file
    serializable_results = {
        'summary': results['summary'],
        'performance_metrics': [
            {
                'test_name': m.test_name,
                'min_time': m.min_time,
                'max_time': m.max_time,
                'avg_time': m.avg_time,
                'median_time': m.median_time,
                'p95_time': m.p95_time,
                'p99_time': m.p99_time,
                'success_rate': m.success_rate,
                'throughput': m.throughput,
                'total_requests': m.total_requests
            }
            for m in results['performance_metrics']
        ],
        'load_test_results': [
            {
                'concurrent_users': r.concurrent_users,
                'total_requests': r.total_requests,
                'successful_requests': r.successful_requests,
                'failed_requests': r.failed_requests,
                'success_rate': r.success_rate,
                'avg_response_time': r.avg_response_time,
                'throughput': r.throughput,
                'errors': r.errors
            }
            for r in results['load_test_results']
        ],
        'resource_usage': results['resource_usage'],
        'bottleneck_analysis': results['bottleneck_analysis'],
        'optimization_recommendations': results['optimization_recommendations']
    }
    
    with open('/home/ubuntu/performance_test_results.json', 'w') as f:
        json.dump(serializable_results, f, indent=2)
    
    print(f"\n📊 Detailed results saved to: /home/ubuntu/performance_test_results.json")
    
    # Determine overall performance status
    rating = summary['overall_performance_rating']
    if rating == 'excellent':
        print("\n✅ OVERALL STATUS: EXCELLENT - Outstanding performance across all metrics")
    elif rating == 'good':
        print("\n✅ OVERALL STATUS: GOOD - Strong performance with minor optimization opportunities")
    elif rating == 'acceptable':
        print("\n⚠️  OVERALL STATUS: ACCEPTABLE - Adequate performance, optimization recommended")
    else:
        print("\n❌ OVERALL STATUS: NEEDS OPTIMIZATION - Performance improvements required")
    
    return results

if __name__ == "__main__":
    main()


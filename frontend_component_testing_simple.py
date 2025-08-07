#!/usr/bin/env python3
"""
Shadowlands RPG - Simplified Frontend Component Testing Suite
Phase FR4.3: Frontend Component Testing Implementation

This module provides comprehensive testing for Shadowlands RPG React components
by analyzing component files, structure, and integration patterns without requiring
complex JavaScript testing frameworks.

Author: Manus AI
Date: July 21, 2025
"""

import os
import re
import json
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import subprocess

@dataclass
class ComponentTestResult:
    """Data class for storing component test results"""
    test_name: str
    success: bool
    duration: float
    error_message: Optional[str] = None
    details: Optional[Dict] = None

class ShadowlandsFrontendTester:
    """
    Simplified frontend component testing framework for Shadowlands RPG.
    
    This class analyzes React components for:
    - File structure and imports
    - Component architecture and patterns
    - State management implementation
    - API integration patterns
    - Performance considerations
    """
    
    def __init__(self):
        self.component_path = '/home/ubuntu/shadowlands-rpg/src/components'
        self.src_path = '/home/ubuntu/shadowlands-rpg/src'
        self.test_results: List[ComponentTestResult] = []
        
    def test_component_file_structure(self) -> List[ComponentTestResult]:
        """
        Test React component file structure and basic validation.
        
        Returns:
            List of ComponentTestResult objects for file structure tests
        """
        results = []
        expected_components = [
            'game/EquipmentManager.jsx',
            'game/CharacterEquipment.jsx', 
            'game/InventoryGrid.jsx',
            'game/EquipmentTooltip.jsx',
            'game/EquipmentSlot.jsx',
            'ui/tabs.jsx',
            'ui/separator.jsx'
        ]
        
        for component in expected_components:
            start_time = time.time()
            file_path = os.path.join(self.component_path, component)
            
            try:
                if os.path.exists(file_path):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Analyze component structure
                    analysis = self.analyze_component_structure(content, component)
                    
                    results.append(ComponentTestResult(
                        test_name=f"Component Structure: {component}",
                        success=analysis['is_valid'],
                        duration=time.time() - start_time,
                        error_message=None if analysis['is_valid'] else analysis['issues'],
                        details=analysis
                    ))
                else:
                    results.append(ComponentTestResult(
                        test_name=f"Component Structure: {component}",
                        success=False,
                        duration=time.time() - start_time,
                        error_message="File does not exist"
                    ))
                    
            except Exception as e:
                results.append(ComponentTestResult(
                    test_name=f"Component Structure: {component}",
                    success=False,
                    duration=time.time() - start_time,
                    error_message=str(e)
                ))
        
        return results
    
    def analyze_component_structure(self, content: str, component_name: str) -> Dict[str, Any]:
        """
        Analyze React component structure and patterns.
        
        Args:
            content: Component file content
            component_name: Name of the component file
            
        Returns:
            Dictionary with analysis results
        """
        analysis = {
            'is_valid': True,
            'issues': [],
            'has_react_import': False,
            'has_export': False,
            'has_jsx': False,
            'has_hooks': False,
            'has_api_calls': False,
            'has_error_handling': False,
            'has_prop_types': False,
            'component_complexity': 'low',
            'file_size': len(content),
            'line_count': len(content.split('\n'))
        }
        
        # Check for React import
        if re.search(r'import\s+React|from\s+[\'"]react[\'"]', content):
            analysis['has_react_import'] = True
        else:
            analysis['issues'].append("Missing React import")
        
        # Check for export
        if re.search(r'export\s+default|export\s+\{', content):
            analysis['has_export'] = True
        else:
            analysis['issues'].append("Missing export statement")
        
        # Check for JSX
        if re.search(r'return\s*\(.*<|return\s*<', content, re.DOTALL):
            analysis['has_jsx'] = True
        else:
            analysis['issues'].append("No JSX found")
        
        # Check for React hooks
        hook_patterns = [
            r'useState', r'useEffect', r'useContext', r'useReducer',
            r'useCallback', r'useMemo', r'useRef'
        ]
        for pattern in hook_patterns:
            if re.search(pattern, content):
                analysis['has_hooks'] = True
                break
        
        # Check for API calls
        api_patterns = [
            r'fetch\(', r'axios\.', r'\.get\(', r'\.post\(',
            r'api/', r'localhost:5001'
        ]
        for pattern in api_patterns:
            if re.search(pattern, content):
                analysis['has_api_calls'] = True
                break
        
        # Check for error handling
        error_patterns = [
            r'try\s*\{', r'catch\s*\(', r'\.catch\(',
            r'error', r'Error', r'throw'
        ]
        for pattern in error_patterns:
            if re.search(pattern, content):
                analysis['has_error_handling'] = True
                break
        
        # Check for prop types or TypeScript
        if re.search(r'PropTypes|interface\s+\w+Props|type\s+\w+Props', content):
            analysis['has_prop_types'] = True
        
        # Determine component complexity
        jsx_elements = len(re.findall(r'<\w+', content))
        if jsx_elements > 20:
            analysis['component_complexity'] = 'high'
        elif jsx_elements > 10:
            analysis['component_complexity'] = 'medium'
        
        # Overall validation
        critical_issues = [
            issue for issue in analysis['issues'] 
            if 'React import' in issue or 'export' in issue or 'JSX' in issue
        ]
        
        if critical_issues:
            analysis['is_valid'] = False
            analysis['issues'] = '; '.join(critical_issues)
        else:
            analysis['is_valid'] = True
            analysis['issues'] = None
        
        return analysis
    
    def test_api_integration_patterns(self) -> List[ComponentTestResult]:
        """
        Test API integration patterns in React components.
        
        Returns:
            List of ComponentTestResult objects for API integration tests
        """
        results = []
        
        # Find all JavaScript/JSX files
        js_files = []
        for root, dirs, files in os.walk(self.src_path):
            for file in files:
                if file.endswith(('.js', '.jsx', '.ts', '.tsx')):
                    js_files.append(os.path.join(root, file))
        
        api_integration_analysis = {
            'files_with_api_calls': 0,
            'total_api_calls': 0,
            'error_handling_present': 0,
            'loading_states': 0,
            'proper_endpoints': 0,
            'session_management': 0
        }
        
        for file_path in js_files:
            start_time = time.time()
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Analyze API integration
                file_analysis = self.analyze_api_integration(content)
                
                # Update overall analysis
                if file_analysis['has_api_calls']:
                    api_integration_analysis['files_with_api_calls'] += 1
                
                api_integration_analysis['total_api_calls'] += file_analysis['api_call_count']
                
                if file_analysis['has_error_handling']:
                    api_integration_analysis['error_handling_present'] += 1
                
                if file_analysis['has_loading_states']:
                    api_integration_analysis['loading_states'] += 1
                
                if file_analysis['uses_proper_endpoints']:
                    api_integration_analysis['proper_endpoints'] += 1
                
                if file_analysis['has_session_management']:
                    api_integration_analysis['session_management'] += 1
                
                # Create individual file result
                relative_path = os.path.relpath(file_path, self.src_path)
                results.append(ComponentTestResult(
                    test_name=f"API Integration: {relative_path}",
                    success=file_analysis['integration_quality'] >= 0.7,
                    duration=time.time() - start_time,
                    error_message=None if file_analysis['integration_quality'] >= 0.7 else "Poor API integration patterns",
                    details=file_analysis
                ))
                
            except Exception as e:
                relative_path = os.path.relpath(file_path, self.src_path)
                results.append(ComponentTestResult(
                    test_name=f"API Integration: {relative_path}",
                    success=False,
                    duration=time.time() - start_time,
                    error_message=str(e)
                ))
        
        # Overall API integration assessment
        total_files = len(js_files)
        overall_quality = (
            (api_integration_analysis['error_handling_present'] / max(api_integration_analysis['files_with_api_calls'], 1)) * 0.3 +
            (api_integration_analysis['loading_states'] / max(api_integration_analysis['files_with_api_calls'], 1)) * 0.2 +
            (api_integration_analysis['proper_endpoints'] / max(api_integration_analysis['files_with_api_calls'], 1)) * 0.3 +
            (api_integration_analysis['session_management'] / max(total_files, 1)) * 0.2
        )
        
        results.append(ComponentTestResult(
            test_name="Overall API Integration Quality",
            success=overall_quality >= 0.75,
            duration=0,
            error_message=None if overall_quality >= 0.75 else f"API integration quality {overall_quality:.2f} below threshold 0.75",
            details={
                'overall_quality': overall_quality,
                'analysis': api_integration_analysis,
                'total_files_analyzed': total_files
            }
        ))
        
        return results
    
    def analyze_api_integration(self, content: str) -> Dict[str, Any]:
        """
        Analyze API integration patterns in a file.
        
        Args:
            content: File content to analyze
            
        Returns:
            Dictionary with API integration analysis
        """
        analysis = {
            'has_api_calls': False,
            'api_call_count': 0,
            'has_error_handling': False,
            'has_loading_states': False,
            'uses_proper_endpoints': False,
            'has_session_management': False,
            'integration_quality': 0.0
        }
        
        # Check for API calls
        api_patterns = [
            r'fetch\s*\(',
            r'axios\.',
            r'\.get\s*\(',
            r'\.post\s*\(',
            r'\.put\s*\(',
            r'\.delete\s*\('
        ]
        
        for pattern in api_patterns:
            matches = re.findall(pattern, content)
            analysis['api_call_count'] += len(matches)
        
        if analysis['api_call_count'] > 0:
            analysis['has_api_calls'] = True
        
        # Check for error handling
        error_patterns = [
            r'\.catch\s*\(',
            r'try\s*\{.*catch',
            r'error\s*=>',
            r'onError',
            r'handleError'
        ]
        
        for pattern in error_patterns:
            if re.search(pattern, content, re.DOTALL):
                analysis['has_error_handling'] = True
                break
        
        # Check for loading states
        loading_patterns = [
            r'loading',
            r'isLoading',
            r'setLoading',
            r'Loading',
            r'Spinner',
            r'pending'
        ]
        
        for pattern in loading_patterns:
            if re.search(pattern, content):
                analysis['has_loading_states'] = True
                break
        
        # Check for proper endpoints
        endpoint_patterns = [
            r'/api/',
            r'localhost:5001',
            r'session/init',
            r'equipment/',
            r'characters/',
            r'quests/'
        ]
        
        for pattern in endpoint_patterns:
            if re.search(pattern, content):
                analysis['uses_proper_endpoints'] = True
                break
        
        # Check for session management
        session_patterns = [
            r'session',
            r'Session',
            r'auth',
            r'Auth',
            r'token',
            r'Token'
        ]
        
        for pattern in session_patterns:
            if re.search(pattern, content):
                analysis['has_session_management'] = True
                break
        
        # Calculate integration quality score
        quality_factors = []
        
        if analysis['has_api_calls']:
            if analysis['has_error_handling']:
                quality_factors.append(0.3)
            if analysis['has_loading_states']:
                quality_factors.append(0.2)
            if analysis['uses_proper_endpoints']:
                quality_factors.append(0.3)
            if analysis['has_session_management']:
                quality_factors.append(0.2)
        
        analysis['integration_quality'] = sum(quality_factors)
        
        return analysis
    
    def test_component_performance_patterns(self) -> List[ComponentTestResult]:
        """
        Test performance-related patterns in React components.
        
        Returns:
            List of ComponentTestResult objects for performance tests
        """
        results = []
        
        # Find all component files
        component_files = []
        for root, dirs, files in os.walk(self.component_path):
            for file in files:
                if file.endswith(('.jsx', '.js')):
                    component_files.append(os.path.join(root, file))
        
        performance_analysis = {
            'components_with_memo': 0,
            'components_with_callback': 0,
            'components_with_effect_cleanup': 0,
            'components_with_key_props': 0,
            'total_components': len(component_files)
        }
        
        for file_path in component_files:
            start_time = time.time()
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Analyze performance patterns
                perf_analysis = self.analyze_performance_patterns(content)
                
                # Update overall analysis
                if perf_analysis['uses_memo']:
                    performance_analysis['components_with_memo'] += 1
                
                if perf_analysis['uses_callback']:
                    performance_analysis['components_with_callback'] += 1
                
                if perf_analysis['has_effect_cleanup']:
                    performance_analysis['components_with_effect_cleanup'] += 1
                
                if perf_analysis['uses_key_props']:
                    performance_analysis['components_with_key_props'] += 1
                
                # Create individual component result
                relative_path = os.path.relpath(file_path, self.component_path)
                results.append(ComponentTestResult(
                    test_name=f"Performance Patterns: {relative_path}",
                    success=perf_analysis['performance_score'] >= 0.6,
                    duration=time.time() - start_time,
                    error_message=None if perf_analysis['performance_score'] >= 0.6 else "Poor performance patterns",
                    details=perf_analysis
                ))
                
            except Exception as e:
                relative_path = os.path.relpath(file_path, self.component_path)
                results.append(ComponentTestResult(
                    test_name=f"Performance Patterns: {relative_path}",
                    success=False,
                    duration=time.time() - start_time,
                    error_message=str(e)
                ))
        
        # Overall performance assessment
        if performance_analysis['total_components'] > 0:
            overall_performance = (
                (performance_analysis['components_with_memo'] / performance_analysis['total_components']) * 0.25 +
                (performance_analysis['components_with_callback'] / performance_analysis['total_components']) * 0.25 +
                (performance_analysis['components_with_effect_cleanup'] / performance_analysis['total_components']) * 0.25 +
                (performance_analysis['components_with_key_props'] / performance_analysis['total_components']) * 0.25
            )
        else:
            overall_performance = 0.0
        
        results.append(ComponentTestResult(
            test_name="Overall Performance Patterns",
            success=overall_performance >= 0.5,
            duration=0,
            error_message=None if overall_performance >= 0.5 else f"Performance patterns score {overall_performance:.2f} below threshold 0.5",
            details={
                'overall_performance': overall_performance,
                'analysis': performance_analysis
            }
        ))
        
        return results
    
    def analyze_performance_patterns(self, content: str) -> Dict[str, Any]:
        """
        Analyze performance-related patterns in component content.
        
        Args:
            content: Component file content
            
        Returns:
            Dictionary with performance analysis
        """
        analysis = {
            'uses_memo': False,
            'uses_callback': False,
            'has_effect_cleanup': False,
            'uses_key_props': False,
            'has_unnecessary_renders': False,
            'performance_score': 0.0
        }
        
        # Check for React.memo or useMemo
        if re.search(r'React\.memo|useMemo', content):
            analysis['uses_memo'] = True
        
        # Check for useCallback
        if re.search(r'useCallback', content):
            analysis['uses_callback'] = True
        
        # Check for effect cleanup
        if re.search(r'return\s*\(\s*\)\s*=>', content) or re.search(r'return\s*function', content):
            analysis['has_effect_cleanup'] = True
        
        # Check for key props in lists
        if re.search(r'key\s*=', content):
            analysis['uses_key_props'] = True
        
        # Check for potential performance issues
        performance_issues = [
            r'\.map\s*\([^)]*\)\s*\.map',  # Chained maps
            r'new\s+\w+\s*\([^)]*\)\s*}',  # Object creation in render
            r'function\s*\([^)]*\)\s*{[^}]*}[^,;]*}',  # Inline functions
        ]
        
        for pattern in performance_issues:
            if re.search(pattern, content):
                analysis['has_unnecessary_renders'] = True
                break
        
        # Calculate performance score
        score = 0.0
        if analysis['uses_memo']:
            score += 0.25
        if analysis['uses_callback']:
            score += 0.25
        if analysis['has_effect_cleanup']:
            score += 0.25
        if analysis['uses_key_props']:
            score += 0.25
        if analysis['has_unnecessary_renders']:
            score -= 0.2  # Penalty for performance issues
        
        analysis['performance_score'] = max(0.0, score)
        
        return analysis
    
    def test_responsive_design_patterns(self) -> List[ComponentTestResult]:
        """
        Test responsive design patterns in components and styles.
        
        Returns:
            List of ComponentTestResult objects for responsive design tests
        """
        results = []
        
        # Check for CSS files and responsive patterns
        css_files = []
        for root, dirs, files in os.walk(self.src_path):
            for file in files:
                if file.endswith(('.css', '.scss', '.module.css')):
                    css_files.append(os.path.join(root, file))
        
        # Also check for Tailwind classes in JSX files
        jsx_files = []
        for root, dirs, files in os.walk(self.src_path):
            for file in files:
                if file.endswith(('.jsx', '.js')):
                    jsx_files.append(os.path.join(root, file))
        
        responsive_analysis = {
            'files_with_responsive_css': 0,
            'files_with_mobile_classes': 0,
            'files_with_breakpoints': 0,
            'total_style_files': len(css_files) + len(jsx_files)
        }
        
        # Analyze CSS files
        for file_path in css_files:
            start_time = time.time()
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                responsive_patterns = self.analyze_responsive_patterns(content, 'css')
                
                if responsive_patterns['has_responsive_design']:
                    responsive_analysis['files_with_responsive_css'] += 1
                
                if responsive_patterns['has_mobile_support']:
                    responsive_analysis['files_with_mobile_classes'] += 1
                
                if responsive_patterns['has_breakpoints']:
                    responsive_analysis['files_with_breakpoints'] += 1
                
                relative_path = os.path.relpath(file_path, self.src_path)
                results.append(ComponentTestResult(
                    test_name=f"Responsive CSS: {relative_path}",
                    success=responsive_patterns['responsive_score'] >= 0.5,
                    duration=time.time() - start_time,
                    error_message=None if responsive_patterns['responsive_score'] >= 0.5 else "Poor responsive design patterns",
                    details=responsive_patterns
                ))
                
            except Exception as e:
                relative_path = os.path.relpath(file_path, self.src_path)
                results.append(ComponentTestResult(
                    test_name=f"Responsive CSS: {relative_path}",
                    success=False,
                    duration=time.time() - start_time,
                    error_message=str(e)
                ))
        
        # Analyze JSX files for Tailwind responsive classes
        for file_path in jsx_files:
            start_time = time.time()
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                responsive_patterns = self.analyze_responsive_patterns(content, 'jsx')
                
                if responsive_patterns['has_responsive_design']:
                    responsive_analysis['files_with_responsive_css'] += 1
                
                if responsive_patterns['has_mobile_support']:
                    responsive_analysis['files_with_mobile_classes'] += 1
                
                if responsive_patterns['has_breakpoints']:
                    responsive_analysis['files_with_breakpoints'] += 1
                
                relative_path = os.path.relpath(file_path, self.src_path)
                results.append(ComponentTestResult(
                    test_name=f"Responsive JSX: {relative_path}",
                    success=responsive_patterns['responsive_score'] >= 0.3,  # Lower threshold for JSX
                    duration=time.time() - start_time,
                    error_message=None if responsive_patterns['responsive_score'] >= 0.3 else "Limited responsive design patterns",
                    details=responsive_patterns
                ))
                
            except Exception as e:
                relative_path = os.path.relpath(file_path, self.src_path)
                results.append(ComponentTestResult(
                    test_name=f"Responsive JSX: {relative_path}",
                    success=False,
                    duration=time.time() - start_time,
                    error_message=str(e)
                ))
        
        # Overall responsive design assessment
        if responsive_analysis['total_style_files'] > 0:
            overall_responsive = (
                (responsive_analysis['files_with_responsive_css'] / responsive_analysis['total_style_files']) * 0.4 +
                (responsive_analysis['files_with_mobile_classes'] / responsive_analysis['total_style_files']) * 0.3 +
                (responsive_analysis['files_with_breakpoints'] / responsive_analysis['total_style_files']) * 0.3
            )
        else:
            overall_responsive = 0.0
        
        results.append(ComponentTestResult(
            test_name="Overall Responsive Design",
            success=overall_responsive >= 0.4,
            duration=0,
            error_message=None if overall_responsive >= 0.4 else f"Responsive design score {overall_responsive:.2f} below threshold 0.4",
            details={
                'overall_responsive': overall_responsive,
                'analysis': responsive_analysis
            }
        ))
        
        return results
    
    def analyze_responsive_patterns(self, content: str, file_type: str) -> Dict[str, Any]:
        """
        Analyze responsive design patterns in content.
        
        Args:
            content: File content to analyze
            file_type: Type of file ('css' or 'jsx')
            
        Returns:
            Dictionary with responsive design analysis
        """
        analysis = {
            'has_responsive_design': False,
            'has_mobile_support': False,
            'has_breakpoints': False,
            'responsive_score': 0.0
        }
        
        if file_type == 'css':
            # CSS responsive patterns
            responsive_patterns = [
                r'@media\s*\(',
                r'min-width',
                r'max-width',
                r'screen\s+and',
                r'orientation',
                r'flex',
                r'grid'
            ]
            
            mobile_patterns = [
                r'768px',
                r'480px',
                r'mobile',
                r'phone',
                r'small'
            ]
            
            breakpoint_patterns = [
                r'@media.*768',
                r'@media.*1024',
                r'@media.*1200',
                r'sm:',
                r'md:',
                r'lg:',
                r'xl:'
            ]
            
        else:  # jsx
            # Tailwind responsive patterns
            responsive_patterns = [
                r'sm:',
                r'md:',
                r'lg:',
                r'xl:',
                r'2xl:',
                r'flex',
                r'grid',
                r'responsive'
            ]
            
            mobile_patterns = [
                r'sm:',
                r'mobile',
                r'touch',
                r'phone'
            ]
            
            breakpoint_patterns = [
                r'sm:',
                r'md:',
                r'lg:',
                r'xl:'
            ]
        
        # Check for responsive patterns
        for pattern in responsive_patterns:
            if re.search(pattern, content):
                analysis['has_responsive_design'] = True
                break
        
        # Check for mobile support
        for pattern in mobile_patterns:
            if re.search(pattern, content):
                analysis['has_mobile_support'] = True
                break
        
        # Check for breakpoints
        for pattern in breakpoint_patterns:
            if re.search(pattern, content):
                analysis['has_breakpoints'] = True
                break
        
        # Calculate responsive score
        score = 0.0
        if analysis['has_responsive_design']:
            score += 0.4
        if analysis['has_mobile_support']:
            score += 0.3
        if analysis['has_breakpoints']:
            score += 0.3
        
        analysis['responsive_score'] = score
        
        return analysis
    
    def run_comprehensive_test_suite(self) -> Dict[str, Any]:
        """
        Execute the complete frontend test suite and generate comprehensive results.
        
        Returns:
            Dictionary containing all test results and analysis
        """
        print("🚀 Starting Comprehensive Shadowlands RPG Frontend Test Suite")
        print("=" * 65)
        
        all_results = []
        
        # Component file structure tests
        print("Testing Component File Structure...")
        structure_results = self.test_component_file_structure()
        all_results.extend(structure_results)
        
        # API integration pattern tests
        print("Testing API Integration Patterns...")
        api_results = self.test_api_integration_patterns()
        all_results.extend(api_results)
        
        # Performance pattern tests
        print("Testing Performance Patterns...")
        performance_results = self.test_component_performance_patterns()
        all_results.extend(performance_results)
        
        # Responsive design tests
        print("Testing Responsive Design Patterns...")
        responsive_results = self.test_responsive_design_patterns()
        all_results.extend(responsive_results)
        
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
            'test_categories': {
                'component_structure': structure_results,
                'api_integration': api_results,
                'performance_patterns': performance_results,
                'responsive_design': responsive_results
            },
            'detailed_results': all_results
        }
        
        return report

def main():
    """Main function to execute the comprehensive frontend test suite."""
    print("Shadowlands RPG - Frontend Component Testing Suite")
    print("Phase FR4.3: Frontend Component Testing Implementation")
    print("=" * 65)
    
    # Initialize tester
    tester = ShadowlandsFrontendTester()
    
    # Run comprehensive test suite
    results = tester.run_comprehensive_test_suite()
    
    # Display results summary
    print("\n" + "=" * 65)
    print("🎯 FRONTEND TEST RESULTS SUMMARY")
    print("=" * 65)
    
    summary = results['test_summary']
    print(f"Total Tests: {summary['total_tests']}")
    print(f"Successful: {summary['successful_tests']}")
    print(f"Failed: {summary['failed_tests']}")
    print(f"Success Rate: {summary['success_rate']:.1f}%")
    print(f"Average Duration: {summary['average_duration']:.3f}s")
    
    # Display category results
    print("\n📊 TEST CATEGORY RESULTS")
    print("-" * 40)
    for category, category_results in results['test_categories'].items():
        category_success = sum(1 for r in category_results if r.success)
        category_total = len(category_results)
        category_rate = (category_success / category_total) * 100 if category_total > 0 else 0
        print(f"{category}: {category_success}/{category_total} ({category_rate:.1f}%)")
    
    # Save detailed results to file
    serializable_results = []
    for result in results['detailed_results']:
        serializable_results.append({
            'test_name': result.test_name,
            'success': result.success,
            'duration': result.duration,
            'error_message': result.error_message,
            'details': result.details
        })
    
    final_results = {
        'test_summary': results['test_summary'],
        'detailed_results': serializable_results
    }
    
    with open('/home/ubuntu/frontend_component_test_results.json', 'w') as f:
        json.dump(final_results, f, indent=2)
    
    print(f"\n📊 Detailed results saved to: /home/ubuntu/frontend_component_test_results.json")
    
    # Determine overall test status
    if summary['success_rate'] >= 85:
        print("\n✅ OVERALL STATUS: EXCELLENT - All components performing well")
    elif summary['success_rate'] >= 70:
        print("\n⚠️  OVERALL STATUS: GOOD - Minor component issues detected")
    else:
        print("\n❌ OVERALL STATUS: NEEDS ATTENTION - Significant component issues detected")
    
    return results

if __name__ == "__main__":
    main()


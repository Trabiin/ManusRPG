#!/usr/bin/env python3
"""
Shadowlands RPG - Cross-Browser and Mobile Compatibility Testing Suite
Phase FR4.6: Cross-Browser and Mobile Compatibility Testing

This module provides comprehensive cross-browser and mobile compatibility testing
for the Shadowlands RPG frontend, including responsive design validation,
touch interface testing, and browser-specific feature compatibility.

Author: Manus AI
Date: July 21, 2025
"""

import time
import json
import re
import os
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

@dataclass
class CompatibilityTestResult:
    """Data class for storing compatibility test results"""
    test_name: str
    browser_type: str
    viewport_size: str
    success: bool
    issues: List[str]
    recommendations: List[str]
    details: Optional[Dict] = None

class ShadowlandsCrossBrowserTester:
    """
    Cross-browser and mobile compatibility testing framework for Shadowlands RPG.
    
    This class provides compatibility testing including:
    - Responsive design validation across different viewport sizes
    - CSS compatibility analysis for different browsers
    - Mobile touch interface compatibility
    - JavaScript feature compatibility
    - Performance across different devices
    """
    
    def __init__(self):
        self.frontend_path = '/home/ubuntu/shadowlands-rpg/src'
        self.test_results: List[CompatibilityTestResult] = []
        
        # Define test configurations
        self.viewport_sizes = {
            'mobile_portrait': {'width': 375, 'height': 667},
            'mobile_landscape': {'width': 667, 'height': 375},
            'tablet_portrait': {'width': 768, 'height': 1024},
            'tablet_landscape': {'width': 1024, 'height': 768},
            'desktop_small': {'width': 1280, 'height': 720},
            'desktop_large': {'width': 1920, 'height': 1080}
        }
        
        self.browser_features = {
            'chrome': {
                'css_grid': True,
                'flexbox': True,
                'css_variables': True,
                'es6_modules': True,
                'fetch_api': True,
                'local_storage': True,
                'touch_events': True
            },
            'firefox': {
                'css_grid': True,
                'flexbox': True,
                'css_variables': True,
                'es6_modules': True,
                'fetch_api': True,
                'local_storage': True,
                'touch_events': True
            },
            'safari': {
                'css_grid': True,
                'flexbox': True,
                'css_variables': True,
                'es6_modules': True,
                'fetch_api': True,
                'local_storage': True,
                'touch_events': True
            },
            'edge': {
                'css_grid': True,
                'flexbox': True,
                'css_variables': True,
                'es6_modules': True,
                'fetch_api': True,
                'local_storage': True,
                'touch_events': True
            },
            'ie11': {
                'css_grid': False,
                'flexbox': True,
                'css_variables': False,
                'es6_modules': False,
                'fetch_api': False,
                'local_storage': True,
                'touch_events': False
            }
        }
    
    def analyze_responsive_design(self) -> List[CompatibilityTestResult]:
        """
        Analyze responsive design patterns in the application.
        
        Returns:
            List of CompatibilityTestResult objects for responsive design tests
        """
        results = []
        
        # Find all CSS and JSX files
        style_files = []
        for root, dirs, files in os.walk(self.frontend_path):
            for file in files:
                if file.endswith(('.css', '.scss', '.jsx', '.js')):
                    style_files.append(os.path.join(root, file))
        
        for viewport_name, viewport_size in self.viewport_sizes.items():
            issues = []
            recommendations = []
            
            # Analyze responsive patterns
            responsive_patterns_found = 0
            total_files_analyzed = 0
            
            for file_path in style_files:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    total_files_analyzed += 1
                    
                    # Check for responsive patterns
                    responsive_indicators = [
                        r'@media',
                        r'min-width',
                        r'max-width',
                        r'sm:',
                        r'md:',
                        r'lg:',
                        r'xl:',
                        r'flex',
                        r'grid',
                        r'responsive'
                    ]
                    
                    file_has_responsive = False
                    for pattern in responsive_indicators:
                        if re.search(pattern, content, re.IGNORECASE):
                            file_has_responsive = True
                            break
                    
                    if file_has_responsive:
                        responsive_patterns_found += 1
                    
                    # Check for viewport-specific issues
                    if viewport_name.startswith('mobile'):
                        # Mobile-specific checks
                        if 'touch' not in content.lower() and file_path.endswith(('.jsx', '.js')):
                            issues.append("No touch event handling detected")
                        
                        if 'hover' in content and not 'touch' in content:
                            issues.append("Hover effects without touch alternatives")
                    
                    elif viewport_name.startswith('tablet'):
                        # Tablet-specific checks
                        if 'orientation' not in content and file_path.endswith('.css'):
                            recommendations.append("Consider orientation-specific styles")
                    
                except Exception as e:
                    issues.append(f"Error analyzing file {file_path}: {str(e)}")
            
            # Calculate responsive design score
            responsive_score = (responsive_patterns_found / total_files_analyzed) if total_files_analyzed > 0 else 0
            
            # Determine success based on responsive patterns
            success = responsive_score >= 0.3  # At least 30% of files should have responsive patterns
            
            if responsive_score < 0.3:
                issues.append(f"Low responsive design coverage ({responsive_score:.1%})")
                recommendations.append("Add more responsive design patterns")
            
            if viewport_name.startswith('mobile') and responsive_score < 0.5:
                issues.append("Insufficient mobile optimization")
                recommendations.append("Implement mobile-first design approach")
            
            results.append(CompatibilityTestResult(
                test_name=f"Responsive Design Analysis",
                browser_type="all",
                viewport_size=f"{viewport_size['width']}x{viewport_size['height']}",
                success=success,
                issues=issues,
                recommendations=recommendations,
                details={
                    'viewport_name': viewport_name,
                    'responsive_score': responsive_score,
                    'files_analyzed': total_files_analyzed,
                    'responsive_files': responsive_patterns_found
                }
            ))
        
        return results
    
    def analyze_css_compatibility(self) -> List[CompatibilityTestResult]:
        """
        Analyze CSS compatibility across different browsers.
        
        Returns:
            List of CompatibilityTestResult objects for CSS compatibility tests
        """
        results = []
        
        # Find all CSS files
        css_files = []
        for root, dirs, files in os.walk(self.frontend_path):
            for file in files:
                if file.endswith(('.css', '.scss')):
                    css_files.append(os.path.join(root, file))
        
        for browser, features in self.browser_features.items():
            issues = []
            recommendations = []
            compatibility_score = 0
            total_features_checked = 0
            
            for file_path in css_files:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Check CSS Grid usage
                    if re.search(r'display:\s*grid|grid-template', content):
                        total_features_checked += 1
                        if features['css_grid']:
                            compatibility_score += 1
                        else:
                            issues.append("CSS Grid not supported")
                            recommendations.append("Provide flexbox fallback for CSS Grid")
                    
                    # Check Flexbox usage
                    if re.search(r'display:\s*flex|flex-direction', content):
                        total_features_checked += 1
                        if features['flexbox']:
                            compatibility_score += 1
                        else:
                            issues.append("Flexbox not supported")
                            recommendations.append("Provide float-based fallback")
                    
                    # Check CSS Variables usage
                    if re.search(r'var\(--', content):
                        total_features_checked += 1
                        if features['css_variables']:
                            compatibility_score += 1
                        else:
                            issues.append("CSS Variables not supported")
                            recommendations.append("Provide static value fallbacks")
                    
                    # Check for vendor prefixes
                    vendor_prefixes = ['-webkit-', '-moz-', '-ms-', '-o-']
                    has_prefixes = any(prefix in content for prefix in vendor_prefixes)
                    
                    if not has_prefixes and browser in ['safari', 'ie11']:
                        recommendations.append("Consider adding vendor prefixes for better compatibility")
                
                except Exception as e:
                    issues.append(f"Error analyzing CSS file {file_path}: {str(e)}")
            
            # Calculate compatibility score
            final_score = (compatibility_score / total_features_checked) if total_features_checked > 0 else 1.0
            success = final_score >= 0.8  # 80% compatibility threshold
            
            if not success:
                issues.append(f"Low CSS compatibility score ({final_score:.1%})")
            
            results.append(CompatibilityTestResult(
                test_name=f"CSS Compatibility Analysis",
                browser_type=browser,
                viewport_size="all",
                success=success,
                issues=issues,
                recommendations=recommendations,
                details={
                    'compatibility_score': final_score,
                    'features_checked': total_features_checked,
                    'supported_features': compatibility_score
                }
            ))
        
        return results
    
    def analyze_javascript_compatibility(self) -> List[CompatibilityTestResult]:
        """
        Analyze JavaScript compatibility across different browsers.
        
        Returns:
            List of CompatibilityTestResult objects for JavaScript compatibility tests
        """
        results = []
        
        # Find all JavaScript files
        js_files = []
        for root, dirs, files in os.walk(self.frontend_path):
            for file in files:
                if file.endswith(('.js', '.jsx')):
                    js_files.append(os.path.join(root, file))
        
        for browser, features in self.browser_features.items():
            issues = []
            recommendations = []
            compatibility_score = 0
            total_features_checked = 0
            
            for file_path in js_files:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Check ES6 modules usage
                    if re.search(r'import\s+.*from|export\s+', content):
                        total_features_checked += 1
                        if features['es6_modules']:
                            compatibility_score += 1
                        else:
                            issues.append("ES6 modules not supported")
                            recommendations.append("Use bundler with transpilation")
                    
                    # Check Fetch API usage
                    if re.search(r'fetch\s*\(', content):
                        total_features_checked += 1
                        if features['fetch_api']:
                            compatibility_score += 1
                        else:
                            issues.append("Fetch API not supported")
                            recommendations.append("Provide XMLHttpRequest fallback")
                    
                    # Check localStorage usage
                    if re.search(r'localStorage', content):
                        total_features_checked += 1
                        if features['local_storage']:
                            compatibility_score += 1
                        else:
                            issues.append("localStorage not supported")
                            recommendations.append("Provide cookie-based fallback")
                    
                    # Check touch events usage
                    if re.search(r'touch|Touch', content):
                        total_features_checked += 1
                        if features['touch_events']:
                            compatibility_score += 1
                        else:
                            issues.append("Touch events not supported")
                            recommendations.append("Provide mouse event fallbacks")
                    
                    # Check for ES6+ features
                    es6_features = [
                        r'const\s+',
                        r'let\s+',
                        r'=>',
                        r'`.*\$\{',
                        r'class\s+\w+',
                        r'async\s+function',
                        r'await\s+'
                    ]
                    
                    for pattern in es6_features:
                        if re.search(pattern, content):
                            total_features_checked += 1
                            if browser != 'ie11':
                                compatibility_score += 1
                            else:
                                issues.append("ES6+ features not supported")
                                recommendations.append("Use Babel for transpilation")
                            break
                
                except Exception as e:
                    issues.append(f"Error analyzing JS file {file_path}: {str(e)}")
            
            # Calculate compatibility score
            final_score = (compatibility_score / total_features_checked) if total_features_checked > 0 else 1.0
            success = final_score >= 0.8  # 80% compatibility threshold
            
            if not success:
                issues.append(f"Low JavaScript compatibility score ({final_score:.1%})")
            
            results.append(CompatibilityTestResult(
                test_name=f"JavaScript Compatibility Analysis",
                browser_type=browser,
                viewport_size="all",
                success=success,
                issues=issues,
                recommendations=recommendations,
                details={
                    'compatibility_score': final_score,
                    'features_checked': total_features_checked,
                    'supported_features': compatibility_score
                }
            ))
        
        return results
    
    def analyze_mobile_touch_interface(self) -> List[CompatibilityTestResult]:
        """
        Analyze mobile touch interface compatibility.
        
        Returns:
            List of CompatibilityTestResult objects for mobile touch interface tests
        """
        results = []
        
        # Find all component files
        component_files = []
        for root, dirs, files in os.walk(self.frontend_path):
            for file in files:
                if file.endswith(('.jsx', '.js')):
                    component_files.append(os.path.join(root, file))
        
        mobile_viewports = ['mobile_portrait', 'mobile_landscape']
        
        for viewport_name in mobile_viewports:
            viewport_size = self.viewport_sizes[viewport_name]
            issues = []
            recommendations = []
            
            touch_compatibility_score = 0
            total_interactive_elements = 0
            
            for file_path in component_files:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Check for interactive elements
                    interactive_patterns = [
                        r'onClick',
                        r'onMouseDown',
                        r'onMouseUp',
                        r'onHover',
                        r'button',
                        r'<a\s',
                        r'input',
                        r'select'
                    ]
                    
                    for pattern in interactive_patterns:
                        matches = len(re.findall(pattern, content, re.IGNORECASE))
                        total_interactive_elements += matches
                    
                    # Check for touch-specific events
                    touch_patterns = [
                        r'onTouchStart',
                        r'onTouchEnd',
                        r'onTouchMove',
                        r'touchstart',
                        r'touchend',
                        r'touchmove'
                    ]
                    
                    has_touch_events = any(re.search(pattern, content, re.IGNORECASE) for pattern in touch_patterns)
                    
                    # Check for hover-only interactions
                    hover_only_patterns = [
                        r':hover(?!\s*,\s*:focus)',
                        r'onMouseEnter(?!.*onTouch)',
                        r'onMouseLeave(?!.*onTouch)'
                    ]
                    
                    has_hover_only = any(re.search(pattern, content) for pattern in hover_only_patterns)
                    
                    if has_hover_only:
                        issues.append("Hover-only interactions detected")
                        recommendations.append("Provide touch alternatives for hover effects")
                    
                    # Check for appropriate touch target sizes
                    button_patterns = [
                        r'className.*button',
                        r'<button',
                        r'role="button"'
                    ]
                    
                    has_buttons = any(re.search(pattern, content, re.IGNORECASE) for pattern in button_patterns)
                    
                    if has_buttons:
                        # Check for touch-friendly sizing
                        size_patterns = [
                            r'min-height:\s*44px',
                            r'min-width:\s*44px',
                            r'padding.*\d+px',
                            r'h-\d+',
                            r'w-\d+'
                        ]
                        
                        has_appropriate_sizing = any(re.search(pattern, content) for pattern in size_patterns)
                        
                        if not has_appropriate_sizing:
                            recommendations.append("Ensure touch targets are at least 44px")
                    
                    # Score touch compatibility
                    if total_interactive_elements > 0:
                        if has_touch_events:
                            touch_compatibility_score += 2
                        if not has_hover_only:
                            touch_compatibility_score += 1
                        if has_buttons and has_appropriate_sizing:
                            touch_compatibility_score += 1
                
                except Exception as e:
                    issues.append(f"Error analyzing file {file_path}: {str(e)}")
            
            # Calculate final score
            max_possible_score = len(component_files) * 4  # Max 4 points per file
            final_score = (touch_compatibility_score / max_possible_score) if max_possible_score > 0 else 0
            success = final_score >= 0.6  # 60% threshold for mobile compatibility
            
            if not success:
                issues.append(f"Low mobile touch compatibility ({final_score:.1%})")
            
            if total_interactive_elements > 0 and touch_compatibility_score == 0:
                issues.append("No touch event handling detected")
                recommendations.append("Implement touch event handlers")
            
            results.append(CompatibilityTestResult(
                test_name=f"Mobile Touch Interface Analysis",
                browser_type="mobile",
                viewport_size=f"{viewport_size['width']}x{viewport_size['height']}",
                success=success,
                issues=issues,
                recommendations=recommendations,
                details={
                    'viewport_name': viewport_name,
                    'touch_compatibility_score': final_score,
                    'interactive_elements': total_interactive_elements,
                    'files_analyzed': len(component_files)
                }
            ))
        
        return results
    
    def analyze_performance_across_devices(self) -> List[CompatibilityTestResult]:
        """
        Analyze performance considerations across different device types.
        
        Returns:
            List of CompatibilityTestResult objects for device performance tests
        """
        results = []
        
        device_categories = {
            'mobile_low_end': {
                'cpu_factor': 0.3,
                'memory_limit': 1024,  # MB
                'network_speed': 'slow_3g'
            },
            'mobile_high_end': {
                'cpu_factor': 0.7,
                'memory_limit': 4096,  # MB
                'network_speed': '4g'
            },
            'tablet': {
                'cpu_factor': 0.8,
                'memory_limit': 2048,  # MB
                'network_speed': 'wifi'
            },
            'desktop': {
                'cpu_factor': 1.0,
                'memory_limit': 8192,  # MB
                'network_speed': 'wifi'
            }
        }
        
        # Analyze bundle size and complexity
        js_files = []
        css_files = []
        
        for root, dirs, files in os.walk(self.frontend_path):
            for file in files:
                if file.endswith(('.js', '.jsx')):
                    js_files.append(os.path.join(root, file))
                elif file.endswith(('.css', '.scss')):
                    css_files.append(os.path.join(root, file))
        
        # Calculate total file sizes
        total_js_size = 0
        total_css_size = 0
        
        for file_path in js_files:
            try:
                total_js_size += os.path.getsize(file_path)
            except:
                pass
        
        for file_path in css_files:
            try:
                total_css_size += os.path.getsize(file_path)
            except:
                pass
        
        # Convert to KB
        total_js_kb = total_js_size / 1024
        total_css_kb = total_css_size / 1024
        total_bundle_kb = total_js_kb + total_css_kb
        
        for device_name, device_specs in device_categories.items():
            issues = []
            recommendations = []
            
            # Performance thresholds based on device type
            if device_name.startswith('mobile_low_end'):
                js_threshold = 200  # KB
                css_threshold = 50   # KB
                total_threshold = 250  # KB
            elif device_name.startswith('mobile'):
                js_threshold = 500  # KB
                css_threshold = 100  # KB
                total_threshold = 600  # KB
            elif device_name == 'tablet':
                js_threshold = 800  # KB
                css_threshold = 150  # KB
                total_threshold = 950  # KB
            else:  # desktop
                js_threshold = 1500  # KB
                css_threshold = 300  # KB
                total_threshold = 1800  # KB
            
            # Check bundle sizes
            if total_js_kb > js_threshold:
                issues.append(f"JavaScript bundle too large ({total_js_kb:.1f}KB > {js_threshold}KB)")
                recommendations.append("Implement code splitting and lazy loading")
            
            if total_css_kb > css_threshold:
                issues.append(f"CSS bundle too large ({total_css_kb:.1f}KB > {css_threshold}KB)")
                recommendations.append("Remove unused CSS and implement critical CSS")
            
            if total_bundle_kb > total_threshold:
                issues.append(f"Total bundle too large ({total_bundle_kb:.1f}KB > {total_threshold}KB)")
                recommendations.append("Optimize assets and implement progressive loading")
            
            # Check for performance-heavy features
            performance_issues = []
            
            for file_path in js_files:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Check for performance-heavy patterns
                    heavy_patterns = [
                        r'setInterval\s*\(',
                        r'setTimeout.*\d+\)',
                        r'new\s+Date\(\)',
                        r'JSON\.parse',
                        r'JSON\.stringify',
                        r'\.map\s*\([^)]*\)\s*\.map',  # Chained maps
                        r'document\.querySelector',
                        r'document\.getElementById'
                    ]
                    
                    for pattern in heavy_patterns:
                        if re.search(pattern, content):
                            performance_issues.append(pattern)
                
                except:
                    pass
            
            if len(performance_issues) > 10:
                issues.append("High number of potentially expensive operations")
                recommendations.append("Optimize JavaScript performance and reduce DOM queries")
            
            # Determine success
            success = len(issues) == 0
            
            results.append(CompatibilityTestResult(
                test_name=f"Device Performance Analysis",
                browser_type=device_name,
                viewport_size="varies",
                success=success,
                issues=issues,
                recommendations=recommendations,
                details={
                    'device_specs': device_specs,
                    'js_size_kb': total_js_kb,
                    'css_size_kb': total_css_kb,
                    'total_size_kb': total_bundle_kb,
                    'performance_issues_count': len(performance_issues)
                }
            ))
        
        return results
    
    def run_comprehensive_compatibility_tests(self) -> Dict[str, Any]:
        """
        Execute the complete cross-browser and mobile compatibility test suite.
        
        Returns:
            Dictionary containing all compatibility test results and analysis
        """
        print("🚀 Starting Comprehensive Cross-Browser and Mobile Compatibility Test Suite")
        print("=" * 75)
        
        all_results = []
        
        # 1. Responsive Design Analysis
        print("1. Responsive Design Analysis")
        print("-" * 40)
        responsive_results = self.analyze_responsive_design()
        all_results.extend(responsive_results)
        
        # 2. CSS Compatibility Analysis
        print("2. CSS Compatibility Analysis")
        print("-" * 40)
        css_results = self.analyze_css_compatibility()
        all_results.extend(css_results)
        
        # 3. JavaScript Compatibility Analysis
        print("3. JavaScript Compatibility Analysis")
        print("-" * 40)
        js_results = self.analyze_javascript_compatibility()
        all_results.extend(js_results)
        
        # 4. Mobile Touch Interface Analysis
        print("4. Mobile Touch Interface Analysis")
        print("-" * 40)
        mobile_results = self.analyze_mobile_touch_interface()
        all_results.extend(mobile_results)
        
        # 5. Device Performance Analysis
        print("5. Device Performance Analysis")
        print("-" * 40)
        performance_results = self.analyze_performance_across_devices()
        all_results.extend(performance_results)
        
        # Calculate overall statistics
        total_tests = len(all_results)
        successful_tests = sum(1 for result in all_results if result.success)
        success_rate = (successful_tests / total_tests) * 100 if total_tests > 0 else 0
        
        # Categorize results
        categorized_results = {
            'responsive_design': responsive_results,
            'css_compatibility': css_results,
            'javascript_compatibility': js_results,
            'mobile_touch_interface': mobile_results,
            'device_performance': performance_results
        }
        
        # Generate comprehensive report
        report = {
            'test_summary': {
                'total_tests': total_tests,
                'successful_tests': successful_tests,
                'failed_tests': total_tests - successful_tests,
                'success_rate': success_rate
            },
            'test_categories': categorized_results,
            'detailed_results': all_results
        }
        
        return report

def main():
    """Main function to execute the comprehensive compatibility test suite."""
    print("Shadowlands RPG - Cross-Browser and Mobile Compatibility Testing Suite")
    print("Phase FR4.6: Cross-Browser and Mobile Compatibility Testing")
    print("=" * 75)
    
    # Initialize tester
    tester = ShadowlandsCrossBrowserTester()
    
    # Run comprehensive compatibility tests
    results = tester.run_comprehensive_compatibility_tests()
    
    # Display results summary
    print("\n" + "=" * 75)
    print("🎯 COMPATIBILITY TEST RESULTS SUMMARY")
    print("=" * 75)
    
    summary = results['test_summary']
    print(f"Total Tests: {summary['total_tests']}")
    print(f"Successful: {summary['successful_tests']}")
    print(f"Failed: {summary['failed_tests']}")
    print(f"Success Rate: {summary['success_rate']:.1f}%")
    
    # Display category results
    print("\n📊 TEST CATEGORY RESULTS")
    print("-" * 50)
    for category, category_results in results['test_categories'].items():
        category_success = sum(1 for r in category_results if r.success)
        category_total = len(category_results)
        category_rate = (category_success / category_total) * 100 if category_total > 0 else 0
        print(f"{category}: {category_success}/{category_total} ({category_rate:.1f}%)")
    
    # Display browser compatibility summary
    print("\n🌐 BROWSER COMPATIBILITY SUMMARY")
    print("-" * 50)
    browser_results = {}
    for result in results['detailed_results']:
        if result.browser_type not in browser_results:
            browser_results[result.browser_type] = {'success': 0, 'total': 0}
        browser_results[result.browser_type]['total'] += 1
        if result.success:
            browser_results[result.browser_type]['success'] += 1
    
    for browser, stats in browser_results.items():
        rate = (stats['success'] / stats['total']) * 100 if stats['total'] > 0 else 0
        print(f"{browser}: {stats['success']}/{stats['total']} ({rate:.1f}%)")
    
    # Display common issues and recommendations
    print("\n⚠️  COMMON ISSUES DETECTED")
    print("-" * 50)
    all_issues = []
    all_recommendations = []
    
    for result in results['detailed_results']:
        all_issues.extend(result.issues)
        all_recommendations.extend(result.recommendations)
    
    # Count issue frequency
    issue_counts = {}
    for issue in all_issues:
        issue_counts[issue] = issue_counts.get(issue, 0) + 1
    
    # Display top 5 issues
    sorted_issues = sorted(issue_counts.items(), key=lambda x: x[1], reverse=True)
    for issue, count in sorted_issues[:5]:
        print(f"• {issue} ({count} occurrences)")
    
    print("\n💡 TOP RECOMMENDATIONS")
    print("-" * 50)
    
    # Count recommendation frequency
    rec_counts = {}
    for rec in all_recommendations:
        rec_counts[rec] = rec_counts.get(rec, 0) + 1
    
    # Display top 5 recommendations
    sorted_recs = sorted(rec_counts.items(), key=lambda x: x[1], reverse=True)
    for rec, count in sorted_recs[:5]:
        print(f"• {rec} ({count} occurrences)")
    
    # Save detailed results to file
    serializable_results = []
    for result in results['detailed_results']:
        serializable_results.append({
            'test_name': result.test_name,
            'browser_type': result.browser_type,
            'viewport_size': result.viewport_size,
            'success': result.success,
            'issues': result.issues,
            'recommendations': result.recommendations,
            'details': result.details
        })
    
    final_results = {
        'test_summary': results['test_summary'],
        'detailed_results': serializable_results
    }
    
    with open('/home/ubuntu/compatibility_test_results.json', 'w') as f:
        json.dump(final_results, f, indent=2)
    
    print(f"\n📊 Detailed results saved to: /home/ubuntu/compatibility_test_results.json")
    
    # Determine overall compatibility status
    if summary['success_rate'] >= 90:
        print("\n✅ OVERALL STATUS: EXCELLENT - Outstanding compatibility across all platforms")
    elif summary['success_rate'] >= 75:
        print("\n✅ OVERALL STATUS: GOOD - Strong compatibility with minor issues")
    elif summary['success_rate'] >= 60:
        print("\n⚠️  OVERALL STATUS: ACCEPTABLE - Adequate compatibility, improvements recommended")
    else:
        print("\n❌ OVERALL STATUS: NEEDS ATTENTION - Significant compatibility issues detected")
    
    return results

if __name__ == "__main__":
    main()


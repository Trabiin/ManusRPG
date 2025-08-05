#!/usr/bin/env python3
"""
API Response Analysis and Standardization Tool
Analyzes current API responses and identifies standardization issues
"""

import requests
import json
import time
from datetime import datetime

class APIResponseAnalyzer:
    def __init__(self, base_url="http://localhost:5001/api"):
        self.base_url = base_url
        self.session = requests.Session()
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "base_url": base_url,
            "endpoints": {},
            "standardization_issues": [],
            "recommendations": []
        }
    
    def test_endpoint(self, endpoint, method="GET", data=None, description=""):
        """Test a single API endpoint and analyze its response format"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            start_time = time.time()
            
            if method == "GET":
                response = self.session.get(url, timeout=10)
            elif method == "POST":
                response = self.session.post(url, json=data, timeout=10)
            
            response_time = (time.time() - start_time) * 1000
            
            # Analyze response
            analysis = {
                "endpoint": endpoint,
                "method": method,
                "description": description,
                "status_code": response.status_code,
                "response_time_ms": round(response_time, 2),
                "success": response.status_code < 400,
                "content_type": response.headers.get('content-type', ''),
                "response_size": len(response.content)
            }
            
            # Try to parse JSON
            try:
                json_data = response.json()
                analysis["json_valid"] = True
                analysis["response_structure"] = self.analyze_json_structure(json_data)
                analysis["has_success_field"] = "success" in json_data
                analysis["has_error_field"] = "error" in json_data or "message" in json_data
                analysis["response_sample"] = json_data if len(str(json_data)) < 500 else "Response too large"
            except:
                analysis["json_valid"] = False
                analysis["response_text"] = response.text[:200] if response.text else "No content"
            
            self.results["endpoints"][endpoint] = analysis
            return analysis
            
        except Exception as e:
            analysis = {
                "endpoint": endpoint,
                "method": method,
                "description": description,
                "error": str(e),
                "success": False,
                "response_time_ms": 0
            }
            self.results["endpoints"][endpoint] = analysis
            return analysis
    
    def analyze_json_structure(self, data):
        """Analyze the structure of JSON response"""
        if isinstance(data, dict):
            return {
                "type": "object",
                "keys": list(data.keys()),
                "key_count": len(data.keys())
            }
        elif isinstance(data, list):
            return {
                "type": "array",
                "length": len(data),
                "item_type": type(data[0]).__name__ if data else "empty"
            }
        else:
            return {
                "type": type(data).__name__,
                "value": str(data)[:100]
            }
    
    def run_comprehensive_analysis(self):
        """Run analysis on all major API endpoints"""
        print("🔍 Starting comprehensive API response analysis...")
        
        # Initialize session first
        print("1. Initializing session...")
        self.test_endpoint("/session/init", "POST", {}, "Initialize game session")
        
        # Test equipment endpoints
        print("2. Testing equipment endpoints...")
        self.test_endpoint("/equipment/available", "GET", None, "Get available equipment")
        self.test_endpoint("/equipment/equipped", "GET", None, "Get equipped items")
        
        # Test character endpoints
        print("3. Testing character endpoints...")
        self.test_endpoint("/characters", "GET", None, "Get character data")
        
        # Test combat endpoints
        print("4. Testing combat endpoints...")
        self.test_endpoint("/combat/encounter/create", "POST", {"encounter_type": "test"}, "Create combat encounter")
        
        # Test quest endpoints
        print("5. Testing quest endpoints...")
        self.test_endpoint("/quests", "GET", None, "Get quest data")
        
        # Analyze results
        self.analyze_standardization_issues()
        self.generate_recommendations()
        
        return self.results
    
    def analyze_standardization_issues(self):
        """Identify standardization issues across endpoints"""
        issues = []
        
        # Check for consistent success/error patterns
        success_patterns = set()
        error_patterns = set()
        
        for endpoint, data in self.results["endpoints"].items():
            if data.get("json_valid"):
                if data.get("has_success_field"):
                    success_patterns.add("success_field")
                if data.get("has_error_field"):
                    error_patterns.add("error_field")
                
                # Check response structure consistency
                structure = data.get("response_structure", {})
                if structure.get("type") == "object":
                    keys = structure.get("keys", [])
                    if "success" not in keys and "error" not in keys and "message" not in keys:
                        issues.append(f"{endpoint}: No standard success/error indicators")
        
        # Check for HTTP status code consistency
        status_codes = [data.get("status_code") for data in self.results["endpoints"].values()]
        unique_statuses = set(status_codes)
        
        if len(unique_statuses) > 3:
            issues.append(f"Inconsistent HTTP status codes: {unique_statuses}")
        
        self.results["standardization_issues"] = issues
    
    def generate_recommendations(self):
        """Generate standardization recommendations"""
        recommendations = []
        
        # Standard response format recommendation
        recommendations.append({
            "priority": "HIGH",
            "category": "Response Format",
            "recommendation": "Implement standard response wrapper",
            "details": "All API responses should follow: {success: boolean, data: any, error?: string, message?: string}"
        })
        
        # HTTP status code standardization
        recommendations.append({
            "priority": "MEDIUM",
            "category": "HTTP Status Codes",
            "recommendation": "Standardize status codes",
            "details": "Use 200 for success, 400 for client errors, 500 for server errors consistently"
        })
        
        # Error handling standardization
        recommendations.append({
            "priority": "HIGH",
            "category": "Error Handling",
            "recommendation": "Consistent error response format",
            "details": "All errors should include: {success: false, error: 'error_code', message: 'human readable message'}"
        })
        
        self.results["recommendations"] = recommendations
    
    def save_results(self, filename="api_response_analysis_results.json"):
        """Save analysis results to file"""
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"✅ Analysis results saved to {filename}")
    
    def print_summary(self):
        """Print analysis summary"""
        total_endpoints = len(self.results["endpoints"])
        successful_endpoints = sum(1 for data in self.results["endpoints"].values() if data.get("success"))
        
        print(f"\n📊 API Response Analysis Summary")
        print(f"=" * 50)
        print(f"Total Endpoints Tested: {total_endpoints}")
        print(f"Successful Responses: {successful_endpoints}")
        print(f"Success Rate: {(successful_endpoints/total_endpoints)*100:.1f}%")
        print(f"Standardization Issues: {len(self.results['standardization_issues'])}")
        print(f"Recommendations: {len(self.results['recommendations'])}")
        
        if self.results["standardization_issues"]:
            print(f"\n⚠️ Key Issues:")
            for issue in self.results["standardization_issues"]:
                print(f"  • {issue}")
        
        print(f"\n🎯 Top Recommendations:")
        for rec in self.results["recommendations"][:3]:
            print(f"  • {rec['category']}: {rec['recommendation']}")

def main():
    analyzer = APIResponseAnalyzer()
    results = analyzer.run_comprehensive_analysis()
    analyzer.print_summary()
    analyzer.save_results()
    return results

if __name__ == "__main__":
    main()


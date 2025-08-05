#!/usr/bin/env python3
"""
Bundle Optimization Analyzer for Shadowlands RPG
Analyzes current bundle size and identifies optimization opportunities
"""

import os
import json
import subprocess
import time
from pathlib import Path

class BundleOptimizationAnalyzer:
    def __init__(self, project_path="/home/ubuntu/shadowlands-rpg"):
        self.project_path = project_path
        self.results = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "project_path": project_path,
            "analysis": {},
            "optimizations": [],
            "recommendations": []
        }
    
    def analyze_project_structure(self):
        """Analyze the project structure and dependencies"""
        print("📁 Analyzing project structure...")
        
        # Check package.json
        package_json_path = os.path.join(self.project_path, "package.json")
        if os.path.exists(package_json_path):
            with open(package_json_path, 'r') as f:
                package_data = json.load(f)
                
            self.results["analysis"]["dependencies"] = {
                "production": package_data.get("dependencies", {}),
                "development": package_data.get("devDependencies", {}),
                "total_prod_deps": len(package_data.get("dependencies", {})),
                "total_dev_deps": len(package_data.get("devDependencies", {}))
            }
        
        # Analyze source file sizes
        src_path = os.path.join(self.project_path, "src")
        if os.path.exists(src_path):
            file_sizes = {}
            total_size = 0
            
            for root, dirs, files in os.walk(src_path):
                for file in files:
                    if file.endswith(('.js', '.jsx', '.ts', '.tsx', '.css')):
                        file_path = os.path.join(root, file)
                        size = os.path.getsize(file_path)
                        relative_path = os.path.relpath(file_path, src_path)
                        file_sizes[relative_path] = size
                        total_size += size
            
            self.results["analysis"]["source_files"] = {
                "files": file_sizes,
                "total_size_bytes": total_size,
                "total_size_kb": round(total_size / 1024, 2),
                "largest_files": sorted(file_sizes.items(), key=lambda x: x[1], reverse=True)[:10]
            }
    
    def check_build_configuration(self):
        """Check Vite build configuration"""
        print("⚙️ Analyzing build configuration...")
        
        vite_config_path = os.path.join(self.project_path, "vite.config.js")
        if os.path.exists(vite_config_path):
            with open(vite_config_path, 'r') as f:
                config_content = f.read()
            
            self.results["analysis"]["build_config"] = {
                "has_vite_config": True,
                "config_size": len(config_content),
                "has_build_optimization": "build:" in config_content,
                "has_rollup_options": "rollupOptions" in config_content,
                "has_chunk_splitting": "manualChunks" in config_content
            }
        else:
            self.results["analysis"]["build_config"] = {"has_vite_config": False}
    
    def analyze_current_bundle(self):
        """Analyze current bundle if it exists"""
        print("📦 Analyzing current bundle...")
        
        dist_path = os.path.join(self.project_path, "dist")
        if os.path.exists(dist_path):
            bundle_info = {}
            total_size = 0
            
            for root, dirs, files in os.walk(dist_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    size = os.path.getsize(file_path)
                    relative_path = os.path.relpath(file_path, dist_path)
                    bundle_info[relative_path] = size
                    total_size += size
            
            self.results["analysis"]["current_bundle"] = {
                "exists": True,
                "files": bundle_info,
                "total_size_bytes": total_size,
                "total_size_kb": round(total_size / 1024, 2),
                "largest_files": sorted(bundle_info.items(), key=lambda x: x[1], reverse=True)[:10]
            }
        else:
            self.results["analysis"]["current_bundle"] = {"exists": False}
    
    def identify_optimization_opportunities(self):
        """Identify specific optimization opportunities"""
        print("🔍 Identifying optimization opportunities...")
        
        optimizations = []
        
        # Check dependencies for optimization
        if "dependencies" in self.results["analysis"]:
            deps = self.results["analysis"]["dependencies"]["production"]
            
            # Check for large dependencies
            heavy_deps = ["moment", "lodash", "react-router-dom", "material-ui"]
            for dep in heavy_deps:
                if dep in deps:
                    optimizations.append({
                        "type": "dependency_optimization",
                        "priority": "HIGH",
                        "description": f"Replace or optimize {dep}",
                        "impact": "Significant bundle size reduction"
                    })
            
            # Check for unused dependencies
            if len(deps) > 20:
                optimizations.append({
                    "type": "dependency_cleanup",
                    "priority": "MEDIUM",
                    "description": "Review and remove unused dependencies",
                    "impact": "Moderate bundle size reduction"
                })
        
        # Check source file sizes
        if "source_files" in self.results["analysis"]:
            largest_files = self.results["analysis"]["source_files"]["largest_files"]
            for file_path, size in largest_files[:3]:
                if size > 50000:  # Files larger than 50KB
                    optimizations.append({
                        "type": "file_optimization",
                        "priority": "HIGH",
                        "description": f"Optimize large file: {file_path} ({round(size/1024, 2)}KB)",
                        "impact": "Direct bundle size reduction"
                    })
        
        # Check build configuration
        if "build_config" in self.results["analysis"]:
            config = self.results["analysis"]["build_config"]
            
            if not config.get("has_chunk_splitting"):
                optimizations.append({
                    "type": "build_optimization",
                    "priority": "HIGH",
                    "description": "Implement code splitting and chunk optimization",
                    "impact": "Better loading performance and caching"
                })
            
            if not config.get("has_rollup_options"):
                optimizations.append({
                    "type": "build_optimization",
                    "priority": "MEDIUM",
                    "description": "Add Rollup optimization options",
                    "impact": "Bundle size reduction through tree shaking"
                })
        
        self.results["optimizations"] = optimizations
    
    def generate_recommendations(self):
        """Generate specific optimization recommendations"""
        print("💡 Generating optimization recommendations...")
        
        recommendations = [
            {
                "category": "Code Splitting",
                "priority": "HIGH",
                "recommendation": "Implement route-based code splitting",
                "implementation": "Use React.lazy() and Suspense for component lazy loading",
                "expected_impact": "30-50% initial bundle size reduction"
            },
            {
                "category": "Dependency Optimization",
                "priority": "HIGH", 
                "recommendation": "Replace heavy dependencies with lighter alternatives",
                "implementation": "Replace moment.js with date-fns, use lodash-es instead of lodash",
                "expected_impact": "20-30% bundle size reduction"
            },
            {
                "category": "Tree Shaking",
                "priority": "MEDIUM",
                "recommendation": "Optimize imports for better tree shaking",
                "implementation": "Use named imports, avoid default imports from large libraries",
                "expected_impact": "10-20% bundle size reduction"
            },
            {
                "category": "Asset Optimization",
                "priority": "MEDIUM",
                "recommendation": "Optimize images and static assets",
                "implementation": "Use WebP format, implement lazy loading for images",
                "expected_impact": "15-25% total size reduction"
            },
            {
                "category": "Build Configuration",
                "priority": "HIGH",
                "recommendation": "Optimize Vite build configuration",
                "implementation": "Add manual chunks, enable compression, optimize CSS",
                "expected_impact": "20-30% bundle size reduction"
            }
        ]
        
        self.results["recommendations"] = recommendations
    
    def create_optimization_implementation(self):
        """Create implementation scripts for optimizations"""
        print("🛠️ Creating optimization implementation...")
        
        # Create optimized Vite config
        optimized_vite_config = '''import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { resolve } from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': resolve(__dirname, './src'),
    },
  },
  build: {
    target: 'es2015',
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true,
        drop_debugger: true,
      },
    },
    rollupOptions: {
      output: {
        manualChunks: {
          // Vendor chunks
          'react-vendor': ['react', 'react-dom'],
          'ui-vendor': ['lucide-react'],
          // Feature chunks
          'game-components': [
            './src/components/game/EquipmentManager.jsx',
            './src/components/game/CharacterPortrait.jsx',
            './src/components/game/GamePanel.jsx'
          ],
          'ui-components': [
            './src/components/ui/card.jsx',
            './src/components/ui/button.jsx',
            './src/components/ui/tabs.jsx'
          ]
        },
        chunkFileNames: 'assets/[name]-[hash].js',
        entryFileNames: 'assets/[name]-[hash].js',
        assetFileNames: 'assets/[name]-[hash].[ext]'
      }
    },
    chunkSizeWarningLimit: 500,
    reportCompressedSize: true,
    sourcemap: false
  },
  server: {
    port: 5173,
    host: true
  }
})'''
        
        # Save optimized config
        config_path = os.path.join(self.project_path, "vite.config.optimized.js")
        with open(config_path, 'w') as f:
            f.write(optimized_vite_config)
        
        self.results["optimization_files"] = {
            "vite_config": config_path
        }
    
    def run_comprehensive_analysis(self):
        """Run complete bundle optimization analysis"""
        print("🚀 Starting comprehensive bundle optimization analysis...")
        
        self.analyze_project_structure()
        self.check_build_configuration()
        self.analyze_current_bundle()
        self.identify_optimization_opportunities()
        self.generate_recommendations()
        self.create_optimization_implementation()
        
        return self.results
    
    def print_summary(self):
        """Print analysis summary"""
        print(f"\\n📊 Bundle Optimization Analysis Summary")
        print(f"=" * 60)
        
        # Current bundle info
        if self.results["analysis"].get("current_bundle", {}).get("exists"):
            current_size = self.results["analysis"]["current_bundle"]["total_size_kb"]
            print(f"Current Bundle Size: {current_size}KB")
            print(f"Target Size: <500KB")
            print(f"Reduction Needed: {max(0, current_size - 500):.1f}KB")
        else:
            print("Current Bundle: Not built yet")
        
        # Source analysis
        if "source_files" in self.results["analysis"]:
            source_size = self.results["analysis"]["source_files"]["total_size_kb"]
            print(f"Source Code Size: {source_size}KB")
        
        # Dependencies
        if "dependencies" in self.results["analysis"]:
            deps = self.results["analysis"]["dependencies"]
            print(f"Production Dependencies: {deps['total_prod_deps']}")
            print(f"Development Dependencies: {deps['total_dev_deps']}")
        
        # Optimizations
        print(f"\\n🎯 Optimization Opportunities: {len(self.results['optimizations'])}")
        for opt in self.results["optimizations"][:3]:
            print(f"  • {opt['description']} ({opt['priority']} priority)")
        
        # Recommendations
        print(f"\\n💡 Top Recommendations:")
        for rec in self.results["recommendations"][:3]:
            print(f"  • {rec['category']}: {rec['expected_impact']}")
    
    def save_results(self, filename="bundle_optimization_analysis.json"):
        """Save analysis results"""
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"✅ Analysis results saved to {filename}")

def main():
    analyzer = BundleOptimizationAnalyzer()
    results = analyzer.run_comprehensive_analysis()
    analyzer.print_summary()
    analyzer.save_results()
    return results

if __name__ == "__main__":
    main()


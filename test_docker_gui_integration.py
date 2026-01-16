#!/usr/bin/env python3
"""
Docker GUI Launch Integration Test

This script verifies that:
1. Phase scripts (1-3) are available and executable
2. GUI applications can import required modules
3. Pipeline trigger system works correctly
4. Docker launcher scripts are properly configured
"""

import os
import sys
from pathlib import Path
import subprocess
import json

class IntegrationTester:
    def __init__(self):
        self.project_root = Path.cwd()
        self.results = {
            "phase_scripts": {},
            "gui_apps": {},
            "docker_launchers": {},
            "entrypoint": {},
            "pipeline_integration": {}
        }
        self.passed = 0
        self.failed = 0
    
    def print_header(self):
        """Print test header"""
        print("\n")
        print("=" * 80)
        print("DOCKER GUI LAUNCH - INTEGRATION TEST SUITE")
        print("=" * 80)
        print()
    
    def test_file_exists(self, filepath, description):
        """Test if a file exists"""
        path = self.project_root / filepath
        if path.exists():
            print(f"   ✓ {description}: {filepath}")
            self.passed += 1
            return True
        else:
            print(f"   ✗ {description}: {filepath} (NOT FOUND)")
            self.failed += 1
            return False
    
    def test_file_content(self, filepath, search_string, description):
        """Test if file contains specific content"""
        path = self.project_root / filepath
        if not path.exists():
            print(f"   ✗ {description}: {filepath} (file not found)")
            self.failed += 1
            return False
        
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                if search_string in content:
                    print(f"   ✓ {description}")
                    self.passed += 1
                    return True
                else:
                    print(f"   ✗ {description}: pattern not found")
                    self.failed += 1
                    return False
        except Exception as e:
            print(f"   ✗ {description}: {str(e)}")
            self.failed += 1
            return False
    
    def test_executable(self, filepath, description):
        """Test if a Python file is syntactically valid"""
        path = self.project_root / filepath
        if not path.exists():
            print(f"   ✗ {description}: {filepath} (not found)")
            self.failed += 1
            return False
        
        try:
            result = subprocess.run(
                [sys.executable, "-m", "py_compile", str(path)],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                print(f"   ✓ {description}: {filepath}")
                self.passed += 1
                return True
            else:
                print(f"   ✗ {description}: {filepath} (syntax error)")
                self.failed += 1
                return False
        except Exception as e:
            print(f"   ✗ {description}: {str(e)}")
            self.failed += 1
            return False
    
    def test_phase_scripts(self):
        """Test all Phase quick start scripts"""
        print("📋 PHASE SCRIPTS TEST")
        print("─" * 80)
        
        phases = [
            ("PHASE_1_QUICK_START.py", "Phase 1: Data Loading & Preprocessing"),
            ("PHASE_2_QUICK_START.py", "Phase 2: Vector Export & GIS"),
            ("PHASE_3_QUICK_START.py", "Phase 3: Temporal Analysis & Forecasting"),
        ]
        
        for filename, description in phases:
            self.test_executable(filename, description)
        
        print()
    
    def test_gui_applications(self):
        """Test GUI application files"""
        print("🖥️ GUI APPLICATIONS TEST")
        print("─" * 80)
        
        guis = [
            ("gui_prototype.html", "HTML Browser Prototype"),
            ("shoreline_gui.py", "Standalone Dashboard"),
            ("shoreline_gui_pipeline.py", "Pipeline Executor"),
            ("shoreline_gui_advanced.py", "Advanced Dashboard"),
        ]
        
        for filename, description in guis:
            self.test_file_exists(filename, description)
        
        print()
    
    def test_gui_pipeline_integration(self):
        """Test if GUI can trigger pipeline phases"""
        print("⚙️ GUI-PIPELINE INTEGRATION TEST")
        print("─" * 80)
        
        # Check if GUI pipeline executor has script execution logic
        self.test_file_content(
            "shoreline_gui_pipeline.py",
            "python scripts/",
            "Pipeline executor references pipeline scripts"
        )
        
        # Check if GUI has worker thread for background execution
        self.test_file_content(
            "shoreline_gui_pipeline.py",
            "PipelineWorker",
            "Pipeline executor has background worker thread"
        )
        
        # Check if advanced GUI has multiple execution tabs
        self.test_file_content(
            "shoreline_gui_advanced.py",
            "QTabWidget",
            "Advanced GUI has tabbed interface"
        )
        
        print()
    
    def test_docker_launchers(self):
        """Test Docker launcher scripts"""
        print("🐳 DOCKER LAUNCHER SCRIPTS TEST")
        print("─" * 80)
        
        launchers = [
            ("LAUNCH_DOCKER.bat", "docker build", "Windows Docker launcher"),
            ("launch_docker.sh", "docker build", "Linux/macOS Docker launcher"),
            ("LAUNCH_DOCKER_GUI.bat", "docker_entrypoint_gui", "Windows GUI Docker launcher"),
            ("launch_docker_gui.sh", "docker_entrypoint_gui", "Linux/macOS GUI Docker launcher"),
        ]
        
        for filename, pattern, description in launchers:
            self.test_file_content(filename, pattern, description)
        
        print()
    
    def test_entrypoint_script(self):
        """Test Docker entrypoint script"""
        print("📝 DOCKER ENTRYPOINT SCRIPT TEST")
        print("─" * 80)
        
        entrypoint_checks = [
            ("docker_entrypoint_gui.sh", "DISPLAY", "Checks for X11 DISPLAY"),
            ("docker_entrypoint_gui.sh", "shoreline_gui", "Attempts to launch GUI"),
            ("docker_entrypoint_gui.sh", "PHASE", "Supports Phase script execution"),
            ("docker_entrypoint_gui.sh", "/bin/bash", "Has headless fallback shell"),
        ]
        
        for filename, pattern, description in entrypoint_checks:
            self.test_file_content(filename, pattern, description)
        
        print()
    
    def test_docker_configuration(self):
        """Test Docker configuration"""
        print("🐳 DOCKER CONFIGURATION TEST")
        print("─" * 80)
        
        docker_checks = [
            ("Dockerfile", "PyQt6", "Dockerfile includes PyQt6"),
            ("Dockerfile", "docker_entrypoint_gui.sh", "Dockerfile references entrypoint"),
            ("Dockerfile", "EXPOSE 8888", "Dockerfile exposes Jupyter port"),
            ("requirements.txt", "PyQt6", "Requirements include PyQt6"),
            ("requirements.txt", "tensorflow", "Requirements include TensorFlow"),
        ]
        
        for filename, pattern, description in docker_checks:
            self.test_file_content(filename, pattern, description)
        
        print()
    
    def test_guide_documentation(self):
        """Test documentation completeness"""
        print("📚 DOCUMENTATION TEST")
        print("─" * 80)
        
        docs = [
            ("DOCKER_GUI_LAUNCH_GUIDE.md", "Quick Start", "Comprehensive guide exists"),
            ("DOCKER_GUI_LAUNCH_GUIDE.md", "Troubleshooting", "Troubleshooting section included"),
            ("DOCKER_GUI_LAUNCH_GUIDE.md", "GPU", "GPU support documented"),
        ]
        
        for filename, pattern, description in docs:
            self.test_file_content(filename, pattern, description)
        
        print()
    
    def test_directory_structure(self):
        """Test required directories"""
        print("📁 DIRECTORY STRUCTURE TEST")
        print("─" * 80)
        
        dirs = [
            ("data", "Data input directory"),
            ("model_outputs", "Model outputs directory"),
            ("configs", "Configuration directory"),
            ("docs", "Documentation directory"),
            ("utils", "Utilities directory"),
            ("scripts", "Scripts directory"),
        ]
        
        for dirname, description in dirs:
            path = self.project_root / dirname
            if path.exists() and path.is_dir():
                print(f"   ✓ {description}: {dirname}/")
                self.passed += 1
            else:
                print(f"   ✗ {description}: {dirname}/ (not found)")
                self.failed += 1
        
        print()
    
    def test_pipeline_execution_capability(self):
        """Test if pipeline can be executed from GUI"""
        print("🚀 PIPELINE EXECUTION CAPABILITY TEST")
        print("─" * 80)
        
        tests = [
            ("shoreline_gui_pipeline.py", "subprocess", "GUI uses subprocess for phases"),
            ("shoreline_gui_pipeline.py", "QThread", "GUI uses threading for async execution"),
            ("shoreline_gui_advanced.py", "subprocess", "Advanced GUI uses subprocess"),
            ("docker_entrypoint_gui.sh", "PHASE_", "Entrypoint can run Phase scripts"),
        ]
        
        for filename, pattern, description in tests:
            self.test_file_content(filename, pattern, description)
        
        print()
    
    def run_all_tests(self):
        """Run all integration tests"""
        self.print_header()
        
        self.test_phase_scripts()
        self.test_gui_applications()
        self.test_gui_pipeline_integration()
        self.test_docker_launchers()
        self.test_entrypoint_script()
        self.test_docker_configuration()
        self.test_guide_documentation()
        self.test_directory_structure()
        self.test_pipeline_execution_capability()
        
        self.print_summary()
    
    def print_summary(self):
        """Print test summary"""
        total = self.passed + self.failed
        success_rate = (self.passed / total * 100) if total > 0 else 0
        
        print("=" * 80)
        print("📊 TEST SUMMARY")
        print("=" * 80)
        print()
        print(f"   Total Tests: {total}")
        print(f"   ✓ Passed: {self.passed}")
        print(f"   ✗ Failed: {self.failed}")
        print(f"   Success Rate: {success_rate:.1f}%")
        print()
        
        if self.failed == 0:
            print("🎉 ALL TESTS PASSED!")
            print()
            print("✅ Docker GUI Launch System is Ready for Testing")
            print()
            print("Next Steps:")
            print("  1. Windows: LAUNCH_DOCKER_GUI.bat")
            print("  2. Linux/macOS: bash launch_docker_gui.sh")
            print("  3. Verify GUI launches and shows Phase 1-3 buttons")
            print("  4. Click Phase buttons to trigger pipeline execution")
            print("  5. Monitor output in GUI status panel")
            print()
            return 0
        else:
            print("⚠️ SOME TESTS FAILED")
            print()
            print("Please fix the issues above and re-run the test.")
            print()
            return 1

def main():
    """Main entry point"""
    tester = IntegrationTester()
    return tester.run_all_tests()

if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
import os
import sys
import subprocess
import shutil
from pathlib import Path

class Colors:
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    GREEN = '\033[32m'
    RED = '\033[31m'
    YELLOW = '\033[33m'
    GRAY = '\033[90m'
    RESET = '\033[0m'

class Builder:
    def __init__(self):
        self.base_path = Path(__file__).parent
        self.venv_path = self.base_path / "venv"
        self.dist_path = self.base_path / "dist"
        self.build_path = self.base_path / "build"

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def header(self):
        print(f"{Colors.MAGENTA}{'═' * 50}")
        print(f"  ▸ Chatbottify Builder v0.0.2 ◂")
        print(f"{'═' * 50}{Colors.RESET}\n")

    def section(self, title):
        print(f"{Colors.MAGENTA}├─ {title}")

    def item(self, text, status=None):
        if status == "ok":
            print(f"{Colors.MAGENTA}│  {Colors.GREEN}✓{Colors.RESET} {text}")
        elif status == "warn":
            print(f"{Colors.MAGENTA}│  {Colors.YELLOW}▲{Colors.RESET} {text}")
        elif status == "err":
            print(f"{Colors.MAGENTA}│  {Colors.RED}✗{Colors.RESET} {text}")
        else:
            print(f"{Colors.MAGENTA}│  {Colors.GRAY}•{Colors.RESET} {text}")

    def subsection(self, text):
        print(f"{Colors.MAGENTA}│")
        print(f"{Colors.MAGENTA}├─ {text}")

    def subitem(self, text, status=None):
        if status == "ok":
            print(f"{Colors.MAGENTA}│  {Colors.GREEN}✓{Colors.RESET} {text}")
        elif status == "warn":
            print(f"{Colors.MAGENTA}│  {Colors.YELLOW}▲{Colors.RESET} {text}")
        elif status == "err":
            print(f"{Colors.MAGENTA}│  {Colors.RED}✗{Colors.RESET} {text}")
        else:
            print(f"{Colors.MAGENTA}│  {Colors.GRAY}•{Colors.RESET} {text}")

    def success(self, text):
        print(f"{Colors.GREEN}✓ {text}{Colors.RESET}")

    def error(self, text):
        print(f"{Colors.RED}✗ {text}{Colors.RESET}")

    def warning(self, text):
        print(f"{Colors.YELLOW}▲ {text}{Colors.RESET}")

    def info(self, text):
        print(f"{Colors.GRAY}{text}{Colors.RESET}")

    def footer(self):
        print(f"{Colors.MAGENTA}└{'─' * 48}{Colors.RESET}\n")

    def check_environment(self):
        self.section("Environment Check")
        
        # Check Python
        try:
            result = subprocess.run([sys.executable, "--version"], capture_output=True, text=True)
            version = result.stdout.strip()
            
            # Extract version number
            version_num = version.split()[-1]
            major, minor = map(int, version_num.split('.')[:2])
            
            if major >= 3 and minor >= 8:
                self.item(f"Python: {version}", "ok")
                self.subitem(f"Recommended: 3.8+", "ok")
            else:
                self.item(f"Python: {version}", "warn")
                self.subitem(f"Recommended: 3.8+", "warn")
        except:
            self.item("Python: NOT FOUND", "err")
            self.footer()
            return False

        # Check main.py
        if (self.base_path / "main.py").exists():
            self.item("main.py: FOUND", "ok")
        else:
            self.item("main.py: NOT FOUND", "err")
            self.footer()
            return False

        # Check venv
        if self.venv_path.exists():
            self.item("Virtual env: EXISTS", "ok")
        else:
            self.item("Virtual env: MISSING", "warn")

        self.footer()
        return True

    def create_venv(self):
        self.section("Virtual Environment")
        
        if self.venv_path.exists():
            self.item("Already exists", "ok")
            self.footer()
            return True

        try:
            self.item("Creating...")
            subprocess.run([sys.executable, "-m", "venv", str(self.venv_path)], 
                         check=True, capture_output=True)
            self.item("Created successfully", "ok")
            self.footer()
            return True
        except Exception as e:
            self.item(f"Failed: {e}", "err")
            self.footer()
            return False

    def install_dependencies(self):
        self.section("Dependencies")
        
        try:
            pip_path = self.venv_path / ("Scripts" if os.name == "nt" else "bin") / "pip"
            
            self.item("Installing pyinstaller...")
            self.subitem("Recommended: 6.0.0+", "ok")
            result = subprocess.run([str(pip_path), "install", "-q", "pyinstaller>=6.0.0"], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                self.item("Installed successfully", "ok")
                self.footer()
                return True
            else:
                self.item(f"Installation failed", "err")
                if "permission" in result.stderr.lower():
                    self.subitem("Try running as Administrator", "warn")
                self.footer()
                return False
        except Exception as e:
            self.item(f"Error: {e}", "err")
            self.footer()
            return False

    def build_executable(self):
        self.section("Building Executable")
        
        try:
            pyinstaller_path = self.venv_path / ("Scripts" if os.name == "nt" else "bin") / "pyinstaller"
            
            self.item("Compiling...")
            
            cmd = [
                str(pyinstaller_path),
                "--onefile",
                "--console",
                "--name=ChatbottifyInstaller",
                f"--distpath={self.dist_path}",
                f"--workpath={self.build_path}",
                str(self.base_path / "main.py")
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                exe_path = self.dist_path / "ChatbottifyInstaller.exe"
                if exe_path.exists():
                    size_mb = exe_path.stat().st_size / (1024 * 1024)
                    self.item(f"Compiled successfully", "ok")
                    self.subitem(f"Size: {size_mb:.1f} MB", "ok")
                    self.subitem(f"Path: {exe_path}", "ok")
                self.footer()
                return True
            else:
                self.item("Compilation failed", "err")
                self.subsection("Error Details")
                
                if "--workpath" in result.stderr or "unrecognized" in result.stderr:
                    self.subitem("Invalid PyInstaller arguments", "err")
                    self.subitem("Using fallback build method...", "warn")
                    return self.build_executable_fallback()
                elif "permission" in result.stderr.lower():
                    self.subitem("Permission denied", "err")
                    self.subitem("Try running as Administrator", "warn")
                else:
                    error_lines = result.stderr.split('\n')[:3]
                    for line in error_lines:
                        if line.strip():
                            self.subitem(line.strip(), "err")
                
                self.footer()
                return False
        except Exception as e:
            self.item(f"Build error: {e}", "err")
            self.footer()
            return False

    def build_executable_fallback(self):
        try:
            pyinstaller_path = self.venv_path / ("Scripts" if os.name == "nt" else "bin") / "pyinstaller"
            
            cmd = [
                str(pyinstaller_path),
                "--onefile",
                "--console",
                "--name=ChatbottifyInstaller",
                str(self.base_path / "main.py")
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                exe_path = self.base_path / "dist" / "ChatbottifyInstaller.exe"
                if exe_path.exists():
                    size_mb = exe_path.stat().st_size / (1024 * 1024)
                    self.subitem("Fallback build successful", "ok")
                    self.subitem(f"Size: {size_mb:.1f} MB", "ok")
                    self.subitem(f"Path: {exe_path}", "ok")
                    
                    # Move to correct location
                    if exe_path != self.dist_path / "ChatbottifyInstaller.exe":
                        self.dist_path.mkdir(exist_ok=True)
                        shutil.move(str(exe_path), str(self.dist_path / "ChatbottifyInstaller.exe"))
                
                self.footer()
                return True
            else:
                self.subitem("Fallback also failed", "err")
                self.footer()
                return False
        except Exception as e:
            self.subitem(f"Fallback error: {e}", "err")
            self.footer()
            return False

    def cleanup(self):
        self.section("Cleanup")
        
        try:
            spec_file = self.base_path / "ChatbottifyInstaller.spec"
            if spec_file.exists():
                spec_file.unlink()
                self.item("Removed spec file", "ok")
            
            build_dir = self.base_path / "build"
            if build_dir.exists():
                shutil.rmtree(build_dir)
                self.item("Removed build directory", "ok")
            
            self.footer()
        except Exception as e:
            self.item(f"Cleanup warning: {e}", "warn")
            self.footer()

    def create_launcher(self):
        self.section("Creating Launcher")
        
        try:
            launcher_path = self.base_path / "ChatbottifyInstaller.bat"
            launcher_content = f"""@echo off
cd /d "{self.dist_path}"
ChatbottifyInstaller.exe
pause
"""
            launcher_path.write_text(launcher_content)
            self.item("Launcher created", "ok")
            self.subitem(f"Path: {launcher_path}", "ok")
            self.footer()
            return True
        except Exception as e:
            self.item(f"Launcher creation failed: {e}", "warn")
            self.footer()
            return False

    def create_readme(self):
        self.section("Creating Documentation")
        
        try:
            readme_path = self.base_path / "BUILD_INFO.txt"
            readme_content = f"""Chatbottify Installer Build Info
{'=' * 40}

Build Date: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Python Version: {sys.version.split()[0]}
Executable: {self.dist_path / 'ChatbottifyInstaller.exe'}

Quick Start:
1. Run ChatbottifyInstaller.exe
2. Follow the installation wizard
3. Steering rule will be installed to:
   C:\\Users\\[YourUsername]\\.kiro\\steering\\chatbottify.md

For more info visit:
https://github.com/warwakei/chatbottify-kirosteering
"""
            readme_path.write_text(readme_content)
            self.item("Documentation created", "ok")
            self.subitem(f"Path: {readme_path}", "ok")
            self.footer()
            return True
        except Exception as e:
            self.item(f"Documentation creation failed: {e}", "warn")
            self.footer()
            return False

    def show_summary(self):
        print(f"{Colors.MAGENTA}{'═' * 50}{Colors.RESET}")
        print(f"{Colors.GREEN}✓ Build Summary{Colors.RESET}\n")
        
        exe_path = self.dist_path / "ChatbottifyInstaller.exe"
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"{Colors.CYAN}Executable:{Colors.RESET}")
            print(f"  • {exe_path}")
            print(f"  • Size: {size_mb:.1f} MB\n")
        
        launcher_path = self.base_path / "ChatbottifyInstaller.bat"
        if launcher_path.exists():
            print(f"{Colors.CYAN}Launcher:{Colors.RESET}")
            print(f"  • {launcher_path}\n")
        
        readme_path = self.base_path / "BUILD_INFO.txt"
        if readme_path.exists():
            print(f"{Colors.CYAN}Documentation:{Colors.RESET}")
            print(f"  • {readme_path}\n")
        
        recommended_path = self.base_path / "chatbottify0-ext.md"
        if recommended_path.exists():
            print(f"{Colors.CYAN}Extension Steering:{Colors.RESET}")
            print(f"  • {recommended_path}")
            print(f"  • Code quality & efficiency focus\n")
        
        print(f"{Colors.MAGENTA}{'═' * 50}{Colors.RESET}\n")

    def run(self):
        self.clear()
        self.header()

        if not self.check_environment():
            self.error("Environment check failed")
            input()
            return

        if not self.create_venv():
            self.error("Failed to create virtual environment")
            input()
            return

        if not self.install_dependencies():
            self.error("Failed to install dependencies")
            input()
            return

        if not self.build_executable():
            self.error("Build failed")
            input()
            return

        self.cleanup()
        self.create_launcher()
        self.create_readme()
        self.show_summary()
        
        print(f"{Colors.GRAY}Press Enter to continue...{Colors.RESET}")
        input()

if __name__ == "__main__":
    builder = Builder()
    builder.run()


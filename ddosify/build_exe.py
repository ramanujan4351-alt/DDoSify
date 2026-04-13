#!/usr/bin/env python3
"""
Build DDoSify GUI Executable
Creates standalone Windows executable
"""

import os
import sys
import subprocess
import shutil

def build_executable():
    """Build the executable using PyInstaller"""
    print("Building DDoSify GUI executable...")
    
    # Install requirements first
    print("Installing requirements...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
    
    # Build executable
    print("Building executable with PyInstaller...")
    cmd = [
        "pyinstaller",
        "--onefile",                    # Create single EXE file
        "--windowed",                   # No console window
        "--name=DDoSify",              # Name of executable
        "--add-data=README.md;.",      # Include README
        "--clean",                     # Clean previous builds
        "ddosify_gui.py"              # Main script
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("\n" + "="*50)
        print("Build successful!")
        print("Executable location: dist/DDoSify.exe")
        print("\nUsage:")
        print("1. Run as Administrator")
        print("2. Configure target and attack parameters")
        print("3. Start attack with monitoring")
        print("\nWARNING: For educational purposes only!")
        print("="*50)
        
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}")
        return False
    
    return True

def create_portable_package():
    """Create a portable package with all files"""
    print("Creating portable package...")
    
    # Create package directory
    package_dir = "DDoSify_Portable"
    if os.path.exists(package_dir):
        shutil.rmtree(package_dir)
    os.makedirs(package_dir)
    
    # Copy files
    files_to_copy = [
        "ddosify.py",
        "ddosify_gui.py", 
        "requirements.txt",
        "README.md",
        "build_exe.py"
    ]
    
    for file in files_to_copy:
        if os.path.exists(file):
            shutil.copy(file, package_dir)
    
    # Create run scripts
    with open(f"{package_dir}/run_gui.bat", "w") as f:
        f.write("@echo off\n")
        f.write("echo Starting DDoSify GUI...\n")
        f.write("python ddosify_gui.py\n")
        f.write("pause\n")
    
    with open(f"{package_dir}/run_cli.bat", "w") as f:
        f.write("@echo off\n")
        f.write("echo DDoSify CLI - Usage:\n")
        f.write("echo python ddosify.py -m http -t 192.168.1.100 -p 80 --threads 100 --duration 30\n")
        f.write("pause\n")
    
    print(f"Portable package created: {package_dir}/")
    return True

if __name__ == "__main__":
    print("DDoSify Build Tool")
    print("="*30)
    
    choice = input("Build option:\n1. GUI Executable\n2. Portable Package\n3. Both\nChoice (1-3): ")
    
    if choice in ["1", "3"]:
        build_executable()
    
    if choice in ["2", "3"]:
        create_portable_package()
    
    print("\nBuild complete!")

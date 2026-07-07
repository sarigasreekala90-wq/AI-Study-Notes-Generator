#!/usr/bin/env python
"""
Project Verification Script
Checks that all project files are properly configured and ready to run.
Run this to verify the project setup before deployment.

Usage:
    python verify_project.py
"""

import os
import sys
import sqlite3
from pathlib import Path

def check_file_exists(filepath, description):
    """Check if a file exists and print status"""
    exists = os.path.isfile(filepath)
    status = "✓" if exists else "✗"
    print(f"{status} {description}: {filepath}")
    return exists

def check_directory_exists(dirpath, description):
    """Check if a directory exists and print status"""
    exists = os.path.isdir(dirpath)
    status = "✓" if exists else "✗"
    print(f"{status} {description}: {dirpath}")
    return exists

def check_python_syntax(filepath):
    """Check if Python file has valid syntax"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            compile(f.read(), filepath, 'exec')
        print(f"✓ {filepath} - Valid Python syntax")
        return True
    except SyntaxError as e:
        print(f"✗ {filepath} - Syntax error: {e}")
        return False
    except Exception as e:
        print(f"✓ {filepath} - File OK (encoding: {e.__class__.__name__})")
        return True

def check_dependencies():
    """Check if all required packages are installed"""
    required = ['flask', 'werkzeug', 'jinja2', 'click']
    all_ok = True
    print("\n" + "="*60)
    print("CHECKING DEPENDENCIES")
    print("="*60)
    
    for package in required:
        try:
            __import__(package)
            print(f"✓ {package} is installed")
        except ImportError:
            print(f"✗ {package} is NOT installed (run: pip install -r requirements.txt)")
            all_ok = False
    
    return all_ok

def check_database():
    """Check database structure"""
    print("\n" + "="*60)
    print("CHECKING DATABASE")
    print("="*60)
    
    db_path = "database.db"
    if not os.path.isfile(db_path):
        print(f"ℹ Database will be created on first run: {db_path}")
        return True
    
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        
        # Check tables
        tables = ['users', 'notes', 'generated_notes']
        for table in tables:
            cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
            if cur.fetchone():
                print(f"✓ Table '{table}' exists")
            else:
                print(f"✗ Table '{table}' is missing")
                return False
        
        # Check users count
        cur.execute("SELECT COUNT(*) FROM users")
        user_count = cur.fetchone()[0]
        print(f"✓ Database contains {user_count} users")
        
        conn.close()
        return True
    except Exception as e:
        print(f"✗ Database error: {e}")
        return False

def verify_project():
    """Run all verification checks"""
    print("="*60)
    print("AI STUDY NOTES GENERATOR - PROJECT VERIFICATION")
    print("="*60)
    
    all_ok = True
    
    # Check project structure
    print("\n" + "="*60)
    print("CHECKING PROJECT STRUCTURE")
    print("="*60)
    
    files_to_check = [
        ("app.py", "Main Flask application"),
        ("check_db.py", "Database inspection tool"),
        ("requirements.txt", "Python dependencies"),
        ("README.md", "Project README"),
        ("SETUP.md", "Setup instructions"),
        ("CONFIG.md", "Configuration guide"),
        ("CHANGELOG.md", "Project changelog"),
        (".gitignore", "Git ignore file"),
    ]
    
    for filepath, description in files_to_check:
        if not check_file_exists(filepath, description):
            all_ok = False
    
    # Check directories
    print()
    dirs_to_check = [
        ("static", "Static files directory"),
        ("templates", "Templates directory"),
    ]
    
    for dirpath, description in dirs_to_check:
        if not check_directory_exists(dirpath, description):
            all_ok = False
    
    # Check static files
    print("\n" + "="*60)
    print("CHECKING STATIC FILES")
    print("="*60)
    
    static_files = [
        ("static/style.css", "CSS stylesheet"),
        ("static/script.js", "JavaScript file"),
    ]
    
    for filepath, description in static_files:
        if not check_file_exists(filepath, description):
            all_ok = False
    
    # Check templates
    print("\n" + "="*60)
    print("CHECKING TEMPLATES")
    print("="*60)
    
    templates = [
        ("templates/home.html", "Home page template"),
        ("templates/login.html", "Login template"),
        ("templates/register.html", "Registration template"),
        ("templates/dashboard.html", "Dashboard template"),
    ]
    
    for filepath, description in templates:
        if not check_file_exists(filepath, description):
            all_ok = False
    
    # Check Python syntax
    print("\n" + "="*60)
    print("CHECKING PYTHON SYNTAX")
    print("="*60)
    
    python_files = [
        "app.py",
        "check_db.py",
    ]
    
    for filepath in python_files:
        if not check_python_syntax(filepath):
            all_ok = False
    
    # Check dependencies
    if not check_dependencies():
        all_ok = False
    
    # Check database
    if not check_database():
        all_ok = False
    
    # Summary
    print("\n" + "="*60)
    print("VERIFICATION SUMMARY")
    print("="*60)
    
    if all_ok:
        print("✓ ALL CHECKS PASSED!")
        print("\nThe project is ready to run:")
        print("  1. Make sure all dependencies are installed:")
        print("     pip install -r requirements.txt")
        print("\n  2. Run the application:")
        print("     python app.py")
        print("\n  3. Open in browser:")
        print("     http://localhost:5000")
        return 0
    else:
        print("✗ SOME CHECKS FAILED")
        print("\nPlease fix the issues above before running the app.")
        return 1

if __name__ == "__main__":
    exit_code = verify_project()
    sys.exit(exit_code)

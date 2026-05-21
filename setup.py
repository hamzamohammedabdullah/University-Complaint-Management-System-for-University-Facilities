#!/usr/bin/env python3
"""
UniCMS Quick Setup Script
Run this once after extracting the project:
  python setup.py
"""
import os, sys, subprocess

def run(cmd, **kwargs):
    print(f"\n>>> {cmd}")
    result = subprocess.run(cmd, shell=True, **kwargs)
    if result.returncode != 0:
        print(f"ERROR running: {cmd}")
        sys.exit(1)

print("\n" + "="*50)
print("  UniCMS — Django Setup")
print("="*50)

# Install dependencies
run(f"{sys.executable} -m pip install -r requirements.txt")

# Run migrations
run(f"{sys.executable} manage.py makemigrations")
run(f"{sys.executable} manage.py migrate")

# Create superuser
print("\n" + "="*50)
print("  Create Admin Account")
print("="*50)
run(f"{sys.executable} manage.py createsuperuser", stdin=sys.stdin)

print("\n" + "="*50)
print("  Setup Complete!")
print("  Run:  python manage.py runserver")
print("  Open: http://127.0.0.1:8000")
print("="*50 + "\n")

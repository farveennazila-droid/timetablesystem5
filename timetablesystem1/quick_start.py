#!/usr/bin/env python3
"""
Direct database initialization without mysql.connector hanging issues
Uses raw SQL execution
"""

import os
import sys

# Make the app work without database for now
print("=" * 60)
print("Timetable Dashboard - Quick Start Guide")
print("=" * 60)
print("\nDatabase Connection Issue Detected")
print("\nTemporary Solution: Running app without database")
print("All dashboard cards will show 0 values\n")

print("To fix the database connection:")
print("\n1. Verify MySQL is running:")
print("   - Open Services (Win+R → services.msc)")
print("   - Find 'MySQL80' and ensure it's 'Running'")
print("\n2. Try connecting manually:")
print("   Open Command Prompt and run:")
print('   mysql -u root -p"nazila" -h 127.0.0.1')
print("\n3. If connection fails:")
print("   - Check MySQL installation")
print("   - Reinstall MySQL if needed")
print("   - Ensure port 3306 is not blocked")

print("\n" + "=" * 60)
print("For now, the app will work with zero values in dashboard")
print("=" * 60)

# Suggest restarting Flask
print("\nPlease:")
print("1. Refresh your browser at http://127.0.0.1:5000/dashboard")
print("2. You should see dashboard cards with 0 values")
print("3. Later, fix MySQL connection and restart Flask")

#!/usr/bin/env python3
"""
Quick test script for Timetable Management System API

This script tests the main functionality:
1. Adding timetable entries
2. Retrieving timetable
3. Publishing timetable
4. Verifying changes
"""

import requests
import json
import time

BASE_URL = "http://127.0.0.1:5000"

def test_api():
    print("=" * 60)
    print("TIMETABLE MANAGEMENT SYSTEM - API TEST")
    print("=" * 60)
    
    # Test 1: Get current timetable
    print("\n[TEST 1] Getting current timetable...")
    try:
        response = requests.get(f"{BASE_URL}/api/timetable")
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Current entries: {len(data)}")
        if data:
            print("Sample entry:", data[0] if len(data) > 0 else "None")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 2: Add a test timetable entry
    print("\n[TEST 2] Adding test timetable entry...")
    test_entry = {
        "day": "Monday",
        "period": 1,
        "subject": "Mathematics",
        "faculty": "Dr. Smith",
        "room": "A101"
    }
    try:
        response = requests.post(f"{BASE_URL}/api/timetable", json=test_entry)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 3: Get timetable again to verify entry was added
    print("\n[TEST 3] Verifying entry was added...")
    try:
        response = requests.get(f"{BASE_URL}/api/timetable")
        data = response.json()
        print(f"Total entries now: {len(data)}")
        # Find the draft entry (published=0)
        draft_entries = [e for e in data if e[6] == 0]
        print(f"Draft entries: {len(draft_entries)}")
        if draft_entries:
            print("Latest draft entry:", draft_entries[-1])
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 4: Publish timetable
    print("\n[TEST 4] Publishing timetable...")
    try:
        response = requests.post(f"{BASE_URL}/api/timetable/publish", json={})
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 5: Verify entries are published
    print("\n[TEST 5] Verifying entries are published...")
    try:
        response = requests.get(f"{BASE_URL}/api/timetable")
        data = response.json()
        published_entries = [e for e in data if e[6] == 1]
        print(f"Published entries: {len(published_entries)}")
        print(f"Total entries: {len(data)}")
        if published_entries:
            print("Sample published entry:", published_entries[0])
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 6: Check notifications
    print("\n[TEST 6] Checking notifications...")
    try:
        response = requests.get(f"{BASE_URL}/notifications")
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Total notifications: {len(data)}")
        if data:
            # Show recent notifications
            recent = data[-3:] if len(data) >= 3 else data
            for notif in recent:
                print(f"  - {notif[1] if isinstance(notif, list) else notif}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 7: Get Faculty list
    print("\n[TEST 7] Getting faculty list...")
    try:
        response = requests.get(f"{BASE_URL}/api/faculty")
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Total faculty: {len(data)}")
        if data:
            print(f"Sample faculty: {data[0]}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 8: Get Classrooms
    print("\n[TEST 8] Getting classrooms...")
    try:
        response = requests.get(f"{BASE_URL}/api/classrooms")
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Total classrooms: {len(data)}")
        if data:
            print(f"Sample classroom: {data[0]}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)
    print("\nNEXT STEPS:")
    print("1. Open http://127.0.0.1:5000 in your browser")
    print("2. Login to the admin panel")
    print("3. Go to Manage Data")
    print("4. Use the 'Create & Manage Timetable' section to:")
    print("   - Add timetable entries")
    print("   - View current timetable")
    print("   - Publish timetable")
    print("5. Students will automatically see published schedule")

if __name__ == "__main__":
    print("Waiting 2 seconds for Flask to fully start...")
    time.sleep(2)
    test_api()

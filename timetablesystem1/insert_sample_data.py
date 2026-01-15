#!/usr/bin/env python3
"""Quick script to insert sample faculty and classroom data"""

import pymysql

try:
    connection = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='nazila',
        database='timetable_db',
        port=3306
    )
    
    cursor = connection.cursor()
    
    print("Inserting sample faculty...")
    faculty_data = [
        ("Dr. John Smith", "Computer Science", "john.smith@university.edu"),
        ("Dr. Jane Doe", "Mathematics", "jane.doe@university.edu"),
        ("Dr. Mike Wilson", "Physics", "mike.wilson@university.edu"),
        ("Prof. Sarah Johnson", "English", "sarah.johnson@university.edu"),
        ("Dr. Robert Brown", "Chemistry", "robert.brown@university.edu"),
    ]
    
    for name, dept, email in faculty_data:
        cursor.execute(
            "INSERT IGNORE INTO faculty (name, department, email) VALUES (%s, %s, %s)",
            (name, dept, email)
        )
        print(f"  ✓ Added: {name}")
    
    print("\nInserting sample classrooms...")
    classroom_data = [
        ("A101", 30, "Building A - Ground Floor"),
        ("A102", 30, "Building A - Ground Floor"),
        ("A201", 25, "Building A - First Floor"),
        ("B201", 40, "Building B - First Floor"),
        ("B202", 40, "Building B - First Floor"),
        ("C301", 50, "Building C - Third Floor"),
        ("C302", 50, "Building C - Third Floor"),
        ("D105", 35, "Building D - Ground Floor"),
    ]
    
    for room, capacity, location in classroom_data:
        cursor.execute(
            "INSERT IGNORE INTO classroom (room_number, capacity, location) VALUES (%s, %s, %s)",
            (room, capacity, location)
        )
        print(f"  ✓ Added: Room {room} ({capacity} seats)")
    
    connection.commit()
    cursor.close()
    connection.close()
    
    print("\n✓ All sample data inserted successfully!")
    print("\nYou can now:")
    print("1. Go to http://127.0.0.1:5000/admin to manage data")
    print("2. Go to http://127.0.0.1:5000/dashboard to see the updated counts")
    
except Exception as e:
    print(f"Error: {e}")

#!/usr/bin/env python3
"""Setup database with proper schema and sample timetable data"""

import pymysql
import sys
import time

try:
    print("Connecting to MySQL server...")
    
    # First connect without database
    connection = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='nazila',
        port=3306,
        connect_timeout=5
    )
    
    cursor = connection.cursor()
    print("[OK] Connected to MySQL server\n")
    
    # Create database
    print("Setting up database schema...")
    try:
        cursor.execute("DROP DATABASE IF EXISTS timetable_db")
        print("  [OK] Cleaned up existing database")
    except Exception as e:
        print(f"  Note: {e}")
    
    cursor.execute("CREATE DATABASE timetable_db")
    print("  [OK] Created database: timetable_db")
    cursor.execute("USE timetable_db")
    
    # Create tables
    cursor.execute("""
    CREATE TABLE faculty (
      id INT AUTO_INCREMENT PRIMARY KEY,
      name VARCHAR(100),
      department VARCHAR(100)
    )
    """)
    print("  [OK] Created faculty table")
    
    cursor.execute("""
    CREATE TABLE classroom (
      room_id INT AUTO_INCREMENT PRIMARY KEY,
      room_name VARCHAR(100),
      capacity INT
    )
    """)
    print("  [OK] Created classroom table")
    
    cursor.execute("""
    CREATE TABLE notification (
      id INT AUTO_INCREMENT PRIMARY KEY,
      message TEXT,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    print("  [OK] Created notification table")
    
    cursor.execute("""
    CREATE TABLE student (
      id INT AUTO_INCREMENT PRIMARY KEY,
      name VARCHAR(100),
      email VARCHAR(100) UNIQUE
    )
    """)
    print("  [OK] Created student table")
    
    cursor.execute("""
    CREATE TABLE enrollment (
      id INT AUTO_INCREMENT PRIMARY KEY,
      student_id INT,
      subject VARCHAR(100),
      FOREIGN KEY(student_id) REFERENCES student(id)
    )
    """)
    print("  [OK] Created enrollment table")
    
    cursor.execute("""
    CREATE TABLE timetable (
      id INT AUTO_INCREMENT PRIMARY KEY,
      day VARCHAR(20),
      period INT,
      subject VARCHAR(100),
      faculty VARCHAR(100),
      room VARCHAR(50),
      published TINYINT(1) NOT NULL DEFAULT 0
    )
    """)
    print("  [OK] Created timetable table")
    
    cursor.execute("""
    CREATE TABLE change_request (
      id INT AUTO_INCREMENT PRIMARY KEY,
      timetable_id INT,
      reason TEXT,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    print("  [OK] Created change_request table")
    
    connection.commit()
    print("\n[OK] All tables created successfully\n")
    
    # Insert sample data
    print("Inserting sample data...")
    
    # Insert faculty
    cursor.execute("INSERT INTO faculty (name, department) VALUES ('Dr Kumar', 'CSE')")
    print("  [OK] Inserted faculty")
    
    # Insert sample classrooms
    sample_classrooms = [
        ('A101', 30),
        ('A102', 30),
        ('A103', 25),
        ('A104', 40),
        ('A105', 40),
    ]
    
    for room_name, capacity in sample_classrooms:
        cursor.execute(
            "INSERT INTO classroom (room_name, capacity) VALUES (%s, %s)",
            (room_name, capacity)
        )
    print(f"  [OK] Inserted {len(sample_classrooms)} classrooms")
    
    # Insert sample student
    cursor.execute("INSERT INTO student (name, email) VALUES ('John Doe', 'john@example.com')")
    student_id = cursor.lastrowid
    print("  [OK] Inserted student")
    
    # Insert sample enrollments
    cursor.execute("INSERT INTO enrollment (student_id, subject) VALUES (%s, 'DBMS')", (student_id,))
    cursor.execute("INSERT INTO enrollment (student_id, subject) VALUES (%s, 'OS')", (student_id,))
    print("  [OK] Inserted enrollments")
    
    # Insert sample timetable with published=1
    sample_timetable = [
        ('Monday', 1, 'DBMS', 'Dr Kumar', 'A101', 1),
        ('Monday', 2, 'OS', 'Dr Kumar', 'A101', 1),
        ('Tuesday', 1, 'AI', 'Dr Kumar', 'A102', 1),
        ('Tuesday', 2, 'Maths', 'Dr Kumar', 'A102', 1),
        ('Wednesday', 1, 'CN', 'Dr Kumar', 'A103', 1),
        ('Wednesday', 2, 'DBMS', 'Dr Kumar', 'A101', 1),
        ('Thursday', 1, 'OS', 'Dr Kumar', 'A104', 1),
        ('Thursday', 2, 'AI', 'Dr Kumar', 'A102', 1),
        ('Friday', 1, 'Maths', 'Dr Kumar', 'A105', 1),
        ('Friday', 2, 'CN', 'Dr Kumar', 'A103', 1),
    ]
    
    for day, period, subject, faculty_name, room, published in sample_timetable:
        cursor.execute(
            "INSERT INTO timetable (day, period, subject, faculty, room, published) VALUES (%s, %s, %s, %s, %s, %s)",
            (day, period, subject, faculty_name, room, published)
        )
    print(f"  [OK] Inserted {len(sample_timetable)} timetable entries (all published)")
    
    # Insert welcome notification
    cursor.execute("INSERT INTO notification (message) VALUES ('Welcome! Your timetable is now available.')")
    print("  [OK] Inserted notification")
    
    connection.commit()
    cursor.close()
    connection.close()
    
    print("\n[OK] Database setup complete!")
    print("\n[OK] Timetable has been PUBLISHED and is visible to all users")
    print("\nAccess the dashboards:")
    print("  - Student Dashboard: http://127.0.0.1:5000/student-dashboard")
    print("  - Faculty Dashboard: http://127.0.0.1:5000/faculty-dashboard")
    print("\nStart the server with: cd backend && python app.py")
    
except pymysql.Error as err:
    if err.args[0] == 2003:
        print(f"\n[ERROR] MySQL Error: Cannot connect to MySQL server on '127.0.0.1'")
        print("  Make sure MySQL is running!")
        print("\n  To start MySQL on Windows:")
        print("    1. Open Services (Win+R -> services.msc)")
        print("    2. Find 'MySQL80' and click 'Start the service'")
    elif err.args[0] == 1049:
        print(f"\n[ERROR] MySQL Error: Unknown database 'timetable_db'")
        print("  The database setup needs to complete first")
    else:
        print(f"\n[ERROR] MySQL Error ({err.args[0]}): {err.args[1]}")
    sys.exit(1)
except Exception as e:
    print(f"\n[ERROR] Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

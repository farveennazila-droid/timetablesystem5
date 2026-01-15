#!/usr/bin/env python3
"""Database setup using PyMySQL - more reliable on Windows"""

import pymysql
import sys

try:
    print("=" * 70)
    print("DATABASE SETUP - Using PyMySQL")
    print("=" * 70)
    print("\nConnecting to MySQL...")
    
    # Connect without database first
    connection = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='nazila',
        port=3306,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    
    print("✓ Connected to MySQL!\n")
    
    cursor = connection.cursor()
    
    # Create database
    print("Creating database...")
    cursor.execute("CREATE DATABASE IF NOT EXISTS timetable_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    print("✓ Database created\n")
    
    # Select database
    cursor.execute("USE timetable_db")
    
    # Define all tables
    print("Creating tables...")
    
    tables = {
        'admin': """
            CREATE TABLE IF NOT EXISTS admin (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(100) NOT NULL,
                email VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """,
        'faculty': """
            CREATE TABLE IF NOT EXISTS faculty (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                department VARCHAR(100),
                email VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """,
        'subject': """
            CREATE TABLE IF NOT EXISTS subject (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                code VARCHAR(50),
                department VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """,
        'classroom': """
            CREATE TABLE IF NOT EXISTS classroom (
                id INT AUTO_INCREMENT PRIMARY KEY,
                room_number VARCHAR(50) NOT NULL,
                capacity INT,
                location VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """,
        'timetable': """
            CREATE TABLE IF NOT EXISTS timetable (
                id INT AUTO_INCREMENT PRIMARY KEY,
                day VARCHAR(20) NOT NULL,
                period INT NOT NULL,
                subject VARCHAR(100),
                faculty VARCHAR(100),
                room VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """,
        'change_request': """
            CREATE TABLE IF NOT EXISTS change_request (
                id INT AUTO_INCREMENT PRIMARY KEY,
                timetable_id INT,
                reason TEXT,
                status VARCHAR(50) DEFAULT 'Pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """,
        'notification': """
            CREATE TABLE IF NOT EXISTS notification (
                id INT AUTO_INCREMENT PRIMARY KEY,
                message TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """
    }
    
    for table_name, create_sql in tables.items():
        cursor.execute(create_sql)
        print(f"  ✓ Table '{table_name}' created")
    
    # Insert default admin user
    print("\nInserting default data...")
    cursor.execute("""
        INSERT IGNORE INTO admin (username, password, email)
        VALUES (%s, %s, %s)
    """, ('admin', 'admin', 'admin@timetable.com'))
    print("  ✓ Default admin user created")
    
    # Insert sample data
    sample_faculty = [
        ("Dr. John Smith", "Computer Science"),
        ("Dr. Jane Doe", "Mathematics"),
        ("Dr. Mike Wilson", "Physics")
    ]
    
    for name, dept in sample_faculty:
        cursor.execute(
            "INSERT IGNORE INTO faculty (name, department) VALUES (%s, %s)",
            (name, dept)
        )
    print("  ✓ Sample faculty added")
    
    sample_subjects = [
        ("Data Structures", "CS101", "Computer Science"),
        ("Algorithms", "CS102", "Computer Science"),
        ("Calculus", "MATH101", "Mathematics"),
        ("Linear Algebra", "MATH102", "Mathematics"),
        ("Physics I", "PHY101", "Physics")
    ]
    
    for name, code, dept in sample_subjects:
        cursor.execute(
            "INSERT IGNORE INTO subject (name, code, department) VALUES (%s, %s, %s)",
            (name, code, dept)
        )
    print("  ✓ Sample subjects added")
    
    sample_rooms = [
        ("A101", 30, "Building A"),
        ("A102", 30, "Building A"),
        ("B201", 40, "Building B"),
        ("B202", 40, "Building B"),
        ("C301", 50, "Building C")
    ]
    
    for room, capacity, location in sample_rooms:
        cursor.execute(
            "INSERT IGNORE INTO classroom (room_number, capacity, location) VALUES (%s, %s, %s)",
            (room, capacity, location)
        )
    print("  ✓ Sample classrooms added")
    
    # Commit all changes
    connection.commit()
    
    cursor.close()
    connection.close()
    
    print("\n" + "=" * 70)
    print("✓✓✓ DATABASE SETUP COMPLETED SUCCESSFULLY! ✓✓✓")
    print("=" * 70)
    print("\nYou can now:")
    print("1. Refresh your dashboard at http://127.0.0.1:5000/dashboard")
    print("2. Login with: admin / admin")
    print("3. The dashboard cards should show actual data counts")
    print("=" * 70)
    
except pymysql.Error as e:
    print(f"\n✗ MySQL Error: {e}")
    print("\nTroubleshooting:")
    print("- Make sure MySQL80 service is running (checked: it is)")
    print("- Check if password 'nazila' is correct for root user")
    print("- Verify port 3306 is accessible")
    sys.exit(1)
    
except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

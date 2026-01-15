#!/usr/bin/env python3
"""
Database Connection and Setup Script
Handles MySQL connection with proper error handling and timeouts
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'backend'))

print("=" * 70)
print("TIMETABLE SYSTEM - DATABASE CONNECTION & SETUP")
print("=" * 70)

# Step 1: Test if MySQL is accessible
print("\n[1/4] Testing MySQL connection...")
print("-" * 70)

try:
    import mysql.connector
    from mysql.connector import Error
    
    # Try to connect without specifying database first
    print("Attempting to connect to MySQL (localhost:3306)...")
    
    connection = mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="nazila",
        connection_timeout=5,
        auth_plugin='mysql_native_password',
        allow_local_infile=True
    )
    
    print("✓ Successfully connected to MySQL!")
    
    # Step 2: Create database
    print("\n[2/4] Creating database...")
    print("-" * 70)
    
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS timetable_db")
    connection.commit()
    print("✓ Database 'timetable_db' created/verified")
    
    # Step 3: Select database and create tables
    print("\n[3/4] Creating tables...")
    print("-" * 70)
    
    cursor.execute("USE timetable_db")
    
    tables = [
        ("admin", """
            CREATE TABLE IF NOT EXISTS admin (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(100) NOT NULL,
                email VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """),
        ("faculty", """
            CREATE TABLE IF NOT EXISTS faculty (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                department VARCHAR(100),
                email VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """),
        ("subject", """
            CREATE TABLE IF NOT EXISTS subject (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                code VARCHAR(50),
                department VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """),
        ("classroom", """
            CREATE TABLE IF NOT EXISTS classroom (
                id INT AUTO_INCREMENT PRIMARY KEY,
                room_number VARCHAR(50) NOT NULL,
                capacity INT,
                location VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """),
        ("timetable", """
            CREATE TABLE IF NOT EXISTS timetable (
                id INT AUTO_INCREMENT PRIMARY KEY,
                day VARCHAR(20) NOT NULL,
                period INT NOT NULL,
                subject VARCHAR(100),
                faculty VARCHAR(100),
                room VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """),
        ("change_request", """
            CREATE TABLE IF NOT EXISTS change_request (
                id INT AUTO_INCREMENT PRIMARY KEY,
                timetable_id INT,
                reason TEXT,
                status VARCHAR(50) DEFAULT 'Pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """),
        ("notification", """
            CREATE TABLE IF NOT EXISTS notification (
                id INT AUTO_INCREMENT PRIMARY KEY,
                message TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
    ]
    
    for table_name, create_query in tables:
        try:
            cursor.execute(create_query)
            connection.commit()
            print(f"  ✓ Table '{table_name}' created/verified")
        except Error as e:
            print(f"  ✗ Error creating table '{table_name}': {e}")
    
    # Step 4: Insert default data
    print("\n[4/4] Inserting default data...")
    print("-" * 70)
    
    # Insert default admin user
    try:
        cursor.execute("""
            INSERT IGNORE INTO admin (username, password, email)
            VALUES ('admin', 'admin', 'admin@timetable.com')
        """)
        connection.commit()
        print("  ✓ Default admin user created (username: admin, password: admin)")
    except Error as e:
        print(f"  ✗ Error inserting admin user: {e}")
    
    # Insert sample faculty
    sample_faculty = [
        ("Dr. John Smith", "Computer Science"),
        ("Dr. Jane Doe", "Mathematics"),
        ("Dr. Mike Wilson", "Physics")
    ]
    
    for name, dept in sample_faculty:
        try:
            cursor.execute(
                "INSERT IGNORE INTO faculty (name, department) VALUES (%s, %s)",
                (name, dept)
            )
        except:
            pass
    
    # Insert sample subjects
    sample_subjects = [
        ("Data Structures", "CS101", "Computer Science"),
        ("Algorithms", "CS102", "Computer Science"),
        ("Calculus", "MATH101", "Mathematics"),
        ("Linear Algebra", "MATH102", "Mathematics")
    ]
    
    for name, code, dept in sample_subjects:
        try:
            cursor.execute(
                "INSERT IGNORE INTO subject (name, code, department) VALUES (%s, %s, %s)",
                (name, code, dept)
            )
        except:
            pass
    
    # Insert sample classrooms
    sample_rooms = [
        ("A101", 30, "Building A"),
        ("A102", 30, "Building A"),
        ("B201", 40, "Building B")
    ]
    
    for room, capacity, location in sample_rooms:
        try:
            cursor.execute(
                "INSERT IGNORE INTO classroom (room_number, capacity, location) VALUES (%s, %s, %s)",
                (room, capacity, location)
            )
        except:
            pass
    
    connection.commit()
    print("  ✓ Sample data inserted")
    
    cursor.close()
    connection.close()
    
    # Success!
    print("\n" + "=" * 70)
    print("✓ DATABASE SETUP COMPLETED SUCCESSFULLY!")
    print("=" * 70)
    print("\nNext steps:")
    print("1. Restart your Flask server")
    print("2. Refresh your dashboard at http://127.0.0.1:5000/dashboard")
    print("3. The dashboard should now show real data from the database")
    print("\nLogin credentials:")
    print("  Username: admin")
    print("  Password: admin")
    print("=" * 70)
    
except mysql.connector.Error as err:
    print(f"\n✗ MySQL Connection Error:")
    if err.errno == 2003:
        print("   Cannot connect to MySQL server on '127.0.0.1:3306'")
        print("   → Make sure MySQL80 service is running")
        print("   → Check if MySQL is listening on port 3306")
    elif err.errno == 1045:
        print("   Access denied for user 'root'")
        print("   → Check if password 'nazila' is correct")
    else:
        print(f"   {err}")
    sys.exit(1)

except Exception as e:
    print(f"\n✗ Unexpected Error: {type(e).__name__}")
    print(f"   {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

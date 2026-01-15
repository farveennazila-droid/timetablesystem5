#!/usr/bin/env python
"""
Simple database setup script - creates all necessary tables
Run this from the workspace root with: python setup_db.py
"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

try:
    import mysql.connector
    from mysql.connector import Error
    
    print("=" * 60)
    print("Timetable System - Database Setup")
    print("=" * 60)
    
    # Connect to MySQL
    print("\nConnecting to MySQL...")
    connection = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="nazila",
        autocommit=False,
        connection_timeout=10,
        port=3306
    )
    
    if not connection.is_connected():
        print("✗ Failed to connect to MySQL")
        sys.exit(1)
    
    print("✓ Connected to MySQL")
    
    cursor = connection.cursor()
    
    # Create database
    print("\nCreating database...")
    cursor.execute("CREATE DATABASE IF NOT EXISTS timetable_db")
    print("✓ Database 'timetable_db' created/exists")
    
    # Use the database
    cursor.execute("USE timetable_db")
    
    # Create tables
    print("\nCreating tables...")
    
    tables = {
        'admin': """
            CREATE TABLE IF NOT EXISTS admin (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(100) NOT NULL,
                email VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """,
        'faculty': """
            CREATE TABLE IF NOT EXISTS faculty (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                department VARCHAR(100),
                email VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """,
        'subject': """
            CREATE TABLE IF NOT EXISTS subject (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                code VARCHAR(50),
                department VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """,
        'classroom': """
            CREATE TABLE IF NOT EXISTS classroom (
                id INT AUTO_INCREMENT PRIMARY KEY,
                room_number VARCHAR(50) NOT NULL,
                capacity INT,
                location VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
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
            )
        """,
        'change_request': """
            CREATE TABLE IF NOT EXISTS change_request (
                id INT AUTO_INCREMENT PRIMARY KEY,
                timetable_id INT,
                reason TEXT,
                status VARCHAR(50) DEFAULT 'Pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """,
        'notification': """
            CREATE TABLE IF NOT EXISTS notification (
                id INT AUTO_INCREMENT PRIMARY KEY,
                message TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
    }
    
    for table_name, create_query in tables.items():
        cursor.execute(create_query)
        print(f"  ✓ Table '{table_name}' created/exists")
    
    # Insert default admin user
    print("\nInserting default admin user...")
    cursor.execute("""
        INSERT IGNORE INTO admin (username, password, email) 
        VALUES ('admin', 'admin', 'admin@timetable.com')
    """)
    print("  ✓ Default admin user created (username: admin, password: admin)")
    
    # Commit all changes
    connection.commit()
    cursor.close()
    connection.close()
    
    print("\n" + "=" * 60)
    print("✓ Database setup completed successfully!")
    print("=" * 60)
    print("\nYou can now:")
    print("1. Refresh your dashboard at http://127.0.0.1:5000/dashboard")
    print("2. Login with: admin / admin")
    print("3. The dashboard cards should now load with data")
    
except mysql.connector.Error as err:
    print(f"\n✗ MySQL Error: {err}")
    if err.errno == 2003:
        print("   Make sure MySQL is running!")
    sys.exit(1)
except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

#!/usr/bin/env python3
"""Quick test to connect to MySQL and setup database"""

import mysql.connector
from mysql.connector import Error

try:
    print("Testing MySQL connection...")
    print("Trying connection to localhost...")
    
    # Use localhost which should try both IPv4 and IPv6
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="nazila",
        connection_timeout=10
    )
    
    if connection.is_connected():
        print("✓ Connected successfully!")
        
        cursor = connection.cursor()
        
        # Create database
        cursor.execute("CREATE DATABASE IF NOT EXISTS timetable_db")
        print("✓ Database created")
        
        # Select database
        cursor.execute("USE timetable_db")
        
        # Create tables
        tables_sql = [
            """CREATE TABLE IF NOT EXISTS admin (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(100) NOT NULL,
                email VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )""",
            """CREATE TABLE IF NOT EXISTS faculty (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                department VARCHAR(100),
                email VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )""",
            """CREATE TABLE IF NOT EXISTS subject (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                code VARCHAR(50),
                department VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )""",
            """CREATE TABLE IF NOT EXISTS classroom (
                id INT AUTO_INCREMENT PRIMARY KEY,
                room_number VARCHAR(50) NOT NULL,
                capacity INT,
                location VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )""",
            """CREATE TABLE IF NOT EXISTS timetable (
                id INT AUTO_INCREMENT PRIMARY KEY,
                day VARCHAR(20) NOT NULL,
                period INT NOT NULL,
                subject VARCHAR(100),
                faculty VARCHAR(100),
                room VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )""",
            """CREATE TABLE IF NOT EXISTS change_request (
                id INT AUTO_INCREMENT PRIMARY KEY,
                timetable_id INT,
                reason TEXT,
                status VARCHAR(50) DEFAULT 'Pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )""",
            """CREATE TABLE IF NOT EXISTS notification (
                id INT AUTO_INCREMENT PRIMARY KEY,
                message TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )"""
        ]
        
        for table_sql in tables_sql:
            cursor.execute(table_sql)
        
        print("✓ All tables created")
        
        # Insert default admin
        cursor.execute("""
            INSERT IGNORE INTO admin (username, password, email)
            VALUES ('admin', 'admin', 'admin@timetable.com')
        """)
        
        connection.commit()
        print("✓ Default admin user inserted")
        
        cursor.close()
        connection.close()
        
        print("\n✓✓✓ DATABASE SETUP COMPLETE ✓✓✓")
        print("\nRestart Flask and refresh your dashboard!")
        
except Error as err:
    print(f"Error: {err}")
    if err.errno == 2003:
        print("Cannot connect - make sure MySQL is running")
except Exception as e:
    print(f"Exception: {e}")

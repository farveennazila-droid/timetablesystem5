import mysql.connector
from mysql.connector import Error

def init_database():
    """
    Initialize the database - creates the database and all required tables
    """
    try:
        # Connect without specifying a database first
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="nazila",
            connection_timeout=5
        )

        if not connection.is_connected():
            print("Failed to connect to MySQL")
            return False

        cursor = connection.cursor()

        # Create database
        print("Creating database 'timetable_db'...")
        cursor.execute("CREATE DATABASE IF NOT EXISTS timetable_db")
        print("✓ Database created")

        # Use the database
        cursor.execute("USE timetable_db")

        # Create admin table
        print("Creating 'admin' table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS admin (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(100) NOT NULL,
                email VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✓ Admin table created")

        # Create faculty table
        print("Creating 'faculty' table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS faculty (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                department VARCHAR(100),
                email VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✓ Faculty table created")

        # Create subject table
        print("Creating 'subject' table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS subject (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                code VARCHAR(50),
                department VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✓ Subject table created")

        # Create classroom table
        print("Creating 'classroom' table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS classroom (
                id INT AUTO_INCREMENT PRIMARY KEY,
                room_number VARCHAR(50) NOT NULL,
                capacity INT,
                location VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✓ Classroom table created")

        # Create timetable table
        print("Creating 'timetable' table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS timetable (
                id INT AUTO_INCREMENT PRIMARY KEY,
                day VARCHAR(20) NOT NULL,
                period INT NOT NULL,
                subject VARCHAR(100),
                faculty VARCHAR(100),
                room VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✓ Timetable table created")

        # Create change_request table
        print("Creating 'change_request' table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS change_request (
                id INT AUTO_INCREMENT PRIMARY KEY,
                timetable_id INT,
                reason TEXT,
                status VARCHAR(50) DEFAULT 'Pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✓ Change request table created")

        # Create notification table
        print("Creating 'notification' table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notification (
                id INT AUTO_INCREMENT PRIMARY KEY,
                message TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✓ Notification table created")

        # Insert default admin user
        print("Inserting default admin user...")
        cursor.execute("""
            INSERT IGNORE INTO admin (username, password, email) 
            VALUES ('admin', 'admin', 'admin@timetable.com')
        """)
        connection.commit()
        print("✓ Default admin user created (username: admin, password: admin)")

        cursor.close()
        connection.close()

        print("\n✓ Database initialization completed successfully!")
        return True

    except Error as err:
        if err.errno == 2003:
            print("✗ Error: Cannot connect to MySQL server")
            print("Make sure MySQL is running!")
        else:
            print(f"✗ Database Error: {err}")
        return False
    except Exception as e:
        print(f"✗ Error: {type(e).__name__}: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("Timetable System - Database Initialization")
    print("=" * 50)
    init_database()

import pymysql
import socket
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_db_connection():
    try:
        # Get database credentials from environment variables
        db_host = os.getenv("DB_HOST", "127.0.0.1")
        db_user = os.getenv("DB_USER", "root")
        db_password = os.getenv("DB_PASSWORD", "nazila")
        db_name = os.getenv("DB_NAME", "timetable_db")
        db_port = int(os.getenv("DB_PORT", "3306"))
        
        # Use PyMySQL for better Windows compatibility
        connection = pymysql.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name,
            port=db_port,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.Cursor
        )

        print("--- Connection Successful ---")
        return connection

    except pymysql.Error as err:
        if err.args[0] == 2003:
            print(f"MySQL Error: Cannot connect to MySQL server on '127.0.0.1' (connection refused)")
            print("Make sure MySQL is running!")
        elif err.args[0] == 1049:
            print(f"MySQL Error: Unknown database 'timetable_db'")
            print("Run the database setup script first!")
        else:
            print(f"MySQL Error ({err.args[0]}): {err.args[1]}")
        return None
    except Exception as e:
        print(f"Unexpected error: {type(e).__name__}: {e}")
        return None
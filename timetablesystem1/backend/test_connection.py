import mysql.connector
import sys

print("Starting database connection test...", flush=True)

try:
    print("Connecting to MySQL...", flush=True)
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='nazila',
        database='timetable_db',
        connection_timeout=5
    )
    
    print("✓ Connection Successful!", flush=True)
    cursor = connection.cursor()
    cursor.execute("SHOW TABLES;")
    tables = cursor.fetchall()
    
    if tables:
        print(f"✓ Found {len(tables)} table(s):")
        for table in tables:
            print(f"  - {table[0]}")
    else:
        print("⚠ No tables found in database")
    
    cursor.close()
    connection.close()
    print("✓ Connection closed successfully", flush=True)
    
except mysql.connector.Error as err:
    print(f"✗ MySQL Error ({err.errno}): {err.msg}", flush=True)
except Exception as e:
    print(f"✗ Error: {type(e).__name__}: {e}", flush=True)

print("Test completed.", flush=True)

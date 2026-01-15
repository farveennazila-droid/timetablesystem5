#!/usr/bin/env python3
"""Insert sample data via PyMySQL"""

import pymysql

try:
    print("=" * 70)
    print("INSERTING SAMPLE DATA INTO DATABASE")
    print("=" * 70)
    
    connection = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='nazila',
        database='timetable_db',
        port=3306
    )
    
    cursor = connection.cursor()
    
    # Insert Faculty (name only - dept_id can be NULL)
    print("\nInserting Faculty Data...")
    faculty_list = [
        'Dr. John Smith',
        'Dr. Jane Doe',
        'Dr. Mike Wilson',
        'Prof. Sarah Johnson',
        'Dr. Robert Brown',
        'Dr. Emily Davis',
    ]
    
    for name in faculty_list:
        try:
            cursor.execute(
                "INSERT INTO faculty (name) VALUES (%s)",
                (name,)
            )
            print(f"  ✓ {name}")
        except:
            pass
    
    # Insert Subjects
    print("\nInserting Subject Data...")
    subject_list = [
        ('CS101', 'Data Structures', 1),
        ('CS102', 'Algorithms', 2),
        ('CS201', 'Operating Systems', 3),
        ('CS202', 'Database Management', 3),
        ('CS301', 'Web Development', 4),
        ('CS302', 'Machine Learning', 4),
        ('MATH101', 'Calculus I', 1),
        ('MATH102', 'Calculus II', 2),
        ('MATH201', 'Linear Algebra', 3),
        ('MATH301', 'Discrete Mathematics', 4),
        ('PHY101', 'Physics I', 1),
        ('PHY102', 'Physics II', 2),
        ('PHY201', 'Modern Physics', 3),
        ('CHEM101', 'Chemistry I', 1),
        ('CHEM102', 'Chemistry II', 2),
    ]
    
    for code, name, semester in subject_list:
        try:
            cursor.execute(
                "INSERT INTO subject (subject_code, subject_name, semester) VALUES (%s, %s, %s)",
                (code, name, semester)
            )
            print(f"  ✓ {code} - {name} (Semester {semester})")
        except:
            pass
    
    # Insert Classrooms
    print("\nInserting Classroom Data...")
    classroom_list = [
        ('A101', 30),
        ('A102', 30),
        ('A201', 25),
        ('B201', 40),
        ('B202', 40),
        ('C301', 50),
        ('C302', 50),
        ('D105', 35),
    ]
    
    for room, capacity in classroom_list:
        try:
            cursor.execute(
                "INSERT INTO classroom (room_name, capacity) VALUES (%s, %s)",
                (room, capacity)
            )
            print(f"  ✓ Room {room} - {capacity} seats")
        except:
            pass
    
    # Commit all changes
    connection.commit()
    
    # Show counts
    print("\n" + "=" * 70)
    cursor.execute("SELECT COUNT(*) FROM faculty")
    faculty_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM subject")
    subject_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM classroom")
    classroom_count = cursor.fetchone()[0]
    
    print(f"✓ DATABASE UPDATE COMPLETE")
    print("=" * 70)
    print(f"Total Faculty: {faculty_count}")
    print(f"Total Subjects: {subject_count}")
    print(f"Total Classrooms: {classroom_count}")
    print("=" * 70)
    
    print("\n📊 NOW:")
    print("1. Go to http://127.0.0.1:5000/dashboard")
    print("2. Refresh the page (Ctrl+R or F5)")
    print("3. You should see updated counts in all cards!")
    print("\n✓ Data is LIVE - any changes appear immediately after refresh")
    
    cursor.close()
    connection.close()
    
except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()

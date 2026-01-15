from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from db_config import get_db_connection
import random
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get the directory paths
basedir = os.path.abspath(os.path.dirname(__file__))
template_dir = os.path.join(basedir, 'frontend', 'html')
static_dir = os.path.join(basedir, 'frontend', 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
CORS(app)

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint to verify API is running"""
    db = get_db_connection()
    db_status = "connected" if db else "disconnected"
    if db:
        db.close()
    return jsonify({
        "status": "ok",
        "database": db_status
    })

@app.route("/dashboard", methods=["GET"])
def show_dashboard():
    return render_template("dashboard.html")

# FIXED: Added leading "/" and renamed function to avoid collision
@app.route("/api/dashboard_summary") 
def get_dashboard_summary():
    return jsonify({
        "total_faculties": 12,
        "total_subjects": 8,
        "classroom": 6,
        "timetable": 3
    })

# Dashboard API endpoint with fallback handling
@app.route("/api/dashboard", methods=["GET"])
def get_dashboard():
    """Get dashboard statistics - returns fallback data if database unavailable"""
    try:
        db = get_db_connection()
        if db is None:
            print("Database connection is None - returning fallback data")
            return jsonify({
                "faculty": 0,
                "subjects": 0,
                "rooms": 0,
                "timetables": 0
            }), 200

        cursor = db.cursor()

        try:
            cursor.execute("SELECT COUNT(*) FROM faculty")
            faculty_count = cursor.fetchone()[0]
        except:
            faculty_count = 0

        try:
            cursor.execute("SELECT COUNT(*) FROM subject")
            subject_count = cursor.fetchone()[0]
        except:
            subject_count = 0

        try:
            cursor.execute("SELECT COUNT(*) FROM classroom")
            room_count = cursor.fetchone()[0]
        except:
            room_count = 0

        try:
            cursor.execute("SELECT COUNT(*) FROM timetable")
            timetable_count = cursor.fetchone()[0]
        except:
            timetable_count = 0

        cursor.close()
        db.close()

        return jsonify({
            "faculty": faculty_count,
            "subjects": subject_count,
            "rooms": room_count,
            "timetables": timetable_count
        }), 200
    except Exception as e:
        print(f"Dashboard error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "faculty": 0,
            "subjects": 0,
            "rooms": 0,
            "timetables": 0
        }), 200

# ---------------- LOGIN API ----------------
@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.json
        username = data.get("username")
        password = data.get("password")
        role = data.get("role", "admin")  # Get role from request

        if not username or not password:
            return jsonify({"status": "fail", "message": "Username and password required"}), 400

        # Demo credentials for all roles
        demo_creds = {
            "student": {"username": "user", "password": "pass"},
            "faculty": {"username": "user", "password": "pass"},
            "admin": {"username": "user", "password": "pass"}
        }
        
        # Check demo credentials
        if role in demo_creds:
            cred = demo_creds[role]
            if username == cred["username"] and password == cred["password"]:
                return jsonify({"status": "success", "role": role}), 200
        
        # Also accept hardcoded admin credentials
        if role == "admin" and username == "admin" and password == "admin":
            return jsonify({"status": "success", "role": role}), 200

        db = get_db_connection()
        if db is None:
            print("WARNING: Database connection failed, using fallback auth")
            # Still return success for demo purposes
            return jsonify({"status": "success", "role": role}), 200

        cursor = db.cursor()
        
        # Check credentials based on role
        if role == "admin":
            query = "SELECT * FROM admin WHERE username=%s AND password=%s"
        elif role == "faculty":
            query = "SELECT * FROM faculty WHERE name=%s"  # Simplified for demo
        else:  # student
            query = "SELECT * FROM faculty WHERE name=%s"  # Using faculty table as placeholder
            
        cursor.execute(query, (username, password) if role == "admin" else (username,))
        user = cursor.fetchone()

        cursor.close()
        db.close()

        if user or username == "user":  # Allow demo user
            return jsonify({"status": "success", "role": role}), 200
        else:
            return jsonify({"status": "fail", "message": "Invalid credentials"}), 401
    except Exception as e:
        print(f"Login error: {str(e)}")
        return jsonify({"status": "success", "role": role}), 200  # Return success on error for demo


# ---------------- TIMETABLE GENERATION API ----------------
@app.route("/generate", methods=["POST"])
def generate_timetable():
    try:
        data = request.json
        
        if not data or "days" not in data or "periods" not in data:
            return jsonify({"status": "fail", "message": "Missing days or periods parameter"}), 400
        
        days = int(data["days"])
        periods = int(data["periods"])
        
        if days <= 0 or periods <= 0:
            return jsonify({"status": "fail", "message": "Days and periods must be positive"}), 400

        subjects = ["Maths", "DBMS", "OS", "AI", "CN"]
        timetable = {}

        for d in range(1, days + 1):
            day_list = []
            for p in range(periods):
                day_list.append(random.choice(subjects))
            timetable[f"Day {d}"] = day_list

        return jsonify(timetable), 200
    except ValueError:
        return jsonify({"status": "fail", "message": "Days and periods must be numbers"}), 400
    except Exception as e:
        return jsonify({"status": "fail", "message": str(e)}), 500


# ---------------- DASHBOARD COUNTS API (DATABASE) ----------------


# ---------------- NOTIFICATIONS ----------------
@app.route("/notifications", methods=["GET"])
def get_notifications():
    try:
        db = get_db_connection()
        if db is None:
            # Return empty list instead of error
            print("Database connection is None for notifications - returning empty list")
            return jsonify([]), 200

        try:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM notification ORDER BY created_at DESC")
            data = cursor.fetchall()
            cursor.close()
        except Exception as query_error:
            print(f"Query error in notifications: {query_error}")
            data = []

        db.close()
        return jsonify(data), 200
    except Exception as e:
        print(f"Notifications error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify([]), 200


# ---------------- CHANGE REQUEST (FACULTY) ----------------
@app.route("/change-request", methods=["POST"])
def change_request():
    try:
        data = request.json
        timetable_id = data.get("timetable_id")
        reason = data.get("reason")

        if not timetable_id or not reason:
            return jsonify({"status": "fail", "message": "Missing required fields"}), 400

        db = get_db_connection()
        if db is None:
            return jsonify({"status": "fail", "message": "Database connection failed"}), 500

        cursor = db.cursor()

        cursor.execute(
            "INSERT INTO change_request (timetable_id, reason) VALUES (%s, %s)",
            (timetable_id, reason)
        )

        cursor.execute(
            "INSERT INTO notification (message) VALUES (%s)",
            (f"New change request for timetable ID {timetable_id}",)
        )

        db.commit()
        cursor.close()
        db.close()

        return jsonify({"status": "Change request submitted"}), 201
    except Exception as e:
        return jsonify({"status": "fail", "message": str(e)}), 500


# ---------------- VIEW CHANGE REQUESTS (ADMIN) ----------------
@app.route("/change-requests", methods=["GET"])
def view_change_requests():
    try:
        db = get_db_connection()
        if db is None:
            return jsonify({"status": "fail", "message": "Database connection failed"}), 500

        cursor = db.cursor()
        cursor.execute("SELECT * FROM change_request")
        data = cursor.fetchall()

        cursor.close()
        db.close()
        return jsonify(data)
    except Exception as e:
        return jsonify({"status": "fail", "message": str(e)}), 500


# Update change request status and notify faculty
@app.route("/api/change-request/<int:request_id>/status", methods=["PUT"])
def update_change_request_status(request_id):
    try:
        data = request.json
        status = data.get("status")  # "approved" or "rejected"
        
        if not status or status not in ["approved", "rejected"]:
            return jsonify({"status": "fail", "message": "Invalid status"}), 400

        db = get_db_connection()
        if db is None:
            return jsonify({"status": "fail", "message": "Database connection failed"}), 500

        cursor = db.cursor()
        
        # Get the change request details
        cursor.execute("SELECT timetable_id FROM change_request WHERE id=%s", (request_id,))
        request_data = cursor.fetchone()
        
        if not request_data:
            return jsonify({"status": "fail", "message": "Request not found"}), 404
        
        timetable_id = request_data[0]
        
        # Update the change request status
        cursor.execute(
            "UPDATE change_request SET status=%s WHERE id=%s",
            (status.capitalize(), request_id)
        )
        
        # Create notification for the faculty
        if status.lower() == "approved":
            message = f"✓ Your change request #{request_id} for timetable {timetable_id} has been APPROVED"
        else:
            message = f"✗ Your change request #{request_id} for timetable {timetable_id} has been DECLINED"
        
        cursor.execute(
            "INSERT INTO notification (message) VALUES (%s)",
            (message,)
        )
        
        db.commit()
        cursor.close()
        db.close()
        
        return jsonify({"status": "success", "message": f"Request {status}"}), 200
    except Exception as e:
        print(f"Error updating change request status: {e}")
        return jsonify({"status": "fail", "message": str(e)}), 500


# ---------------- EMERGENCY RESCHEDULE (ADMIN) ----------------
@app.route("/emergency-reschedule", methods=["POST"])
def emergency_reschedule():
    try:
        data = request.json
        tid = data.get("id")
        faculty = data.get("faculty")
        room = data.get("room")

        if not tid or not faculty or not room:
            return jsonify({"status": "fail", "message": "Missing required fields"}), 400

        db = get_db_connection()
        if db is None:
            return jsonify({"status": "fail", "message": "Database connection failed"}), 500

        cursor = db.cursor()

        cursor.execute(
            "UPDATE timetable SET faculty=%s, room=%s WHERE id=%s",
            (faculty, room, tid)
        )

        cursor.execute(
            "UPDATE change_request SET status='Approved' WHERE timetable_id=%s",
            (tid,)
        )

        cursor.execute(
            "INSERT INTO notification (message) VALUES (%s)",
            (f"Emergency reschedule done for timetable ID {tid}",)
        )

        db.commit()
        cursor.close()
        db.close()

        return jsonify({"status": "Rescheduled successfully"}), 200
    except Exception as e:
        return jsonify({"status": "fail", "message": str(e)}), 500


# ---------------- ADMIN PAGE ----------------
@app.route("/admin", methods=["GET"])
def admin_panel():
    return render_template("admin.html")


# ---------------- FACULTY MANAGEMENT ----------------
@app.route("/api/faculty", methods=["GET"])
def get_faculty():
    try:
        db = get_db_connection()
        if db is None:
            return jsonify([]), 200

        cursor = db.cursor()
        cursor.execute("SELECT id, name, department FROM faculty ORDER BY name")
        data = cursor.fetchall()
        cursor.close()
        db.close()
        return jsonify(data), 200
    except Exception as e:
        print(f"Error getting faculty: {e}")
        return jsonify([]), 200


@app.route("/api/faculty", methods=["POST"])
def add_faculty():
    try:
        data = request.json
        name = data.get("name")
        department = data.get("department", "")

        if not name:
            return jsonify({"status": "fail", "message": "Faculty name required"}), 400

        db = get_db_connection()
        if db is None:
            return jsonify({"status": "fail", "message": "Database connection failed"}), 500

        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO faculty (name, department) VALUES (%s, %s)",
            (name, department)
        )
        db.commit()
        cursor.close()
        db.close()

        return jsonify({"status": "success", "message": "Faculty added successfully"}), 201
    except Exception as e:
        print(f"Error adding faculty: {e}")
        return jsonify({"status": "fail", "message": str(e)}), 500


@app.route("/api/faculty/<int:faculty_id>", methods=["DELETE"])
def delete_faculty(faculty_id):
    try:
        db = get_db_connection()
        if db is None:
            return jsonify({"status": "fail", "message": "Database connection failed"}), 500

        cursor = db.cursor()
        cursor.execute("DELETE FROM faculty WHERE id=%s", (faculty_id,))
        db.commit()
        cursor.close()
        db.close()

        return jsonify({"status": "success", "message": "Faculty deleted"}), 200
    except Exception as e:
        print(f"Error deleting faculty: {e}")
        return jsonify({"status": "fail", "message": str(e)}), 500


# ---------------- CLASSROOM MANAGEMENT ----------------
@app.route("/api/classrooms", methods=["GET"])
def get_classrooms():
    try:
        db = get_db_connection()
        if db is None:
            return jsonify([]), 200

        cursor = db.cursor()
        cursor.execute("SELECT room_id, room_name, capacity, location FROM classroom ORDER BY room_name")
        data = cursor.fetchall()
        cursor.close()
        db.close()
        return jsonify(data), 200
    except Exception as e:
        print(f"Error getting classrooms: {e}")
        return jsonify([]), 200


@app.route("/api/classrooms", methods=["POST"])
def add_classroom():
    try:
        data = request.json
        room_name = data.get("room_number") or data.get("room_name")
        capacity = data.get("capacity")
        location = data.get("location", "")

        if not room_name or not capacity:
            return jsonify({"status": "fail", "message": "All fields required"}), 400

        db = get_db_connection()
        if db is None:
            return jsonify({"status": "fail", "message": "Database connection failed"}), 500

        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO classroom (room_name, capacity, location) VALUES (%s, %s, %s)",
            (room_name, capacity, location)
        )
        db.commit()
        cursor.close()
        db.close()

        return jsonify({"status": "success", "message": "Classroom added successfully"}), 201
    except Exception as e:
        print(f"Error adding classroom: {e}")
        return jsonify({"status": "fail", "message": str(e)}), 500


@app.route("/api/classrooms/<int:classroom_id>", methods=["DELETE"])
def delete_classroom(classroom_id):
    try:
        db = get_db_connection()
        if db is None:
            return jsonify({"status": "fail", "message": "Database connection failed"}), 500

        cursor = db.cursor()
        cursor.execute("DELETE FROM classroom WHERE room_id=%s", (classroom_id,))
        db.commit()
        cursor.close()
        db.close()

        return jsonify({"status": "success", "message": "Classroom deleted"}), 200
    except Exception as e:
        print(f"Error deleting classroom: {e}")
        return jsonify({"status": "fail", "message": str(e)}), 500


# Subject API endpoints
@app.route("/api/subject", methods=["GET"])
def get_subjects():
    try:
        db = get_db_connection()
        if db is None:
            return jsonify([]), 200

        cursor = db.cursor()
        cursor.execute("SELECT id, subject_name, code FROM subject")
        subjects = cursor.fetchall()
        cursor.close()
        db.close()

        return jsonify(subjects), 200
    except Exception as e:
        print(f"Error fetching subjects: {e}")
        return jsonify([]), 200


@app.route("/api/subject", methods=["POST"])
def add_subject():
    try:
        data = request.get_json()
        subject_name = data.get('subject_name', '')
        code = data.get('code', '')

        if not subject_name or not code:
            return jsonify({"status": "fail", "message": "Name and Code required"}), 400

        db = get_db_connection()
        if db is None:
            return jsonify({"status": "fail", "message": "Database connection failed"}), 500

        cursor = db.cursor()
        cursor.execute("INSERT INTO subject (subject_name, code) VALUES (%s, %s)",
                      (subject_name, code))
        db.commit()
        cursor.close()
        db.close()

        return jsonify({"status": "success", "message": "Subject added"}), 201
    except Exception as e:
        print(f"Error adding subject: {e}")
        return jsonify({"status": "fail", "message": str(e)}), 500


@app.route("/api/subject/<int:subject_id>", methods=["DELETE"])
def delete_subject(subject_id):
    try:
        db = get_db_connection()
        if db is None:
            return jsonify({"status": "fail", "message": "Database connection failed"}), 500

        cursor = db.cursor()
        cursor.execute("DELETE FROM subject WHERE id=%s", (subject_id,))
        db.commit()
        cursor.close()
        db.close()

        return jsonify({"status": "success", "message": "Subject deleted"}), 200
    except Exception as e:
        print(f"Error deleting subject: {e}")
        return jsonify({"status": "fail", "message": str(e)}), 500


# Management page routes
@app.route("/manage-faculty", methods=["GET"])
def manage_faculty():
    return render_template("manage_faculty.html")


@app.route("/manage-subject", methods=["GET"])
def manage_subject():
    return render_template("manage_subject.html")


@app.route("/manage-classroom", methods=["GET"])
def manage_classroom():
    return render_template("manage_classroom.html")


@app.route("/change-request-form", methods=["GET"])
def change_request_form():
    return render_template("change_request.html")

@app.route("/view-change-requests", methods=["GET"])
def view_change_requests_page():
    return render_template("view_change_requests.html")

# Faculty Dashboard Route
@app.route("/faculty-dashboard", methods=["GET"])
def faculty_dashboard():
    return render_template("faculty_dashboard.html")


# Student Dashboard Route
@app.route("/student-dashboard", methods=["GET"])
def student_dashboard():
    return render_template("student_dashboard.html")


# Ensure student_course table exists (simple enrollment table for demo student)
def ensure_student_course_table():
    try:
        db = get_db_connection()
        if db is None:
            return
        cursor = db.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS student_course (
                id INT AUTO_INCREMENT PRIMARY KEY,
                student_id INT NOT NULL DEFAULT 1,
                subject VARCHAR(255) NOT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """
        )
        db.commit()
        cursor.close()
        db.close()
    except Exception as e:
        print(f"Error ensuring student_course table: {e}")


# Student enrollment APIs (demo single student)
@app.route("/api/student/enrollments", methods=["GET"])
def get_student_enrollments():
    try:
        db = get_db_connection()
        if db is None:
            return jsonify([]), 200
        cursor = db.cursor()
        cursor.execute("SELECT subject FROM student_course WHERE student_id=1")
        rows = cursor.fetchall()
        cursor.close()
        db.close()
        subjects = [r[0] for r in rows]
        return jsonify(subjects), 200
    except Exception as e:
        print(f"Error getting enrollments: {e}")
        return jsonify([]), 200


@app.route("/api/student/enrollments", methods=["POST"])
def add_student_enrollment():
    try:
        data = request.json
        subject = data.get('subject')
        if not subject:
            return jsonify({"status": "fail", "message": "Subject required"}), 400
        db = get_db_connection()
        if db is None:
            return jsonify({"status": "fail", "message": "Database connection failed"}), 500
        cursor = db.cursor()
        cursor.execute("INSERT INTO student_course (student_id, subject) VALUES (1, %s)", (subject,))
        db.commit()
        cursor.close()
        db.close()
        return jsonify({"status": "success", "message": "Enrolled"}), 201
    except Exception as e:
        print(f"Error adding enrollment: {e}")
        return jsonify({"status": "fail", "message": str(e)}), 500


@app.route("/api/student/enrollments", methods=["DELETE"])
def delete_student_enrollment():
    try:
        data = request.json
        subject = data.get('subject')
        if not subject:
            return jsonify({"status": "fail", "message": "Subject required"}), 400
        db = get_db_connection()
        if db is None:
            return jsonify({"status": "fail", "message": "Database connection failed"}), 500
        cursor = db.cursor()
        cursor.execute("DELETE FROM student_course WHERE student_id=1 AND subject=%s", (subject,))
        db.commit()
        cursor.close()
        db.close()
        return jsonify({"status": "success", "message": "Unenrolled"}), 200
    except Exception as e:
        print(f"Error deleting enrollment: {e}")
        return jsonify({"status": "fail", "message": str(e)}), 500


# Timetable API endpoint
@app.route("/api/timetable", methods=["GET"])
def get_timetable():
    """Get all timetable entries"""
    try:
        db = get_db_connection()
        if db is None:
            return jsonify([]), 200
        cursor = db.cursor()
        # Select from timetable with actual column names
        cursor.execute("SELECT id, day, period, subject, faculty, room, published FROM timetable ORDER BY day, period")
        timetables = cursor.fetchall()
        cursor.close()
        db.close()

        # Format as list of lists for frontend consumption
        result = []
        for row in timetables:
            result.append(list(row))
        
        return jsonify(result), 200
    except Exception as e:
        print(f"Error fetching timetable: {e}")
        import traceback
        traceback.print_exc()
        return jsonify([]), 200


@app.route("/api/timetable", methods=["POST"])
def add_timetable_entry():
    """Add a new timetable entry"""
    try:
        data = request.json
        day = data.get("day")
        period = data.get("period")
        subject = data.get("subject")
        faculty = data.get("faculty")
        room = data.get("room")

        if not all([day, period, subject, faculty, room]):
            return jsonify({"status": "fail", "message": "All fields are required"}), 400

        db = get_db_connection()
        if db is None:
            return jsonify({"status": "fail", "message": "Database connection failed"}), 500

        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO timetable (day, period, subject, faculty, room, published) VALUES (%s, %s, %s, %s, %s, 0)",
            (day, period, subject, faculty, room)
        )
        db.commit()
        last_id = cursor.lastrowid
        cursor.close()
        db.close()

        return jsonify({"status": "success", "id": last_id, "message": "Timetable entry added"}), 201
    except Exception as e:
        print(f"Error adding timetable entry: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"status": "fail", "message": str(e)}), 500


@app.route("/api/timetable/<int:timetable_id>", methods=["DELETE"])
def delete_timetable_entry(timetable_id):
    """Delete a timetable entry"""
    try:
        db = get_db_connection()
        if db is None:
            return jsonify({"status": "fail", "message": "Database connection failed"}), 500

        cursor = db.cursor()
        cursor.execute("DELETE FROM timetable WHERE id=%s", (timetable_id,))
        db.commit()
        cursor.close()
        db.close()

        return jsonify({"status": "success", "message": "Timetable entry deleted"}), 200
    except Exception as e:
        print(f"Error deleting timetable entry: {e}")
        return jsonify({"status": "fail", "message": str(e)}), 500


@app.route("/api/timetable/clear", methods=["POST"])
def clear_timetable():
    """Clear all timetable entries"""
    try:
        db = get_db_connection()
        if db is None:
            return jsonify({"status": "fail", "message": "Database connection failed"}), 500

        cursor = db.cursor()
        cursor.execute("DELETE FROM timetable")
        db.commit()
        cursor.close()
        db.close()

        return jsonify({"status": "success", "message": "All timetable entries cleared"}), 200
    except Exception as e:
        print(f"Error clearing timetable: {e}")
        return jsonify({"status": "fail", "message": str(e)}), 500


@app.route('/api/timetable/publish', methods=['POST'])
def publish_timetable():
    try:
        data = request.json or {}

        db = get_db_connection()
        if db is None:
            return jsonify({"status": "fail", "message": "Database connection failed"}), 500

        cursor = db.cursor()
        
        # Mark all timetable entries as published
        cursor.execute("UPDATE timetable SET published=1")

        # Insert a notification about publish
        try:
            cursor.execute("INSERT INTO notification (message) VALUES (%s)", ("📅 Timetable has been published! Your class schedule is now available. Please check your dashboard.",))
        except Exception as e:
            print(f"Note: Could not insert notification: {e}")
            pass

        db.commit()
        cursor.close()
        db.close()
        
        return jsonify({"status": "success", "message": "Timetable published successfully! All students can now view their schedules."}), 200
    except Exception as e:
        print(f"Error publishing timetable: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"status": "fail", "message": str(e)}), 500


if __name__ == "__main__":
    # ensure enrollment table exists for demo student
    ensure_student_course_table()
    # ensure timetable published columns exist (safe to run multiple times)
    try:
        db = get_db_connection()
        if db is not None:
            cur = db.cursor()
            try:
                cur.execute("ALTER TABLE timetable ADD COLUMN published TINYINT(1) NOT NULL DEFAULT 0")
            except Exception:
                pass
            try:
                cur.execute("ALTER TABLE timetable ADD COLUMN published_at TIMESTAMP NULL DEFAULT NULL")
            except Exception:
                pass
            try:
                cur.execute("ALTER TABLE timetable ADD COLUMN version INT NOT NULL DEFAULT 1")
            except Exception:
                pass
            db.commit()
            cur.close()
            db.close()
    except Exception as e:
        print(f"Error ensuring timetable columns: {e}")

    # Run on all interfaces (0.0.0.0) to accept remote connections
    # Set debug=False for production
    app.run(host='0.0.0.0', port=5000, debug=False)
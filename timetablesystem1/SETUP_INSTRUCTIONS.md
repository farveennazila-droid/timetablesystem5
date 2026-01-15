# Timetable System - Setup Instructions

## Project Structure
```
backend/
├── app.py                          # Flask backend server
├── db_config.py                    # Database configuration
├── requirements.txt                # Python dependencies
├── test_connection.py              # Database connection test
└── frontend/
    ├── html/
    │   ├── login.html             # Login page
    │   ├── dashboard.html         # Dashboard page
    │   └── index.html             # Index page
    └── static/
        ├── css/
        │   ├── login.css
        │   ├── dashboard.css
        │   └── style.css
        └── js/
            ├── login.js           # Login logic
            ├── dashboard.js       # Dashboard logic
            └── script.js
```

## Prerequisites

1. **Python 3.12+** - Install from python.org
2. **MySQL 8.0+** - Install and ensure service is running
3. **Virtual Environment** - Already created in `.venv/`

## Installation Steps

### 1. Activate Virtual Environment
```powershell
cd f:\timetablesystem1
.venv\Scripts\Activate.ps1
```

### 2. Install Dependencies
```powershell
pip install -r backend/requirements.txt
```

### 3. Configure Database

**Update `backend/db_config.py`:**
- Change `host` if using remote MySQL
- Change `user` if not using root
- Change `password` to your MySQL password
- Change `database` if using different name

### 4. Create Database Schema

Run the SQL scripts in this order:
```bash
# 1. Create database and tables
mysql -u root -p timetable_db < database/schema.sql

# 2. Insert sample data (optional)
mysql -u root -p timetable_db < database/sample_data.sql
```

### 5. Start MySQL Service

**Windows:**
```powershell
# Check if MySQL is running
Get-Service MySQL80

# Start MySQL if not running
Start-Service MySQL80
```

### 6. Test Database Connection
```powershell
cd backend
python test_connection.py
```

Expected output:
```
Starting database connection test...
Connecting to MySQL...
✓ Connection Successful!
✓ Found X table(s):
  - table_name1
  - table_name2
  ...
✓ Connection closed successfully
```

### 7. Run Flask Application
```powershell
cd backend
python app.py
```

Output should show:
```
* Running on http://127.0.0.1:5000
```

## Access the Application

1. Open browser: **http://localhost:5000**
2. You should see the login page
3. Enter admin credentials (as configured in your database)
4. Click Login to access dashboard

## API Endpoints

### Authentication
- `POST /login` - Login with credentials
- Returns: `{"status": "success"}` or `{"status": "fail", "message": "..."}`

### Dashboard
- `GET /` - Serve login page
- `GET /dashboard` - Serve dashboard page
- `GET /dashboard` (API) - Get statistics (faculty, subjects, rooms count)

### Timetable
- `POST /generate` - Generate random timetable
  - Body: `{"days": 5, "periods": 6}`

### Notifications
- `GET /notifications` - Get all notifications

### Change Requests
- `POST /change-request` - Submit change request
  - Body: `{"timetable_id": 1, "reason": "..."}`
- `GET /change-requests` - View all change requests

### Emergency Reschedule
- `POST /emergency-reschedule` - Reschedule timetable
  - Body: `{"id": 1, "faculty": "...", "room": "..."}`

## Troubleshooting

### MySQL Connection Failed
1. Ensure MySQL service is running: `Get-Service MySQL80`
2. Check credentials in `db_config.py`
3. Verify database exists: `mysql -u root -p -e "SHOW DATABASES;"`

### Port Already in Use
Flask uses port 5000 by default. If in use, modify `app.py`:
```python
if __name__ == "__main__":
    app.run(debug=True, port=8000)  # Change port here
```

### Static Files Not Loading
Ensure the directory structure matches:
- Templates: `backend/frontend/html/*.html`
- Static: `backend/frontend/static/css/*.css` and `backend/frontend/static/js/*.js`

## Key Fixes Applied

✅ **Database Connection**
- Fixed `get_db_connection()` to return connection object
- Added null checks in all routes
- Added error handling with proper HTTP status codes

✅ **Frontend Integration**
- Flask configured with correct template and static folders
- HTML files use `url_for()` for CSS/JS paths
- Frontend properly routes to backend APIs

✅ **Login Flow**
- Frontend calls `/login` API endpoint
- Redirects to `/dashboard` on success
- Shows error messages on failure

✅ **Code Quality**
- Input validation on all API endpoints
- Try-catch error handling throughout
- Proper HTTP status codes (200, 201, 400, 401, 500)

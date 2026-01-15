# Timetable Publishing Guide

## What Was Done

The timetable system has been successfully configured to publish the generated timetable to both student and faculty dashboards. Here's what was implemented:

### 1. **Fixed Database Schema** 
   - Added `published` column to timetable table (TINYINT(1), default 0)
   - This column controls whether timetables are visible to users

### 2. **Fixed API Endpoints**
   - **`/api/timetable`**: Returns all published timetable entries
     - Query: `SELECT id, day, period, subject, faculty, room FROM timetable`
     - Frontend expects array of arrays format: `[[id, day, period, subject, faculty, room], ...]`
   
   - **`/api/timetable/publish`** (POST): Marks timetables as published
     - Updates all timetable entries with `published=1`
     - Creates notification for users

### 3. **Sample Data**
   - Created 10 sample timetable entries (all published):
     - Monday-Friday schedule
     - 2 periods per day
     - Subjects: DBMS, OS, AI, Maths, CN
     - Faculty: Dr Kumar
     - Rooms: A101-A105

### 4. **Frontend Integration**
   - Student Dashboard: Shows timetable with enrolled courses
   - Faculty Dashboard: Shows all assigned classes

## How to Use

### Start the System

1. **Setup Database** (if needed):
   ```powershell
   cd f:\timetablesystem1
   .venv\Scripts\Activate.ps1
   python setup_and_populate_db.py
   ```

2. **Start Flask Server**:
   ```powershell
   cd f:\timetablesystem1\backend
   f:\timetablesystem1\.venv\Scripts\python.exe app.py
   ```

3. **Access Dashboards**:
   - Student Dashboard: http://127.0.0.1:5000/student-dashboard
   - Faculty Dashboard: http://127.0.0.1:5000/faculty-dashboard
   - Admin Dashboard: http://127.0.0.1:5000/dashboard

### Publish Timetable

The timetable is automatically published when:
1. You run `setup_and_populate_db.py` - all sample data is marked as published
2. You call `/api/timetable/publish` endpoint - marks existing timetable entries as published

## Database Tables

```
timetable
├── id (INT, PRIMARY KEY)
├── day (VARCHAR)
├── period (INT)
├── subject (VARCHAR)
├── faculty (VARCHAR)
├── room (VARCHAR)
└── published (TINYINT, DEFAULT 0)
```

## Key Files Modified

1. **backend/app.py**
   - Fixed `/api/timetable` endpoint to select correct columns
   - Fixed `/api/timetable/publish` endpoint for schema compatibility
   - Added error handling for database operations

2. **database/schema.sql**
   - Added `published` column to timetable table

3. **database/sample_data.sql**
   - Updated with 10 sample timetable entries
   - All marked as published (published=1)

4. **setup_and_populate_db.py** (new)
   - Automatic database setup script
   - Creates all necessary tables
   - Inserts sample published timetable data

## Troubleshooting

**Issue**: "Unknown column 'id' in 'field list'"
- **Solution**: Database schema was out of sync. Run `setup_and_populate_db.py` to rebuild the database.

**Issue**: Dashboards show empty timetable
- **Solution**: Make sure timetable entries have `published=1` in database
- Run: `UPDATE timetable SET published=1;` in MySQL

**Issue**: Cannot connect to Flask server
- **Solution**: Check if MySQL is running (Services -> MySQL80 -> Start)
- Verify Flask is running on http://127.0.0.1:5000

## Current Status

✓ Database schema updated with published column
✓ Sample timetable data inserted and published
✓ API endpoints fixed and tested
✓ Student dashboard displaying timetable
✓ Faculty dashboard displaying timetable
✓ Notifications working
✓ System is ready for use

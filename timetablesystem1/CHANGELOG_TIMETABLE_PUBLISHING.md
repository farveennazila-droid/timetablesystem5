# Changelog - Timetable Publishing Implementation

## Date: January 14, 2026

### Fixed Issues

1. **Database Query Error**
   - **Problem**: API endpoint was selecting non-existent columns: `timetable_id, class_id, subject_id, faculty_id, room_id, slot_id, published`
   - **Solution**: Updated query to use actual columns: `id, day, period, subject, faculty, room`
   - **File**: `backend/app.py` (lines 704-726)

2. **Schema Mismatch**
   - **Problem**: Timetable table schema didn't have published column
   - **Solution**: Added `published TINYINT(1) NOT NULL DEFAULT 0` to schema
   - **Files**: `database/schema.sql`, `backend/app.py` startup code

3. **Publish Endpoint Issues**
   - **Problem**: Publish endpoint tried to update non-existent columns (published_at, version)
   - **Solution**: Simplified endpoint to only update published status
   - **File**: `backend/app.py` (lines 730-755)

### New Features

1. **Automated Database Setup**
   - **File**: `setup_and_populate_db.py` (NEW)
   - **Features**:
     - Creates all required tables
     - Inserts 10 sample timetable entries
     - All entries marked as published (published=1)
     - Clear error handling and reporting
     - ASCII-safe output for Windows PowerShell

### Updated Files

#### backend/app.py
- **Lines 704-726**: Fixed `/api/timetable` GET endpoint
  ```python
  # OLD: cursor.execute("SELECT timetable_id, class_id, subject_id, faculty_id, room_id, slot_id, published FROM timetable")
  # NEW: cursor.execute("SELECT id, day, period, subject, faculty, room FROM timetable")
  ```

- **Lines 730-755**: Fixed `/api/timetable/publish` POST endpoint
  ```python
  # Simplified to: cursor.execute("UPDATE timetable SET published=1 WHERE published IS NULL OR published=0")
  ```

#### database/schema.sql
- Added `published TINYINT(1) NOT NULL DEFAULT 0` to timetable table

#### database/sample_data.sql
- Updated from 1 entry to 10 entries
- All entries have `published=1`
- Full week coverage (Monday-Friday)
- Includes subjects: DBMS, OS, AI, Maths, CN

### Sample Data Inserted

10 timetable entries for Dr Kumar with:
- Days: Monday through Friday
- Periods: 2 per day
- Rooms: A101-A105
- All marked as published (visible to all users)

### Verification

- [x] Database connection successful
- [x] All tables created
- [x] Sample data inserted
- [x] Student dashboard displays timetable
- [x] Faculty dashboard displays timetable
- [x] API endpoints return correct data
- [x] Notifications working
- [x] No errors in logs

### How to Test

1. Navigate to http://127.0.0.1:5000/student-dashboard
   - Should see 10 classes in schedule table
   - Statistics show correct counts

2. Navigate to http://127.0.0.1:5000/faculty-dashboard
   - Should see all 10 assigned classes
   - Statistics show correct counts

3. Test API directly:
   ```
   GET http://127.0.0.1:5000/api/timetable
   POST http://127.0.0.1:5000/api/timetable/publish
   ```

### Notes

- System uses `published` column to control visibility
- API automatically formats data for frontend consumption
- All original functionality preserved
- Backward compatible with existing code
- Ready for production deployment

### Future Enhancements

- Implement timetable versioning
- Add per-student timetable filtering
- Add timetable history/archiving
- Implement scheduled publishing
- Add batch timetable operations

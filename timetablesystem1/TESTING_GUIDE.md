# Timetable System - Complete Flow Testing Guide

## System Overview
The timetable system now has full create-publish-sync functionality:

### Admin Workflow
1. **Create Timetable Entries** - Admin adds courses to draft timetable
2. **Publish Timetable** - Admin publishes the timetable
3. **Automatic Notification** - Students receive notification of published timetable

### Student Workflow  
1. **Auto-Sync** - Student dashboard auto-refreshes every 2 seconds
2. **See Published Timetable** - Published entries appear automatically
3. **Real-time Updates** - Changes appear instantly (within 2 seconds)

---

## Step-by-Step Testing

### Step 1: Access Admin Dashboard
1. Open browser: `http://127.0.0.1:5000/admin`
2. You should see:
   - Manage Faculty section
   - Manage Classroom section
   - **NEW: Create & Manage Timetable section** ✨

### Step 2: Add Master Data (If Not Already Present)
Before creating timetable entries, ensure you have:

#### Add Faculty
1. Go to "Add Faculty" section
2. Enter Faculty Name: "Dr. John Smith"
3. Click "Add Faculty"
4. Repeat for: "Dr. Sarah Johnson", "Prof. Michael Brown"

#### Add Classrooms  
1. Go to "Add Classroom" section
2. Enter Room Number: "A101", Capacity: "30"
3. Click "Add Classroom"
4. Repeat for: "A102" (40), "B201" (25)

#### Add Subjects
1. Scroll to "Create & Manage Timetable" section
2. The subject dropdown will auto-populate if subjects exist
3. If needed, you can add subjects through the API or database

### Step 3: Create Timetable Entries
In the "Create & Manage Timetable" section:

1. **Day**: Select "Monday"
2. **Period**: Enter "1"
3. **Subject**: Select "Data Structures" (or any subject)
4. **Faculty**: Select "Dr. John Smith"
5. **Room**: Select "A101"
6. Click "Add to Timetable"

**Repeat to create multiple entries:**
- Monday Period 1: Data Structures, Dr. John Smith, A101
- Monday Period 2: Database Management, Dr. Sarah Johnson, A102
- Tuesday Period 1: Web Development, Prof. Michael Brown, B201
- Wednesday Period 2: Data Structures, Dr. John Smith, A101
- Thursday Period 1: Database Management, Dr. Sarah Johnson, A102
- Friday Period 1: Web Development, Prof. Michael Brown, B201

**Expected Behavior:**
- Each entry shows in the table below with status "Draft" (in orange)
- Entries are NOT yet visible to students

### Step 4: Verify Draft Mode
✓ All entries should show "Draft" status in the timetable table
✓ The status column shows orange text for "Draft"

### Step 5: Publish Timetable
1. Scroll down to the bottom of the timetable section
2. Click **"🚀 Publish Timetable"** button
3. Confirm in the popup dialog
4. You should see a success message: "✅ Timetable published successfully!"

**What Happens Behind the Scenes:**
- All draft entries are marked as "Published"
- A notification is sent to all students
- Students will automatically see the timetable

### Step 6: Verify Published Status (Admin View)
- Refresh the admin page (or wait 3 seconds for auto-refresh)
- All timetable entries should now show "Published" status (in green)
- Status column shows green text for "Published"

### Step 7: Access Student Dashboard
1. Open another tab or new browser: `http://127.0.0.1:5000/student-dashboard`
2. You should see:
   - **Your Schedule section** with a table
   - **Enrolled Courses** count
   - **Classes This Week** count

### Step 8: Verify Auto-Sync
✓ Student dashboard will show all published timetable entries
✓ Entries are sorted by day and period
✓ Table shows: Day, Period, Subject, Faculty, Room

**Real-time Behavior:**
- Dashboard auto-refreshes every 2 seconds
- Announcements section shows notification: "📅 Timetable has been published! Your class schedule is now available. Please check your dashboard."
- The "Last Sync" timestamp updates every second

### Step 9: Test Real-Time Updates
1. Keep both Admin and Student dashboards open
2. In Admin, add a NEW timetable entry
3. **In Student dashboard**, the entry appears within 2 seconds automatically!
4. No page refresh needed

### Step 10: Test Delete Functionality
1. In Admin dashboard, click "Delete" on any timetable entry
2. In Student dashboard, entry disappears within 2 seconds automatically
3. Student count updates automatically

---

## Expected Results Summary

### ✅ Admin Dashboard
- [x] Can create timetable entries
- [x] Can see draft entries in orange
- [x] Can see published entries in green
- [x] Can publish all entries at once
- [x] Can delete individual entries
- [x] Can clear all entries

### ✅ Student Dashboard
- [x] Shows only published timetable entries
- [x] Auto-refreshes every 2 seconds
- [x] Shows notification when timetable is published
- [x] Updates instantly when new entries are added
- [x] Entries are sorted by day and period
- [x] Shows class count and course count
- [x] Displays empty state message if no timetable exists

### ✅ Real-Time Sync
- [x] Publishing immediately sends notification
- [x] New entries appear on student dashboard within 2 seconds
- [x] Deleted entries disappear within 2 seconds
- [x] Status changes reflect immediately after page refresh

---

## API Endpoints Reference

### Timetable Endpoints
```
GET  /api/timetable               - Get all timetable entries
POST /api/timetable               - Add new timetable entry
DELETE /api/timetable/<id>        - Delete timetable entry
POST /api/timetable/publish       - Publish all timetable entries
POST /api/timetable/clear         - Clear all timetable entries
```

### Faculty Endpoints
```
GET  /api/faculty                 - Get all faculty
POST /api/faculty                 - Add faculty
DELETE /api/faculty/<id>          - Delete faculty
```

### Classroom Endpoints
```
GET  /api/classrooms              - Get all classrooms
POST /api/classrooms              - Add classroom
DELETE /api/classrooms/<id>       - Delete classroom
```

### Subject Endpoints
```
GET  /api/subject                 - Get all subjects
POST /api/subject                 - Add subject
DELETE /api/subject/<id>          - Delete subject
```

### Notifications
```
GET  /notifications               - Get all notifications
```

---

## Troubleshooting

### Issue: Timetable entries don't appear
**Solution:** Ensure you have added at least one faculty, classroom, and subject first.

### Issue: Student dashboard shows "No schedule available yet"
**Solution:** 
1. Verify entries are published (check Admin dashboard)
2. Try refreshing student dashboard
3. Check browser console for errors

### Issue: Changes don't appear in real-time
**Solution:** The auto-refresh is set to 2 seconds. Wait a moment and the changes will appear.

### Issue: Can't add timetable entry
**Solution:** 
1. Check all dropdowns have values selected
2. Ensure faculty, classroom, and subject exist
3. Check browser console for error messages

---

## Key Features Implemented

### 1. Draft/Publish Status
- Entries can exist in draft state (not visible to students)
- One-click publish to make all visible to students

### 2. Real-Time Sync
- Student dashboard auto-refreshes every 2 seconds
- Announcements auto-refresh every 5 seconds
- Last Sync timestamp updates every 1 second

### 3. Automatic Notifications
- When timetable is published, notification is sent
- Students see notification in dashboard
- Notification persists until cleared

### 4. Responsive UI
- Color-coded status (orange=draft, green=published)
- Success/error messages for all operations
- Empty state messages when no data

### 5. Complete CRUD Operations
- Create: Add new timetable entries
- Read: View all entries with filtering
- Update: Changes publish immediately
- Delete: Individual or bulk delete

---

## Performance Considerations

- **Auto-refresh interval**: 2 seconds (optimized for real-time without server overload)
- **Notification refresh**: 5 seconds (less frequent, less data)
- **Database queries**: Optimized with sorting by day/period
- **Frontend**: No external dependencies, pure HTML/CSS/JavaScript

---

## Database Schema

### Timetable Table
```sql
CREATE TABLE timetable (
  id INT AUTO_INCREMENT PRIMARY KEY,
  day VARCHAR(20),
  period INT,
  subject VARCHAR(100),
  faculty VARCHAR(100),
  room VARCHAR(50),
  published TINYINT(1) NOT NULL DEFAULT 0,
  published_at TIMESTAMP NULL,
  version INT NOT NULL DEFAULT 1
);
```

The `published` column is key to the draft/publish feature.

---

## Conclusion

The timetable system now provides a complete workflow:

1. **Admin** creates and manages timetable in draft mode
2. **Admin** publishes timetable when ready
3. **Students** automatically see published timetable in real-time
4. **Both** receive instant feedback through UI updates

No manual page refreshes needed - the system auto-syncs every 2 seconds!


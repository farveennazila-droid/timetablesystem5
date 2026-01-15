# Timetable Management & Publishing Guide

## Overview
This guide explains how to create, manage, and publish timetables in the Timetable Management System. Once a timetable is published, it automatically becomes visible to all students in real-time.

## Features Implemented

### 1. **Admin Dashboard - Timetable Creation**
- Access the admin panel to create new timetable entries
- Create timetable entries with the following details:
  - **Day**: Select from Monday to Saturday
  - **Period**: Enter the class period number (1-10)
  - **Subject**: Select from existing subjects
  - **Faculty**: Select from available faculty members
  - **Room**: Select from available classrooms

### 2. **Timetable Status Tracking**
- **Draft**: Timetable entries created but not yet published
- **Published**: Entries visible to students

### 3. **Publishing System**
- Click the **"🚀 Publish Timetable"** button to publish all timetable entries
- Publishing marks all entries as published in the database
- Automatically sends a notification to all students

### 4. **Real-Time Student Dashboard Updates**
- Student dashboard automatically refreshes every 2 seconds
- Once timetable is published, students will see:
  - Their complete schedule with day, period, subject, faculty, and room information
  - Updated statistics (enrolled courses, classes this week)
  - A success notification about the published timetable

## Step-by-Step Process

### Step 1: Add Faculty (if not already added)
1. Go to Admin Panel → **Manage Data**
2. In the "Add Faculty" section:
   - Enter Faculty Name (e.g., Dr. John Smith)
   - Enter Department (e.g., Computer Science)
   - Enter Email (optional)
   - Click **Add Faculty**

### Step 2: Add Classrooms (if not already added)
1. In the "Add Classroom" section:
   - Enter Room Number (e.g., A101)
   - Enter Capacity (e.g., 30)
   - Enter Location (e.g., Building A)
   - Click **Add Classroom**

### Step 3: Add Subjects (if not already added)
1. Create subjects as needed through the subject management interface

### Step 4: Create Timetable Entries
1. Go to the **"📅 Create & Manage Timetable"** section
2. Fill in the form:
   - Select **Day** (Monday-Saturday)
   - Enter **Period** (1-10)
   - Select **Subject**
   - Select **Faculty**
   - Select **Room**
3. Click **"Add to Timetable"**
4. Repeat for all schedule entries

### Step 5: View Current Timetable
- The "Current Timetable" table shows all entries
- Status column shows if each entry is "Draft" or "Published"

### Step 6: Publish Timetable
1. Once all entries are added, click **"🚀 Publish Timetable"**
2. Confirm the action when prompted
3. System will:
   - Mark all timetable entries as published
   - Send notification to all students
   - Make schedule visible on student dashboards

### Step 7: Students View Schedule
1. Students log into their dashboard
2. Schedule automatically appears with real-time updates
3. Students see:
   - Complete class schedule sorted by day and period
   - Updated statistics in cards (courses, classes this week, attendance)
   - Notifications about published timetable

## Auto-Refresh Mechanism

### Admin Dashboard
- Timetable list refreshes every 3 seconds
- Ensures admin sees latest changes

### Student Dashboard
- Schedule refreshes every 2 seconds
- Announcements refresh every 5 seconds
- Last updated timestamp updates every second
- Students will see published timetables immediately after admin publishes

## API Endpoints

### Create Timetable Entry
- **POST** `/api/timetable`
- Request body:
  ```json
  {
    "day": "Monday",
    "period": 1,
    "subject": "Mathematics",
    "faculty": "Dr. Smith",
    "room": "A101"
  }
  ```

### Get All Timetable Entries
- **GET** `/api/timetable`
- Returns array of entries with published status

### Delete Timetable Entry
- **DELETE** `/api/timetable/<id>`
- Removes specific entry

### Publish Timetable
- **POST** `/api/timetable/publish`
- Marks all entries as published
- Sends notification to students

### Clear All Entries
- **POST** `/api/timetable/clear`
- Removes all timetable entries (use with caution)

## Notification System

When timetable is published:
- A notification is created: **"📅 Timetable has been published! Your class schedule is now available. Please check your dashboard."**
- Students see this notification in the announcements section
- Notification box is styled as "success" (green background)

## Database Schema

The timetable system uses the following columns:
- `id`: Unique identifier
- `day`: Day of the week (Monday-Saturday)
- `period`: Class period number
- `subject`: Subject name
- `faculty`: Faculty name
- `room`: Classroom/room name
- `published`: Boolean flag (0 = Draft, 1 = Published)

## Best Practices

1. **Verify Data First**: Add all faculty, subjects, and classrooms before creating timetable entries
2. **Review Before Publishing**: Always check the current timetable before publishing
3. **Notify Timing**: Publish during off-peak hours if possible to minimize load
4. **Update Management**: To update entries, delete and recreate them
5. **Backup**: Keep backups of timetable data before major changes

## Troubleshooting

### Timetable not showing on student dashboard
- Check if timetable entries are marked as "Published"
- Try refreshing the student dashboard (F5)
- Verify database connection is active

### Students not seeing updates
- Dashboard auto-refreshes every 2 seconds
- Manual refresh (F5) can help
- Check browser console for any JavaScript errors

### Admin dashboard not updating
- Admin timetable list refreshes every 3 seconds
- Manual refresh (F5) recommended

### Error when publishing
- Verify database connection is active
- Check if there are timetable entries to publish
- Review browser console for specific error messages

## Support

For issues or questions:
1. Check the browser console for error messages
2. Verify database connectivity
3. Restart the Flask application
4. Check that all required fields are populated

---

**Last Updated**: January 2026
**Version**: 1.0

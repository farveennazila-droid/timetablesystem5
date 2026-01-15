# Database Connection Troubleshooting

## Current Status
The app is running, but the database connection is failing because **MySQL is not set up**.

## Quick Fix - Initialize Database

### Step 1: Make sure MySQL is running
- **Windows**: Open Services (services.msc) and start "MySQL80" or similar
- **Or**: Start MySQL from MySQL Command Line Client

### Step 2: Run the database initialization script
From the backend directory, run:

```powershell
cd backend
..\venv\Scripts\Activate.ps1  # Activate virtual environment if not already
python init_db.py
```

This will:
✓ Create the `timetable_db` database
✓ Create all required tables
✓ Insert a default admin user (username: admin, password: admin)

### Step 3: Test the connection
```powershell
python test_connection.py
```

## Alternative - Manual Database Setup

If you prefer to set up manually:

1. Open MySQL Command Line Client
2. Run the SQL commands from `database/schema.sql`
3. Run the SQL commands from `database/sample_data.sql`

## Check Connection Status

Visit: `http://127.0.0.1:5000/health`

Should return:
```json
{
  "status": "ok",
  "database": "connected"
}
```

## Common Errors

**Error: "Cannot connect to MySQL server"**
- MySQL is not running. Start it from Services or MySQL Command Line Client

**Error: "Unknown database 'timetable_db'"**
- Run `python init_db.py` to create the database

**Error: "Access denied for user 'root'"**
- Wrong password in `db_config.py`
- Update the password in `db_config.py` and try again

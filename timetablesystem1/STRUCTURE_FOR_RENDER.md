# Render-Optimized File Structure

## Project Structure

```
timetable-system/
├── app.py                          # ⭐ Root entry point for Render
├── requirements.txt                 # ⭐ Root-level dependencies
├── runtime.txt                      # ⭐ Python version for Render
├── render.yaml                      # ⭐ Render configuration
├── Procfile                         # ⭐ Process file for Render
├── build.sh                         # Build script
├── .gitignore                       # Git exclusions
├── .env.example                     # Environment template
│
├── backend/                         # Flask application
│   ├── app.py                       # Main Flask app (imported by root app.py)
│   ├── db_config.py                 # Database configuration (uses env vars)
│   ├── requirements.txt             # Backend dependencies (copied to root)
│   ├── .env                         # NOT in git (local only)
│   ├── .env.example                 # Template for env vars
│   │
│   └── frontend/
│       ├── html/
│       │   ├── login.html
│       │   ├── admin.html
│       │   ├── student_dashboard.html
│       │   ├── dashboard.html
│       │   ├── public_timetable.html
│       │   └── ...
│       │
│       └── static/
│           ├── css/
│           │   ├── dashboard.css
│           │   ├── login.css
│           │   └── style.css
│           │
│           └── js/
│               ├── dashboard.js
│               ├── login.js
│               └── script.js
│
├── database/
│   ├── schema.sql                   # Database schema
│   ├── sample_data.sql              # Sample data
│   └── setup.sql
│
├── Documentation files (*.md)
│   ├── README.md                    # Main documentation
│   ├── RENDER_DEPLOYMENT.md         # ⭐ Render-specific guide
│   ├── DEPLOYMENT_GUIDE.md          # Other platforms
│   ├── GitHub_Setup.md
│   ├── FINAL_VERIFICATION.md
│   └── ...

```

## Key Changes for Render

### 1. Root-Level Entry Point
**File**: `app.py` (in root)
```python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
from app import app  # Import backend app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
```

### 2. Root-Level Requirements
**File**: `requirements.txt` (in root)
- Contains all dependencies
- Includes `python-dotenv` for environment variables
- Includes `gunicorn` for production server

### 3. Render Configuration
**File**: `render.yaml`
- Specifies build command
- Specifies start command
- Defines environment variables
- Configurable for MySQL add-on

### 4. Environment Variables Support
**Files**: `backend/db_config.py`, `backend/app.py`
- Uses `python-dotenv` to load `.env`
- Reads from environment variables:
  - `DB_HOST`
  - `DB_USER`
  - `DB_PASSWORD`
  - `DB_NAME`
  - `DB_PORT`

### 5. Python Version Specification
**File**: `runtime.txt`
```
python-3.12.0
```

## Deployment Flow

1. **Push to GitHub**
   ```bash
   git push origin main
   ```

2. **Render Detects Changes**
   - Sees `render.yaml`
   - Reads configuration

3. **Build Phase**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start Phase**
   ```bash
   gunicorn app:app --bind 0.0.0.0:$PORT
   ```

5. **Application Runs**
   - Root `app.py` starts
   - Imports backend `app.py`
   - Flask app runs on port 5000 (or assigned PORT)

## Environment Variables

Set these in Render dashboard:

| Variable | Value | Example |
|----------|-------|---------|
| DB_HOST | Database host | db.xxxxx.cloud.render.com |
| DB_USER | Database user | admin |
| DB_PASSWORD | Database password | strong-password-here |
| DB_NAME | Database name | timetable_db |
| DB_PORT | Database port | 3306 |
| FLASK_ENV | production | production |
| FLASK_DEBUG | False | False |

## Local Development

For local testing with same structure:

```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file
cp backend/.env.example .env
# Edit .env with your local credentials

# Run app
python app.py
# Visit http://localhost:5000
```

## File Structure Benefits

✅ Root entry point for easy Render deployment
✅ Environment variables properly managed
✅ Backend logic separated but accessible
✅ Static files and templates properly pathed
✅ Production-ready with gunicorn
✅ Easy to debug and maintain

## Testing on Render

After deployment:

1. Health check: `https://your-app.onrender.com/health`
2. Login: `https://your-app.onrender.com`
3. Admin: `https://your-app.onrender.com/admin`
4. API: `https://your-app.onrender.com/api/faculty`

## Troubleshooting

### Port Issues
- Render assigns PORT env variable
- App reads: `port = int(os.environ.get("PORT", 5000))`
- Must bind to `0.0.0.0`

### Path Issues
- Root `app.py` adds `backend` to Python path
- Templates/static paths in Flask are relative to backend/frontend

### Environment Variables
- Must be set in Render dashboard
- Not read from `.env` in production (only local)
- Check Render environment tab if values not working

---

**Structure optimized for Render deployment!**

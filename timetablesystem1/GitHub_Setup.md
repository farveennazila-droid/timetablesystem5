# Hosting on GitHub

## Step 1: Create GitHub Repository

1. Go to [GitHub.com](https://github.com)
2. Click **New repository** (or use the **+** menu)
3. Name it: `timetable-system`
4. Choose **Public** or **Private**
5. **Do NOT** initialize with README (we have one)
6. Click **Create repository**

## Step 2: Initialize Git Locally

Open PowerShell in your project folder (`f:\timetablesystem1`) and run:

```powershell
git init
git add .
git commit -m "Initial commit: Complete timetable management system"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/timetable-system.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username.

## Step 3: Verify Files Are Excluded

Check that sensitive files are NOT pushed:
- `.env` - Should be excluded ✓
- `__pycache__/` - Should be excluded ✓
- `.venv/` - Should be excluded ✓

To verify:
```powershell
git status
```

None of the excluded files should appear.

## Step 4: Add .env to GitHub (Template Only)

Create `backend/.env.example` for reference:

```
DB_HOST=127.0.0.1
DB_USER=root
DB_PASSWORD=your_password_here
DB_NAME=timetable_db
DB_PORT=3306
FLASK_ENV=production
FLASK_DEBUG=False
```

Push this file so developers know what env variables to set.

## Step 5: Update GitHub Repository Settings

1. Go to **Settings** → **Secrets and variables** → **Codespaces**
2. Add secrets for:
   - `DB_HOST`
   - `DB_USER`
   - `DB_PASSWORD`
   - `DB_NAME`

(These will be used for CI/CD if you add GitHub Actions)

## Step 6: Add Branch Protection (Optional)

1. Go to **Settings** → **Branches**
2. Add rule for `main` branch
3. Require pull request reviews before merging

## Useful Git Commands

```powershell
# Check status
git status

# See commit history
git log --oneline

# Create a new branch for features
git checkout -b feature/new-feature
git push -u origin feature/new-feature

# Push changes
git add .
git commit -m "Your message"
git push

# Pull changes
git pull
```

## GitHub Pages (Optional - For Documentation)

If you want to host documentation:
1. Go to **Settings** → **Pages**
2. Select `main` branch
3. Documentation will be available at: `https://your-username.github.io/timetable-system/`

## Next: Deploy to Live Server

After pushing to GitHub, you can deploy to hosting providers like:
- **Heroku** - Easy Flask hosting
- **PythonAnywhere** - Python-specific hosting
- **AWS EC2** - Full control
- **DigitalOcean** - Affordable VPS
- **Render** - Modern deployment platform

See `DEPLOYMENT_GUIDE.md` for detailed deployment instructions.

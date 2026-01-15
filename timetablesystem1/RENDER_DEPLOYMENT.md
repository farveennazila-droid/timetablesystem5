# Deploying to Render

This guide walks through deploying the Timetable Management System to Render.

## Prerequisites

1. GitHub account with your repo pushed
2. Render account (create at render.com)
3. MySQL database (external or Render MySQL)

## Step 1: Push to GitHub

Make sure your code is pushed to GitHub:

```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

## Step 2: Create Render Account

1. Go to [render.com](https://render.com)
2. Sign up with GitHub account
3. Authorize Render to access your repositories

## Step 3: Deploy Web Service

1. Click **New** → **Web Service**
2. Select your `timetable-system` repository
3. Configure:
   - **Name**: `timetable-system`
   - **Environment**: Python 3.12
   - **Region**: Select closest region
   - **Branch**: `main`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT`
   - **Plan**: Free (or paid for better uptime)

## Step 4: Configure Environment Variables

In Render dashboard:
1. Go to **Environment**
2. Add these variables:

```
DB_HOST=your-database-host
DB_USER=your-database-user
DB_PASSWORD=your-database-password
DB_NAME=timetable_db
DB_PORT=3306
FLASK_ENV=production
FLASK_DEBUG=False
```

## Step 5: Setup Database

### Option A: Use Render MySQL (Recommended)

1. In Render, click **New** → **MySQL**
2. Choose plan and region
3. Create database
4. Copy connection details
5. Paste into environment variables above
6. Run migrations:

```bash
mysql -h <host> -u <user> -p <password> < database/schema.sql
```

### Option B: Use External Database

Use your existing MySQL database credentials in environment variables.

## Step 6: Deploy

1. Click **Deploy**
2. Wait for build and deployment to complete
3. Your app will be available at: `https://timetable-system.onrender.com`

## Step 7: Initialize Database

After first deployment:

1. SSH into Render (or use external MySQL tool)
2. Run schema setup:

```bash
mysql -h <host> -u <user> -p
CREATE DATABASE timetable_db;
USE timetable_db;
-- Run schema.sql content
```

## Access Your App

- **Admin Dashboard**: `https://timetable-system.onrender.com/admin`
- **Student Dashboard**: `https://timetable-system.onrender.com`
- **Login**: Use default credentials (change in production!)

## Troubleshooting

### Build Fails

Check build logs in Render dashboard:
1. Go to **Deployments** tab
2. Click on failed deployment
3. View logs to see error

Common issues:
- Missing dependencies → Update requirements.txt
- Wrong Python version → Specify in runtime.txt
- Environment variables missing → Check Render environment tab

### Database Connection Error

1. Verify DB credentials in environment variables
2. Test connection: `mysql -h <host> -u <user> -p`
3. Ensure database exists: `SHOW DATABASES;`
4. Check firewall allows connection

### Static Files Not Loading

1. Ensure `frontend/static/` directory exists
2. Check Render logs for 404 errors
3. Verify paths in Flask app

### Slow Performance

- Use paid plan for better resources
- Enable caching
- Optimize database queries
- Use CDN for static files

## Monitoring

### View Logs

In Render dashboard:
1. Go to **Logs** tab
2. Filter by service
3. Search for errors

### Performance Monitoring

1. Check **Metrics** tab for:
   - CPU usage
   - Memory usage
   - Request rate
   - Response time

## Auto-Deploys

Render automatically deploys when you push to GitHub:

```bash
git add .
git commit -m "Update app"
git push origin main
# Auto-deploy starts within seconds
```

## Scaling

As traffic grows:

1. Upgrade to **Pro** or **Advanced** plan
2. Add more resources
3. Enable horizontal scaling
4. Setup load balancing

## Backup & Recovery

### Database Backups

```bash
# Backup
mysqldump -h <host> -u <user> -p <db> > backup.sql

# Restore
mysql -h <host> -u <user> -p <db> < backup.sql
```

### Code Rollback

In Render:
1. Go to **Deployments**
2. Find previous deployment
3. Click **Redeploy** to go back

## Security

- [ ] Change default credentials
- [ ] Enable HTTPS (automatic on Render)
- [ ] Use strong database password
- [ ] Regularly update dependencies
- [ ] Monitor logs for suspicious activity

## Support

- [Render Docs](https://render.com/docs)
- [Flask Documentation](https://flask.palletsprojects.com)
- Check application logs for errors

---

**Your app is now live on Render! 🚀**

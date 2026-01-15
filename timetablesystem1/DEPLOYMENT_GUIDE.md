# Deployment Guide - Timetable System

## Option 1: Heroku (Easiest)

### Prerequisites
- GitHub account with your repo pushed
- Heroku account (free tier available)
- Heroku CLI installed

### Steps

1. **Create Procfile** in root directory:
```
web: cd backend && python app.py
```

2. **Create runtime.txt**:
```
python-3.12.0
```

3. **Push to GitHub**:
```powershell
git add Procfile runtime.txt
git commit -m "Add Heroku deployment files"
git push
```

4. **Deploy via Heroku Dashboard**:
   - Go to heroku.com → New → Create new app
   - Connect to GitHub
   - Select your `timetable-system` repository
   - Click "Deploy Branch"

5. **Set Environment Variables**:
   - Go to Settings → Config Vars
   - Add: DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

6. **Access Your App**:
   - Heroku provides a URL like: `https://your-app-name.herokuapp.com`

---

## Option 2: PythonAnywhere (Beginner-Friendly)

### Steps

1. Go to [pythonanywhere.com](https://www.pythonanywhere.com)
2. Create account (free tier includes 100MB storage)
3. Click **New console** → **Bash**
4. Clone your repo:
```bash
git clone https://github.com/YOUR_USERNAME/timetable-system.git
cd timetable-system/backend
pip install -r requirements.txt
```

5. Go to **Web** tab → **Add new web app**
   - Choose Python 3.12
   - Choose Flask
   - Point to your `backend/app.py`

6. Configure database connection (add MySQL credentials)

7. Your app runs at: `https://yourusername.pythonanywhere.com`

---

## Option 3: AWS EC2 (Full Control)

### Prerequisites
- AWS account
- EC2 instance running Ubuntu 22.04
- Security group allowing ports 80, 443, 5000

### Steps

1. **SSH into your instance**:
```bash
ssh -i your-key.pem ubuntu@your-instance-ip
```

2. **Install dependencies**:
```bash
sudo apt update
sudo apt install python3-pip mysql-server git -y
```

3. **Clone repository**:
```bash
git clone https://github.com/YOUR_USERNAME/timetable-system.git
cd timetable-system/backend
pip install -r requirements.txt
```

4. **Create `.env` file**:
```bash
nano .env
# Add your database credentials
```

5. **Run with Gunicorn** (production server):
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

6. **Setup Nginx reverse proxy** (optional but recommended):
```bash
sudo apt install nginx -y
sudo systemctl start nginx
# Configure nginx to forward requests to gunicorn
```

7. **Use systemd service** (auto-restart):
Create `/etc/systemd/system/timetable.service`:
```ini
[Unit]
Description=Timetable System
After=network.target

[Service]
Type=notify
User=ubuntu
WorkingDirectory=/home/ubuntu/timetable-system/backend
ExecStart=/usr/bin/python3 -m gunicorn -w 4 -b 127.0.0.1:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl daemon-reload
sudo systemctl start timetable
sudo systemctl enable timetable
```

---

## Option 4: DigitalOcean (Affordable VPS)

### Steps

1. Create DigitalOcean account
2. Create Droplet (Ubuntu 22.04, $5/month)
3. SSH in and follow **Option 3: AWS EC2** steps
4. Use DigitalOcean's App Platform for easier deployment:
   - Connect GitHub repo
   - Set environment variables
   - One-click deploy

---

## Option 5: Render (Modern & Simple)

### Steps

1. Go to [render.com](https://render.com)
2. Connect GitHub account
3. Create **New** → **Web Service**
4. Select your repository
5. Configure:
   - **Runtime**: Python 3.12
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `cd backend && python app.py`
6. Add environment variables
7. Deploy

---

## Post-Deployment Checklist

- [ ] Test login functionality
- [ ] Add faculty, classroom, subject
- [ ] Create and publish timetable
- [ ] Verify student dashboard sync
- [ ] Check admin notifications
- [ ] Monitor logs for errors
- [ ] Setup automated backups for database
- [ ] Enable HTTPS/SSL certificate
- [ ] Add custom domain (if applicable)

---

## Monitoring & Maintenance

### View Logs
```bash
# Heroku
heroku logs --tail

# AWS/DigitalOcean
sudo tail -f /var/log/timetable.log

# PythonAnywhere
Check Web tab → Error log
```

### Update Code
```bash
cd timetable-system
git pull
pip install -r backend/requirements.txt
# Restart service
```

### Database Backups
```bash
# MySQL dump
mysqldump -u root -p timetable_db > backup.sql

# Restore
mysql -u root -p timetable_db < backup.sql
```

---

## Troubleshooting

**Problem**: Database connection refused
- **Solution**: Verify DB_HOST, DB_USER, DB_PASSWORD in .env
- Check MySQL is running on server

**Problem**: Port 5000 already in use
- **Solution**: Change port or kill existing process
```bash
lsof -i :5000  # See what's using port
kill -9 <PID>  # Kill the process
```

**Problem**: Static files not loading
- **Solution**: Check FLASK_ENV=production and static folder path

**Problem**: CORS errors
- **Solution**: Update CORS settings in app.py or frontend domain

---

## Security Best Practices

1. ✅ Use `.env` for credentials (never commit to git)
2. ✅ Enable HTTPS/SSL
3. ✅ Set strong database passwords
4. ✅ Use database backups
5. ✅ Monitor server logs
6. ✅ Keep dependencies updated
7. ✅ Use firewall rules to restrict access
8. ✅ Enable 2FA on GitHub and hosting accounts

---

## Next Steps

- Monitor uptime and performance
- Plan scalability (more servers, caching, CDN)
- Setup automated deployments with GitHub Actions
- Add monitoring/alerting tools
- Schedule regular security audits

# Timetable Management System

A complete web-based timetable management system built with Flask and MySQL. Features real-time synchronization, admin dashboard, and student view with automatic updates.

## 🎯 Features

✅ **Admin Dashboard**
- Faculty management with department tracking
- Classroom management
- Subject management  
- Timetable creation and publishing

✅ **Faculty Management**
- Add/edit/delete faculty members
- Track departments for organizational purposes
- Email integration

✅ **Timetable Management**
- Create timetable entries with day, period, subject, faculty, and room
- Publish timetables to make them live
- Clear all entries when needed
- Notifications when published

✅ **Student Dashboard**
- Real-time automatic sync (every 2 seconds)
- View only published timetables
- Filter by course/classroom
- Notifications for updates

✅ **Real-Time Synchronization**
- Admin changes instantly reflect on student dashboard
- No page refresh needed
- Polling-based architecture (2-5 second intervals)

✅ **Security**
- Login system with user authentication
- Role-based access (Admin/Student)
- Database connection security

## 🛠 Tech Stack

- **Backend**: Python 3.12, Flask, CORS
- **Database**: MySQL/MariaDB
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Real-time**: Client-side polling
- **ORM**: PyMySQL

## 📋 Requirements

- Python 3.12+
- MySQL 5.7+ or MariaDB
- pip (Python package manager)

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/YOUR_USERNAME/timetable-system.git
cd timetable-system
```

### 2. Setup Database
```bash
# Open MySQL
mysql -u root -p

# Run setup script
source database/schema.sql
source database/sample_data.sql
exit
```

### 3. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 4. Configure Environment
Create `backend/.env`:
```
DB_HOST=127.0.0.1
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=timetable_db
DB_PORT=3306
FLASK_ENV=production
FLASK_DEBUG=False
```

### 5. Run Application
```bash
python app.py
```

Visit: `http://localhost:5000`

## 📂 Project Structure

```
timetable-system/
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── db_config.py           # Database configuration
│   ├── requirements.txt       # Python dependencies
│   ├── .env                   # Environment variables (not in git)
│   └── frontend/
│       ├── html/              # HTML templates
│       │   ├── login.html
│       │   ├── admin.html
│       │   ├── student_dashboard.html
│       │   └── ...
│       └── static/
│           ├── css/           # Stylesheets
│           └── js/            # JavaScript files
├── database/
│   ├── schema.sql             # Database structure
│   ├── sample_data.sql        # Sample data
│   └── setup.sql              # Database setup
├── .gitignore                 # Git exclusions
├── GitHub_Setup.md            # GitHub hosting guide
├── DEPLOYMENT_GUIDE.md        # Deployment instructions
└── README.md                  # This file
```

## 🔑 Default Credentials

**Login Credentials** (from sample data):
- Admin: `admin` / `password`
- Student: `student` / `password`

⚠️ **Important**: Change these in production!

## 📖 Usage

### Admin Panel
1. Login with admin credentials
2. Navigate to **Manage Faculty** to add departments
3. Add classrooms and subjects
4. Create timetable entries
5. Click **Publish Timetable** to make live
6. View notifications for confirmations

### Student Panel
1. Login with student credentials
2. View published timetables
3. Auto-refresh every 2 seconds for updates
4. Filter by course or classroom

## 🔄 API Endpoints

### Faculty Management
- `GET /api/faculty` - Get all faculty
- `POST /api/faculty` - Add new faculty
- `DELETE /api/faculty/<id>` - Delete faculty

### Classroom Management
- `GET /api/classrooms` - Get all classrooms
- `POST /api/classrooms` - Add new classroom
- `DELETE /api/classrooms/<id>` - Delete classroom

### Timetable Management
- `GET /api/timetable` - Get all timetable entries
- `POST /api/timetable` - Add timetable entry
- `POST /api/timetable/publish` - Publish all entries
- `DELETE /api/timetable/<id>` - Delete entry

### Other
- `GET /health` - Health check endpoint
- `GET /api/notifications` - Get notifications

## 📱 Real-Time Features

The system uses **client-side polling** to keep dashboards synchronized:

- **Admin Dashboard**: Refreshes every 3 seconds
- **Student Dashboard**: Refreshes every 2 seconds
- **Announcements**: Refreshes every 5 seconds
- **Timestamp**: Updates every 1 second

No WebSocket or external services required!

## 🔐 Security Notes

1. **Never commit `.env` file** to version control
2. Use strong database passwords
3. Change default credentials before deployment
4. Enable HTTPS in production
5. Implement rate limiting for API endpoints
6. Regular database backups

## 📦 Deployment

Multiple hosting options available:

- **Render** - Recommended, free tier available (see [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md))
- **Heroku** - Easy setup (see DEPLOYMENT_GUIDE.md)
- **PythonAnywhere** - Python-specific hosting
- **AWS EC2** - Full control and scalability
- **DigitalOcean** - Affordable VPS

👉 **For Render: See [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md)**
👉 **For other platforms: See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)**

## 📝 Database Schema

### Faculty Table
```sql
CREATE TABLE faculty (
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(100),
  department VARCHAR(100),
  email VARCHAR(100)
);
```

### Classroom Table
```sql
CREATE TABLE classroom (
  id INT PRIMARY KEY AUTO_INCREMENT,
  room_number VARCHAR(50),
  capacity INT,
  location VARCHAR(100)
);
```

### Timetable Table
```sql
CREATE TABLE timetable (
  id INT PRIMARY KEY AUTO_INCREMENT,
  day VARCHAR(20),
  period INT,
  subject VARCHAR(100),
  faculty VARCHAR(100),
  room VARCHAR(50),
  published TINYINT(1) DEFAULT 0
);
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit changes (`git commit -m 'Add new feature'`)
4. Push to branch (`git push origin feature/new-feature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Troubleshooting

### MySQL Connection Error
- Ensure MySQL is running
- Check DB_HOST, DB_USER, DB_PASSWORD in `.env`
- Verify database exists: `timetable_db`

### Static Files Not Loading
- Check `FLASK_ENV=production` in `.env`
- Verify `frontend/static/` folder exists
- Clear browser cache

### Real-Time Updates Not Working
- Check browser console for JavaScript errors
- Verify `/api/timetable` endpoint returns data
- Check network tab in DevTools

### Port Already in Use
```bash
# Windows PowerShell
Get-Process -Id (Get-NetTCPConnection -LocalPort 5000).OwningProcess | Stop-Process -Force

# Linux/Mac
lsof -i :5000
kill -9 <PID>
```

## 📞 Support

For issues or questions:
1. Check [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
2. Review [GitHub_Setup.md](GitHub_Setup.md)
3. Check application logs
4. Open a GitHub issue

## 🎓 Educational

This project is ideal for:
- Learning Flask web development
- Understanding database design
- Real-time web application architecture
- Git and GitHub workflows
- Web hosting and deployment

---

**Happy coding! 🚀**

*Last updated: January 14, 2026*

// Initialize chart after page loads
let dashboardChart = null;

document.addEventListener('DOMContentLoaded', function() {
    showDashboard();
    
    const ctx = document.getElementById('chart');
    if (!ctx) {
        console.error('Canvas element not found');
        return;
    }
    
    // Check if Chart.js loaded
    if (typeof Chart === 'undefined') {
        console.error('Chart.js library not loaded. Skipping chart initialization.');
        console.log('Continuing with data loading...');
    } else {
        const chartContext = ctx.getContext('2d');
        
        dashboardChart = new Chart(chartContext, {
            type: 'bar',
            data: {
                labels: ['Faculty', 'Subjects', 'Rooms', 'Timetables'],
                datasets: [{
                    label: 'Count',
                    data: [0, 0, 0, 0],
                    backgroundColor: '#4CAF50',
                    borderColor: '#45a049',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }
    
    // Load dashboard statistics
    loadDashboardStats();
    
    // Load notifications
    loadNotifications();
});

function showDashboard() {
    document.getElementById('dashboard-view').style.display = 'block';
    document.getElementById('timetable-view').style.display = 'none';
}

function showGenerateTimetable() {
    document.getElementById('dashboard-view').style.display = 'none';
    document.getElementById('timetable-view').style.display = 'block';
}

function generateTimetable() {
    let days = document.getElementById("days").value;
    let periods = document.getElementById("periods").value;

    if (days == "" || periods == "") {
        alert("Please fill all fields");
        return;
    }

    fetch("/generate", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            days: parseInt(days),
            periods: parseInt(periods)
        })
    })
    .then(response => response.json())
    .then(data => {
        let output = "<table border='1'><tr><th>Day / Period</th>";

        for (let p = 1; p <= periods; p++) {
            output += "<th>P" + p + "</th>";
        }
        output += "</tr>";

        for (let day in data) {
            output += "<tr><th>" + day + "</th>";
            for (let subject of data[day]) {
                output += "<td>" + subject + "</td>";
            }
            output += "</tr>";
        }

        output += "</table>";
        document.getElementById("output").innerHTML = output;
        // show publish button after generation
        const pubBtn = document.getElementById('publish-btn');
        if (pubBtn) pubBtn.style.display = 'inline-block';
    })
    .catch(error => {
        console.error("Error:", error);
        alert("Failed to generate timetable");
    });
}

function publishTimetable() {
    if (!confirm('Publish the current timetable to all users?')) return;
    fetch('/api/timetable/publish', { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify({}) })
        .then(r => r.json())
        .then(j => {
            if (j.status === 'success') {
                alert('Timetable published');
                // hide publish button
                const pubBtn = document.getElementById('publish-btn');
                if (pubBtn) pubBtn.style.display = 'none';
            } else {
                alert('Publish failed: ' + (j.message || ''));
            }
        })
        .catch(err => { console.error(err); alert('Error publishing timetable'); });
}

function loadDashboardStats() {
    fetch('/api/dashboard')
        .then(response => {
            console.log('API Response Status:', response.status);
            return response.json();
        })
        .then(data => {
            console.log('Dashboard data received:', data);
            document.getElementById('faculty-count').textContent = data.faculty !== undefined ? data.faculty : 0;
            document.getElementById('subject-count').textContent = data.subjects !== undefined ? data.subjects : 0;
            document.getElementById('room-count').textContent = data.rooms !== undefined ? data.rooms : 0;
            document.getElementById('timetable-count').textContent = data.timetables !== undefined ? data.timetables : 0;
            
            // Update chart with real data
            if (dashboardChart) {
                dashboardChart.data.datasets[0].data = [
                    data.faculty || 0,
                    data.subjects || 0,
                    data.rooms || 0,
                    data.timetables || 0
                ];
                dashboardChart.update();
            }
        })
        .catch(error => {
            console.error('Error loading dashboard stats:', error);
            document.getElementById('faculty-count').textContent = '0';
            document.getElementById('subject-count').textContent = '0';
            document.getElementById('room-count').textContent = '0';
            document.getElementById('timetable-count').textContent = '0';
        });
}

function loadNotifications() {
    fetch('/notifications')
        .then(response => response.json())
        .then(data => {
            const notificationList = document.getElementById('notifications');
            if (notificationList) {
                notificationList.innerHTML = '';
                if (Array.isArray(data) && data.length > 0) {
                    data.forEach(notification => {
                        const li = document.createElement('li');
                        li.textContent = notification.message || notification;
                        notificationList.appendChild(li);
                    });
                } else {
                    notificationList.innerHTML = '<li>No notifications</li>';
                }
            }
        })
        .catch(error => {
            console.error('Error loading notifications:', error);
            document.getElementById('notifications').innerHTML = '<li>No notifications</li>';
        });
}

function logout() {
    window.location.href = "/";
}
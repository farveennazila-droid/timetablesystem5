import pymysql
db = pymysql.connect(host='127.0.0.1', user='root', password='nazila', database='timetable_db', charset='utf8mb4')
c = db.cursor()
c.execute("SHOW COLUMNS FROM timetable")
print("Timetable columns:")
for row in c.fetchall():
    print(" -", row[0])
c.close()
db.close()

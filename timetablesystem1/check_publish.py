import pymysql
db = pymysql.connect(host='127.0.0.1', user='root', password='nazila', database='timetable_db', charset='utf8mb4')
c = db.cursor()
c.execute("SELECT COUNT(*) FROM timetable WHERE published=1")
count = c.fetchone()[0]
print(f"Published timetable rows: {count}")
c.execute("SELECT COUNT(*) FROM timetable")
total = c.fetchone()[0]
print(f"Total timetable rows: {total}")
c.close()
db.close()

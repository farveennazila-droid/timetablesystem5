-- Insert Sample Faculty Data
INSERT INTO faculty (name, department, email) VALUES
('Dr. John Smith', 'Computer Science', 'john.smith@university.edu'),
('Dr. Jane Doe', 'Mathematics', 'jane.doe@university.edu'),
('Dr. Mike Wilson', 'Physics', 'mike.wilson@university.edu'),
('Prof. Sarah Johnson', 'English', 'sarah.johnson@university.edu'),
('Dr. Robert Brown', 'Chemistry', 'robert.brown@university.edu'),
('Dr. Emily Davis', 'Biology', 'emily.davis@university.edu');

-- Insert Sample Classroom Data
INSERT INTO classroom (room_number, capacity, location) VALUES
('A101', 30, 'Building A - Ground Floor'),
('A102', 30, 'Building A - Ground Floor'),
('A201', 25, 'Building A - First Floor'),
('B201', 40, 'Building B - First Floor'),
('B202', 40, 'Building B - First Floor'),
('C301', 50, 'Building C - Third Floor'),
('C302', 50, 'Building C - Third Floor'),
('D105', 35, 'Building D - Ground Floor');

-- View inserted data
SELECT COUNT(*) as Total_Faculty FROM faculty;
SELECT COUNT(*) as Total_Classrooms FROM classroom;

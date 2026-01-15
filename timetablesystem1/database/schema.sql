CREATE DATABASE timetable_db;
USE timetable_db;

CREATE TABLE faculty (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100),
  department VARCHAR(100),
  email VARCHAR(100)
);

CREATE TABLE classroom (
  room_id INT AUTO_INCREMENT PRIMARY KEY,
  room_name VARCHAR(100),
  capacity INT,
  location VARCHAR(100)
);

CREATE TABLE subject (
  id INT AUTO_INCREMENT PRIMARY KEY,
  subject_name VARCHAR(100),
  code VARCHAR(50)
);

CREATE TABLE admin (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(100),
  password VARCHAR(100)
);

CREATE TABLE notification (
  id INT AUTO_INCREMENT PRIMARY KEY,
  message VARCHAR(500),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE timetable (
  id INT AUTO_INCREMENT PRIMARY KEY,
  day VARCHAR(20),
  period INT,
  subject VARCHAR(100),
  faculty VARCHAR(100),
  room VARCHAR(50),
  published TINYINT(1) NOT NULL DEFAULT 0
);
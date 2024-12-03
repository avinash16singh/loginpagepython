# loginpagepython

# THIS IS DATABASE CONNECT OF THAT PROGRAM

//
DROP DATABASE IF EXISTS acadmic_db;
CREATE DATABASE acadmic_db;
USE acadmic_db;

CREATE TABLE admin (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(50) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(15) NOT NULL,
    reg_no VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE acadmic_dbs (
    entry_id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    Username VARCHAR(255) NOT NULL,
    age INT NOT NULL,
    gender VARCHAR(10) NOT NULL,
    Current_school_Level VARCHAR(255) NOT NULL,
    Grades VARCHAR(255) NOT NULL,
    Average_Hours_Spent_Studying_per_Day INT NOT NULL,
    Preferred_Study_Methods VARCHAR(255) NOT NULL,
    Attendance_Rate INT NOT NULL,
    Engagement_Level_in_Class INT NOT NULL,
    Primary_Motivation_for_Studying VARCHAR(255) NOT NULL,
    Future_Career_Goals VARCHAR(255) NOT NULL,
    submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
//

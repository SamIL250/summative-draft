# CREATE DATABASE IF NOT EXISTS learntrack;
# USE learntrack;

# -- Students Table
# CREATE TABLE students (
#     student_id INT PRIMARY KEY AUTO_INCREMENT,
#     first_name VARCHAR(50) NOT NULL,
#     last_name VARCHAR(50) NOT NULL,
#     email VARCHAR(100) UNIQUE NOT NULL,
#     phone VARCHAR(15),
#     date_of_birth DATE,
#     enrollment_date DATE DEFAULT (CURRENT_DATE),
#     status ENUM('active', 'inactive', 'graduated') DEFAULT 'active',
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# );

# -- Courses Table
# CREATE TABLE courses (
#     course_id INT PRIMARY KEY AUTO_INCREMENT,
#     course_code VARCHAR(20) UNIQUE NOT NULL,
#     course_name VARCHAR(100) NOT NULL,
#     credits INT DEFAULT 3,
#     description TEXT
# );

# -- Academic Records Table
# CREATE TABLE academic_records (
#     record_id INT PRIMARY KEY AUTO_INCREMENT,
#     student_id INT NOT NULL,
#     course_id INT NOT NULL,
#     semester VARCHAR(20),
#     grade VARCHAR(5),
#     score DECIMAL(5,2),
#     year INT,
#     remarks TEXT,
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
#     FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE
# );

# -- Attendance Table
# CREATE TABLE attendance (
#     attendance_id INT PRIMARY KEY AUTO_INCREMENT,
#     student_id INT NOT NULL,
#     course_id INT NOT NULL,
#     attendance_date DATE NOT NULL,
#     status ENUM('present', 'absent', 'late', 'excused') NOT NULL,
#     remarks TEXT,
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
#     FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE
# );

# -- Documents Table
# CREATE TABLE documents (
#     document_id INT PRIMARY KEY AUTO_INCREMENT,
#     student_id INT NOT NULL,
#     document_type VARCHAR(50) NOT NULL,
#     document_name VARCHAR(200) NOT NULL,
#     file_path VARCHAR(500),
#     upload_date DATE DEFAULT (CURRENT_DATE),
#     description TEXT,
#     FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
# );

# -- Learning Outcomes Table
# CREATE TABLE learning_outcomes (
#     outcome_id INT PRIMARY KEY AUTO_INCREMENT,
#     student_id INT NOT NULL,
#     course_id INT NOT NULL,
#     outcome_description TEXT NOT NULL,
#     achievement_level ENUM('not_met', 'partially_met', 'met', 'exceeded') NOT NULL,
#     assessment_date DATE,
#     notes TEXT,
#     FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
#     FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE
# );


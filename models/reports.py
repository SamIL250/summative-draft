from database.connection import DatabaseConnection
from tabulate import tabulate

class Reports:
    def __init__(self):
        self.db = DatabaseConnection()
        self.db.connect()
    
    def generate_student_report(self, student_id):
        """Generate comprehensive performance report for a student"""
        # Get student info
        student_query = "SELECT * FROM students WHERE student_id = %s"
        student = self.db.fetch_one(student_query, (student_id,))
        
        if not student:
            print(f"Student {student_id} not found!")
            return
        
        print("\n" + "="*80)
        print("                    STUDENT PERFORMANCE REPORT")
        print("="*80)
        print(f"\nStudent ID: {student['student_id']}")
        print(f"Name: {student['first_name']} {student['last_name']}")
        print(f"Email: {student['email']}")
        print(f"Status: {student['status']}")
        print(f"Enrollment Date: {student['enrollment_date']}")
        print("\n" + "-"*80)
        
        # Academic Performance
        academic_query = """
        SELECT 
            COUNT(*) as total_courses,
            AVG(score) as avg_score,
            MAX(score) as highest_score,
            MIN(score) as lowest_score
        FROM academic_records
        WHERE student_id = %s
        """
        academic = self.db.fetch_one(academic_query, (student_id,))
        
        if academic and academic['total_courses'] > 0:
            gpa = (academic['avg_score'] / 100) * 4.0
            
            print("\n ACADEMIC PERFORMANCE")
            print(f"Total Courses Completed: {academic['total_courses']}")
            print(f"Average Score: {academic['avg_score']:.2f}%")
            print(f"GPA (4.0 scale): {gpa:.2f}")
            print(f"Highest Score: {academic['highest_score']:.2f}%")
            print(f"Lowest Score: {academic['lowest_score']:.2f}%")
        else:
            print("\n ACADEMIC PERFORMANCE")
            print("No academic records available")
        
        # Attendance
        attendance_query = """
        SELECT 
            COUNT(*) as total_classes,
            SUM(CASE WHEN status = 'present' THEN 1 ELSE 0 END) as present,
            ROUND((SUM(CASE WHEN status = 'present' THEN 1 ELSE 0 END) / COUNT(*)) * 100, 2) as percentage
        FROM attendance
        WHERE student_id = %s
        """
        attendance = self.db.fetch_one(attendance_query, (student_id,))
        
        print("\n ATTENDANCE")
        if attendance and attendance['total_classes'] > 0:
            print(f"Total Classes: {attendance['total_classes']}")
            print(f"Classes Attended: {attendance['present']}")
            print(f"Attendance Rate: {attendance['percentage']:.2f}%")
            
            if attendance['percentage'] >= 90:
                print("Status: ✓ Excellent Attendance")
            elif attendance['percentage'] >= 75:
                print("Status: ✓ Good Attendance")
            else:
                print("Status: ⚠ Poor Attendance - Needs Improvement")
        else:
            print("No attendance records available")
        
        # Learning Outcomes
        outcomes_query = """
        SELECT 
            achievement_level,
            COUNT(*) as count
        FROM learning_outcomes
        WHERE student_id = %s
        GROUP BY achievement_level
        """
        outcomes = self.db.fetch_all(outcomes_query, (student_id,))
        
        print("\n LEARNING OUTCOMES")
        if outcomes:
            total_outcomes = sum(o['count'] for o in outcomes)
            print(f"Total Outcomes Assessed: {total_outcomes}")
            
            for outcome in outcomes:
                percentage = (outcome['count'] / total_outcomes) * 100
                print(f"  {outcome['achievement_level']}: {outcome['count']} ({percentage:.1f}%)")
        else:
            print("No learning outcomes assessed")
        
        # Documents
        docs_query = "SELECT COUNT(*) as doc_count FROM documents WHERE student_id = %s"
        docs = self.db.fetch_one(docs_query, (student_id,))
        
        print("\n DOCUMENTS")
        print(f"Total Documents on File: {docs['doc_count'] if docs else 0}")
        
        print("\n" + "="*80)
        
        # Overall Assessment
        print("\n OVERALL ASSESSMENT")
        if academic and academic['total_courses'] > 0:
            gpa = (academic['avg_score'] / 100) * 4.0
            att_pct = attendance['percentage'] if attendance and attendance['total_classes'] > 0 else 0
            
            if gpa >= 3.5 and att_pct >= 90:
                print("✓ EXCELLENT - Student is performing exceptionally well")
            elif gpa >= 3.0 and att_pct >= 75:
                print("✓ GOOD - Student is performing well")
            elif gpa >= 2.5 and att_pct >= 60:
                print("⚠ SATISFACTORY - Student meets minimum requirements")
            else:
                print("⚠ NEEDS IMPROVEMENT - Student requires additional support")
        else:
            print("Insufficient data for overall assessment")
        
        print("="*80)
    
    def generate_course_report(self, course_id):
        """Generate report for a specific course"""
        # Get course info
        course_query = "SELECT * FROM courses WHERE course_id = %s"
        course = self.db.fetch_one(course_query, (course_id,))
        
        if not course:
            print(f"Course {course_id} not found!")
            return
        
        print("\n" + "="*80)
        print("                        COURSE REPORT")
        print("="*80)
        print(f"\nCourse ID: {course['course_id']}")
        print(f"Course Code: {course['course_code']}")
        print(f"Course Name: {course['course_name']}")
        print(f"Credits: {course['credits']}")
        print("\n" + "-"*80)
        
        # Enrollment
        enrollment_query = """
        SELECT COUNT(DISTINCT student_id) as total_students
        FROM academic_records
        WHERE course_id = %s
        """
        enrollment = self.db.fetch_one(enrollment_query, (course_id,))
        
        print(f"\n ENROLLMENT")
        print(f"Total Students Enrolled: {enrollment['total_students'] if enrollment else 0}")
        
        # Academic Performance
        performance_query = """
        SELECT 
            AVG(score) as avg_score,
            MAX(score) as highest_score,
            MIN(score) as lowest_score,
            COUNT(CASE WHEN score >= 90 THEN 1 END) as a_count,
            COUNT(CASE WHEN score >= 80 AND score < 90 THEN 1 END) as b_count,
            COUNT(CASE WHEN score >= 70 AND score < 80 THEN 1 END) as c_count,
            COUNT(CASE WHEN score >= 60 AND score < 70 THEN 1 END) as d_count,
            COUNT(CASE WHEN score < 60 THEN 1 END) as f_count
        FROM academic_records
        WHERE course_id = %s
        """
        performance = self.db.fetch_one(performance_query, (course_id,))
        
        if performance and performance['avg_score']:
            print(f"\n ACADEMIC PERFORMANCE")
            print(f"Average Score: {performance['avg_score']:.2f}%")
            print(f"Highest Score: {performance['highest_score']:.2f}%")
            print(f"Lowest Score: {performance['lowest_score']:.2f}%")
            
            print(f"\n GRADE DISTRIBUTION")
            total = (performance['a_count'] + performance['b_count'] + 
                    performance['c_count'] + performance['d_count'] + performance['f_count'])
            
            if total > 0:
                print(f"  A (90-100): {performance['a_count']} ({(performance['a_count']/total)*100:.1f}%)")
                print(f"  B (80-89):  {performance['b_count']} ({(performance['b_count']/total)*100:.1f}%)")
                print(f"  C (70-79):  {performance['c_count']} ({(performance['c_count']/total)*100:.1f}%)")
                print(f"  D (60-69):  {performance['d_count']} ({(performance['d_count']/total)*100:.1f}%)")
                print(f"  F (0-59):   {performance['f_count']} ({(performance['f_count']/total)*100:.1f}%)")
        
        # Attendance
        attendance_query = """
        SELECT 
            COUNT(*) as total_records,
            ROUND(AVG(CASE WHEN status = 'present' THEN 100 ELSE 0 END), 2) as avg_attendance
        FROM attendance
        WHERE course_id = %s
        """
        attendance = self.db.fetch_one(attendance_query, (course_id,))
        
        if attendance and attendance['total_records'] > 0:
            print(f"\n ATTENDANCE")
            print(f"Average Attendance Rate: {attendance['avg_attendance']:.2f}%")
        
        print("\n" + "="*80)
    
    def generate_overall_statistics(self):
        """Generate system-wide statistics"""
        print("\n" + "="*80)
        print("                    OVERALL SYSTEM STATISTICS")
        print("="*80)
        
        # Student Statistics
        student_query = """
        SELECT 
            COUNT(*) as total,
            COUNT(CASE WHEN status = 'active' THEN 1 END) as active,
            COUNT(CASE WHEN status = 'inactive' THEN 1 END) as inactive,
            COUNT(CASE WHEN status = 'graduated' THEN 1 END) as graduated
        FROM students
        """
        students = self.db.fetch_one(student_query)
        
        print("\n STUDENTS")
        if students:
            print(f"Total Students: {students['total']}")
            print(f"  Active: {students['active']}")
            print(f"  Inactive: {students['inactive']}")
            print(f"  Graduated: {students['graduated']}")
        
        # Course Statistics
        course_query = "SELECT COUNT(*) as total FROM courses"
        courses = self.db.fetch_one(course_query)
        
        print(f"\n COURSES")
        print(f"Total Courses: {courses['total'] if courses else 0}")
        
        # Academic Records
        records_query = """
        SELECT 
            COUNT(*) as total_records,
            AVG(score) as avg_score
        FROM academic_records
        """
        records = self.db.fetch_one(records_query)
        
        print(f"\n ACADEMIC RECORDS")
        if records and records['total_records'] > 0:
            print(f"Total Grade Records: {records['total_records']}")
            print(f"System-wide Average Score: {records['avg_score']:.2f}%")
            print(f"System-wide GPA: {(records['avg_score']/100)*4:.2f}/4.0")
        
        # Attendance
        attendance_query = """
        SELECT 
            COUNT(*) as total_records,
            ROUND(AVG(CASE WHEN status = 'present' THEN 100 ELSE 0 END), 2) as avg_attendance
        FROM attendance
        """
        attendance = self.db.fetch_one(attendance_query)
        
        print(f"\n ATTENDANCE")
        if attendance and attendance['total_records'] > 0:
            print(f"Total Attendance Records: {attendance['total_records']}")
            print(f"System-wide Attendance Rate: {attendance['avg_attendance']:.2f}%")
        
        # Documents
        docs_query = "SELECT COUNT(*) as total FROM documents"
        docs = self.db.fetch_one(docs_query)
        
        print(f"\n DOCUMENTS")
        print(f"Total Documents: {docs['total'] if docs else 0}")
        
        print("\n" + "="*80)
    
    def view_top_performers(self, limit=10):
        """View top performing students"""
        query = """
        SELECT 
            s.student_id,
            s.first_name,
            s.last_name,
            COUNT(ar.record_id) as courses_taken,
            AVG(ar.score) as avg_score,
            ROUND((AVG(ar.score) / 100) * 4, 2) as gpa
        FROM students s
        JOIN academic_records ar ON s.student_id = ar.student_id
        GROUP BY s.student_id, s.first_name, s.last_name
        HAVING courses_taken >= 3
        ORDER BY avg_score DESC
        LIMIT %s
        """
        performers = self.db.fetch_all(query, (limit,))
        
        if performers:
            print(f"\n TOP {limit} PERFORMERS")
            print("="*80)
            headers = performers[0].keys()
            rows = [list(p.values()) for p in performers]
            print(tabulate(rows, headers=headers, tablefmt="grid"))
        else:
            print("No data available")
    
    def view_low_performers(self, threshold=60, limit=10):
        """View students who need academic support"""
        query = """
        SELECT 
            s.student_id,
            s.first_name,
            s.last_name,
            s.email,
            COUNT(ar.record_id) as courses_taken,
            AVG(ar.score) as avg_score,
            ROUND((AVG(ar.score) / 100) * 4, 2) as gpa
        FROM students s
        JOIN academic_records ar ON s.student_id = ar.student_id
        WHERE s.status = 'active'
        GROUP BY s.student_id, s.first_name, s.last_name, s.email
        HAVING avg_score < %s
        ORDER BY avg_score ASC
        LIMIT %s
        """
        performers = self.db.fetch_all(query, (threshold, limit))
        
        if performers:
            print(f"\n⚠ STUDENTS NEEDING SUPPORT (Score < {threshold}%)")
            print("="*80)
            headers = performers[0].keys()
            rows = [list(p.values()) for p in performers]
            print(tabulate(rows, headers=headers, tablefmt="grid"))
            print(f"\n⚠ {len(performers)} student(s) may need additional academic support")
        else:
            print(f"✓ No students with average score below {threshold}%")
    
    def view_attendance_summary(self):
        """View attendance summary for all students"""
        query = """
        SELECT 
            s.student_id,
            s.first_name,
            s.last_name,
            COUNT(a.attendance_id) as total_classes,
            SUM(CASE WHEN a.status = 'present' THEN 1 ELSE 0 END) as present,
            ROUND((SUM(CASE WHEN a.status = 'present' THEN 1 ELSE 0 END) / COUNT(*)) * 100, 2) as percentage
        FROM students s
        JOIN attendance a ON s.student_id = a.student_id
        WHERE s.status = 'active'
        GROUP BY s.student_id, s.first_name, s.last_name
        ORDER BY percentage ASC
        LIMIT 20
        """
        summary = self.db.fetch_all(query)
        
        if summary:
            print("\n ATTENDANCE SUMMARY (Bottom 20 Students)")
            print("="*80)
            headers = summary[0].keys()
            rows = [list(s.values()) for s in summary]
            print(tabulate(rows, headers=headers, tablefmt="grid"))
            
            # Show students with critical attendance
            critical = [s for s in summary if s['percentage'] < 75]
            if critical:
                print(f"\n⚠ {len(critical)} student(s) have attendance below 75%")
        else:
            print("No attendance data available")
    
    def generate_semester_report(self, semester, year):
        """Generate report for a specific semester"""
        print("\n" + "="*80)
        print(f"              SEMESTER REPORT: {semester} {year}")
        print("="*80)
        
        # Students enrolled
        enrollment_query = """
        SELECT COUNT(DISTINCT student_id) as total
        FROM academic_records
        WHERE semester = %s AND year = %s
        """
        enrollment = self.db.fetch_one(enrollment_query, (semester, year))
        
        print(f"\n Students Enrolled: {enrollment['total'] if enrollment else 0}")
        
        # Academic Performance
        performance_query = """
        SELECT 
            AVG(score) as avg_score,
            COUNT(*) as total_grades
        FROM academic_records
        WHERE semester = %s AND year = %s
        """
        performance = self.db.fetch_one(performance_query, (semester, year))
        
        if performance and performance['total_grades'] > 0:
            print(f"\n ACADEMIC PERFORMANCE")
            print(f"Total Grades Issued: {performance['total_grades']}")
            print(f"Semester Average: {performance['avg_score']:.2f}%")
            print(f"Semester GPA: {(performance['avg_score']/100)*4:.2f}/4.0")
        
        # Course-wise breakdown
        courses_query = """
        SELECT 
            c.course_code,
            c.course_name,
            COUNT(*) as students,
            AVG(ar.score) as avg_score
        FROM academic_records ar
        JOIN courses c ON ar.course_id = c.course_id
        WHERE ar.semester = %s AND ar.year = %s
        GROUP BY c.course_id, c.course_code, c.course_name
        ORDER BY c.course_code
        """
        courses = self.db.fetch_all(courses_query, (semester, year))
        
        if courses:
            print(f"\n COURSE-WISE BREAKDOWN")
            headers = courses[0].keys()
            rows = [list(c.values()) for c in courses]
            print(tabulate(rows, headers=headers, tablefmt="grid"))
        
        print("\n" + "="*80)
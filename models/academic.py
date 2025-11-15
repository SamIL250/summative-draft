from database.connection import DatabaseConnection
from tabulate import tabulate

class AcademicRecord:
    def __init__(self):
        self.db = DatabaseConnection()
        self.db.connect()
    
    # ============ COURSE MANAGEMENT ============
    
    def add_course(self, course_code, course_name, credits, description):
        """Add a new course"""
        query = """
        INSERT INTO courses (course_code, course_name, credits, description)
        VALUES (%s, %s, %s, %s)
        """
        params = (course_code, course_name, credits, description)
        result = self.db.execute_query(query, params)
        if result:
            print(f"✓ Course '{course_name}' added successfully!")
            return True
        return False
    
    def view_all_courses(self):
        """Display all courses"""
        query = "SELECT * FROM courses ORDER BY course_code"
        courses = self.db.fetch_all(query)
        
        if courses:
            headers = courses[0].keys()
            rows = [list(course.values()) for course in courses]
            print(tabulate(rows, headers=headers, tablefmt="grid"))
        else:
            print("No courses found.")
    
    def search_course(self, course_id):
        """Search for a specific course"""
        query = "SELECT * FROM courses WHERE course_id = %s"
        course = self.db.fetch_one(query, (course_id,))
        
        if course:
            print("\n=== Course Details ===")
            for key, value in course.items():
                print(f"{key}: {value}")
            return course
        else:
            print(f"No course found with ID: {course_id}")
            return None
    
    def delete_course(self, course_id):
        """Delete a course"""
        query = "DELETE FROM courses WHERE course_id = %s"
        result = self.db.execute_query(query, (course_id,))
        if result:
            print(f"✓ Course {course_id} deleted successfully!")
            return True
        return False
    
    # ============ ACADEMIC RECORDS ============
    
    def add_academic_record(self, student_id, course_id, semester, grade, score, year, remarks):
        """Add an academic record (grade) for a student"""
        query = """
        INSERT INTO academic_records (student_id, course_id, semester, grade, score, year, remarks)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (student_id, course_id, semester, grade, score, year, remarks)
        result = self.db.execute_query(query, params)
        if result:
            print(f"✓ Academic record added successfully!")
            return True
        return False
    
    def view_student_grades(self, student_id):
        """View all grades for a specific student"""
        query = """
        SELECT 
            ar.record_id,
            c.course_code,
            c.course_name,
            ar.semester,
            ar.year,
            ar.grade,
            ar.score,
            c.credits,
            ar.remarks
        FROM academic_records ar
        JOIN courses c ON ar.course_id = c.course_id
        WHERE ar.student_id = %s
        ORDER BY ar.year DESC, ar.semester DESC
        """
        records = self.db.fetch_all(query, (student_id,))
        
        if records:
            headers = records[0].keys()
            rows = [list(record.values()) for record in records]
            print("\n=== Academic Records ===")
            print(tabulate(rows, headers=headers, tablefmt="grid"))
            return records
        else:
            print(f"No academic records found for student ID: {student_id}")
            return []
    
    def calculate_gpa(self, student_id):
        """Calculate GPA for a student"""
        query = """
        SELECT AVG(score) as gpa, COUNT(*) as total_courses
        FROM academic_records 
        WHERE student_id = %s
        """
        result = self.db.fetch_one(query, (student_id,))
        
        if result and result['gpa']:
            gpa = result['gpa']
            total = result['total_courses']
            gpa_4_scale = (gpa / 100) * 4.0
            
            print("\n=== GPA Summary ===")
            print(f"Student ID: {student_id}")
            print(f"Total Courses: {total}")
            print(f"Average Score: {gpa:.2f}%")
            print(f"GPA (4.0 scale): {gpa_4_scale:.2f}")
            
            return gpa_4_scale
        else:
            print("No grades available to calculate GPA")
            return None
    
    def view_transcript(self, student_id):
        """Generate a complete transcript for a student"""
        # Get student info
        student_query = "SELECT * FROM students WHERE student_id = %s"
        student = self.db.fetch_one(student_query, (student_id,))
        
        if not student:
            print(f"Student {student_id} not found!")
            return
        
        print("\n" + "="*70)
        print("                        OFFICIAL TRANSCRIPT")
        print("="*70)
        print(f"\nStudent Name: {student['first_name']} {student['last_name']}")
        print(f"Student ID: {student['student_id']}")
        print(f"Email: {student['email']}")
        print(f"Enrollment Date: {student['enrollment_date']}")
        print(f"Status: {student['status']}")
        print("\n" + "-"*70)
        
        # Get grades by semester
        query = """
        SELECT 
            ar.semester,
            ar.year,
            c.course_code,
            c.course_name,
            c.credits,
            ar.grade,
            ar.score
        FROM academic_records ar
        JOIN courses c ON ar.course_id = c.course_id
        WHERE ar.student_id = %s
        ORDER BY ar.year, ar.semester, c.course_code
        """
        records = self.db.fetch_all(query, (student_id,))
        
        if records:
            current_semester = None
            semester_credits = 0
            semester_points = 0
            
            for record in records:
                semester_key = f"{record['semester']} {record['year']}"
                
                if current_semester != semester_key:
                    if current_semester:
                        # Print semester summary
                        sem_gpa = (semester_points / semester_credits) if semester_credits > 0 else 0
                        print(f"\nSemester Credits: {semester_credits} | Semester GPA: {sem_gpa:.2f}")
                        print("-"*70)
                    
                    current_semester = semester_key
                    print(f"\n{semester_key}")
                    print("-"*70)
                    semester_credits = 0
                    semester_points = 0
                
                grade_point = self._convert_score_to_gpa(record['score'])
                semester_credits += record['credits']
                semester_points += grade_point * record['credits']
                
                print(f"{record['course_code']:<10} {record['course_name']:<30} "
                      f"Credits: {record['credits']:<3} Grade: {record['grade']:<5} "
                      f"Score: {record['score']:.1f}")
            
            # Final semester summary
            if semester_credits > 0:
                sem_gpa = (semester_points / semester_credits)
                print(f"\nSemester Credits: {semester_credits} | Semester GPA: {sem_gpa:.2f}")
            
            print("\n" + "="*70)
            
            # Overall GPA
            self.calculate_gpa(student_id)
        else:
            print("\nNo academic records found.")
        
        print("="*70)
    
    def _convert_score_to_gpa(self, score):
        """Convert percentage score to 4.0 GPA scale"""
        if score >= 90:
            return 4.0
        elif score >= 80:
            return 3.0
        elif score >= 70:
            return 2.0
        elif score >= 60:
            return 1.0
        else:
            return 0.0
    
    def update_academic_record(self, record_id, field, new_value):
        """Update an academic record"""
        allowed_fields = ['grade', 'score', 'remarks', 'semester', 'year']
        
        if field not in allowed_fields:
            print(f"Invalid field. Allowed: {allowed_fields}")
            return False
        
        query = f"UPDATE academic_records SET {field} = %s WHERE record_id = %s"
        result = self.db.execute_query(query, (new_value, record_id))
        
        if result:
            print(f"✓ Academic record {record_id} updated successfully!")
            return True
        return False
    
    def get_course_statistics(self, course_id):
        """Get statistics for a specific course"""
        query = """
        SELECT 
            COUNT(*) as total_students,
            AVG(score) as average_score,
            MAX(score) as highest_score,
            MIN(score) as lowest_score,
            COUNT(CASE WHEN score >= 90 THEN 1 END) as a_grades,
            COUNT(CASE WHEN score >= 80 AND score < 90 THEN 1 END) as b_grades,
            COUNT(CASE WHEN score >= 70 AND score < 80 THEN 1 END) as c_grades,
            COUNT(CASE WHEN score >= 60 AND score < 70 THEN 1 END) as d_grades,
            COUNT(CASE WHEN score < 60 THEN 1 END) as f_grades
        FROM academic_records
        WHERE course_id = %s
        """
        stats = self.db.fetch_one(query, (course_id,))
        
        if stats and stats['total_students'] > 0:
            print("\n=== Course Statistics ===")
            print(f"Total Students: {stats['total_students']}")
            print(f"Average Score: {stats['average_score']:.2f}%")
            print(f"Highest Score: {stats['highest_score']:.2f}%")
            print(f"Lowest Score: {stats['lowest_score']:.2f}%")
            print("\nGrade Distribution:")
            print(f"  A (90-100): {stats['a_grades']} students")
            print(f"  B (80-89):  {stats['b_grades']} students")
            print(f"  C (70-79):  {stats['c_grades']} students")
            print(f"  D (60-69):  {stats['d_grades']} students")
            print(f"  F (0-59):   {stats['f_grades']} students")
            return stats
        else:
            print("No data available for this course.")
            return None
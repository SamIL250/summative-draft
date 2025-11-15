from database.connection import DatabaseConnection
from tabulate import tabulate
from datetime import date, datetime, timedelta

class Attendance:
    def __init__(self):
        self.db = DatabaseConnection()
        self.db.connect()
    
    def mark_attendance(self, student_id, course_id, status, remarks=""):
        """Mark attendance for a student"""
        # Check if attendance already marked for today
        check_query = """
        SELECT * FROM attendance 
        WHERE student_id = %s AND course_id = %s AND attendance_date = %s
        """
        existing = self.db.fetch_one(check_query, (student_id, course_id, date.today()))
        
        if existing:
            print(f"⚠ Attendance already marked for today. Updating...")
            update_query = """
            UPDATE attendance 
            SET status = %s, remarks = %s 
            WHERE student_id = %s AND course_id = %s AND attendance_date = %s
            """
            result = self.db.execute_query(update_query, (status, remarks, student_id, course_id, date.today()))
        else:
            query = """
            INSERT INTO attendance (student_id, course_id, attendance_date, status, remarks)
            VALUES (%s, %s, %s, %s, %s)
            """
            params = (student_id, course_id, date.today(), status, remarks)
            result = self.db.execute_query(query, params)
        
        if result:
            print(f"✓ Attendance marked as '{status}' for student {student_id}")
            return True
        return False
    
    def view_attendance(self, student_id, course_id=None):
        """View attendance records for a student"""
        if course_id:
            query = """
            SELECT 
                a.attendance_date,
                c.course_code,
                c.course_name,
                a.status,
                a.remarks
            FROM attendance a
            JOIN courses c ON a.course_id = c.course_id
            WHERE a.student_id = %s AND a.course_id = %s
            ORDER BY a.attendance_date DESC
            """
            params = (student_id, course_id)
        else:
            query = """
            SELECT 
                a.attendance_date,
                c.course_code,
                c.course_name,
                a.status,
                a.remarks
            FROM attendance a
            JOIN courses c ON a.course_id = c.course_id
            WHERE a.student_id = %s
            ORDER BY a.attendance_date DESC
            """
            params = (student_id,)
        
        records = self.db.fetch_all(query, params)
        
        if records:
            headers = records[0].keys()
            rows = [list(record.values()) for record in records]
            print("\n=== Attendance Records ===")
            print(tabulate(rows, headers=headers, tablefmt="grid"))
            return records
        else:
            print("No attendance records found")
            return []
    
    def get_attendance_percentage(self, student_id, course_id):
        """Calculate attendance percentage for a student in a course"""
        query = """
        SELECT 
            COUNT(*) as total,
            SUM(CASE WHEN status = 'present' THEN 1 ELSE 0 END) as present,
            SUM(CASE WHEN status = 'absent' THEN 1 ELSE 0 END) as absent,
            SUM(CASE WHEN status = 'late' THEN 1 ELSE 0 END) as late,
            SUM(CASE WHEN status = 'excused' THEN 1 ELSE 0 END) as excused
        FROM attendance
        WHERE student_id = %s AND course_id = %s
        """
        result = self.db.fetch_one(query, (student_id, course_id))
        
        if result and result['total'] > 0:
            present = result['present']
            total = result['total']
            percentage = (present / total) * 100
            
            print("\n=== Attendance Summary ===")
            print(f"Student ID: {student_id}")
            print(f"Course ID: {course_id}")
            print(f"Total Classes: {total}")
            print(f"Present: {result['present']}")
            print(f"Absent: {result['absent']}")
            print(f"Late: {result['late']}")
            print(f"Excused: {result['excused']}")
            print(f"Attendance Percentage: {percentage:.2f}%")
            
            # Status indicator
            if percentage >= 90:
                print("Status: ✓ Excellent")
            elif percentage >= 75:
                print("Status: ⚠ Good")
            elif percentage >= 60:
                print("Status: ⚠ Warning - Low Attendance")
            else:
                print("Status: ❌ Critical - Very Low Attendance")
            
            return percentage
        else:
            print("No attendance records found")
            return 0
    
    def view_course_attendance(self, course_id):
        """View attendance for all students in a course"""
        query = """
        SELECT 
            s.student_id,
            s.first_name,
            s.last_name,
            COUNT(*) as total_classes,
            SUM(CASE WHEN a.status = 'present' THEN 1 ELSE 0 END) as present,
            ROUND((SUM(CASE WHEN a.status = 'present' THEN 1 ELSE 0 END) / COUNT(*)) * 100, 2) as percentage
        FROM students s
        JOIN attendance a ON s.student_id = a.student_id
        WHERE a.course_id = %s
        GROUP BY s.student_id, s.first_name, s.last_name
        ORDER BY percentage DESC
        """
        records = self.db.fetch_all(query, (course_id,))
        
        if records:
            headers = records[0].keys()
            rows = [list(record.values()) for record in records]
            print("\n=== Course Attendance Report ===")
            print(tabulate(rows, headers=headers, tablefmt="grid"))
            
            # Calculate course average
            total_percentage = sum(record['percentage'] for record in records)
            avg_percentage = total_percentage / len(records)
            print(f"\nCourse Average Attendance: {avg_percentage:.2f}%")
            
            return records
        else:
            print("No attendance records found for this course")
            return []
    
    def view_attendance_by_date(self, attendance_date):
        """View all attendance records for a specific date"""
        query = """
        SELECT 
            s.student_id,
            s.first_name,
            s.last_name,
            c.course_code,
            c.course_name,
            a.status,
            a.remarks
        FROM attendance a
        JOIN students s ON a.student_id = s.student_id
        JOIN courses c ON a.course_id = c.course_id
        WHERE a.attendance_date = %s
        ORDER BY c.course_code, s.last_name
        """
        records = self.db.fetch_all(query, (attendance_date,))
        
        if records:
            headers = records[0].keys()
            rows = [list(record.values()) for record in records]
            print(f"\n=== Attendance for {attendance_date} ===")
            print(tabulate(rows, headers=headers, tablefmt="grid"))
            
            # Summary statistics
            total = len(records)
            present = sum(1 for r in records if r['status'] == 'present')
            absent = sum(1 for r in records if r['status'] == 'absent')
            
            print(f"\nSummary: Total: {total} | Present: {present} | Absent: {absent}")
            
            return records
        else:
            print(f"No attendance records found for {attendance_date}")
            return []
    
    def get_student_attendance_summary(self, student_id):
        """Get overall attendance summary for a student across all courses"""
        query = """
        SELECT 
            c.course_code,
            c.course_name,
            COUNT(*) as total,
            SUM(CASE WHEN a.status = 'present' THEN 1 ELSE 0 END) as present,
            ROUND((SUM(CASE WHEN a.status = 'present' THEN 1 ELSE 0 END) / COUNT(*)) * 100, 2) as percentage
        FROM attendance a
        JOIN courses c ON a.course_id = c.course_id
        WHERE a.student_id = %s
        GROUP BY c.course_id, c.course_code, c.course_name
        ORDER BY percentage DESC
        """
        records = self.db.fetch_all(query, (student_id,))
        
        if records:
            headers = records[0].keys()
            rows = [list(record.values()) for record in records]
            print(f"\n=== Attendance Summary for Student {student_id} ===")
            print(tabulate(rows, headers=headers, tablefmt="grid"))
            
            # Overall average
            total_percentage = sum(record['percentage'] for record in records)
            avg_percentage = total_percentage / len(records)
            print(f"\nOverall Attendance: {avg_percentage:.2f}%")
            
            return records
        else:
            print("No attendance records found")
            return []
    
    def get_low_attendance_students(self, threshold=75):
        """Get list of students with attendance below threshold"""
        query = """
        SELECT 
            s.student_id,
            s.first_name,
            s.last_name,
            s.email,
            COUNT(*) as total_classes,
            SUM(CASE WHEN a.status = 'present' THEN 1 ELSE 0 END) as present,
            ROUND((SUM(CASE WHEN a.status = 'present' THEN 1 ELSE 0 END) / COUNT(*)) * 100, 2) as percentage
        FROM students s
        JOIN attendance a ON s.student_id = a.student_id
        GROUP BY s.student_id, s.first_name, s.last_name, s.email
        HAVING percentage < %s
        ORDER BY percentage ASC
        """
        records = self.db.fetch_all(query, (threshold,))
        
        if records:
            headers = records[0].keys()
            rows = [list(record.values()) for record in records]
            print(f"\n=== Students with Attendance Below {threshold}% ===")
            print(tabulate(rows, headers=headers, tablefmt="grid"))
            print(f"\n⚠ {len(records)} student(s) need attention")
            
            return records
        else:
            print(f"✓ No students with attendance below {threshold}%")
            return []
    
    def mark_bulk_attendance(self, course_id, student_ids, status, remarks=""):
        """Mark attendance for multiple students at once"""
        success_count = 0
        
        for student_id in student_ids:
            if self.mark_attendance(student_id, course_id, status, remarks):
                success_count += 1
        
        print(f"\n✓ Bulk attendance marked: {success_count}/{len(student_ids)} students")
        return success_count
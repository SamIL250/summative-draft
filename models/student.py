from database.connection import DatabaseConnection
from tabulate import tabulate

class Student:
    def __init__(self):
        self.db = DatabaseConnection()
        self.db.connect()
    
    def add_student(self, first_name, last_name, email, phone, dob):
        query = """
        INSERT INTO students (first_name, last_name, email, phone, date_of_birth)
        VALUES (%s, %s, %s, %s, %s)
        """
        params = (first_name, last_name, email, phone, dob)
        result = self.db.execute_query(query, params)
        if result:
            print(f"✓ Student {first_name} {last_name} added successfully!")
            return True
        return False
    
    def view_all_students(self):
        query = "SELECT * FROM students ORDER BY student_id"
        students = self.db.fetch_all(query)
        
        if students:
            headers = students[0].keys()
            rows = [list(student.values()) for student in students]
            print("\n" + tabulate(rows, headers=headers, tablefmt="grid"))
        else:
            print("No students found.")
    
    def search_student(self, student_id):
        query = "SELECT * FROM students WHERE student_id = %s"
        student = self.db.fetch_one(query, (student_id,))
        
        if student:
            print("\n=== Student Details ===")
            for key, value in student.items():
                print(f"{key}: {value}")
            return student
        else:
            print(f"No student found with ID: {student_id}")
            return None
    
    def update_student(self, student_id, field, new_value):
        allowed_fields = ['first_name', 'last_name', 'email', 'phone', 'status']
        if field not in allowed_fields:
            print(f"Invalid field. Allowed: {allowed_fields}")
            return False
        
        query = f"UPDATE students SET {field} = %s WHERE student_id = %s"
        result = self.db.execute_query(query, (new_value, student_id))
        if result:
            print(f"✓ Student {student_id} updated successfully!")
            return True
        return False
    
    def delete_student(self, student_id):
        query = "DELETE FROM students WHERE student_id = %s"
        result = self.db.execute_query(query, (student_id,))
        if result:
            print(f"✓ Student {student_id} deleted successfully!")
            return True
        return False
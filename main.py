from models.student import Student
from models.academic import AcademicRecord
from models.attendance import Attendance
from models.document import Document
from models.learning_outcome import LearningOutcome
from models.reports import Reports
from utils.menu import *
from utils.validators import *
import sys

def student_management():
    """Handle all student-related operations"""
    student = Student()
    while True:
        display_student_menu()
        choice = input("\nEnter choice: ")
        
        if choice == '1':
            print("\n=== Add New Student ===")
            first_name = input("First Name: ").strip()
            last_name = input("Last Name: ").strip()
            email = input("Email: ").strip()
            
            if not validate_email(email):
                print("Invalid email format!")
                continue
                
            phone = input("Phone: ").strip()
            dob = input("Date of Birth (YYYY-MM-DD): ").strip()
            
            if not validate_date(dob):
                print("Invalid date format!")
                continue
                
            student.add_student(first_name, last_name, email, phone, dob)
        
        elif choice == '2':
            print("\n=== All Students ===")
            student.view_all_students()
        
        elif choice == '3':
            student_id = input("Enter Student ID: ").strip()
            if student_id.isdigit():
                student.search_student(int(student_id))
            else:
                print("Invalid Student ID!")
        
        elif choice == '4':
            student_id = input("Enter Student ID: ").strip()
            if not student_id.isdigit():
                print("Invalid Student ID!")
                continue
                
            print("\nFields you can update:")
            print("1. first_name")
            print("2. last_name")
            print("3. email")
            print("4. phone")
            print("5. status (active/inactive/graduated)")
            
            field = input("\nField to update: ").strip()
            new_value = input("New value: ").strip()
            
            student.update_student(int(student_id), field, new_value)
        
        elif choice == '5':
            student_id = input("Enter Student ID: ").strip()
            if not student_id.isdigit():
                print("Invalid Student ID!")
                continue
                
            confirm = input(f"Delete student {student_id}? (yes/no): ")
            if confirm.lower() == 'yes':
                student.delete_student(int(student_id))
        
        elif choice == '0':
            break
        
        else:
            print("Invalid choice!")

def course_management():
    """Handle all course-related operations"""
    academic = AcademicRecord()
    while True:
        display_course_menu()
        choice = input("\nEnter choice: ")
        
        if choice == '1':
            print("\n=== Add New Course ===")
            course_code = input("Course Code (e.g., CS101): ").strip().upper()
            course_name = input("Course Name: ").strip()
            credits = input("Credits (default 3): ").strip()
            credits = int(credits) if credits.isdigit() else 3
            description = input("Description: ").strip()
            
            academic.add_course(course_code, course_name, credits, description)
        
        elif choice == '2':
            print("\n=== All Courses ===")
            academic.view_all_courses()
        
        elif choice == '3':
            course_id = input("Enter Course ID: ").strip()
            if course_id.isdigit():
                academic.search_course(int(course_id))
            else:
                print("Invalid Course ID!")
        
        elif choice == '4':
            course_id = input("Enter Course ID: ").strip()
            if not course_id.isdigit():
                print("Invalid Course ID!")
                continue
                
            confirm = input(f"Delete course {course_id}? (yes/no): ")
            if confirm.lower() == 'yes':
                academic.delete_course(int(course_id))
        
        elif choice == '0':
            break
        
        else:
            print("Invalid choice!")

def academic_records_management():
    """Handle academic records and grades"""
    academic = AcademicRecord()
    while True:
        display_academic_menu()
        choice = input("\nEnter choice: ")
        
        if choice == '1':
            print("\n=== Add Academic Record ===")
            student_id = input("Student ID: ").strip()
            course_id = input("Course ID: ").strip()
            semester = input("Semester (e.g., Fall 2024): ").strip()
            year = input("Year: ").strip()
            grade = input("Grade (A, B, C, D, F): ").strip().upper()
            score = input("Score (0-100): ").strip()
            remarks = input("Remarks (optional): ").strip()
            
            if not (student_id.isdigit() and course_id.isdigit() and 
                    year.isdigit() and score.replace('.', '').isdigit()):
                print("Invalid input! Please check your entries.")
                continue
            
            academic.add_academic_record(
                int(student_id), int(course_id), semester, 
                grade, float(score), int(year), remarks
            )
        
        elif choice == '2':
            student_id = input("Enter Student ID: ").strip()
            if student_id.isdigit():
                academic.view_student_grades(int(student_id))
            else:
                print("Invalid Student ID!")
        
        elif choice == '3':
            student_id = input("Enter Student ID: ").strip()
            if student_id.isdigit():
                academic.calculate_gpa(int(student_id))
            else:
                print("Invalid Student ID!")
        
        elif choice == '4':
            student_id = input("Enter Student ID: ").strip()
            if student_id.isdigit():
                academic.view_transcript(int(student_id))
            else:
                print("Invalid Student ID!")
        
        elif choice == '5':
            record_id = input("Enter Record ID: ").strip()
            if not record_id.isdigit():
                print("Invalid Record ID!")
                continue
                
            field = input("Field to update (grade/score/remarks): ").strip()
            new_value = input("New value: ").strip()
            
            academic.update_academic_record(int(record_id), field, new_value)
        
        elif choice == '0':
            break
        
        else:
            print("Invalid choice!")

def attendance_management():
    """Handle attendance tracking"""
    attendance = Attendance()
    while True:
        display_attendance_menu()
        choice = input("\nEnter choice: ")
        
        if choice == '1':
            print("\n=== Mark Attendance ===")
            student_id = input("Student ID: ").strip()
            course_id = input("Course ID: ").strip()
            
            if not (student_id.isdigit() and course_id.isdigit()):
                print("Invalid input!")
                continue
            
            print("\nStatus Options:")
            print("1. present")
            print("2. absent")
            print("3. late")
            print("4. excused")
            status_choice = input("Choose status (1-4): ").strip()
            
            status_map = {'1': 'present', '2': 'absent', '3': 'late', '4': 'excused'}
            status = status_map.get(status_choice, 'present')
            
            remarks = input("Remarks (optional): ").strip()
            
            attendance.mark_attendance(int(student_id), int(course_id), status, remarks)
        
        elif choice == '2':
            student_id = input("Enter Student ID: ").strip()
            course_id = input("Course ID (press Enter for all courses): ").strip()
            
            if not student_id.isdigit():
                print("Invalid Student ID!")
                continue
            
            if course_id and course_id.isdigit():
                attendance.view_attendance(int(student_id), int(course_id))
            elif student_id.isdigit():
                attendance.view_attendance(int(student_id))
        
        elif choice == '3':
            student_id = input("Enter Student ID: ").strip()
            course_id = input("Enter Course ID: ").strip()
            
            if student_id.isdigit() and course_id.isdigit():
                attendance.get_attendance_percentage(int(student_id), int(course_id))
            else:
                print("Invalid input!")
        
        elif choice == '4':
            course_id = input("Enter Course ID: ").strip()
            if course_id.isdigit():
                attendance.view_course_attendance(int(course_id))
            else:
                print("Invalid Course ID!")
        
        elif choice == '5':
            date = input("Enter date (YYYY-MM-DD): ").strip()
            if validate_date(date):
                attendance.view_attendance_by_date(date)
            else:
                print("Invalid date format!")
        
        elif choice == '0':
            break
        
        else:
            print("Invalid choice!")

def document_management():
    """Handle document management"""
    document = Document()
    while True:
        display_document_menu()
        choice = input("\nEnter choice: ")
        
        if choice == '1':
            print("\n=== Add Document ===")
            student_id = input("Student ID: ").strip()
            
            if not student_id.isdigit():
                print("Invalid Student ID!")
                continue
            
            print("\nDocument Types:")
            print("1. Transcript")
            print("2. Certificate")
            print("3. ID Card")
            print("4. Medical Record")
            print("5. Other")
            
            doc_type_choice = input("Choose type (1-5): ").strip()
            doc_types = {
                '1': 'Transcript',
                '2': 'Certificate',
                '3': 'ID Card',
                '4': 'Medical Record',
                '5': 'Other'
            }
            doc_type = doc_types.get(doc_type_choice, 'Other')
            
            doc_name = input("Document Name: ").strip()
            file_path = input("File Path (optional): ").strip()
            description = input("Description: ").strip()
            
            document.add_document(int(student_id), doc_type, doc_name, file_path, description)
        
        elif choice == '2':
            student_id = input("Enter Student ID: ").strip()
            if student_id.isdigit():
                document.view_student_documents(int(student_id))
            else:
                print("Invalid Student ID!")
        
        elif choice == '3':
            document_id = input("Enter Document ID: ").strip()
            if not document_id.isdigit():
                print("Invalid Document ID!")
                continue
                
            confirm = input(f"Delete document {document_id}? (yes/no): ")
            if confirm.lower() == 'yes':
                document.delete_document(int(document_id))
        
        elif choice == '0':
            break
        
        else:
            print("Invalid choice!")

def learning_outcomes_management():
    """Handle learning outcomes tracking"""
    outcome = LearningOutcome()
    while True:
        display_learning_outcomes_menu()
        choice = input("\nEnter choice: ")
        
        if choice == '1':
            print("\n=== Add Learning Outcome ===")
            student_id = input("Student ID: ").strip()
            course_id = input("Course ID: ").strip()
            
            if not (student_id.isdigit() and course_id.isdigit()):
                print("Invalid input!")
                continue
            
            description = input("Outcome Description: ").strip()
            
            print("\nAchievement Level:")
            print("1. not_met")
            print("2. partially_met")
            print("3. met")
            print("4. exceeded")
            level_choice = input("Choose level (1-4): ").strip()
            
            levels = {
                '1': 'not_met',
                '2': 'partially_met',
                '3': 'met',
                '4': 'exceeded'
            }
            level = levels.get(level_choice, 'met')
            
            assessment_date = input("Assessment Date (YYYY-MM-DD): ").strip()
            notes = input("Notes (optional): ").strip()
            
            if not validate_date(assessment_date):
                print("Invalid date format!")
                continue
            
            outcome.add_learning_outcome(
                int(student_id), int(course_id), description, 
                level, assessment_date, notes
            )
        
        elif choice == '2':
            student_id = input("Enter Student ID: ").strip()
            if student_id.isdigit():
                outcome.view_student_outcomes(int(student_id))
            else:
                print("Invalid Student ID!")
        
        elif choice == '3':
            course_id = input("Enter Course ID: ").strip()
            if course_id.isdigit():
                outcome.view_course_outcomes(int(course_id))
            else:
                print("Invalid Course ID!")
        
        elif choice == '4':
            student_id = input("Enter Student ID: ").strip()
            if student_id.isdigit():
                outcome.get_achievement_summary(int(student_id))
            else:
                print("Invalid Student ID!")
        
        elif choice == '0':
            break
        
        else:
            print("Invalid choice!")

def reports_and_analytics():
    """Handle reports and analytics"""
    reports = Reports()
    while True:
        display_reports_menu()
        choice = input("\nEnter choice: ")
        
        if choice == '1':
            student_id = input("Enter Student ID: ").strip()
            if student_id.isdigit():
                reports.generate_student_report(int(student_id))
            else:
                print("Invalid Student ID!")
        
        elif choice == '2':
            course_id = input("Enter Course ID: ").strip()
            if course_id.isdigit():
                reports.generate_course_report(int(course_id))
            else:
                print("Invalid Course ID!")
        
        elif choice == '3':
            reports.generate_overall_statistics()
        
        elif choice == '4':
            reports.view_top_performers()
        
        elif choice == '5':
            reports.view_low_performers()
        
        elif choice == '6':
            reports.view_attendance_summary()
        
        elif choice == '7':
            semester = input("Enter Semester (e.g., Fall 2024): ").strip()
            year = input("Enter Year: ").strip()
            if year.isdigit():
                reports.generate_semester_report(semester, int(year))
            else:
                print("Invalid year!")
        
        elif choice == '0':
            break
        
        else:
            print("Invalid choice!")

def main():
    """Main application entry point"""
    print("\n" + "="*60)
    print("🎓 Welcome to LearnTrack - Student Performance Tracking System")
    print("="*60)
    
    while True:
        display_main_menu()
        choice = input("\nEnter your choice: ").strip()
        
        if choice == '1':
            student_management()
        
        elif choice == '2':
            course_management()
        
        elif choice == '3':
            academic_records_management()
        
        elif choice == '4':
            attendance_management()
        
        elif choice == '5':
            document_management()
        
        elif choice == '6':
            learning_outcomes_management()
        
        elif choice == '7':
            reports_and_analytics()
        
        elif choice == '0':
            print("\n" + "="*60)
            print("Thank you for using LearnTrack!")
            print("="*60)
            sys.exit(0)
        
        else:
            print("\n❌ Invalid choice! Please try again.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        sys.exit(1)
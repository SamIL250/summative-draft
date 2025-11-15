from database.connection import DatabaseConnection
from tabulate import tabulate

class LearningOutcome:
    def __init__(self):
        self.db = DatabaseConnection()
        self.db.connect()
    
    def add_learning_outcome(self, student_id, course_id, description, achievement_level, assessment_date, notes=""):
        """Add a learning outcome assessment for a student"""
        query = """
        INSERT INTO learning_outcomes 
        (student_id, course_id, outcome_description, achievement_level, assessment_date, notes)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (student_id, course_id, description, achievement_level, assessment_date, notes)
        result = self.db.execute_query(query, params)
        
        if result:
            print(f"✓ Learning outcome added successfully!")
            return True
        return False
    
    def view_student_outcomes(self, student_id):
        """View all learning outcomes for a student"""
        query = """
        SELECT 
            lo.outcome_id,
            c.course_code,
            c.course_name,
            lo.outcome_description,
            lo.achievement_level,
            lo.assessment_date,
            lo.notes
        FROM learning_outcomes lo
        JOIN courses c ON lo.course_id = c.course_id
        WHERE lo.student_id = %s
        ORDER BY lo.assessment_date DESC
        """
        outcomes = self.db.fetch_all(query, (student_id,))
        
        if outcomes:
            headers = outcomes[0].keys()
            rows = [list(outcome.values()) for outcome in outcomes]
            print(f"\n=== Learning Outcomes for Student {student_id} ===")
            print(tabulate(rows, headers=headers, tablefmt="grid"))
            return outcomes
        else:
            print("No learning outcomes found")
            return []
    
    def view_course_outcomes(self, course_id):
        """View learning outcomes for all students in a course"""
        query = """
        SELECT 
            s.student_id,
            s.first_name,
            s.last_name,
            lo.outcome_description,
            lo.achievement_level,
            lo.assessment_date
        FROM learning_outcomes lo
        JOIN students s ON lo.student_id = s.student_id
        WHERE lo.course_id = %s
        ORDER BY s.last_name, lo.assessment_date DESC
        """
        outcomes = self.db.fetch_all(query, (course_id,))
        
        if outcomes:
            headers = outcomes[0].keys()
            rows = [list(outcome.values()) for outcome in outcomes]
            print(f"\n=== Learning Outcomes for Course {course_id} ===")
            print(tabulate(rows, headers=headers, tablefmt="grid"))
            return outcomes
        else:
            print("No learning outcomes found for this course")
            return []
    
    def get_achievement_summary(self, student_id):
        """Get achievement summary for a student"""
        query = """
        SELECT 
            achievement_level,
            COUNT(*) as count
        FROM learning_outcomes
        WHERE student_id = %s
        GROUP BY achievement_level
        """
        summary = self.db.fetch_all(query, (student_id,))
        
        if summary:
            print(f"\n=== Achievement Summary for Student {student_id} ===")
            
            total = sum(item['count'] for item in summary)
            
            for item in summary:
                level = item['achievement_level']
                count = item['count']
                percentage = (count / total) * 100
                
                # Visual representation
                bars = '█' * int(percentage / 5)
                
                print(f"{level:<20} {count:>3} ({percentage:>5.1f}%) {bars}")
            
            print(f"\nTotal Outcomes Assessed: {total}")
            
            # Calculate achievement score
            level_scores = {
                'exceeded': 4,
                'met': 3,
                'partially_met': 2,
                'not_met': 1
            }
            
            total_score = sum(level_scores.get(item['achievement_level'], 0) * item['count'] 
                            for item in summary)
            avg_score = total_score / total if total > 0 else 0
            
            print(f"Average Achievement Score: {avg_score:.2f}/4.0")
            
            if avg_score >= 3.5:
                print("Overall Performance: ✓ Excellent")
            elif avg_score >= 3.0:
                print("Overall Performance: ✓ Good")
            elif avg_score >= 2.5:
                print("Overall Performance: ⚠ Satisfactory")
            else:
                print("Overall Performance: ⚠ Needs Improvement")
            
            return summary
        else:
            print("No learning outcomes found")
            return []
    
    def update_learning_outcome(self, outcome_id, field, new_value):
        """Update a learning outcome"""
        allowed_fields = ['outcome_description', 'achievement_level', 'assessment_date', 'notes']
        
        if field not in allowed_fields:
            print(f"Invalid field. Allowed: {allowed_fields}")
            return False
        
        query = f"UPDATE learning_outcomes SET {field} = %s WHERE outcome_id = %s"
        result = self.db.execute_query(query, (new_value, outcome_id))
        
        if result:
            print(f"✓ Learning outcome {outcome_id} updated successfully!")
            return True
        return False
    
    def delete_learning_outcome(self, outcome_id):
        """Delete a learning outcome"""
        query = "DELETE FROM learning_outcomes WHERE outcome_id = %s"
        result = self.db.execute_query(query, (outcome_id,))
        
        if result:
            print(f"✓ Learning outcome {outcome_id} deleted successfully!")
            return True
        return False
    
    def get_course_achievement_statistics(self, course_id):
        """Get achievement statistics for a course"""
        query = """
        SELECT 
            achievement_level,
            COUNT(*) as count
        FROM learning_outcomes
        WHERE course_id = %s
        GROUP BY achievement_level
        """
        stats = self.db.fetch_all(query, (course_id,))
        
        if stats:
            print(f"\n=== Achievement Statistics for Course {course_id} ===")
            
            total = sum(item['count'] for item in stats)
            
            for item in stats:
                level = item['achievement_level']
                count = item['count']
                percentage = (count / total) * 100
                bars = '█' * int(percentage / 5)
                
                print(f"{level:<20} {count:>3} ({percentage:>5.1f}%) {bars}")
            
            print(f"\nTotal Assessments: {total}")
            
            # Success rate (met or exceeded)
            success_count = sum(item['count'] for item in stats 
                              if item['achievement_level'] in ['met', 'exceeded'])
            success_rate = (success_count / total) * 100 if total > 0 else 0
            
            print(f"Success Rate (Met/Exceeded): {success_rate:.1f}%")
            
            return stats
        else:
            print("No learning outcome data available for this course")
            return []
    
    def compare_student_performance(self, student_id, course_id):
        """Compare student's performance with course average"""
        # Get student's achievement
        student_query = """
        SELECT achievement_level, COUNT(*) as count
        FROM learning_outcomes
        WHERE student_id = %s AND course_id = %s
        GROUP BY achievement_level
        """
        student_data = self.db.fetch_all(student_query, (student_id, course_id))
        
        # Get course average
        course_query = """
        SELECT achievement_level, COUNT(*) as count
        FROM learning_outcomes
        WHERE course_id = %s
        GROUP BY achievement_level
        """
        course_data = self.db.fetch_all(course_query, (course_id,))
        
        if not student_data or not course_data:
            print("Insufficient data for comparison")
            return
        
        level_scores = {
            'exceeded': 4,
            'met': 3,
            'partially_met': 2,
            'not_met': 1
        }
        
        # Calculate student average
        student_total = sum(item['count'] for item in student_data)
        student_score = sum(level_scores.get(item['achievement_level'], 0) * item['count'] 
                          for item in student_data) / student_total
        
        # Calculate course average
        course_total = sum(item['count'] for item in course_data)
        course_score = sum(level_scores.get(item['achievement_level'], 0) * item['count'] 
                         for item in course_data) / course_total
        
        print(f"\n=== Performance Comparison ===")
        print(f"Student {student_id} Average: {student_score:.2f}/4.0")
        print(f"Course Average: {course_score:.2f}/4.0")
        
        difference = student_score - course_score
        if difference > 0.5:
            print(f"✓ Performing {difference:.2f} points above course average")
        elif difference < -0.5:
            print(f"⚠ Performing {abs(difference):.2f} points below course average")
        else:
            print("✓ Performing at course average")
        
        return {
            'student_score': student_score,
            'course_score': course_score,
            'difference': difference
        }
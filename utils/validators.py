import re
from datetime import datetime

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """Validate phone number (basic validation)"""
    pattern = r'^\+?1?\d{9,15}$'
    return re.match(pattern, phone.replace('-', '').replace(' ', '')) is not None

def validate_date(date_string):
    """Validate date format (YYYY-MM-DD)"""
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def validate_grade(grade):
    """Validate grade format"""
    valid_grades = ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'D-', 'F']
    return grade.upper() in valid_grades

def validate_score(score):
    """Validate score (0-100)"""
    try:
        score_float = float(score)
        return 0 <= score_float <= 100
    except ValueError:
        return False

def validate_positive_integer(value):
    """Validate positive integer"""
    try:
        return int(value) > 0
    except ValueError:
        return False

def validate_year(year):
    """Validate year (1900-2100)"""
    try:
        year_int = int(year)
        return 1900 <= year_int <= 2100
    except ValueError:
        return False

def validate_status(status):
    """Validate student/course status"""
    valid_statuses = ['active', 'inactive', 'graduated', 'suspended']
    return status.lower() in valid_statuses

def validate_attendance_status(status):
    """Validate attendance status"""
    valid_statuses = ['present', 'absent', 'late', 'excused']
    return status.lower() in valid_statuses

def sanitize_input(text):
    """Remove potentially dangerous characters from input"""
    return text.strip().replace(';', '').replace('--', '')
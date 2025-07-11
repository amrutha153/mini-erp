import re

def is_valid_email(email):
    # Simple regex for email validation
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

def is_valid_phone(phone):
    # Simple check for 10-digit phone numbers
    return re.match(r"^\d{10}$", phone) is not None

def is_positive_number(value):
    try:
        return float(value) > 0
    except ValueError:
        return False

def is_non_empty(value):
    return bool(value and str(value).strip()) 
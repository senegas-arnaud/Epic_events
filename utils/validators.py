import re
from datetime import datetime

def validate_email(email: str) -> bool:
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
    return bool(re.match(pattern, email))

def validate_phone(phone: str) -> bool:
    pattern = r'^\+?[\d\s\-]{7,20}$'
    return bool(re.match(pattern, phone))

def validate_date(date_str: str) -> datetime | None:
    try:
        return datetime.strptime(date_str, "%d/%m/%Y %H:%M")
    except ValueError:
        return None

def validate_positive_float(value: str) -> float | None:
    try:
        f = float(value)
        return f if f >= 0 else None
    except ValueError:
        return None

def validate_positive_int(value: str) -> int | None:
    try:
        i = int(value)
        return i if i >= 0 else None
    except ValueError:
        return None
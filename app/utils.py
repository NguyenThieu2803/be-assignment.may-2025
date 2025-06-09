def generate_uuid():
    import uuid
    return uuid.uuid4()

def format_timestamp(timestamp):
    return timestamp.isoformat() if timestamp else None

def validate_email(email):
    import re
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None
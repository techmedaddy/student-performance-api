# app/utils/validators.py

def validate_score(score: float):
    if not 0 <= score <= 100:
        raise ValueError("Score must be between 0 and 100.")

def validate_name(name: str):
    if not name or not name.strip():
        raise ValueError("Name cannot be empty or contain only whitespace.")

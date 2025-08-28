# app/crud/score.py

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.score import Score
from app.models.student import Student
from app.schemas.score import ScoreCreate

def add_or_update_score(db: Session, student_id: int, score: ScoreCreate) -> Score:
    db_score = db.query(Score).filter(
        Score.student_id == student_id, 
        Score.subject == score.subject
    ).first()

    if db_score:
        db_score.score = score.score
    else:
        db_score = Score(**score.dict(), student_id=student_id)
        db.add(db_score)
    
    db.commit()
    db.refresh(db_score)
    return db_score

def get_average_score(db: Session, student_id: int) -> float | None:
    result = db.query(func.avg(Score.score)).filter(Score.student_id == student_id).scalar()
    return result

def get_top_scorer_in_subject(db: Session, subject: str) -> Student | None:
    top_score = db.query(Score).filter(Score.subject == subject).order_by(Score.score.desc()).first()
    if top_score:
        return top_score.student
    return None

def get_department_average(db: Session, department: str) -> float | None:
    result = db.query(func.avg(Score.score)).join(Student).filter(Student.department == department).scalar()
    return result

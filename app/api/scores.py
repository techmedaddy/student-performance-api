# app/api/scores.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud import score as score_crud
from app.crud import student as student_crud
from app.schemas.score import ScoreCreate, ScoreResponse
from app.core.database import get_db
from app.models.score import Score

router = APIRouter()

@router.post("/students/{student_id}/scores/", response_model=ScoreResponse, status_code=status.HTTP_201_CREATED)
def add_student_score(student_id: int, score: ScoreCreate, db: Session = Depends(get_db)):
    db_student = student_crud.get_student_by_id(db, student_id=student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return score_crud.add_or_update_score(db=db, student_id=student_id, score=score)

@router.get("/students/{student_id}/average-score/")
def get_student_average_score(student_id: int, db: Session = Depends(get_db)):
    db_student = student_crud.get_student_by_id(db, student_id=student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    
    average_score = score_crud.get_average_score(db, student_id=student_id)
    if average_score is None:
        raise HTTPException(status_code=404, detail="No scores found for this student")
        
    return {"student_id": student_id, "average_score": round(average_score, 2)}

@router.get("/students/top-scorer/{subject}/")
def get_top_scorer(subject: str, db: Session = Depends(get_db)):
    top_student = score_crud.get_top_scorer_in_subject(db, subject=subject)
    if top_student is None:
        raise HTTPException(status_code=404, detail=f"No scores found for subject '{subject}'")
    
    # Fetch the specific score to include in the response
    score_obj = db.query(Score).filter(
        Score.student_id == top_student.id, 
        Score.subject == subject
    ).first()

    return {
        "student_id": top_student.id,
        "name": top_student.name,
        "subject": subject,
        "score": score_obj.score
    }

@router.get("/departments/{department}/average-score/")
def get_department_average_score(department: str, db: Session = Depends(get_db)):
    average_score = score_crud.get_department_average(db, department=department)
    if average_score is None:
        raise HTTPException(status_code=404, detail=f"No scores found for department '{department}'")
        
    return {"department": department, "average_score": round(average_score, 2)}

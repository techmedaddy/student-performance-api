# app/api/students.py

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud import student as student_crud
from app.schemas.student import StudentCreate, StudentResponse
from app.core.database import get_db

router = APIRouter()

@router.post("/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    return student_crud.create_student(db=db, student=student)

@router.get("/", response_model=List[StudentResponse])
def read_students(db: Session = Depends(get_db)):
    students = student_crud.get_students(db)
    return students

@router.get("/search/", response_model=List[StudentResponse])
def search_students_by_name(name: str, db: Session = Depends(get_db)):
    students = student_crud.get_student_by_name(db, name=name)
    if not students:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No students found with name matching '{name}'"
        )
    return students

@router.get("/{student_id}", response_model=StudentResponse)
def read_student(student_id: int, db: Session = Depends(get_db)):
    db_student = student_crud.get_student_by_id(db, student_id=student_id)
    if db_student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Student not found"
        )
    return db_student

@router.delete("/{student_id}", status_code=status.HTTP_200_OK)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    db_student = student_crud.delete_student(db, student_id=student_id)
    if db_student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Student not found"
        )
    return {"message": f"Student with id {student_id} deleted successfully."}

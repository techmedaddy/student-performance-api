# app/crud/student.py

from typing import List
from sqlalchemy.orm import Session

from app.models.student import Student
from app.schemas.student import StudentCreate

def get_students(db: Session) -> List[Student]:
    return db.query(Student).all()

def get_student_by_id(db: Session, student_id: int) -> Student | None:
    return db.query(Student).filter(Student.id == student_id).first()

def get_student_by_name(db: Session, name: str) -> List[Student]:
    search = f"%{name}%"
    return db.query(Student).filter(Student.name.ilike(search)).all()

def create_student(db: Session, student: StudentCreate) -> Student:
    db_student = Student(
        name=student.name, 
        age=student.age, 
        department=student.department
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def delete_student(db: Session, student_id: int) -> Student | None:
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if db_student:
        db.delete(db_student)
        db.commit()
    return db_student

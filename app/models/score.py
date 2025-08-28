# app/models/score.py

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base

class Score(Base):
    __tablename__ = "scores"

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String, index=True, nullable=False)
    score = Column(Float, nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)

    student = relationship("Student", back_populates="scores")

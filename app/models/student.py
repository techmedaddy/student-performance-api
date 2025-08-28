# app/models/student.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base

class Student(Base):
    """
    SQLAlchemy model for the 'students' table.
    """
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    age = Column(Integer, nullable=False)
    department = Column(String, nullable=False)

    # Relationship to the Score model
    # This creates a one-to-many relationship.
    # The 'back_populates' argument establishes a bidirectional relationship
    # with the 'student' attribute on the Score model.
    # 'cascade="all, delete-orphan"' means that if a Student is deleted,
    # all of their associated Score records will also be deleted.
    scores = relationship("Score", back_populates="student", cascade="all, delete-orphan")

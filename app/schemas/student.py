# app/schemas/student.py

from pydantic import BaseModel

class StudentBase(BaseModel):
    """
    Base Pydantic model for a student with common attributes.
    """
    name: str
    age: int
    department: str

class StudentCreate(StudentBase):
    """
    Pydantic model for creating a new student.
    Inherits all fields from StudentBase.
    No additional fields are needed for creation in this case.
    """
    pass

class StudentResponse(StudentBase):
    """
    Pydantic model for returning student data from the API.
    Includes the database-generated ID.
    """
    id: int

    class Config:
        """
        Pydantic's configuration class.
        orm_mode = True allows the model to be populated from a
        SQLAlchemy ORM object.
        """
        orm_mode = True

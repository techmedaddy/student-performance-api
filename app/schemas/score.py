# app/schemas/score.py

from pydantic import BaseModel

class ScoreBase(BaseModel):
    subject: str
    score: float

class ScoreCreate(ScoreBase):
    pass

class ScoreResponse(ScoreBase):
    id: int
    student_id: int

    class Config:
        orm_mode = True

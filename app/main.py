# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from app.api.v1.endpoints import students, scores
# from app.core.database import engine, Base 

app = FastAPI(
    title="Student Performance API",
    description="An API to manage student data and performance scores.",
    version="1.0.0",
)

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.on_event("startup")
# async def startup_db_client():
#     Base.metadata.create_all(bind=engine)

# @app.on_event("shutdown")
# async def shutdown_db_client():
#     pass

# app.include_router(students.router, prefix="/api/v1/students", tags=["Students"])
# app.include_router(scores.router, prefix="/api/v1/scores", tags=["Scores"])

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the Student Performance API!"}

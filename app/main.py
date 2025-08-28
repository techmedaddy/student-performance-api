from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import students, scores
from app.core.database import engine, Base

app = FastAPI(
    title="Student Performance API",
    description="An API to manage student data and performance scores.",
    version="1.0.0",
)

# Allow all origins (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create DB tables on startup (good for dev, Alembic is better for prod)
@app.on_event("startup")
async def startup_db_client():
    Base.metadata.create_all(bind=engine)

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the Student Performance API!"}

# Register routers
app.include_router(students.router, prefix="/students", tags=["Students"])
app.include_router(scores.router, prefix="/scores", tags=["Scores"])

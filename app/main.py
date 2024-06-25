# app/main.py

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from uuid import UUID, uuid4
from sqlalchemy.orm import Session
import app.models as models
from app.database import SessionLocal, init_db

app = FastAPI()

# Initialize the database
init_db()

class JobCreate(BaseModel):
    company_name: str
    job_title: str
    job_description: str
    experience: int
    package_upto: float
    skills: List[str]
    location: str
    job_type: str
    email: str

class JobRead(JobCreate):
    id: UUID

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/jobs/", response_model=JobRead)
def create_job(job: JobCreate, db: Session = Depends(get_db)):
    db_job = models.Job(
        id=uuid4(),
        company_name=job.company_name,
        job_title=job.job_title,
        job_description=job.job_description,
        experience=job.experience,
        package_upto=job.package_upto,
        skills=",".join(job.skills),  # Convert list to comma-separated string
        location=job.location,
        job_type=job.job_type,
        email=job.email,
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

@app.get("/jobs/", response_model=List[JobRead])
def get_jobs(db: Session = Depends(get_db)):
    return db.query(models.Job).all()

@app.get("/jobs/{job_id}", response_model=JobRead)
def read_job(job_id: UUID, db: Session = Depends(get_db)):
    db_job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return db_job

@app.put("/jobs/{job_id}", response_model=JobRead)
def update_job(job_id: UUID, job: JobCreate, db: Session = Depends(get_db)):
    db_job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    db_job.company_name = job.company_name
    db_job.job_title = job.job_title
    db_job.job_description = job.job_description
    db_job.experience = job.experience
    db_job.package_upto = job.package_upto
    db_job.skills = ",".join(job.skills)
    db_job.location = job.location
    db_job.job_type = job.job_type
    db_job.email = job.email
    db.commit()
    db.refresh(db_job)
    return db_job

@app.delete("/jobs/{job_id}", response_model=JobRead)
def delete_job(job_id: UUID, db: Session = Depends(get_db)):
    db_job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    db.delete(db_job)
    db.commit()
    return db_job

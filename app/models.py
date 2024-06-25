# app/models.py
from sqlalchemy import Column, String, Integer, Float, Table
from sqlalchemy.dialects.sqlite import BLOB
from sqlalchemy.ext.declarative import declarative_base
from uuid import uuid4

Base = declarative_base()

class Job(Base):
    __tablename__ = "jobs"
    id = Column(BLOB, primary_key=True, default=uuid4)
    company_name = Column(String, nullable=False)
    job_title = Column(String, nullable=False)
    job_description = Column(String, nullable=False)
    experience = Column(Integer, nullable=False)
    package_upto = Column(Float, nullable=False)
    skills = Column(String, nullable=False)  # Store skills as a comma-separated string
    location = Column(String, nullable=False)
    job_type = Column(String, nullable=False)
    email = Column(String, nullable=False)

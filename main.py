from fastapi import FastAPI , HTTPException
from pydantic import BaseModel
from typing import List
from uuid import uuid4 , UUID

app=FastAPI()

class job(BaseModel):
    id:UUID
    company_name :str
    job_tittle:str
    job_Description:str
    experience:int
    package_upto:float
    skill: List[str]
    locaton:str
    jobs_type:str
    email:str
    
    
jobs=[]

@app.post("/jobs/")
def create_job(job:job):
    job.id=uuid4()
    jobs.append(job)
    return job
    
@app.get("/")
def get_one():
    return jobs


@app.get("/jobs/{job_id}")
def read_job(job_id: UUID):
    
    for job in jobs:
        if job.id == job_id:
            
           return job
    raise HTTPException(status_code=404,detail="job not found")
    

@app.put("/jobs/{job_id}")

def update_job(job_id:UUID,update_job:job):
    
    for i, job in enumerate(jobs):
        
        if job.id == job_id:
            jobs[i] =update_job
            jobs[i].id = job_id
            
            return update_job
    raise HTTPException(status_code=404,detail="job not found")    


@app.delete("/jobs/{job_id}")

def delete_job(job_id:UUID):
    for i , job in enumerate(jobs):
        if job.id==job_id:
            delete_job=jobs.pop(i)
            return delete_job
        
    raise HTTPException(status_code=404,detail="job not found")    


   
if __name__ =="__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0" ,port=8000)
from fastapi import FastAPI , HTTPException
from pydantic import BaseModel
from typing import List

app=FastAPI()

class job(BaseModel):
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
    jobs.append(job)
    return job
    
    

@app.get("/jobs/")

def get_one():
    return jobs


@app.get("/jobs/{job_id}")

def read_job(job_id:int):
    if job_id >=len(jobs) or job_id<0:
        raise HTTPException(status_code=404,detail="job not found")
    
    return jobs[job_id]
   



if __name__ =="__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0" ,port=8000)
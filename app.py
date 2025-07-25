from fastapi import FastAPI
from pydantic import BaseModel
import openai

app = FastAPI()

class JobInput(BaseModel):
    job_description: str
    resume_summary: str

@app.post("/generate-cover-letter")
def generate_letter(data: JobInput):
    prompt = f"Write a tailored cover letter for the following job using this resume:

Job: {data.job_description}

Resume: {data.resume_summary}"
    # Mock response from GPT
    return {"cover_letter": "Dear Hiring Manager, I am excited to apply for..."}


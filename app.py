from fastapi import FastAPI
from pydantic import BaseModel
import openai

app = FastAPI()

class JobInput(BaseModel):
    job_description: str
    resume_summary: str

@app.post("/generate-cover-letter")
def generate_letter(data: JobInput):
    prompt = (
        f"Write a tailored cover letter for the following job using this resume.\n\n"
        f"Job Description:\n{data.job_description}\n\n"
        f"Resume Summary:\n{data.resume_summary}"
    )
    
    # Placeholder response - replace with actual OpenAI API call if needed
    return {"cover_letter": "Dear Hiring Manager, I am excited to apply for this role..."}
@app.get("/")
def home():
    return {"message": "LLM Job Application Agent is live!"}


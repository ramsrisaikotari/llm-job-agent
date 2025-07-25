import os
import openai
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Load API key securely from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

class JobInput(BaseModel):
    job_description: str
    resume_summary: str

@app.get("/")
def home():
    return {"message": "LLM Job Application Agent is live!"}

@app.post("/generate-cover-letter")
def generate_letter(data: JobInput):
    prompt = (
        f"You are a job applicant with the following background:\n"
        f"{data.resume_summary}\n\n"
        f"Write a personalized cover letter tailored to this job description:\n"
        f"{data.job_description}\n\n"
        f"Make it concise (under 300 words), professional, and avoid repetition."
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that writes excellent cover letters."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return {"cover_letter": response['choices'][0]['message']['content'].strip()}
    except Exception as e:
        return {"error": str(e)}

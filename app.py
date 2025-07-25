import os
import openai
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Load API key securely
openai.api_key = os.getenv("OPENAI_API_KEY")

class JobInput(BaseModel):
    job_description: str
    resume_summary: str
    tone: str = "professional"     # Optional field with default
    language: str = "English"
    job_title: str = "Software Engineer"

@app.get("/")
def home():
    return {"message": "LLM Job Application Agent is live!"}

@app.post("/generate-cover-letter")
def generate_letter(data: JobInput):
    prompt = (
        f"Write a {data.tone} cover letter in {data.language} for the job title '{data.job_title}'.\n\n"
        f"Job Description:\n{data.job_description}\n\n"
        f"Resume Summary:\n{data.resume_summary}\n\n"
        f"Make it concise (under 300 words), professional, well-structured, and avoid repetition."
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that writes excellent cover letters."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=600
        )
        return {"cover_letter": response['choices'][0]['message']['content'].strip()}
    except Exception as e:
        return {"error": str(e)}

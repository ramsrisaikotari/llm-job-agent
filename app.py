import os
import openai
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://ramsrisaikotari.github.io"],  # or use ["*"] for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load API key securely
openai.api_key = os.getenv("OPENAI_API_KEY")

class JobInput(BaseModel):
    job_description: str
    resume_summary: str
    job_title: str = "Software Engineer"
    tone: str = "Professional"
    language: str = "English"

@app.get("/")
def home():
    return {"message": "LLM Job Application Agent is live!"}

@app.post("/generate-cover-letter")
def generate_letter(data: JobInput):
    prompt = (
        f"You are a job applicant applying for the position of {data.job_title}. "
        f"Your tone should be {data.tone}, and your letter must be in {data.language}.\n\n"
        f"Background:\n{data.resume_summary}\n\n"
        f"Job Description:\n{data.job_description}\n\n"
        f"Write a customized, concise (under 300 words), professional cover letter tailored for this role."
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert at writing tailored, ATS-optimized cover letters."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=600
        )
        return {
            "success": True,
            "job_title": data.job_title,
            "tone": data.tone,
            "language": data.language,
            "cover_letter": response['choices'][0]['message']['content'].strip()
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from pydantic import BaseModel
import httpx

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://ramsrisaikotari.github.io"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Set your OpenRouter API key here
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

class JobInput(BaseModel):
    job_description: str
    resume_summary: str
    job_title: str = "Software Engineer"
    tone: str = "Professional"
    language: str = "English"
    model: str = "openrouter/google/gemma-7b-it"  # ✅ default safe model

@app.get("/")
def home():
    return {"message": "LLM Job Application Agent is live!"}

@app.options("/generate-cover-letter")
async def preflight_handler(request: Request):
    return JSONResponse(content={"message": "CORS preflight passed"}, status_code=200)

@app.post("/generate-cover-letter")
async def generate_letter(data: JobInput):
    prompt = (
        f"You are a job applicant applying for the position of {data.job_title}. "
        f"Your tone should be {data.tone}, and your letter must be in {data.language}.\n\n"
        f"Background:\n{data.resume_summary}\n\n"
        f"Job Description:\n{data.job_description}\n\n"
        f"Write a customized, concise (under 300 words), professional cover letter tailored for this role."
    )

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://ramsrisaikotari.github.io",  # Your public site
        "X-Title": "LLM Job Application Agent"
    }

    payload = {
        "model": data.model,
        "messages": [
            {"role": "system", "content": "You are an expert at writing tailored, ATS-optimized cover letters."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 600
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            completion = response.json()
            return {
                "success": True,
                "cover_letter": completion["choices"][0]["message"]["content"].strip(),
                "model_used": data.model
            }
    except httpx.HTTPStatusError as e:
        return {"success": False, "error": f"Error code: {e.response.status_code} - {e.response.text}"}
    except Exception as e:
        return {"success": False, "error": str(e)}

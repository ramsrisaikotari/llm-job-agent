import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import httpx

app = FastAPI()

# ✅ CORS for GitHub Pages
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://ramsrisaikotari.github.io"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Input model
class JobInput(BaseModel):
    job_description: str
    resume_summary: str
    job_title: str = "Software Engineer"
    tone: str = "Professional"
    language: str = "English"
    model: str = "openrouter/openai/gpt-3.5-turbo"  # default fallback

@app.get("/")
def home():
    return {"message": "LLM Job Application Agent is live!"}

@app.options("/generate-cover-letter")
async def preflight_handler(request: Request):
    return JSONResponse(content={"message": "CORS preflight passed"}, status_code=200)

@app.post("/generate-cover-letter")
async def generate_letter(data: JobInput):
    # Construct the prompt
    prompt = (
        f"You are a job applicant applying for the position of {data.job_title}. "
        f"Your tone should be {data.tone}, and your letter must be in {data.language}.\n\n"
        f"Background:\n{data.resume_summary}\n\n"
        f"Job Description:\n{data.job_description}\n\n"
        f"Write a customized, concise (under 300 words), professional cover letter tailored for this role."
    )

    # Request payload for OpenRouter
    payload = {
        "model": data.model,
        "messages": [
            {"role": "system", "content": "You are an expert at writing tailored, ATS-optimized cover letters."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 600,
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
                    "HTTP-Referer": "https://ramsrisaikotari.github.io",  # optional but helps for tracking
                    "X-Title": "LLM Job App Agent",
                    "Content-Type": "application/json"
                },
                json=payload
            )
            response.raise_for_status()
            result = response.json()

        content = result["choices"][0]["message"]["content"].strip()
        return {
            "success": True,
            "job_title": data.job_title,
            "tone": data.tone,
            "language": data.language,
            "cover_letter": content
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

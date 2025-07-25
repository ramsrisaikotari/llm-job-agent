import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import httpx

# Replace with your actual site if different
FRONTEND_ORIGIN = "https://ramsrisaikotari.github.io"

# Get OpenRouter key from environment
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

app = FastAPI()

# ✅ Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class JobInput(BaseModel):
    job_title: str = "Software Engineer"
    tone: str = "Professional"
    language: str = "English"
    resume_summary: str
    job_description: str
    model: str = "openai/gpt-3.5-turbo"  # Default model

@app.get("/")
def read_root():
    return {"message": "LLM Job Agent API is live."}

@app.options("/generate-cover-letter")
async def handle_options(request: Request):
    return JSONResponse(content={"message": "CORS OK"}, status_code=200)

@app.post("/generate-cover-letter")
async def generate_letter(data: JobInput):
    prompt = (
        f"You are a job applicant applying for the position of {data.job_title}. "
        f"Your tone should be {data.tone}, and your letter must be in {data.language}.\n\n"
        f"Resume Summary:\n{data.resume_summary}\n\n"
        f"Job Description:\n{data.job_description}\n\n"
        f"Write a customized, concise (under 300 words), professional cover letter tailored for this role."
    )

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
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
            response = await client.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=body)
            result = response.json()

        if "choices" in result and result["choices"]:
            return {
                "success": True,
                "cover_letter": result["choices"][0]["message"]["content"].strip()
            }
        else:
            return {"success": False, "error": "Invalid response from model."}
    except Exception as e:
        return {"success": False, "error": str(e)}

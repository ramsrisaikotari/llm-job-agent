# AI-Powered Job Application Agent

An intelligent agent that scans job boards, matches resume keywords, and auto-generates tailored cover letters using GPT-4 and LangChain.

---

## Tech Stack
- OpenAI GPT-4 APIs + LangChain
- FastAPI (Python) for orchestration
- AWS Lambda for serverless deployment
- Resume parser with spaCy
- GitHub Copilot + ChatGPT Enterprise used for development

---

## How It Works
1. Scrapes job descriptions from LinkedIn/Indeed
2. Parses JD & resume content using NLP
3. Uses prompt-engineered GPT-4 templates for cover letter generation
4. Auto-fills job forms (planned via Puppeteer)

---

## Key Features
- End-to-end LLM agent pipeline
- Personalized application generation
- Confidential resume & JD matching system

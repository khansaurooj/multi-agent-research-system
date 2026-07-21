from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from agents.planner import plan_research
from agents.researcher import research_topic
from agents.summarizer import summarize_research
from agents.writer import write_report
from agents.reviewer import review_report
from agents.searcher import search_web
from utils.pdf_generator import generate_pdf

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ResearchRequest(BaseModel):
    topic: str

class TextRequest(BaseModel):
    text: str

class PDFRequest(BaseModel):
    topic: str
    plan: str = ""
    research: str = ""
    summary: str = ""
    report: str = ""
    review: str = ""
    sources: list = []

@app.get("/")
def root():
    return {"status": "Multi-Agent Research API is running"}

@app.post("/plan")
def get_plan(request: ResearchRequest):
    plan = plan_research(request.topic)
    return {"topic": request.topic, "plan": plan}

@app.post("/research")
def get_research(request: ResearchRequest):
    try:
        research, sources = research_topic(request.topic)
        return {"topic": request.topic, "research": research, "sources": sources}
    except Exception as e:
        return {"error": f"Research failed: {str(e)}"}

@app.post("/summarize-text")
def summarize_text(request: TextRequest):
    try:
        summary = summarize_research(request.text)
        return {"summary": summary}
    except Exception as e:
        return {"error": f"Summarize failed: {str(e)}"}

@app.post("/review-text")
def review_text(request: TextRequest):
    try:
        review = review_report(request.text)
        return {"review": review}
    except Exception as e:
        return {"error": f"Review failed: {str(e)}"}

@app.post("/export-pdf")
def export_pdf(request: PDFRequest):
    try:
        content = {
            "plan": request.plan,
            "research": request.research,
            "summary": request.summary,
            "report": request.report,
            "review": request.review,
            "sources": request.sources
        }
        pdf_path = generate_pdf(request.topic, content)
        return FileResponse(pdf_path, media_type="application/pdf", filename="research-report.pdf")
    except Exception as e:
        return {"error": f"PDF export failed: {str(e)}"}

@app.post("/pipeline")
def run_pipeline(request: ResearchRequest):
    try:
        plan = plan_research(request.topic)
        research, sources = research_topic(request.topic)
        summary = summarize_research(research)
        report = write_report(request.topic, summary)
        review = review_report(report)

        return {
            "topic": request.topic,
            "plan": plan,
            "research": research,
            "sources": sources,
            "summary": summary,
            "report": report,
            "review": review
        }
    except Exception as e:
        return {"error": f"Pipeline failed: {str(e)}"}
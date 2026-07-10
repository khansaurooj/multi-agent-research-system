from fastapi import FastAPI
from pydantic import BaseModel
from agents.planner import plan_research
from agents.researcher import research_topic
from agents.summarizer import summarize_research
from agents.writer import write_report
from agents.reviewer import review_report

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ResearchRequest(BaseModel):
    topic: str

@app.get("/")
def root():
    return {"status": "Multi-Agent Research API is running"}

@app.post("/plan")
def get_plan(request: ResearchRequest):
    plan = plan_research(request.topic)
    return {"topic": request.topic, "plan": plan}
class TextRequest(BaseModel):
    text: str

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

@app.post("/research")
def get_research(request: ResearchRequest):
    research = research_topic(request.topic)
    return {"topic": request.topic, "research": research}

@app.post("/pipeline")
def run_pipeline(request: ResearchRequest):
    try:
        plan = plan_research(request.topic)
        research = research_topic(request.topic)
        summary = summarize_research(research)
        report = write_report(request.topic, summary)
        review = review_report(report)

        return {
            "topic": request.topic,
            "plan": plan,
            "research": research,
            "summary": summary,
            "report": report,
            "review": review
        }
    except Exception as e:
        return {"error": f"Pipeline failed: {str(e)}"}


    return {
        "topic": request.topic,
        "plan": plan,
        "research": research,
        "summary": summary,
        "report": report,
        "review": review
    }

    
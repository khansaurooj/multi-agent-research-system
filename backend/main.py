from fastapi import FastAPI
from pydantic import BaseModel
from agents.planner import plan_research
from agents.researcher import research_topic
from agents.summarizer import summarize_research
from agents.writer import write_report
from agents.reviewer import review_report

app = FastAPI()

class ResearchRequest(BaseModel):
    topic: str

@app.get("/")
def root():
    return {"status": "Multi-Agent Research API is running"}

@app.post("/plan")
def get_plan(request: ResearchRequest):
    plan = plan_research(request.topic)
    return {"topic": request.topic, "plan": plan}

@app.post("/research")
def get_research(request: ResearchRequest):
    research = research_topic(request.topic)
    return {"topic": request.topic, "research": research}
@app.post("/pipeline")
def run_pipeline(request: ResearchRequest):
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
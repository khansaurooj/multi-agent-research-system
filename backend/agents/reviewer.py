import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def review_report(report: str) -> str:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=600,
        messages=[{
            "role": "user",
            "content": f"""You are a senior editor reviewing a research report. Check for: grammar issues, missing sections, unclear explanations, and repeated content. 

If the report is good, respond with "APPROVED" followed by a one-sentence reason.
If it needs fixes, respond with "NEEDS REVISION" followed by a bullet list of specific issues.

Report:
{report}"""
        }]
    )
    return response.choices[0].message.content
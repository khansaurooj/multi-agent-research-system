from utils.groq_client import client

def review_report(text: str) -> str:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=600,
        messages=[{
            "role": "user",
            "content": f"""You are an editor. Review the text below and give direct, useful feedback.

If it's a short phrase, sentence, or question: check spelling, grammar, and word choice only. Don't ask for missing sections like introduction or conclusion — that doesn't apply.

If it's a full document or report: check grammar, structure, missing sections, clarity, and repetition.

Text:
{text}

Respond with your specific feedback. If nothing is wrong, just say so plainly."""
        }]
    )
    return response.choices[0].message.content
from fpdf import FPDF
import re

def clean_text(text) -> str:
    if not text:
        return ""
    text = str(text)
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'#+\s*', '', text)
    text = re.sub(r'[^\x00-\x7F]+', '', text)  # strip all non-ASCII (emojis, special symbols)
    return text

def generate_pdf(topic: str, content: dict) -> str:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 18)
    pdf.multi_cell(0, 10, clean_text(topic))
    pdf.ln(5)

    sections = [
        ("Plan", content.get("plan")),
        ("Research", content.get("research")),
        ("Summary", content.get("summary")),
        ("Report", content.get("report")),
        ("Review", content.get("review")),
    ]

    for title, text in sections:
        if not text:
            continue
        pdf.set_font("Helvetica", "B", 14)
        pdf.multi_cell(0, 10, clean_text(title))
        pdf.ln(1)
        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(0, 7, clean_text(text))
        pdf.ln(5)

    if content.get("sources"):
        pdf.set_font("Helvetica", "B", 14)
        pdf.multi_cell(0, 10, "Sources")
        pdf.set_font("Helvetica", "", 10)
        for i, source in enumerate(content["sources"], 1):
            line = f"{i}. {clean_text(source.get('title', ''))} - {clean_text(source.get('url', ''))}"
            pdf.multi_cell(0, 6, line)

    output_path = "/tmp/report.pdf"
    pdf.output(output_path)
    return output_path
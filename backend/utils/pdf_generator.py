from fpdf import FPDF
import re
import textwrap

def clean_text(text) -> str:
    if not text:
        return ""
    text = str(text)
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'#+\s*', '', text)
    text = re.sub(r'[^\x00-\x7F]+', '', text)
    return text

def write_wrapped(pdf, text, width_chars=85, line_height=7):
    """Manually wrap text into short lines using textwrap, then print each
    line with a simple cell call. This avoids fpdf2's internal word-wrap
    entirely, so long URLs or unbroken strings can never cause a crash."""
    if not text:
        return
    paragraphs = text.split('\n')
    for para in paragraphs:
        if para.strip() == "":
            pdf.ln(line_height / 2)
            continue
        # hard-wrap even single long words/URLs with no spaces
        wrapped_lines = textwrap.wrap(
            para, width=width_chars, break_long_words=True, break_on_hyphens=False
        )
        if not wrapped_lines:
            wrapped_lines = [""]
        for line in wrapped_lines:
            pdf.cell(0, line_height, line, new_x="LMARGIN", new_y="NEXT")

def generate_pdf(topic: str, content: dict) -> str:
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 18)
    write_wrapped(pdf, clean_text(topic), width_chars=60, line_height=10)
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
        write_wrapped(pdf, clean_text(title), width_chars=70, line_height=10)
        pdf.ln(1)
        pdf.set_font("Helvetica", "", 11)
        write_wrapped(pdf, clean_text(text), width_chars=85, line_height=7)
        pdf.ln(5)

    if content.get("sources"):
        pdf.set_font("Helvetica", "B", 14)
        write_wrapped(pdf, "Sources", width_chars=70, line_height=10)
        pdf.set_font("Helvetica", "", 10)
        for i, source in enumerate(content["sources"], 1):
            title_text = clean_text(source.get('title', ''))
            url_text = clean_text(source.get('url', ''))
            write_wrapped(pdf, f"{i}. {title_text}", width_chars=85, line_height=6)
            pdf.set_font("Helvetica", "I", 9)
            write_wrapped(pdf, url_text, width_chars=90, line_height=6)
            pdf.set_font("Helvetica", "", 10)
            pdf.ln(2)

    output_path = "/tmp/report.pdf"
    pdf.output(output_path)
    return output_path
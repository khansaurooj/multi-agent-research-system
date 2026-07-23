# 🤖 Multi-Agent Research System

An AI-powered research assistant that plans, researches, summarizes, writes, and reviews reports — powered by 6 specialized agents working together, grounded in real-time web search.

**🔗 Live Demo:** [(https://multi-agent-research-system-ten.vercel.app/)]

---

## 💡 What It Does

Instead of asking one AI model to do everything at once, this system splits the work across 6 specialized agents — the same way a real research team would operate:
User Topic
↓
🧭 Planner → breaks the topic into a research plan
↓
🔍 Researcher → searches the live web (via Tavily) for real, current facts
↓
✂️ Summarizer → condenses findings into a clean summary
↓
📝 Writer → turns the summary into a polished, structured report
↓
✅ Reviewer → checks the report for quality, clarity, and gaps
↓
Final Report + Sources

## ✨ Features

- **4 usage modes** — Full Report, Quick Research, Summarize Text, Review Text
- **Real web search grounding** — Researcher pulls live results via Tavily, not just model memory
- **Clickable source citations** — every research result links back to its real source
- **Report history** — past reports are saved (SQLite) and revisitable from a sidebar
- **PDF & text export** — download any report as a formatted PDF or plain text
- **Live agent progress tracker** — see which agent is currently working
- **Typewriter-style report reveal** for a more natural feel
- **Fully responsive, animated dashboard** with a particle-network background

## 🛠️ Tech Stack

**Backend**
- FastAPI (Python)
- Groq (Llama 3.3 70B) — LLM inference
- Tavily API — real-time web search
- SQLite — report history persistence
- fpdf2 — PDF generation

**Frontend**
- React (Vite)
- react-markdown — renders formatted agent output
- Custom CSS animations (particle canvas, typewriter effect, transitions)

**Deployment**
- Backend: Railway
- Frontend: [Vercel / wherever you deployed]

## 📸 Screenshots

<!-- Add 2-4 screenshots here showing: the mode selector, a generated report with sources, the history sidebar, and the PDF export -->

## 🚀 Running Locally

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file in `backend/`:
GROQ_API_KEY=your_key_here
TAVILY_API_KEY=your_key_here

Run the server:
```bash
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Update `BACKEND_URL` in `frontend/src/App.jsx` to point to your running backend.

## 🧠 Architecture Decisions

- **Why multiple agents instead of one prompt?** Each agent has a single responsibility, making outputs more reliable and the system easier to debug and extend — mirroring how real engineering teams divide work.
- **Why Groq?** Free tier, fast inference (Llama 3.3 70B), no credit card required for students building and iterating quickly.
- **Why Tavily?** Purpose-built search API for AI agents — returns clean, structured results instead of raw HTML scraping.

## 🔮 Future Improvements

- Fact-Checker agent to cross-verify claims against sources
- Streaming responses instead of waiting for full pipeline completion
- User accounts for private report history

## 📄 License

MIT
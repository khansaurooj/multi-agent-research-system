import { useState, useEffect } from 'react'
import ReactMarkdown from 'react-markdown'
import Typewriter from './Typewriter'
import ParticleBackground from './ParticleBackground'
import './App.css'

const BACKEND_URL = "https://multi-agent-research-system-production-d88d.up.railway.app"
const AGENTS = [
  { key: "plan", label: "Planner", icon: "🧭", status: "Planning the research approach..." },
  { key: "research", label: "Researcher", icon: "🔍", status: "Searching the web for current info..." },
  { key: "summary", label: "Summarizer", icon: "✂️", status: "Condensing findings..." },
  { key: "report", label: "Writer", icon: "📝", status: "Writing the final report..." },
  { key: "review", label: "Reviewer", icon: "✅", status: "Reviewing quality and clarity..." },
]

const MODES = [
  { key: "pipeline", label: "Full Report", icon: "🚀", desc: "Runs all 6 agents on a topic" },
  { key: "research", label: "Quick Research", icon: "🔍", desc: "Just research a topic" },
  { key: "summarize", label: "Summarize Text", icon: "✂️", desc: "Paste text, get a summary" },
  { key: "review", label: "Review Text", icon: "✅", desc: "Paste text, get feedback" },
]

function App() {
  const [mode, setMode] = useState("pipeline")
  const [input, setInput] = useState("")
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState("")
  const [activeTab, setActiveTab] = useState("report")
  const [progressStep, setProgressStep] = useState(0)
  const [history, setHistory] = useState([])
  const [sidebarOpen, setSidebarOpen] = useState(false)

  const endpoints = {
    pipeline: { url: "/pipeline", body: (v) => ({ topic: v }) },
    research: { url: "/research", body: (v) => ({ topic: v }) },
    summarize: { url: "/summarize-text", body: (v) => ({ text: v }) },
    review: { url: "/review-text", body: (v) => ({ text: v }) },
  }

  const tabKeys = result ? Object.keys(result).filter(k => k !== "topic" && k !== "sources" && k !== "id") : []

  useEffect(() => {
    loadHistory()
  }, [])

  const loadHistory = async () => {
    try {
      const res = await fetch(`${BACKEND_URL}/history`)
      const data = await res.json()
      setHistory(data.reports || [])
    } catch (err) {
      console.error("Failed to load history")
    }
  }

  const loadReport = async (id) => {
    try {
      const res = await fetch(`${BACKEND_URL}/history/${id}`)
      const data = await res.json()
      setResult(data)
      setMode("pipeline")
      setActiveTab("report")
      setSidebarOpen(false)
    } catch (err) {
      alert("Failed to load report")
    }
  }

  const copyToClipboard = () => {
    const text = result[activeTab] || result[tabKeys[0]]
    navigator.clipboard.writeText(text)
    alert("Copied to clipboard!")
  }

  const downloadAsText = () => {
    const text = result[activeTab] || result[tabKeys[0]]
    const blob = new Blob([text], { type: "text/plain" })
    const url = URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url
    a.download = `${activeTab}-${Date.now()}.txt`
    a.click()
    URL.revokeObjectURL(url)
  }

  const downloadPDF = async () => {
    try {
      const response = await fetch(`${BACKEND_URL}/export-pdf`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          topic: result.topic || input,
          plan: result.plan || "",
          research: result.research || "",
          summary: result.summary || "",
          report: result.report || "",
          review: result.review || "",
          sources: result.sources || []
        })
      })
      const contentType = response.headers.get("content-type")
      if (!response.ok || (contentType && contentType.includes("application/json"))) {
        const errData = await response.json()
        alert("PDF export failed: " + (errData.error || "Unknown error"))
        return
      }
      const blob = await response.blob()
      const url = URL.createObjectURL(blob)
      const a = document.createElement("a")
      a.href = url
      a.download = "research-report.pdf"
      a.click()
      URL.revokeObjectURL(url)
    } catch (err) {
      alert("PDF export failed: " + err.message)
    }
  }

  const runAction = async () => {
    if (!input.trim()) return
    setLoading(true)
    setError("")
    setResult(null)
    setProgressStep(0)

    let stepTimer
    if (mode === "pipeline") {
      stepTimer = setInterval(() => {
        setProgressStep((prev) => (prev < AGENTS.length - 1 ? prev + 1 : prev))
      }, 1400)
    }

    try {
      const { url, body } = endpoints[mode]
      const response = await fetch(`${BACKEND_URL}${url}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body(input))
      })
      if (!response.ok) throw new Error("Server error")
      const data = await response.json()
      if (data.error) {
        setError(data.error)
      } else {
        setResult(data)
        if (mode === "pipeline") loadHistory()
        const keys = Object.keys(data).filter(k => k !== "topic" && k !== "sources" && k !== "id")
        setActiveTab(mode === "pipeline" ? "report" : keys[0])
        setProgressStep(AGENTS.length)
      }
    } catch (err) {
      setError("Something went wrong. Check your backend is running.")
    } finally {
      if (stepTimer) clearInterval(stepTimer)
      setLoading(false)
    }
  }

  const currentStatus = mode === "pipeline" && loading ? AGENTS[Math.min(progressStep, AGENTS.length - 1)].status : ""

  return (
    <div className="page">
      <ParticleBackground />

      <header className="header">
        <div className="logo">⚛️ Multi-Agent Research</div>
        <div className="header-right">
          <button className="history-toggle" onClick={() => setSidebarOpen(!sidebarOpen)}>
            🕘 History
          </button>
          <div className="header-tag">6 agents · 4 modes</div>
        </div>
      </header>

      <div className={`sidebar ${sidebarOpen ? "open" : ""}`}>
        <div className="sidebar-header">
          <h3>Past Reports</h3>
          <button className="sidebar-close" onClick={() => setSidebarOpen(false)}>✕</button>
        </div>
        <div className="sidebar-list">
          {history.length === 0 && <p className="sidebar-empty">No reports yet</p>}
          {history.map((item) => (
            <button key={item.id} className="sidebar-item" onClick={() => loadReport(item.id)}>
              <span className="sidebar-item-topic">{item.topic}</span>
              <span className="sidebar-item-date">{new Date(item.created_at).toLocaleDateString()}</span>
            </button>
          ))}
        </div>
      </div>
      {sidebarOpen && <div className="sidebar-overlay" onClick={() => setSidebarOpen(false)}></div>}

      <main className="container">
        <div className="mode-grid">
          {MODES.map((m) => (
            <button
              key={m.key}
              className={`mode-card ${mode === m.key ? "active" : ""}`}
              onClick={() => { setMode(m.key); setResult(null); setInput("") }}
            >
              <div className="mode-icon">{m.icon}</div>
              <div className="mode-label">{m.label}</div>
              <div className="mode-desc">{m.desc}</div>
            </button>
          ))}
        </div>

        <div className="hero-card">
          <div className="input-row">
            {mode === "summarize" || mode === "review" ? (
              <textarea
                placeholder="Paste your text here..."
                value={input}
                onChange={(e) => setInput(e.target.value)}
                rows={5}
              />
            ) : (
              <input
                type="text"
                placeholder="e.g. Explain quantum computing"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && runAction()}
              />
            )}
            <button onClick={runAction} disabled={loading}>
              {loading ? "Running..." : "Run"}
            </button>
          </div>

          {mode === "pipeline" && (loading || result) && (
            <>
              <div className="pipeline-track">
                {AGENTS.map((agent, i) => (
                  <div
                    key={agent.key}
                    className={`pipeline-step ${i < progressStep ? "done" : ""} ${i === progressStep && loading ? "active" : ""}`}
                  >
                    <div className="step-icon">{agent.icon}</div>
                    <span>{agent.label}</span>
                  </div>
                ))}
              </div>
              {currentStatus && <p className="status-text">{currentStatus}</p>}
            </>
          )}

          {error && <p className="error">{error}</p>}
        </div>

        {result && (
          <div className="results-card">
            {tabKeys.length > 1 && (
              <div className="tabs">
                {tabKeys.map((key) => (
                  <button
                    key={key}
                    className={`tab ${activeTab === key ? "active" : ""}`}
                    onClick={() => setActiveTab(key)}
                  >
                    {key.charAt(0).toUpperCase() + key.slice(1)}
                  </button>
                ))}
              </div>
            )}
            <div className="tab-content">
              <div className="tab-actions">
                <button className="action-btn" onClick={copyToClipboard}>📋 Copy</button>
                <button className="action-btn" onClick={downloadAsText}>⬇️ Download</button>
                {mode === "pipeline" && (
                  <button className="action-btn" onClick={downloadPDF}>📄 Download PDF</button>
                )}
              </div>

              <Typewriter text={result[activeTab] || result[tabKeys[0]]} key={activeTab} />

              {result.sources && result.sources.length > 0 && activeTab === "research" && (
                <div className="sources-section">
                  <h3>🔗 Sources</h3>
                  <div className="sources-grid">
                    {result.sources.map((source, i) => (
                      <a
                        key={i}
                        href={source.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="source-card"
                      >
                        <span className="source-number">{i + 1}</span>
                        <span className="source-title">{source.title}</span>
                      </a>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        )}
      </main>
    </div>
  )
}

export default App
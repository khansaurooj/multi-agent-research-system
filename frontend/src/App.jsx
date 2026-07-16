import { useState } from 'react'
import ReactMarkdown from 'react-markdown'
import './App.css'

const BACKEND_URL = "https://super-engine-g4rxxpxrxx47cvq54-8000.app.github.dev"

const AGENTS = [
  { key: "plan", label: "Planner", icon: "🧭" },
  { key: "research", label: "Researcher", icon: "🔍" },
  { key: "summary", label: "Summarizer", icon: "✂️" },
  { key: "report", label: "Writer", icon: "📝" },
  { key: "review", label: "Reviewer", icon: "✅" },
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

  const endpoints = {
    pipeline: { url: "/pipeline", body: (v) => ({ topic: v }) },
    research: { url: "/research", body: (v) => ({ topic: v }) },
    summarize: { url: "/summarize-text", body: (v) => ({ text: v }) },
    review: { url: "/review-text", body: (v) => ({ text: v }) },
  }

  const tabKeys = result ? Object.keys(result).filter(k => k !== "topic" && k !== "sources") : []

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
        const keys = Object.keys(data).filter(k => k !== "topic" && k !== "sources")
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

  return (
    <div className="page">
      <div className="bg-orb orb-1"></div>
      <div className="bg-orb orb-2"></div>
      <div className="bg-orb orb-3"></div>

      <header className="header">
        <div className="logo">⚛️ Multi-Agent Research</div>
        <div className="header-tag">6 agents · 4 modes</div>
      </header>

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
              </div>
              <ReactMarkdown>{result[activeTab] || result[tabKeys[0]]}</ReactMarkdown>

              {result.sources && result.sources.length > 0 && (
                <div className="sources-section">
                  <h3>🔗 Sources</h3>
                  <div className="sources-grid">
                    {result.sources.map((source, i) => (
                      
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
import { useState, useEffect, useRef } from 'react'
import ReactMarkdown from 'react-markdown'

function Typewriter({ text, speed = 8 }) {
  const [displayed, setDisplayed] = useState("")
  const indexRef = useRef(0)

  useEffect(() => {
    setDisplayed("")
    indexRef.current = 0

    const interval = setInterval(() => {
      indexRef.current += 3 // characters per tick, adjust for speed
      setDisplayed(text.slice(0, indexRef.current))
      if (indexRef.current >= text.length) {
        clearInterval(interval)
      }
    }, speed)

    return () => clearInterval(interval)
  }, [text, speed])

  return <ReactMarkdown>{displayed}</ReactMarkdown>
}

export default Typewriter
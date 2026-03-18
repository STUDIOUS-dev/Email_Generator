import { useState, useEffect, useCallback } from 'react'
import Header from './components/Header'
import EmailForm from './components/EmailForm'
import JobCard from './components/JobCard'
import EmailOutput from './components/EmailOutput'
import Loader from './components/Loader'
import StatusBadge from './components/StatusBadge'
import { generateEmail, checkHealth } from './api/emailApi'
import { AlertTriangle, RefreshCw } from 'lucide-react'

export default function App() {
  const [providers, setProviders] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [result, setResult] = useState(null)          // { email, job, provider_used, portfolio_links }
  const [error, setError] = useState(null)

  // Fetch provider health on mount
  useEffect(() => {
    checkHealth()
      .then((data) => setProviders(data.providers ?? []))
      .catch(() => setProviders([]))
  }, [])

  const handleGenerate = useCallback(async (formData) => {
    setIsLoading(true)
    setError(null)
    setResult(null)
    try {
      const data = await generateEmail(formData)
      setResult(data)
    } catch (err) {
      const msg =
        err?.response?.data?.detail ||
        err?.message ||
        'An unexpected error occurred. Please try again.'
      setError(msg)
    } finally {
      setIsLoading(false)
    }
  }, [])

  return (
    <div className="min-h-screen bg-pink-100">
      <Header providerStatus={providers} />

      <main className="max-w-3xl mx-auto px-4 py-10 space-y-6">

        {/* Hero line */}
        <div className="text-center animate-fade-in">
          <h2 className="text-3xl font-bold text-pink-950 tracking-tight mb-2">
            Land Your Dream Job with AI
          </h2>
          <p className="text-pink-400 text-base max-w-lg mx-auto">
            Paste a job posting URL. Our AI scrapes the listing, extracts the key requirements,
            and writes a compelling, personalised application email that positions you as the ideal candidate.
          </p>
        </div>

        {/* Provider status row */}
        {providers.length > 0 && (
          <div className="flex items-center gap-3 justify-center flex-wrap animate-fade-in">
            <span className="text-xs text-pink-400 font-medium">LLM Providers:</span>
            <StatusBadge providers={providers} />
          </div>
        )}

        {/* Input form */}
        <EmailForm onSubmit={handleGenerate} isLoading={isLoading} />

        {/* Error state */}
        {error && (
          <div className="card p-5 border-red-200 bg-red-50/50 flex items-start gap-3 animate-fade-in">
            <AlertTriangle size={18} className="text-red-500 mt-0.5 shrink-0" />
            <div>
              <p className="text-sm font-semibold text-red-700 mb-1">Something went wrong</p>
              <p className="text-xs text-red-600 leading-relaxed">{error}</p>
            </div>
          </div>
        )}

        {/* Loading skeleton */}
        {isLoading && <Loader />}

        {/* Results */}
        {result && !isLoading && (
          <div className="space-y-4">
            <JobCard job={result.job} />
            <EmailOutput
              email={result.email}
              portfolioLinks={result.portfolio_links}
              providerUsed={result.provider_used}
            />
            {/* Regenerate */}
            <div className="text-center pt-2">
              <button
                onClick={() => setResult(null)}
                className="btn-secondary"
              >
                <RefreshCw size={14} />
                Generate Another
              </button>
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="text-center py-10 text-xs text-pink-400 border-t border-pink-400/20 mt-auto">
        AI Job Application Writer &mdash; Powered by Groq &amp; Gemini with automatic LLM fallback
      </footer>
    </div>
  )
}

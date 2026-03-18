import { useState } from 'react'
import { Link, ChevronDown, ChevronUp, Sparkles, User, Github, Linkedin, Code } from 'lucide-react'

const DEFAULTS = {
  applicant_name: 'Abhay Kumar',
  applicant_skills: 'Python, Machine Learning, LangChain, FastAPI, LLMs, RAG, LangGraph',
  applicant_experience:
    'ML Engineer with hands-on experience building AI-powered applications including LLM-based agents, RAG pipelines, and full-stack ML products deployed on cloud infrastructure. Passionate about turning cutting-edge research into production-ready systems.',
  applicant_github: 'https://github.com/kabhay0120',
  applicant_linkedin: '',
}

export default function EmailForm({ onSubmit, isLoading }) {
  const [url, setUrl] = useState('')
  const [showAdvanced, setShowAdvanced] = useState(false)
  const [applicantName, setApplicantName] = useState(DEFAULTS.applicant_name)
  const [applicantSkills, setApplicantSkills] = useState(DEFAULTS.applicant_skills)
  const [applicantExperience, setApplicantExperience] = useState(DEFAULTS.applicant_experience)
  const [applicantGithub, setApplicantGithub] = useState(DEFAULTS.applicant_github)
  const [applicantLinkedin, setApplicantLinkedin] = useState(DEFAULTS.applicant_linkedin)
  const [urlError, setUrlError] = useState('')

  function validateUrl(value) {
    if (!value.trim()) return 'Job posting URL is required.'
    if (!value.startsWith('http://') && !value.startsWith('https://'))
      return 'URL must start with http:// or https://'
    return ''
  }

  function handleSubmit(e) {
    e.preventDefault()
    const err = validateUrl(url)
    if (err) { setUrlError(err); return }
    setUrlError('')
    onSubmit({
      url: url.trim(),
      applicant_name: applicantName.trim() || DEFAULTS.applicant_name,
      applicant_skills: applicantSkills.trim() || DEFAULTS.applicant_skills,
      applicant_experience: applicantExperience.trim() || DEFAULTS.applicant_experience,
      applicant_github: applicantGithub.trim(),
      applicant_linkedin: applicantLinkedin.trim(),
    })
  }

  return (
    <form onSubmit={handleSubmit} className="card p-8 animate-fade-in">
      <div className="mb-6">
        <h2 className="section-title mb-1">Job Posting URL</h2>
        <p className="text-pink-400 text-sm">
          Paste the URL of the job listing you want to apply for. The AI will scrape and analyse it automatically.
        </p>
      </div>

      {/* URL field */}
      <div className="mb-5">
        <label htmlFor="url" className="field-label">
          Job URL *
        </label>
        <div className="relative">
          <div className="absolute inset-y-0 left-3.5 flex items-center pointer-events-none">
            <Link size={15} className="text-pink-400" />
          </div>
          <input
            id="url"
            type="url"
            value={url}
            onChange={(e) => { setUrl(e.target.value); setUrlError('') }}
            placeholder="https://jobs.company.com/job/12345"
            className={`input-field pl-10 ${urlError ? 'border-red-400 focus:ring-red-300' : ''}`}
            disabled={isLoading}
            autoComplete="url"
          />
        </div>
        {urlError && (
          <p className="mt-1.5 text-xs text-red-500 font-medium">{urlError}</p>
        )}
      </div>

      {/* Applicant profile settings */}
      <div className="border-t border-pink-400/20 pt-4 mb-6">
        <button
          type="button"
          onClick={() => setShowAdvanced((v) => !v)}
          className="flex items-center gap-1.5 text-sm font-medium text-pink-700 hover:text-pink-950 transition-colors"
        >
          {showAdvanced ? <ChevronUp size={15} /> : <ChevronDown size={15} />}
          Your Profile &amp; Details
        </button>

        {showAdvanced && (
          <div className="mt-4 grid gap-4 animate-slide-up">

            {/* Name */}
            <div>
              <label htmlFor="applicant_name" className="field-label">
                <User size={11} className="inline mr-1" />Your Full Name
              </label>
              <input
                id="applicant_name"
                type="text"
                value={applicantName}
                onChange={(e) => setApplicantName(e.target.value)}
                placeholder="Abhay Kumar"
                className="input-field"
                disabled={isLoading}
              />
            </div>

            {/* Skills */}
            <div>
              <label htmlFor="applicant_skills" className="field-label">
                <Code size={11} className="inline mr-1" />Your Key Skills
              </label>
              <input
                id="applicant_skills"
                type="text"
                value={applicantSkills}
                onChange={(e) => setApplicantSkills(e.target.value)}
                placeholder="Python, Machine Learning, FastAPI, LangChain…"
                className="input-field"
                disabled={isLoading}
              />
              <p className="mt-1 text-xs text-pink-400">Comma-separated list of your top skills.</p>
            </div>

            {/* Experience summary */}
            <div>
              <label htmlFor="applicant_experience" className="field-label">
                Background &amp; Experience
              </label>
              <textarea
                id="applicant_experience"
                value={applicantExperience}
                onChange={(e) => setApplicantExperience(e.target.value)}
                placeholder="2–3 sentences summarising your background, what you build, and what makes you stand out…"
                className="input-field"
                rows={3}
                disabled={isLoading}
              />
            </div>

            {/* GitHub + LinkedIn */}
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label htmlFor="applicant_github" className="field-label">
                  <Github size={11} className="inline mr-1" />GitHub URL
                </label>
                <input
                  id="applicant_github"
                  type="url"
                  value={applicantGithub}
                  onChange={(e) => setApplicantGithub(e.target.value)}
                  placeholder="https://github.com/yourusername"
                  className="input-field"
                  disabled={isLoading}
                />
              </div>
              <div>
                <label htmlFor="applicant_linkedin" className="field-label">
                  <Linkedin size={11} className="inline mr-1" />LinkedIn URL
                </label>
                <input
                  id="applicant_linkedin"
                  type="url"
                  value={applicantLinkedin}
                  onChange={(e) => setApplicantLinkedin(e.target.value)}
                  placeholder="https://linkedin.com/in/yourprofile"
                  className="input-field"
                  disabled={isLoading}
                />
              </div>
            </div>

          </div>
        )}
      </div>

      {/* Submit */}
      <button type="submit" className="btn-primary w-full justify-center py-3.5 text-base" disabled={isLoading}>
        {isLoading ? (
          <>
            <span className="w-4 h-4 border-2 border-white/40 border-t-white rounded-full animate-spin" />
            Generating…
          </>
        ) : (
          <>
            <Sparkles size={17} strokeWidth={2} />
            Generate Application Email
          </>
        )}
      </button>
    </form>
  )
}

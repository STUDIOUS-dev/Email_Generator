import { CheckCircle, XCircle, AlertCircle } from 'lucide-react'

/**
 * Shows available/unavailable LLM providers inline.
 */
export default function StatusBadge({ providers }) {
  if (!providers?.length) return null

  return (
    <div className="flex flex-wrap gap-2">
      {providers.map((p) => (
        <div
          key={p.name}
          title={p.available ? `${p.name} — Available` : `${p.name} — No API key configured`}
          className={`flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium border transition-colors
            ${p.available
              ? 'bg-green-50 border-green-200 text-green-700'
              : 'bg-pink-100 border-pink-400/30 text-pink-400'
            }`}
        >
          {p.available
            ? <CheckCircle size={11} strokeWidth={2.5} />
            : <XCircle size={11} strokeWidth={2.5} />
          }
          <span>{p.name.split(' ')[0]}</span>
        </div>
      ))}
    </div>
  )
}

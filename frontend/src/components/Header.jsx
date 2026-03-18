import { Mail, Zap } from 'lucide-react'

export default function Header({ providerStatus }) {
  const activeProvider = providerStatus?.find((p) => p.available)

  return (
    <header className="bg-white/70 backdrop-blur-md border-b border-pink-400/20 sticky top-0 z-50">
      <div className="max-w-5xl mx-auto px-6 py-4 flex items-center justify-between">
        {/* Logo + wordmark */}
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-pink-700 flex items-center justify-center shadow-btn">
            <Mail size={18} color="white" strokeWidth={2} />
          </div>
          <div>
            <h1 className="text-pink-950 font-bold text-lg leading-tight tracking-tight">
              AI Job Application Writer
            </h1>
            <p className="text-pink-400 text-xs font-medium">
              Personalised emails in seconds
            </p>
          </div>
        </div>

        {/* Active LLM badge */}
        {activeProvider && (
          <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-full
                          bg-pink-700/8 border border-pink-700/20 text-pink-700 text-xs font-medium">
            <Zap size={11} strokeWidth={2.5} />
            <span>{activeProvider.name.split(' ')[0]}</span>
          </div>
        )}
      </div>
    </header>
  )
}

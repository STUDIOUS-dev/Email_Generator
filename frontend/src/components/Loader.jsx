export default function Loader() {
  return (
    <div className="space-y-4 animate-fade-in" aria-label="Loading…" role="status">
      {/* Job card skeleton */}
      <div className="card p-6">
        <div className="flex items-center gap-2.5 mb-5">
          <div className="skeleton w-8 h-8 rounded-lg" />
          <div className="skeleton h-5 w-40 rounded-lg" />
        </div>
        <div className="space-y-3">
          <div className="skeleton h-4 w-1/3 rounded-md" />
          <div className="skeleton h-4 w-full rounded-md" />
          <div className="skeleton h-4 w-5/6 rounded-md" />
          <div className="skeleton h-4 w-2/3 rounded-md" />
          <div className="flex gap-2 mt-4">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="skeleton h-6 w-20 rounded-full" />
            ))}
          </div>
        </div>
      </div>

      {/* Email skeleton */}
      <div className="card p-6">
        <div className="flex items-center justify-between mb-5">
          <div className="flex items-center gap-2.5">
            <div className="skeleton w-8 h-8 rounded-lg" />
            <div className="skeleton h-5 w-36 rounded-lg" />
          </div>
          <div className="flex gap-2">
            <div className="skeleton h-9 w-20 rounded-xl" />
            <div className="skeleton h-9 w-24 rounded-xl" />
          </div>
        </div>
        <div className="space-y-2.5">
          {[85, 95, 70, 90, 60, 80, 75, 88, 65, 78].map((w, i) => (
            <div key={i} className={`skeleton h-4 rounded-md`} style={{ width: `${w}%` }} />
          ))}
        </div>
      </div>

      {/* Floating status */}
      <p className="text-center text-sm text-pink-400 animate-pulse-soft font-medium pt-2">
        Scraping page &amp; generating email with AI…
      </p>
    </div>
  )
}

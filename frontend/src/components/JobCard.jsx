import { Briefcase, Clock, Wrench, FileText } from 'lucide-react'

export default function JobCard({ job }) {
  if (!job) return null

  const fields = [
    { icon: Briefcase, label: 'Role', value: job.role },
    { icon: Clock,     label: 'Experience', value: job.experience },
    { icon: FileText,  label: 'Description', value: job.description },
  ]

  return (
    <div className="card p-6 animate-slide-up">
      <div className="flex items-center gap-2.5 mb-5">
        <div className="w-8 h-8 rounded-lg bg-pink-100 border border-pink-400/30 flex items-center justify-center">
          <Briefcase size={15} className="text-pink-700" />
        </div>
        <h2 className="section-title">Extracted Job Details</h2>
      </div>

      <div className="space-y-4">
        {fields.map(({ icon: Icon, label, value }) =>
          value ? (
            <div key={label}>
              <div className="flex items-center gap-1.5 mb-1.5">
                <Icon size={12} className="text-pink-700" />
                <span className="field-label mb-0">{label}</span>
              </div>
              <p className="text-pink-950 text-sm leading-relaxed">{value}</p>
            </div>
          ) : null
        )}

        {/* Skills chips */}
        {job.skills?.length > 0 && (
          <div>
            <div className="flex items-center gap-1.5 mb-2">
              <Wrench size={12} className="text-pink-700" />
              <span className="field-label mb-0">Skills Required</span>
            </div>
            <div className="flex flex-wrap gap-2">
              {job.skills.map((skill, i) => (
                <span key={i} className="skill-chip">{skill}</span>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

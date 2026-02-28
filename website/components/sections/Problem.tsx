export default function Problem() {
    const challenges = [
        {
            icon: (
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z" />
                    <line x1="12" y1="9" x2="12" y2="13" /><line x1="12" y1="17" x2="12.01" y2="17" />
                </svg>
            ),
            title: "Sequencing Errors",
            desc: "Manual dependency management leads to cascading sequencing failures that delay entire projects."
        },
        {
            icon: (
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
                    <line x1="12" y1="1" x2="12" y2="23" /><path d="M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6" />
                </svg>
            ),
            title: "Cost Overruns",
            desc: "Poor pre-construction planning causes average cost overruns of 28% on large civil projects."
        },
        {
            icon: (
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
                    <circle cx="12" cy="12" r="10" /><polyline points="12 6 12 12 16 14" />
                </svg>
            ),
            title: "Late Conflict Detection",
            desc: "Clashes between structural, MEP, and civil elements are only found once work has already begun."
        },
        {
            icon: (
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
                    <polyline points="22 12 18 12 15 21 9 3 6 12 2 12" />
                </svg>
            ),
            title: "Unsystematic Risk",
            desc: "Risk simulation is rarely systematic — decisions are made on gut feel, not engineering data."
        },
    ]

    return (
        <section className="py-28 px-6 relative">
            <div className="max-w-7xl mx-auto">

                {/* Section label */}
                <div className="flex items-center gap-3 mb-6">
                    <div className="w-8 h-px bg-primary" />
                    <span className="text-primary text-xs font-semibold uppercase tracking-widest">The Challenge</span>
                </div>

                <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-16">
                    <h2 className="text-4xl md:text-5xl font-black leading-tight tracking-tight max-w-xl">
                        WHY PRE-CONSTRUCTION<br />
                        <span className="text-gradient">KEEPS FAILING</span>
                    </h2>
                    <p className="text-muted max-w-sm leading-relaxed">
                        The construction industry loses $1.8 trillion annually to rework,
                        delays, and planning failures. It doesn't have to be this way.
                    </p>
                </div>

                <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-5">
                    {challenges.map((c) => (
                        <div key={c.title} className="border border-border bg-surface rounded-xl p-6 card-hover">
                            <div className="w-11 h-11 flex items-center justify-center rounded-lg bg-primary/10 text-primary mb-5">
                                {c.icon}
                            </div>
                            <h3 className="text-white font-bold text-lg mb-3">{c.title}</h3>
                            <p className="text-muted text-sm leading-relaxed">{c.desc}</p>
                        </div>
                    ))}
                </div>
            </div>
        </section>
    )
}

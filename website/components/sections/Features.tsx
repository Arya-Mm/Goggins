const features = [
    {
        icon: (
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
                <path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z" />
                <line x1="12" y1="9" x2="12" y2="13" /><line x1="12" y1="17" x2="12.01" y2="17" />
            </svg>
        ),
        title: "Conflict Detection",
        desc: "Automatically surface curing conflicts, task overlaps, and workforce overload conditions before they become field problems.",
        tag: "Real-time"
    },
    {
        icon: (
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
                <circle cx="12" cy="12" r="10" />
                <polyline points="12 6 12 12 16 14" />
            </svg>
        ),
        title: "Buildability Score™",
        desc: "A single 0–100 executive metric derived from deterministic structural risk modeling. No black boxes. Fully explainable.",
        tag: "Proprietary"
    },
    {
        icon: (
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
                <polyline points="22 12 18 12 15 21 9 3 6 12 2 12" />
            </svg>
        ),
        title: "What-If Simulation",
        desc: "Adjust workforce allocation, timelines, and constraints. StructuraAI instantly recalculates execution outcomes across the entire graph.",
        tag: "Interactive"
    },
    {
        icon: (
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
                <circle cx="18" cy="18" r="3" /><circle cx="6" cy="6" r="3" /><path d="M13 6h3a2 2 0 012 2v7" /><line x1="6" y1="9" x2="6" y2="21" />
            </svg>
        ),
        title: "Dependency Graphs",
        desc: "Every structural element mapped as a network node. Powered by NetworkX — full topological analysis of your construction sequence.",
        tag: "NetworkX"
    },
    {
        icon: (
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
                <path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z" />
            </svg>
        ),
        title: "Explainable AI",
        desc: "Local LLM via Ollama provides structured, transparent reasoning for every strategic recommendation. No cloud. No guesswork.",
        tag: "Local LLM"
    },
    {
        icon: (
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
                <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
                <line x1="3" y1="9" x2="21" y2="9" /><line x1="9" y1="21" x2="9" y2="9" />
            </svg>
        ),
        title: "Digital Structural Twin",
        desc: "A live computational mirror of your entire structure. Every element, relationship, and constraint — modeled before construction starts.",
        tag: "Core Tech"
    },
]

export default function Features() {
    return (
        <section id="features" className="py-28 px-6 bg-surface relative overflow-hidden">
            <div className="absolute inset-0 bg-grid opacity-40 pointer-events-none" />

            <div className="max-w-7xl mx-auto relative">
                <div className="flex items-center gap-3 mb-6">
                    <div className="w-8 h-px bg-primary" />
                    <span className="text-primary text-xs font-semibold uppercase tracking-widest">Platform Features</span>
                </div>

                <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-16">
                    <h2 className="text-4xl md:text-5xl font-black leading-tight tracking-tight">
                        BUILT FOR<br />
                        <span className="text-gradient">ENGINEERING TEAMS</span>
                    </h2>
                    <p className="text-muted max-w-sm leading-relaxed text-sm">
                        Six core capabilities that replace months of manual planning
                        with hours of automated, verifiable intelligence.
                    </p>
                </div>

                <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-5">
                    {features.map((f) => (
                        <div key={f.title} className="border border-border bg-background rounded-xl p-7 card-hover group">
                            <div className="flex items-start justify-between mb-5">
                                <div className="w-12 h-12 flex items-center justify-center rounded-xl bg-primary/10 text-primary group-hover:bg-primary group-hover:text-black transition-colors duration-300">
                                    {f.icon}
                                </div>
                                <span className="text-[10px] font-bold uppercase tracking-widest text-muted border border-border px-2.5 py-1 rounded-full">
                                    {f.tag}
                                </span>
                            </div>
                            <h3 className="text-white font-bold text-lg mb-3">{f.title}</h3>
                            <p className="text-muted text-sm leading-relaxed">{f.desc}</p>
                        </div>
                    ))}
                </div>
            </div>
        </section>
    )
}

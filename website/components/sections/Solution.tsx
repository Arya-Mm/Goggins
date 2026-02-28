export default function Solution() {
    const points = [
        "Converts static blueprints into a Digital Structural Twin",
        "Models dependencies using deterministic graph intelligence",
        "Generates multiple optimized execution strategies",
        "Simulates risk propagation across the structural graph",
        "Produces a Buildability Score™ for executive decisions",
    ]

    return (
        <section className="py-28 px-6 bg-surface relative overflow-hidden">
            {/* Background accent */}
            <div className="absolute inset-0 bg-grid opacity-50 pointer-events-none" />

            <div className="max-w-7xl mx-auto relative">
                <div className="grid lg:grid-cols-2 gap-16 items-center">

                    {/* Left: Text */}
                    <div>
                        <div className="flex items-center gap-3 mb-6">
                            <div className="w-8 h-px bg-primary" />
                            <span className="text-primary text-xs font-semibold uppercase tracking-widest">The Solution</span>
                        </div>

                        <h2 className="text-4xl md:text-5xl font-black leading-tight tracking-tight mb-8">
                            DETERMINISTIC<br />
                            <span className="text-gradient">CONSTRUCTION</span><br />
                            INTELLIGENCE
                        </h2>

                        <p className="text-muted leading-relaxed mb-10">
                            StructuraAI replaces guesswork with engineering-grade analysis.
                            Every output is traceable, explainable, and optimizable — powered by
                            graph algorithms, not black-box models.
                        </p>

                        <ul className="space-y-4">
                            {points.map((p) => (
                                <li key={p} className="flex items-start gap-3 text-muted-light text-sm">
                                    <span className="mt-0.5 flex-shrink-0 w-5 h-5 rounded-full bg-primary/15 flex items-center justify-center">
                                        <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="#F59E0B" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round">
                                            <polyline points="20 6 9 17 4 12" />
                                        </svg>
                                    </span>
                                    {p}
                                </li>
                            ))}
                        </ul>
                    </div>

                    {/* Right: Visual card */}
                    <div className="relative">
                        <div className="border border-border rounded-2xl bg-background p-8 glow-amber">
                            <div className="flex items-center gap-3 mb-6">
                                <div className="w-3 h-3 rounded-full bg-red-500/70" />
                                <div className="w-3 h-3 rounded-full bg-yellow-500/70" />
                                <div className="w-3 h-3 rounded-full bg-green-500/70" />
                                <span className="ml-2 text-muted text-xs font-mono">structura_analysis.json</span>
                            </div>
                            <div className="space-y-3 font-mono text-sm">
                                <div className="text-muted-light"><span className="text-primary">"blueprint"</span>: <span className="text-green-400">"foundation_v3.pdf"</span>,</div>
                                <div className="text-muted-light"><span className="text-primary">"twin_nodes"</span>: <span className="text-amber-300">1240</span>,</div>
                                <div className="text-muted-light"><span className="text-primary">"dependencies"</span>: <span className="text-amber-300">3871</span>,</div>
                                <div className="text-muted-light"><span className="text-primary">"conflicts_detected"</span>: <span className="text-red-400">3</span>,</div>
                                <div className="text-muted-light"><span className="text-primary">"strategies"</span>: [<span className="text-green-400">"critical_path"</span>, <span className="text-green-400">"parallel"</span>],</div>
                                <div className="text-muted-light"><span className="text-primary">"buildability_score"</span>: <span className="text-amber-300">87.4</span>,</div>
                                <div className="text-muted-light"><span className="text-primary">"risk_level"</span>: <span className="text-green-400">"LOW"</span></div>
                            </div>
                            <div className="mt-6 pt-6 border-t border-border flex items-center justify-between">
                                <span className="text-muted text-xs">Analysis complete</span>
                                <span className="text-primary font-semibold text-sm">Buildability Score™ 87.4</span>
                            </div>
                        </div>

                        {/* Floating badge */}
                        <div className="absolute -top-4 -right-4 bg-primary text-black text-xs font-bold px-3 py-1.5 rounded-full">
                            100% Algorithmic
                        </div>
                    </div>
                </div>
            </div>
        </section>
    )
}

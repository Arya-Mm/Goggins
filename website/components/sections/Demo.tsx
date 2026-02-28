export default function Demo() {
    const steps = [
        { n: "01", t: "Upload Blueprint", d: "Drag in any PDF, DWG, or IFC file." },
        { n: "02", t: "Generate Digital Twin", d: "Structural elements and relationships are automatically extracted." },
        { n: "03", t: "Run Intelligence Analysis", d: "Dependency graph, conflicts, risk scores — all computed in minutes." },
        { n: "04", t: "Receive Buildability Report", d: "Full strategy comparison, score, and AI explanation delivered instantly." },
    ]

    return (
        <section id="demo" className="py-28 px-6">
            <div className="max-w-7xl mx-auto">

                <div className="flex items-center gap-3 mb-6">
                    <div className="w-8 h-px bg-primary" />
                    <span className="text-primary text-xs font-semibold uppercase tracking-widest">Demo Walkthrough</span>
                </div>

                <div className="grid lg:grid-cols-2 gap-16 items-center">
                    <div>
                        <h2 className="text-4xl md:text-5xl font-black leading-tight tracking-tight mb-8">
                            SEE IT<br />
                            <span className="text-gradient">IN ACTION</span>
                        </h2>
                        <p className="text-muted leading-relaxed mb-10">
                            From raw blueprint to full construction intelligence report in four steps.
                            No setup. No training data. No cloud dependency.
                        </p>

                        <div className="space-y-6">
                            {steps.map((s, i) => (
                                <div key={s.n} className="flex gap-5 items-start group">
                                    <div className={`flex-shrink-0 w-10 h-10 rounded-lg flex items-center justify-center text-xs font-bold
                    ${i === 0 ? "bg-primary text-black" : "border border-border text-muted group-hover:border-primary/50 group-hover:text-primary transition-colors"}`}>
                                        {s.n}
                                    </div>
                                    <div>
                                        <h4 className="text-white font-semibold mb-1">{s.t}</h4>
                                        <p className="text-muted text-sm">{s.d}</p>
                                    </div>
                                </div>
                            ))}
                        </div>

                        <button className="btn-primary mt-10 inline-flex items-center gap-2">
                            Request a Live Demo
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5"><path d="M5 12h14M12 5l7 7-7 7" /></svg>
                        </button>
                    </div>

                    {/* Metrics panel */}
                    <div className="grid grid-cols-2 gap-4">
                        {[
                            { label: "Blueprint Accuracy", value: "95%", sub: "vs. manual parsing" },
                            { label: "Conflicts Found", value: "12×", sub: "more than visual review" },
                            { label: "Planning Time", value: "−70%", sub: "average reduction" },
                            { label: "Buildability Score", value: "87.4", sub: "example project" },
                        ].map((m) => (
                            <div key={m.label} className="border border-border bg-surface rounded-xl p-6 card-hover">
                                <div className="text-3xl font-black text-gradient mb-1">{m.value}</div>
                                <div className="text-white font-semibold text-sm mb-1">{m.label}</div>
                                <div className="text-muted text-xs">{m.sub}</div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </section>
    )
}

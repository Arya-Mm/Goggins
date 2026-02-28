export default function Demo() {
    const steps = [
        { n: "01", t: "Upload Blueprint", d: "Drag in any PDF, DWG, or IFC file." },
        { n: "02", t: "Generate Digital Twin", d: "Structural elements and relationships are automatically extracted." },
        { n: "03", t: "Run Intelligence Analysis", d: "Dependency graph, conflicts, risk scores — all computed in minutes." },
        { n: "04", t: "Receive Buildability Report", d: "Full strategy comparison, score, and AI explanation delivered instantly." },
    ]

    const bars = [
        { label: "Structural Integrity Analysis", pct: 92, color: "#F59E0B" },
        { label: "Dependency Resolution", pct: 96, color: "#F59E0B" },
        { label: "Conflict Detection Coverage", pct: 88, color: "#60A5FA" },
        { label: "Risk Propagation Accuracy", pct: 94, color: "#F59E0B" },
        { label: "Buildability Score Reliability", pct: 91, color: "#34D399" },
    ]

    return (
        <section id="demo" className="py-28 px-6 relative overflow-hidden">

            {/* Rebar diagonal stripe on the left edge */}
            <div className="absolute left-0 top-0 bottom-0 w-2 rebar-pattern opacity-60" />

            <div className="max-w-7xl mx-auto">
                <div className="flex items-center gap-3 mb-6">
                    <div className="w-8 h-px bg-primary" />
                    <span className="text-primary text-xs font-semibold uppercase tracking-widest">Demo Walkthrough</span>
                </div>

                <div className="grid lg:grid-cols-2 gap-16 items-start">

                    {/* LEFT: Steps */}
                    <div>
                        <h2 className="text-4xl md:text-5xl font-black leading-tight tracking-tight mb-8">
                            SEE IT<br />
                            <span className="text-gradient">IN ACTION</span>
                        </h2>
                        <p className="text-muted leading-relaxed mb-10">
                            From raw blueprint to full construction intelligence report in four steps. No setup. No training data. No cloud dependency.
                        </p>

                        <div className="space-y-5">
                            {steps.map((s, i) => (
                                <div key={s.n} className="flex gap-5 items-start group">
                                    <div className={`flex-shrink-0 w-10 h-10 rounded-lg flex items-center justify-center text-xs font-bold font-mono
                    ${i === 0 ? "bg-primary text-black" : "border border-border text-muted group-hover:border-primary/50 group-hover:text-primary transition-colors"}`}>
                                        {s.n}
                                    </div>
                                    <div className="pt-1.5">
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

                    {/* RIGHT: Construction bar charts + metrics */}
                    <div>
                        {/* Metrics grid */}
                        <div className="grid grid-cols-2 gap-3 mb-8">
                            {[
                                { label: "Blueprint Accuracy", value: "95%", sub: "vs. manual parsing" },
                                { label: "Conflicts Found", value: "12×", sub: "more than visual review" },
                                { label: "Planning Time", value: "−70%", sub: "average reduction" },
                                { label: "Buildability Score", value: "87.4", sub: "example project" },
                            ].map((m) => (
                                <div key={m.label} className="border border-border bg-surface rounded-xl p-5 card-hover">
                                    <div className="text-2xl font-black text-gradient mb-0.5">{m.value}</div>
                                    <div className="text-white font-semibold text-sm mb-0.5">{m.label}</div>
                                    <div className="text-muted text-xs">{m.sub}</div>
                                </div>
                            ))}
                        </div>

                        {/* Construction bar chart — like steel rebar load bars */}
                        <div className="border border-border bg-surface rounded-xl p-6">
                            <div className="flex items-center gap-2 mb-6">
                                {/* I-beam icon decoration */}
                                <div className="flex flex-col items-center gap-0.5">
                                    <div className="w-5 h-0.5 bg-primary/60 rounded" />
                                    <div className="w-1 h-3 bg-primary/40 rounded" />
                                    <div className="w-5 h-0.5 bg-primary/60 rounded" />
                                </div>
                                <span className="text-white font-bold text-sm">Platform Performance Metrics</span>
                            </div>

                            <div className="space-y-4">
                                {bars.map((b, i) => (
                                    <div key={b.label}>
                                        <div className="flex justify-between items-center mb-1.5">
                                            <span className="text-muted text-xs font-mono">{b.label}</span>
                                            <span className="text-white text-xs font-bold">{b.pct}%</span>
                                        </div>
                                        {/* Bar track */}
                                        <div className="h-2.5 bg-border rounded-full overflow-hidden relative">
                                            {/* Rebar stripe inside bar */}
                                            <div
                                                className="h-full rounded-full relative overflow-hidden"
                                                style={{
                                                    width: `${b.pct}%`,
                                                    background: `linear-gradient(90deg, ${b.color}CC, ${b.color})`,
                                                    transition: `width 1.2s cubic-bezier(0.4,0,0.2,1) ${i * 0.15}s`
                                                }}
                                            >
                                                {/* Rebar knurling pattern inside bar */}
                                                <div className="absolute inset-0"
                                                    style={{
                                                        backgroundImage: `repeating-linear-gradient(90deg, transparent, transparent 12px, rgba(0,0,0,0.15) 12px, rgba(0,0,0,0.15) 14px)`
                                                    }} />
                                            </div>
                                            {/* Segment markers (like rebar notches) */}
                                            {[25, 50, 75].map((mark) => (
                                                <div key={mark} className="absolute top-0 bottom-0 w-px bg-background/40"
                                                    style={{ left: `${mark}%` }} />
                                            ))}
                                        </div>
                                    </div>
                                ))}
                            </div>

                            {/* Bar legend */}
                            <div className="flex items-center gap-4 mt-5 pt-4 border-t border-border">
                                <div className="flex items-center gap-1.5">
                                    <div className="w-3 h-0.5 bg-primary/70" />
                                    <span className="text-muted text-[10px] font-mono">CORE ENGINE</span>
                                </div>
                                <div className="flex items-center gap-1.5">
                                    <div className="w-3 h-0.5 bg-blue-400/70" />
                                    <span className="text-muted text-[10px] font-mono">DETECTION</span>
                                </div>
                                <div className="flex items-center gap-1.5">
                                    <div className="w-3 h-0.5 bg-emerald-400/70" />
                                    <span className="text-muted text-[10px] font-mono">SCORING</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Rebar stripe right edge */}
            <div className="absolute right-0 top-0 bottom-0 w-2 rebar-pattern opacity-60" />
        </section>
    )
}

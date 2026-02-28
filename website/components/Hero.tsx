export default function Hero() {
    return (
        <section className="relative pt-14 pb-14 px-6 bg-black grid-bg overflow-hidden">
            <div
                className="absolute top-0 left-1/2 -translate-x-1/2 w-[700px] h-[400px] opacity-20 pointer-events-none"
                style={{ background: "radial-gradient(ellipse at center, rgba(34,211,238,0.3) 0%, transparent 70%)" }}
            />

            <div className="max-w-6xl mx-auto relative z-10">
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
                    {/* Left */}
                    <div>
                        <div className="inline-flex items-center gap-2 border border-cyan-400/20 bg-cyan-400/5 text-cyan-400 text-[10px] font-semibold px-2.5 py-1 rounded-full mb-4 tracking-widest uppercase">
                            <span className="w-1.5 h-1.5 rounded-full bg-cyan-400" style={{ boxShadow: "0 0 6px #22d3ee" }} />
                            Pre-Construction AI
                        </div>

                        <h1 className="text-4xl lg:text-5xl font-extrabold text-white leading-tight tracking-tight mb-3">
                            Blueprints to{" "}
                            <span style={{ background: "linear-gradient(90deg, #22d3ee, #818cf8)", WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent", backgroundClip: "text" }}>
                                Execution Intelligence
                            </span>
                        </h1>

                        <p className="text-sm text-white/40 leading-relaxed mb-6 max-w-sm">
                            Autonomous pre-construction planning from 2D structural drawings.
                        </p>

                        <div className="flex flex-row gap-3">
                            <a href="#cta" id="hero-request-demo" className="btn-primary inline-flex items-center gap-2 text-sm px-5 py-2.5 rounded-lg">
                                Request Demo
                                <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
                                </svg>
                            </a>
                            <a href="#architecture" id="hero-view-architecture" className="inline-flex items-center gap-2 border border-white/10 hover:border-white/20 text-white/50 hover:text-white text-sm px-5 py-2.5 rounded-lg transition-all">
                                View Architecture
                            </a>
                        </div>
                    </div>

                    {/* Right: Pipeline Card */}
                    <div className="flex justify-center lg:justify-end">
                        <div className="w-full max-w-sm rounded-2xl p-5"
                            style={{ background: "rgba(255,255,255,0.02)", border: "1px solid rgba(255,255,255,0.06)", boxShadow: "0 0 40px rgba(34,211,238,0.06)" }}>
                            <p className="text-[10px] text-white/25 uppercase tracking-widest font-semibold mb-4 text-center">Execution Pipeline</p>
                            <div className="space-y-2">
                                {[
                                    { label: "Blueprint Upload", color: "#22d3ee", bg: "rgba(34,211,238,0.07)", border: "rgba(34,211,238,0.14)" },
                                    { label: "Dependency Graph", color: "#818cf8", bg: "rgba(129,140,248,0.07)", border: "rgba(129,140,248,0.14)" },
                                    { label: "Schedule + Risk", color: "#34d399", bg: "rgba(52,211,153,0.07)", border: "rgba(52,211,153,0.14)" },
                                ].map((step, i) => (
                                    <div key={i}>
                                        <div className="flex items-center gap-2.5 rounded-xl px-3.5 py-2.5" style={{ background: step.bg, border: `1px solid ${step.border}` }}>
                                            <div className="w-1.5 h-1.5 rounded-full flex-shrink-0" style={{ background: step.color, boxShadow: `0 0 6px ${step.color}` }} />
                                            <p className="text-sm font-medium text-white/90">{step.label}</p>
                                        </div>
                                        {i < 2 && (
                                            <div className="flex justify-center py-0.5">
                                                <svg className="w-3 h-3 text-white/15" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                                                </svg>
                                            </div>
                                        )}
                                    </div>
                                ))}
                                <div className="flex justify-center py-0.5">
                                    <svg className="w-3 h-3 text-white/15" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                                    </svg>
                                </div>
                                <div className="flex items-center gap-3 rounded-xl px-3.5 py-3"
                                    style={{ background: "linear-gradient(135deg, rgba(34,211,238,0.09), rgba(99,102,241,0.06))", border: "1px solid rgba(34,211,238,0.22)", boxShadow: "0 0 16px rgba(34,211,238,0.07)" }}>
                                    <p className="text-sm font-semibold text-cyan-400">Buildability Score™</p>
                                    <div className="ml-auto flex items-baseline gap-0.5">
                                        <span className="text-xl font-extrabold text-cyan-400" style={{ textShadow: "0 0 16px rgba(34,211,238,0.5)" }}>87</span>
                                        <span className="text-white/30 text-xs">/100</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    );
}

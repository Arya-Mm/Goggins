const steps = [
    { num: "01", title: "Blueprint Ingestion", desc: "Upload any civil, structural, or MEP blueprint. Automatic parsing and element extraction." },
    { num: "02", title: "Digital Structural Twin", desc: "Every structural element becomes a node. Relationships become edges in a live dependency graph." },
    { num: "03", title: "Dependency Intelligence", desc: "NetworkX-powered graph analysis maps every dependency — spatial, temporal, and logical." },
    { num: "04", title: "Execution Strategies", desc: "Critical Path, Parallel, and Hybrid execution plans are generated and ranked automatically." },
    { num: "05", title: "Conflict Detection", desc: "Curing clashes, task overlaps, and workforce overloads are flagged before work begins." },
    { num: "06", title: "Risk Simulation", desc: "Delay propagation modeled across the entire graph. Quantified risk at every node." },
    { num: "07", title: "Buildability Score™", desc: "A single executive metric — 0 to 100 — expressing the structural viability of the plan." },
    { num: "08", title: "What-If Optimization", desc: "Adjust workforce, timelines, and constraints. Instantly recalculate outcomes." },
    { num: "09", title: "AI Explanation", desc: "Local LLM provides plain-English reasoning for every decision. Fully transparent." },
]

export default function Pipeline() {
    return (
        <section id="pipeline" className="py-28 px-6">
            <div className="max-w-7xl mx-auto">
                <div className="flex items-center gap-3 mb-6">
                    <div className="w-8 h-px bg-primary" />
                    <span className="text-primary text-xs font-semibold uppercase tracking-widest">Intelligence Pipeline</span>
                </div>

                <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-16">
                    <h2 className="text-4xl md:text-5xl font-black leading-tight tracking-tight">
                        FROM BLUEPRINT<br />
                        <span className="text-gradient">TO BUILDABILITY</span>
                    </h2>
                    <p className="text-muted max-w-sm leading-relaxed text-sm">
                        Nine stages of deterministic analysis — transforming raw drawings
                        into a complete, executable construction intelligence report.
                    </p>
                </div>

                {/* Steps grid */}
                <div className="grid md:grid-cols-3 gap-4">
                    {steps.map((step, i) => (
                        <div
                            key={step.num}
                            className={`border border-border bg-surface rounded-xl p-6 card-hover relative overflow-hidden
                ${i === 6 ? "md:col-span-1 border-primary/30 bg-primary/5" : ""}`}
                        >
                            {/* Step number watermark */}
                            <div className="absolute top-4 right-5 text-5xl font-black text-white/[0.03] select-none">{step.num}</div>

                            <div className="text-primary text-xs font-bold uppercase tracking-widest mb-3">{step.num}</div>
                            <h3 className="text-white font-bold text-base mb-2">{step.title}</h3>
                            <p className="text-muted text-sm leading-relaxed">{step.desc}</p>

                            {i === 6 && (
                                <div className="mt-4 inline-flex items-center gap-1.5 text-primary text-xs font-semibold">
                                    <span className="w-1.5 h-1.5 bg-primary rounded-full" />
                                    Core Metric
                                </div>
                            )}
                        </div>
                    ))}
                </div>
            </div>
        </section>
    )
}

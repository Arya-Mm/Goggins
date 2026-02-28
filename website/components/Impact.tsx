const metrics = [
    { value: "85%", label: "Less rework", color: "#22d3ee" },
    { value: "3×", label: "Faster scheduling", color: "#818cf8" },
    { value: "100%", label: "Offline capable", color: "#34d399" },
];

const bullets = [
    "Detect conflicts before execution begins",
    "Optimize crew and material timelines",
    "Deploy on air-gapped infrastructure",
    "Full audit trail on every decision",
];

export default function Impact() {
    return (
        <section id="impact" className="py-10 px-6 relative overflow-hidden" style={{ background: "#050505" }}>
            <div className="accent-line w-full absolute top-0 left-0 opacity-30" />
            <div className="max-w-6xl mx-auto">
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-start">
                    {/* Left */}
                    <div>
                        <p className="text-[10px] font-semibold text-cyan-400 uppercase tracking-widest mb-2">Impact</p>
                        <h2 className="text-2xl font-bold text-white tracking-tight mb-5">Built for Infrastructure Teams</h2>
                        <div className="space-y-3">
                            {bullets.map((b, i) => (
                                <div key={i} className="flex items-center gap-3">
                                    <div className="w-0.5 h-3.5 rounded-full flex-shrink-0" style={{ background: "linear-gradient(180deg, #22d3ee, #818cf8)" }} />
                                    <p className="text-xs text-white/55">{b}</p>
                                </div>
                            ))}
                        </div>
                    </div>

                    {/* Right: Metrics */}
                    <div className="space-y-3">
                        {metrics.map((m, i) => (
                            <div key={i} className="card-glass card-glass-hover rounded-xl px-5 py-4 flex items-center gap-5">
                                <p className="text-3xl font-extrabold tracking-tight w-20 flex-shrink-0" style={{ color: m.color, textShadow: `0 0 20px ${m.color}70` }}>
                                    {m.value}
                                </p>
                                <div className="h-6 w-px" style={{ background: "rgba(255,255,255,0.06)" }} />
                                <p className="text-xs text-white/45 font-medium">{m.label}</p>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </section>
    );
}

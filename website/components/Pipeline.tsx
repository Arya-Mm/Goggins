const steps = [
    "Blueprint Upload", "Structural Twin", "Dependency Graph", "Schedule Engine",
    "Conflict Analysis", "Buildability Score™", "What-If Modeling", "AI Explanation",
];

export default function Pipeline() {
    return (
        <section id="pipeline" className="py-10 px-6 relative overflow-hidden" style={{ background: "#050505" }}>
            <div className="accent-line w-full absolute top-0 left-0 opacity-30" />
            <div className="max-w-6xl mx-auto">
                <div className="mb-6">
                    <p className="text-[10px] font-semibold text-cyan-400 uppercase tracking-widest mb-2">How It Works</p>
                    <h2 className="text-2xl font-bold text-white tracking-tight">Autonomous Planning Pipeline</h2>
                </div>

                <div className="relative">
                    <div className="hidden lg:block absolute top-3.5 left-0 right-0 h-px"
                        style={{ background: "linear-gradient(90deg, transparent, rgba(34,211,238,0.2), rgba(99,102,241,0.2), transparent)" }} />
                    <div className="grid grid-cols-4 lg:grid-cols-8 gap-3">
                        {steps.map((step, i) => (
                            <div key={i} className="relative flex flex-col items-center text-center z-10 group">
                                <div className="w-7 h-7 rounded-full flex items-center justify-center mb-2 transition-all duration-200 group-hover:shadow-[0_0_12px_rgba(34,211,238,0.3)]"
                                    style={{ background: "rgba(34,211,238,0.07)", border: "1px solid rgba(34,211,238,0.22)" }}>
                                    <span className="text-[10px] font-bold text-cyan-400">{i + 1}</span>
                                </div>
                                <p className="text-[10px] font-medium text-white/55 leading-snug">{step}</p>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </section>
    );
}

const problems = [
    {
        accent: "#22d3ee", bg: "rgba(34,211,238,0.05)", border: "rgba(34,211,238,0.12)",
        title: "Hidden Dependency Conflicts",
        description: "Structural clashes stay invisible until costly rework begins on site.",
    },
    {
        accent: "#818cf8", bg: "rgba(129,140,248,0.05)", border: "rgba(129,140,248,0.12)",
        title: "Workforce Overload",
        description: "Manual crew scheduling causes resource contention and timeline slippage.",
    },
    {
        accent: "#34d399", bg: "rgba(52,211,153,0.05)", border: "rgba(52,211,153,0.12)",
        title: "Delays Discovered Too Late",
        description: "Sequencing failures surface during execution, when costs are highest.",
    },
];

export default function Problem() {
    return (
        <section id="problem" className="py-12 px-6 bg-black relative overflow-hidden">
            <div className="accent-line w-full absolute top-0 left-0 opacity-30" />
            <div className="max-w-6xl mx-auto">
                <div className="mb-7">
                    <p className="text-[10px] font-semibold text-cyan-400 uppercase tracking-widest mb-2">The Problem</p>
                    <h2 className="text-2xl font-bold text-white tracking-tight">Construction Planning is Broken</h2>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    {problems.map((p, i) => (
                        <div key={i} className="card-glass rounded-xl p-5"
                            style={{ borderColor: p.border, background: p.bg }}>
                            <div className="w-2 h-2 rounded-full mb-4" style={{ background: p.accent, boxShadow: `0 0 8px ${p.accent}` }} />
                            <h3 className="text-sm font-semibold text-white mb-1.5">{p.title}</h3>
                            <p className="text-xs text-white/40 leading-relaxed">{p.description}</p>
                        </div>
                    ))}
                </div>
            </div>
        </section>
    );
}

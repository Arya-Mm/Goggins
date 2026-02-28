const features = [
    { title: "Digital Structural Twin", description: "Converts 2D drawings into a queryable structural model.", icon: <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" /> },
    { title: "Dependency Intelligence", description: "Maps structural and temporal construction relationships.", icon: <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" /> },
    { title: "Multi-Strategy Scheduling", description: "Generates Fast, Balanced, and Cost-optimized schedules.", icon: <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" /> },
    { title: "Conflict Detection", description: "Flags curing overlaps and sequencing violations pre-execution.", icon: <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /> },
    { title: "Risk Propagation", description: "Models how one delay cascades across the dependency graph.", icon: <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M13 10V3L4 14h7v7l9-11h-7z" /> },
    { title: "Buildability Score™", description: "Execution readiness index from 0 to 100.", icon: <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" /> },
    { title: "What-If Modeling", description: "Evaluates timeline and resource change scenarios instantly.", icon: <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" /> },
    { title: "Offline AI Explanation", description: "Engineering-grade reasoning with no cloud dependency.", icon: <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" /> },
];

export default function Features() {
    return (
        <section id="features" className="py-10 px-6 bg-black relative overflow-hidden">
            <div className="accent-line w-full absolute top-0 left-0 opacity-30" />

            <div className="max-w-6xl mx-auto relative z-10">
                <div className="mb-6">
                    <p className="text-[10px] font-semibold text-cyan-400 uppercase tracking-widest mb-2">Capabilities</p>
                    <h2 className="text-2xl font-bold text-white tracking-tight">Core Features</h2>
                </div>

                <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
                    {features.map((f, i) => (
                        <div key={i} className="card-glass card-glass-hover rounded-xl p-4">
                            <div className="w-6 h-6 rounded-md flex items-center justify-center mb-3"
                                style={{ background: "rgba(34,211,238,0.07)", border: "1px solid rgba(34,211,238,0.14)" }}>
                                <svg className="w-3.5 h-3.5" fill="none" stroke="#22d3ee" viewBox="0 0 24 24">{f.icon}</svg>
                            </div>
                            <h3 className="text-xs font-semibold text-white mb-1">{f.title}</h3>
                            <p className="text-[11px] text-white/35 leading-relaxed">{f.description}</p>
                        </div>
                    ))}
                </div>
            </div>
        </section>
    );
}

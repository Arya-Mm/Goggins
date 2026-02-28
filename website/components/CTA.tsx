export default function CTA() {
    return (
        <section id="cta" className="py-10 px-6 bg-black relative overflow-hidden">
            <div className="accent-line w-full absolute top-0 left-0 opacity-30" />
            <div className="max-w-6xl mx-auto">
                <div className="relative rounded-2xl overflow-hidden px-8 py-12 text-center"
                    style={{ background: "rgba(255,255,255,0.02)", border: "1px solid rgba(34,211,238,0.12)" }}>
                    <div className="absolute inset-0 grid-bg opacity-40" />
                    <div className="absolute top-0 left-1/4 w-64 h-36 pointer-events-none"
                        style={{ background: "radial-gradient(ellipse, rgba(34,211,238,0.09), transparent 70%)" }} />

                    <div className="relative z-10">
                        <p className="text-[10px] font-semibold text-cyan-400 uppercase tracking-widest mb-3">Ready to Deploy</p>
                        <h2 className="text-2xl md:text-3xl font-extrabold text-white tracking-tight mb-3 max-w-lg mx-auto">
                            From Drawings to{" "}
                            <span style={{ background: "linear-gradient(90deg, #22d3ee, #818cf8)", WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent", backgroundClip: "text" }}>
                                Execution Intelligence
                            </span>
                        </h2>
                        <p className="text-white/30 text-xs mb-6">See how StructuraAI handles your project type.</p>
                        <a href="mailto:demo@structuraai.com" id="cta-schedule-demo"
                            className="btn-primary inline-flex items-center gap-2 text-sm px-6 py-2.5 rounded-lg">
                            Schedule a Demo
                            <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
                            </svg>
                        </a>
                    </div>
                </div>
            </div>
        </section>
    );
}

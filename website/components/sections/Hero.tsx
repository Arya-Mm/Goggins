export default function Hero() {
    return (
        <section className="relative min-h-screen flex flex-col justify-center pt-24 pb-16 px-6 overflow-hidden bg-grid">

            {/* Amber glow orb */}
            <div className="absolute top-1/3 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] rounded-full pointer-events-none"
                style={{ background: "radial-gradient(circle, rgba(245,158,11,0.08) 0%, transparent 70%)" }} />

            <div className="max-w-7xl mx-auto w-full">

                {/* Badge */}
                <div className="inline-flex items-center gap-2 border border-primary/30 bg-primary/5 text-primary text-xs font-semibold px-4 py-2 rounded-full mb-8 uppercase tracking-widest">
                    <span className="w-1.5 h-1.5 bg-primary rounded-full animate-pulse" />
                    Pre-Construction AI Platform
                </div>

                {/* Main headline */}
                <h1 className="text-5xl md:text-7xl lg:text-8xl font-black leading-none tracking-tight mb-6 max-w-5xl">
                    AUTONOMOUS<br />
                    <span className="text-gradient">PRE-CONSTRUCTION</span><br />
                    INTELLIGENCE
                </h1>

                {/* Subtext */}
                <p className="text-muted-light text-lg md:text-xl max-w-2xl mb-10 leading-relaxed">
                    Transform civil engineering blueprints into executable, optimized, and
                    explainable construction strategies — before a single brick is laid.
                </p>

                {/* CTA buttons */}
                <div className="flex flex-wrap gap-4 mb-20">
                    <button className="btn-primary text-base">
                        Request Demo
                    </button>
                    <button className="btn-outline text-base flex items-center gap-2">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="12" cy="12" r="10" /><polygon points="10 8 16 12 10 16 10 8" /></svg>
                        Watch Overview
                    </button>
                </div>

                {/* Stats bar */}
                <div className="divider mb-10" />
                <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
                    {[
                        { value: "95%", label: "Blueprint Accuracy" },
                        { value: "2×", label: "Faster Planning" },
                        { value: "60%", label: "Conflict Reduction" },
                        { value: "100%", label: "Algorithmic Core" },
                    ].map((stat) => (
                        <div key={stat.label}>
                            <div className="stat-number text-gradient">{stat.value}</div>
                            <div className="text-muted text-sm mt-1">{stat.label}</div>
                        </div>
                    ))}
                </div>
            </div>

            {/* Bottom fade */}
            <div className="absolute bottom-0 left-0 right-0 h-32 pointer-events-none"
                style={{ background: "linear-gradient(to bottom, transparent, #07090C)" }} />
        </section>
    )
}

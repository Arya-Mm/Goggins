export default function Hero() {
    return (
        <section className="relative min-h-screen flex flex-col justify-center pt-24 pb-0 overflow-hidden bg-grid">

            {/* Amber glow */}
            <div className="absolute top-1/3 left-1/4 w-[500px] h-[500px] rounded-full pointer-events-none"
                style={{ background: "radial-gradient(circle, rgba(245,158,11,0.07) 0%, transparent 70%)" }} />

            <div className="max-w-7xl mx-auto w-full px-6">
                <div className="grid lg:grid-cols-2 gap-8 items-center">

                    {/* LEFT: Content */}
                    <div className="relative z-10 py-12">
                        {/* Badge */}
                        <div className="inline-flex items-center gap-2 border border-primary/30 bg-primary/5 text-primary text-xs font-semibold px-4 py-2 rounded-full mb-8 uppercase tracking-widest">
                            <span className="w-1.5 h-1.5 bg-primary rounded-full animate-pulse" />
                            Pre-Construction AI Platform
                        </div>

                        {/* Headline */}
                        <h1 className="text-5xl md:text-6xl lg:text-7xl font-black leading-none tracking-tight mb-6">
                            AUTONOMOUS<br />
                            <span className="text-gradient">PRE-CONSTRUCTION</span><br />
                            INTELLIGENCE
                        </h1>

                        <p className="text-muted-light text-lg max-w-lg mb-10 leading-relaxed">
                            Transform civil engineering blueprints into executable, optimized,
                            and explainable construction strategies — before a single brick is laid.
                        </p>

                        {/* CTAs */}
                        <div className="flex flex-wrap gap-4 mb-12">
                            <button className="btn-primary text-base">Request Demo</button>
                            <button className="btn-outline text-base flex items-center gap-2">
                                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="12" cy="12" r="10" /><polygon points="10 8 16 12 10 16 10 8" /></svg>
                                Watch Overview
                            </button>
                        </div>

                        {/* Stats bar */}
                        <div className="grid grid-cols-2 gap-x-8 gap-y-5">
                            {[
                                { value: "95%", label: "Blueprint Accuracy" },
                                { value: "2×", label: "Faster Planning" },
                                { value: "60%", label: "Conflict Reduction" },
                                { value: "100%", label: "Algorithmic Core" },
                            ].map((stat) => (
                                <div key={stat.label} className="flex items-center gap-3">
                                    <div className="w-px h-8 bg-primary/40" />
                                    <div>
                                        <div className="text-2xl font-black text-gradient leading-none">{stat.value}</div>
                                        <div className="text-muted text-xs mt-0.5">{stat.label}</div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>

                    {/* RIGHT: Steel Structure Image */}
                    <div className="relative hidden lg:block">
                        {/* Glow behind image */}
                        <div className="absolute inset-0 rounded-2xl pointer-events-none"
                            style={{ background: "radial-gradient(ellipse at center, rgba(245,158,11,0.12) 0%, transparent 70%)" }} />

                        {/* Construction bars decorative element */}
                        <div className="absolute -left-4 top-1/2 -translate-y-1/2 flex flex-col gap-2 z-10">
                            {[80, 60, 90, 45, 70].map((h, i) => (
                                <div key={i} className="flex items-center gap-1.5">
                                    <div className="w-1 rounded-full bg-primary/40" style={{ height: `${h * 0.4}px` }} />
                                    <div className="w-0.5 rounded-full bg-primary/20" style={{ height: `${h * 0.3}px` }} />
                                </div>
                            ))}
                        </div>

                        <div className="relative rounded-2xl overflow-hidden border border-primary/20">
                            {/* Blueprint grid overlay */}
                            <div className="absolute inset-0 bg-grid opacity-60 z-10 pointer-events-none" />

                            {/* Steel structure image */}
                            {/* eslint-disable-next-line @next/next/no-img-element */}
                            <img
                                src="/steel-structure.png"
                                alt="Steel frame building structural elevation"
                                className="w-full object-cover"
                                style={{ maxHeight: "560px" }}
                            />

                            {/* Top overlay tag */}
                            <div className="absolute top-4 left-4 z-20 bg-background/80 backdrop-blur-sm border border-primary/30 px-3 py-1.5 rounded text-xs font-mono text-primary">
                                STRUCTURAL ELEVATION — GRID A-D / L1-L4
                            </div>

                            {/* Floating data badge */}
                            <div className="absolute bottom-4 right-4 z-20 bg-background/90 backdrop-blur-sm border border-primary/30 rounded-lg px-4 py-3">
                                <div className="text-xs text-muted mb-1 font-mono">BUILDABILITY SCORE™</div>
                                <div className="text-2xl font-black text-gradient">87.4</div>
                            </div>
                        </div>

                        {/* Rebar bars (right side decor) */}
                        <div className="absolute -right-4 top-1/4 flex flex-col gap-1.5 z-10">
                            {[1, 1, 1, 1, 1, 1, 1, 1].map((_, i) => (
                                <div key={i} className="flex gap-1">
                                    <div className="w-6 h-1 rounded-full bg-primary/30" />
                                    <div className="w-3 h-1 rounded-full bg-primary/15" />
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </div>

            {/* Bottom fade */}
            <div className="h-20 w-full mt-0 pointer-events-none"
                style={{ background: "linear-gradient(to bottom, transparent, #07090C)" }} />
        </section>
    )
}

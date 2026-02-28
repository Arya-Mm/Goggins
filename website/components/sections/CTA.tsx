export default function CTA() {
    return (
        <section className="py-28 px-6 bg-surface relative overflow-hidden">
            {/* Background glow */}
            <div className="absolute inset-0 pointer-events-none"
                style={{ background: "radial-gradient(ellipse at 50% 100%, rgba(245,158,11,0.1) 0%, transparent 70%)" }} />
            <div className="absolute inset-0 bg-grid opacity-30 pointer-events-none" />

            <div className="max-w-4xl mx-auto text-center relative">

                <div className="inline-flex items-center gap-2 border border-primary/30 bg-primary/5 text-primary text-xs font-semibold px-4 py-2 rounded-full mb-8 uppercase tracking-widest">
                    <span className="w-1.5 h-1.5 bg-primary rounded-full animate-pulse" />
                    Ready to start
                </div>

                <h2 className="text-5xl md:text-6xl lg:text-7xl font-black leading-none tracking-tight mb-6">
                    TRANSFORM<br />
                    <span className="text-gradient">PRE-CONSTRUCTION</span><br />
                    PLANNING
                </h2>

                <p className="text-muted text-lg max-w-xl mx-auto mb-12 leading-relaxed">
                    Join engineering teams who are replacing manual guesswork with
                    deterministic, explainable construction intelligence.
                </p>



                {/* Trust bar */}
                <div className="mt-16 pt-8 border-t border-border flex flex-wrap justify-center gap-8 text-muted text-sm">
                    <span className="flex items-center gap-2">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#F59E0B" strokeWidth="2"><polyline points="20 6 9 17 4 12" /></svg>
                        No cloud dependency
                    </span>
                    <span className="flex items-center gap-2">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#F59E0B" strokeWidth="2"><polyline points="20 6 9 17 4 12" /></svg>
                        100% deterministic outputs
                    </span>
                    <span className="flex items-center gap-2">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#F59E0B" strokeWidth="2"><polyline points="20 6 9 17 4 12" /></svg>
                        Explainable at every step
                    </span>
                </div>
            </div>
        </section>
    )
}

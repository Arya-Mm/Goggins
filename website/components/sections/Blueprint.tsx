export default function Blueprint() {
    return (
        <section className="py-28 px-6 relative overflow-hidden" style={{ background: "#040A14" }}>

            {/* Blueprint grid background */}
            <div className="absolute inset-0 pointer-events-none"
                style={{
                    backgroundImage: `
            linear-gradient(rgba(59,130,246,0.08) 1px, transparent 1px),
            linear-gradient(90deg, rgba(59,130,246,0.08) 1px, transparent 1px)
          `,
                    backgroundSize: "40px 40px"
                }}
            />
            {/* Crosshairs at intersections (small dots) */}
            <div className="absolute inset-0 pointer-events-none"
                style={{
                    backgroundImage: `radial-gradient(circle, rgba(59,130,246,0.25) 1px, transparent 1px)`,
                    backgroundSize: "40px 40px",
                    backgroundPosition: "0 0"
                }}
            />

            <div className="max-w-7xl mx-auto relative">

                {/* Section header */}
                <div className="flex items-center gap-3 mb-4">
                    <div className="w-8 h-px bg-blue-400" />
                    <span className="text-blue-400 text-xs font-semibold uppercase tracking-widest font-mono">
                        SHEET AR-401 — INTELLIGENCE ARCHITECTURE
                    </span>
                </div>

                <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-12">
                    <h2 className="text-4xl md:text-5xl font-black leading-tight tracking-tight">
                        THE BLUEPRINT<br />
                        <span style={{ color: "#60A5FA" }}>OF YOUR PROJECT</span>
                    </h2>
                    <p className="text-blue-300/70 max-w-sm leading-relaxed text-sm font-mono">
                        Every construction project starts with a blueprint.
                        StructuraAI converts yours into living intelligence.
                    </p>
                </div>

                {/* Main blueprint image */}
                <div className="relative rounded-xl overflow-hidden border border-blue-500/20">
                    {/* Ruler tick marks - top */}
                    <div className="h-6 bg-blue-950/80 border-b border-blue-500/20 flex items-end px-4 overflow-hidden">
                        <div className="flex w-full">
                            {Array.from({ length: 32 }).map((_, i) => (
                                <div key={i} className="flex-1 flex justify-center">
                                    <div className={`bg-blue-400/40 w-px ${i % 4 === 0 ? "h-4" : "h-2"}`} />
                                </div>
                            ))}
                        </div>
                    </div>

                    <div className="relative flex">
                        {/* Ruler tick marks - left */}
                        <div className="w-6 bg-blue-950/80 border-r border-blue-500/20 flex flex-col items-end py-0 overflow-hidden flex-shrink-0">
                            {Array.from({ length: 20 }).map((_, i) => (
                                <div key={i} className="flex-1 flex items-center justify-end pr-0.5">
                                    <div className={`bg-blue-400/40 h-px ${i % 4 === 0 ? "w-4" : "w-2"}`} />
                                </div>
                            ))}
                        </div>

                        {/* Blueprint image */}
                        {/* eslint-disable-next-line @next/next/no-img-element */}
                        <img
                            src="/blueprint-floorplan.png"
                            alt="Blueprint floor plan showing the StructuraAI intelligence architecture"
                            className="w-full object-cover"
                            style={{ maxHeight: "560px", filter: "brightness(0.9) saturate(1.1)" }}
                        />

                        {/* Overlay labels on top of blueprint */}
                        <div className="absolute inset-0 pointer-events-none">
                            {/* Top-left callout */}
                            <div className="absolute top-6 left-10 bg-blue-900/70 backdrop-blur-sm border border-blue-400/30 rounded px-3 py-1.5">
                                <div className="text-blue-200 text-xs font-mono font-bold">BLUEPRINT INGESTION ZONE</div>
                                <div className="text-blue-400/70 text-[10px] font-mono">NODE EXTRACTION + PARSING</div>
                            </div>

                            {/* Center callout */}
                            <div className="absolute top-6 left-1/2 -translate-x-1/2 bg-blue-900/70 backdrop-blur-sm border border-blue-400/30 rounded px-3 py-1.5">
                                <div className="text-blue-200 text-xs font-mono font-bold">DEPENDENCY GRAPH ENGINE</div>
                                <div className="text-blue-400/70 text-[10px] font-mono">NetworkX • 3,871 EDGES</div>
                            </div>

                            {/* Bottom-right callout */}
                            <div className="absolute bottom-6 right-6 bg-amber-950/80 backdrop-blur-sm border border-primary/40 rounded px-3 py-2">
                                <div className="text-primary text-xs font-mono font-bold">BUILDABILITY CORE</div>
                                <div className="text-2xl font-black text-gradient leading-none mt-0.5">87.4</div>
                                <div className="text-primary/60 text-[10px] font-mono">SCORE™</div>
                            </div>
                        </div>
                    </div>

                    {/* Bottom ruler */}
                    <div className="h-6 bg-blue-950/80 border-t border-blue-500/20 flex items-start px-4 overflow-hidden">
                        <div className="flex w-full">
                            {Array.from({ length: 32 }).map((_, i) => (
                                <div key={i} className="flex-1 flex justify-center">
                                    <div className={`bg-blue-400/40 w-px ${i % 4 === 0 ? "h-4" : "h-2"}`} />
                                </div>
                            ))}
                        </div>
                    </div>
                </div>

                {/* Stats below blueprint */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-8">
                    {[
                        { label: "NODES EXTRACTED", value: "1,240", unit: "elements" },
                        { label: "DEPENDENCIES MAPPED", value: "3,871", unit: "edges" },
                        { label: "CONFLICTS FLAGGED", value: "3", unit: "before construction" },
                        { label: "STRATEGIES GENERATED", value: "4", unit: "execution plans" },
                    ].map((s) => (
                        <div key={s.label} className="border border-blue-500/15 bg-blue-950/20 rounded-lg px-4 py-4">
                            <div className="text-blue-400/60 text-[10px] font-mono uppercase tracking-widest mb-2">{s.label}</div>
                            <div className="text-white font-black text-2xl leading-none">{s.value}</div>
                            <div className="text-blue-400/50 text-xs font-mono mt-1">{s.unit}</div>
                        </div>
                    ))}
                </div>
            </div>
        </section>
    )
}

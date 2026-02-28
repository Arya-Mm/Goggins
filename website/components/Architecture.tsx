const layers = [
    {
        label: "Perception Layer",
        accent: "#22d3ee", bg: "rgba(34,211,238,0.05)", border: "rgba(34,211,238,0.15)",
        items: ["YOLOv8 Detection", "OCR Extraction", "Scale Calibration"],
    },
    {
        label: "Intelligence Core",
        accent: "#818cf8", bg: "rgba(129,140,248,0.05)", border: "rgba(129,140,248,0.15)",
        items: ["Graph Engine", "CPM / PERT Scheduler", "Conflict Detector", "Risk Model"],
    },
    {
        label: "Cognitive Layer",
        accent: "#34d399", bg: "rgba(52,211,153,0.05)", border: "rgba(52,211,153,0.15)",
        items: ["What-If Optimizer", "Offline LLM", "Report Generation"],
    },
];

export default function Architecture() {
    return (
        <section id="architecture" className="py-10 px-6 bg-black relative overflow-hidden">
            <div className="accent-line w-full absolute top-0 left-0 opacity-30" />

            <div className="max-w-6xl mx-auto relative z-10">
                <div className="mb-6">
                    <p className="text-[10px] font-semibold text-cyan-400 uppercase tracking-widest mb-2">System Design</p>
                    <h2 className="text-2xl font-bold text-white tracking-tight">Three-Layer Architecture</h2>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                    {layers.map((layer, i) => (
                        <div key={i} className="card-glass card-glass-hover rounded-xl p-5" style={{ borderColor: layer.border, background: layer.bg }}>
                            <p className="text-[10px] font-bold uppercase tracking-widest mb-3" style={{ color: layer.accent }}>{layer.label}</p>
                            <div className="flex flex-wrap gap-1.5">
                                {layer.items.map((item, j) => (
                                    <span key={j} className="text-[10px] font-medium px-2 py-0.5 rounded"
                                        style={{ background: "rgba(255,255,255,0.04)", border: `1px solid ${layer.border}`, color: layer.accent }}>
                                        {item}
                                    </span>
                                ))}
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </section>
    );
}

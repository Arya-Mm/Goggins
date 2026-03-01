// ─────────────────────────────────────────────────────────────────────────────
// TO ADD YOUR DEMO VIDEO:
//   1. Upload your video to YouTube, Vimeo, or any platform that gives an embed URL
//   2. Paste the embed URL below (YouTube example: https://www.youtube.com/embed/YOUR_VIDEO_ID)
//   3. Save the file — the placeholder will be replaced by the real player instantly
//
//   Leave VIDEO_URL as an empty string ("") to keep the "Coming Soon" placeholder.
// ─────────────────────────────────────────────────────────────────────────────
const VIDEO_URL = ""
// ─────────────────────────────────────────────────────────────────────────────

export default function DemoPage() {
    return (
        <main className="min-h-screen bg-background flex flex-col">

            {/* Page header */}
            <div className="pt-32 pb-12 px-6 text-center">
                <div className="inline-flex items-center gap-2 border border-primary/30 bg-primary/5 text-primary text-xs font-semibold px-4 py-2 rounded-full mb-6 uppercase tracking-widest">
                    <span className="w-1.5 h-1.5 bg-primary rounded-full" />
                    Product Demo
                </div>

                <h1 className="text-4xl md:text-5xl font-black tracking-tight mb-4">
                    SEE <span className="text-gradient">STRUCTURAAI</span> IN ACTION
                </h1>
                <p className="text-muted max-w-xl mx-auto leading-relaxed">
                    Watch how StructuraAI converts a raw civil blueprint into a full
                    construction intelligence report — in minutes.
                </p>
            </div>

            {/* Video player area */}
            <div className="flex-1 px-6 pb-20">
                <div className="max-w-4xl mx-auto">

                    {VIDEO_URL ? (
                        /* ── Real video player (shown when VIDEO_URL is set) ── */
{VIDEO_URL ? (
    /* ── Real video player (shown when VIDEO_URL is set) ── */
    <div
        className="relative w-full rounded-2xl overflow-hidden border border-border"
        style={{ paddingBottom: "56.25%" /* 16:9 ratio */ }}
    >
        <iframe
            src={VIDEO_URL}
            title="StructuraAI Demo Video"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
            allowFullScreen
            className="absolute inset-0 w-full h-full"
        />
    </div>
) : (
                        </div>
                    ) : (
                        /* ── Placeholder (shown when VIDEO_URL is empty) ── */
                        <div className="relative rounded-2xl overflow-hidden border border-border bg-surface aspect-video flex flex-col items-center justify-center gap-6">

                            {/* Grid background */}
                            <div className="absolute inset-0 bg-grid opacity-40 pointer-events-none" />

                            {/* Rebar edge decorations */}
                            <div className="absolute left-0 top-0 bottom-0 w-1.5 rebar-pattern opacity-50" />
                            <div className="absolute right-0 top-0 bottom-0 w-1.5 rebar-pattern opacity-50" />

                            {/* Play button */}
                            <div className="relative z-10 w-20 h-20 rounded-full bg-primary/10 border border-primary/30 flex items-center justify-center">
                                <svg width="32" height="32" viewBox="0 0 24 24" fill="currentColor" className="text-primary ml-1">
                                    <polygon points="5 3 19 12 5 21 5 3" />
                                </svg>
                            </div>

                            <div className="relative z-10 text-center">
                                <p className="text-white font-bold text-lg mb-1">Demo Video Coming Soon</p>
                                <p className="text-muted text-sm">
                                    Set <code className="text-primary bg-primary/10 px-1.5 py-0.5 rounded text-xs">VIDEO_URL</code> in{" "}
                                    <code className="text-muted-light bg-surface-2 px-1.5 py-0.5 rounded text-xs">app/demo/page.tsx</code>{" "}
                                    to publish your video.
                                </p>
                            </div>

                            {/* Corner grid reference labels */}
                            <div className="absolute top-3 left-5 text-[10px] font-mono text-muted/40">AR-DEMO / SHEET 01</div>
                            <div className="absolute bottom-3 right-5 text-[10px] font-mono text-muted/40">SCALE: FULL</div>
                        </div>
                    )}

                    {/* Below-player info cards */}
                    <div className="grid md:grid-cols-3 gap-4 mt-8">
                        {[
                            { label: "Duration", value: "~8 min", sub: "Full walkthrough" },
                            { label: "Covers", value: "9 Stages", sub: "End-to-end pipeline" },
                            { label: "Output", value: "Live Report", sub: "Buildability Score™ + AI" },
                        ].map((c) => (
                            <div key={c.label} className="border border-border bg-surface rounded-xl px-5 py-4 text-center">
                                <div className="text-muted text-xs font-mono uppercase tracking-widest mb-1">{c.label}</div>
                                <div className="text-white font-black text-xl leading-none">{c.value}</div>
                                <div className="text-muted text-xs mt-1">{c.sub}</div>
                            </div>
                        ))}
                    </div>


                </div>
            </div>
        </main>
    )
}

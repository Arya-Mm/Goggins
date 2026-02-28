import Link from "next/link"

export default function Footer() {
    return (
        <footer className="border-t border-border bg-background">
            <div className="max-w-7xl mx-auto px-6 py-16">
                <div className="grid md:grid-cols-4 gap-12 mb-12">

                    {/* Brand */}
                    <div className="md:col-span-1">
                        <Link href="/" className="flex items-center gap-2.5 mb-4">
                            <div className="w-7 h-7 bg-primary rounded flex items-center justify-center">
                                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#000" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                                    <polygon points="3 9 12 2 21 9 21 20 3 20 3 9" />
                                    <line x1="9" y1="20" x2="9" y2="12" />
                                    <line x1="15" y1="20" x2="15" y2="12" />
                                    <line x1="9" y1="12" x2="15" y2="12" />
                                </svg>
                            </div>
                            <span className="text-base font-bold">Structura<span className="text-primary">AI</span></span>
                        </Link>
                        <p className="text-muted text-sm leading-relaxed">
                            Autonomous Pre-Construction Intelligence Engine for civil engineering teams.
                        </p>
                    </div>

                    {/* Product */}
                    <div>
                        <h4 className="text-white font-semibold text-sm mb-4">Product</h4>
                        <ul className="space-y-3 text-muted text-sm">
                            <li><a href="/#features" className="hover:text-white transition-colors">Features</a></li>
                            <li><a href="/#pipeline" className="hover:text-white transition-colors">Pipeline</a></li>
                            <li><a href="/demo" className="hover:text-white transition-colors">Demo</a></li>
                            <li><Link href="/architecture" className="hover:text-white transition-colors">Architecture</Link></li>
                        </ul>
                    </div>

                    {/* Company */}
                    <div>
                        <h4 className="text-white font-semibold text-sm mb-4">Company</h4>
                        <ul className="space-y-3 text-muted text-sm">
                            <li><Link href="/about" className="hover:text-white transition-colors">About</Link></li>
                            <li><a href="#" className="hover:text-white transition-colors">Careers</a></li>
                            <li><a href="#" className="hover:text-white transition-colors">Contact</a></li>
                        </ul>
                    </div>

                    {/* Technology */}
                    <div>
                        <h4 className="text-white font-semibold text-sm mb-4">Technology</h4>
                        <ul className="space-y-3 text-muted text-sm">
                            <li className="flex items-center gap-2"><span className="w-1.5 h-1.5 rounded-full bg-primary/60" />NetworkX Graph Engine</li>
                            <li className="flex items-center gap-2"><span className="w-1.5 h-1.5 rounded-full bg-primary/60" />Local LLM (Ollama)</li>
                            <li className="flex items-center gap-2"><span className="w-1.5 h-1.5 rounded-full bg-primary/60" />Buildability Score™</li>
                            <li className="flex items-center gap-2"><span className="w-1.5 h-1.5 rounded-full bg-primary/60" />Zero Cloud Dependency</li>
                        </ul>
                    </div>
                </div>

                <div className="divider mb-8" />

                <div className="flex flex-col md:flex-row justify-between items-center gap-4 text-muted text-sm">
                    <span>© {new Date().getFullYear()} StructuraAI. Autonomous Pre-Construction Intelligence.</span>
                    <div className="flex items-center gap-1.5">
                        <span className="w-2 h-2 rounded-full bg-green-400 animate-pulse" />
                        <span>All systems operational</span>
                    </div>
                </div>
            </div>
        </footer>
    )
}

import Link from "next/link"

export default function Navbar() {
    return (
        <nav className="fixed top-0 left-0 right-0 z-50 border-b border-border bg-background/90 backdrop-blur-md">
            <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
                {/* Logo */}
                <Link href="/" className="flex items-center gap-2.5 group">
                    <div className="w-8 h-8 bg-primary rounded flex items-center justify-center">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#000" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                            <polygon points="3 9 12 2 21 9 21 20 3 20 3 9" />
                            <line x1="9" y1="20" x2="9" y2="12" />
                            <line x1="15" y1="20" x2="15" y2="12" />
                            <line x1="9" y1="12" x2="15" y2="12" />
                        </svg>
                    </div>
                    <span className="text-lg font-bold tracking-tight">
                        Structura<span className="text-primary">AI</span>
                    </span>
                </Link>

                {/* Nav links */}
                <div className="hidden md:flex items-center gap-8 text-sm font-medium text-muted-light">
                    <Link href="/architecture" className="hover:text-white transition-colors">Architecture</Link>
                    <Link href="/about" className="hover:text-white transition-colors">About</Link>
                    <a href="/#features" className="hover:text-white transition-colors">Features</a>
                    <a href="/#pipeline" className="hover:text-white transition-colors">Pipeline</a>
                </div>

                {/* CTA */}
                <Link
                    href="/demo"
                    className="btn-primary text-sm hidden md:inline-flex items-center gap-2"
                >
                    Request Demo
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5"><path d="M5 12h14M12 5l7 7-7 7" /></svg>
                </Link>
            </div>
        </nav>
    )
}

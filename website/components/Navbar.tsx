import Link from "next/link"

export default function Navbar() {
    return (
        <nav className="w-full border-b border-border bg-background">
            <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
                <Link href="/" className="text-xl font-semibold">
                    StructuraAI
                </Link>

                <div className="space-x-6 text-sm text-muted">
                    <Link href="/architecture">Architecture</Link>
                    <Link href="/about">About</Link>
                </div>
            </div>
        </nav>
    )
}

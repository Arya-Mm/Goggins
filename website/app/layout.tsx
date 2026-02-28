import "./globals.css"
import Navbar from "@/components/Navbar"
import Footer from "@/components/Footer"

export const metadata = {
    title: "StructuraAI — Autonomous Pre-Construction Intelligence Engine",
    description: "Transform civil blueprints into executable construction strategies."
}

export default function RootLayout({
    children,
}: {
    children: React.ReactNode
}) {
    return (
        <html lang="en">
            <body>
                <Navbar />
                {children}
                <Footer />
            </body>
        </html>
    )
}

/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "./app/**/*.{ts,tsx}",
        "./components/**/*.{ts,tsx}"
    ],
    theme: {
        extend: {
            colors: {
                background: "#07090C",
                surface: "#0D1117",
                "surface-2": "#131920",
                primary: "#F59E0B",
                "primary-hover": "#D97706",
                accent: "#1D4ED8",
                muted: "#6B7280",
                "muted-light": "#9CA3AF",
                border: "#1F2937",
                "border-light": "#374151",
            },
            fontFamily: {
                sans: ["Inter", "ui-sans-serif", "system-ui", "sans-serif"],
            },
            backgroundImage: {
                "grid-pattern": "linear-gradient(rgba(245,158,11,0.04) 1px, transparent 1px), linear-gradient(90deg, rgba(245,158,11,0.04) 1px, transparent 1px)",
            },
            backgroundSize: {
                "grid": "60px 60px",
            },
        },
    },
    plugins: [],
}

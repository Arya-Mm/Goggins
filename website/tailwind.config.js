/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "./app/**/*.{ts,tsx}",
        "./components/**/*.{ts,tsx}"
    ],
    theme: {
        extend: {
            colors: {
                background: "#0B0F14",
                surface: "#121821",
                primary: "#1E90FF",
                muted: "#94A3B8",
                border: "#1F2937"
            }
        },
    },
    plugins: [],
}

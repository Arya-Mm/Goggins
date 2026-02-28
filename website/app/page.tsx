import Hero from "@/components/sections/Hero"
import Problem from "@/components/sections/Problem"
import Solution from "@/components/sections/Solution"
import Pipeline from "@/components/sections/Pipeline"
import Features from "@/components/sections/Features"
import Demo from "@/components/sections/Demo"
import CTA from "@/components/sections/CTA"

export default function Home() {
    return (
        <>
            <Hero />
            <Problem />
            <Solution />
            <Pipeline />
            <Features />
            <Demo />
            <CTA />
        </>
    )
}

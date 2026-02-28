import Hero from "@/components/sections/Hero"
import Problem from "@/components/sections/Problem"
import Blueprint from "@/components/sections/Blueprint"
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
            <Blueprint />
            <Solution />
            <Pipeline />
            <Features />
            <Demo />
            <CTA />
        </>
    )
}

export default function Features() {
    return (
        <section className="py-24 px-6">
            <div className="max-w-6xl mx-auto grid md:grid-cols-2 gap-12">
                <div>
                    <h3 className="text-xl font-semibold mb-4">Conflict Detection</h3>
                    <p className="text-muted">
                        Automatically detect curing conflicts, task overlaps,
                        and workforce overload conditions.
                    </p>
                </div>

                <div>
                    <h3 className="text-xl font-semibold mb-4">Buildability Score™</h3>
                    <p className="text-muted">
                        Executive-level decision metric based on deterministic
                        structural risk modeling.
                    </p>
                </div>

                <div>
                    <h3 className="text-xl font-semibold mb-4">What-If Simulation</h3>
                    <p className="text-muted">
                        Adjust workforce, delays, and constraints to simulate
                        real-world execution outcomes.
                    </p>
                </div>

                <div>
                    <h3 className="text-xl font-semibold mb-4">Explainable AI</h3>
                    <p className="text-muted">
                        Local LLM reasoning layer provides transparent,
                        structured engineering explanations.
                    </p>
                </div>
            </div>
        </section>
    )
}

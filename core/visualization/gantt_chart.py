import matplotlib.pyplot as plt


def generate_gantt_chart(G, output_path="gantt_chart.png"):
    """
    Generates simple Gantt-style chart from CPM graph.
    """

    tasks = []
    start_times = []
    durations = []

    for node in G.nodes:
        es = G.nodes[node].get("ES", 0)
        ef = G.nodes[node].get("EF", 0)
        duration = ef - es

        tasks.append(node)
        start_times.append(es)
        durations.append(duration)

    plt.figure(figsize=(10, 6))

    for i in range(len(tasks)):
        plt.barh(tasks[i], durations[i], left=start_times[i])

    plt.xlabel("Time")
    plt.ylabel("Tasks")
    plt.title("Project Schedule Gantt Chart")
    plt.tight_layout()

    plt.savefig(output_path)
    plt.close()

    return output_path
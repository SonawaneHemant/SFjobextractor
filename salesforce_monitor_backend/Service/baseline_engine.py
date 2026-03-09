def calculate_baseline(metrics_history):

    if not metrics_history:
        return {}

    baseline = {}

    baseline["avg_failures"] = sum(
        m["failed"] for m in metrics_history
    ) / len(metrics_history)

    baseline["avg_errors"] = sum(
        m["total_errors"] for m in metrics_history
    ) / len(metrics_history)

    return baseline
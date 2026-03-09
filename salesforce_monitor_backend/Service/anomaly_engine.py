def detect_anomalies(metrics):

    anomalies = []

    if metrics["failed"] > 10:
        anomalies.append("Spike in failed jobs")

    if metrics["total_errors"] > 50:
        anomalies.append("High error volume detected")

    failure_rate = 0

    if metrics["total_jobs"] > 0:
        failure_rate = metrics["failed"] / metrics["total_jobs"]

    if failure_rate > 0.15:
        anomalies.append("Failure rate above 15%")

    return anomalies
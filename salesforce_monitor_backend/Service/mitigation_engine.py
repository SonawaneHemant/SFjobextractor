def recommend_action(anomalies):

    actions = []

    for anomaly in anomalies:

        if "failed jobs" in anomaly:
            actions.append(
                "Investigate recent deployments or failing Apex classes"
            )

        if "error volume" in anomaly:
            actions.append(
                "Review error logs and integration calls"
            )

        if "Failure rate" in anomaly:
            actions.append(
                "Temporarily pause heavy batch jobs"
            )

    return actions
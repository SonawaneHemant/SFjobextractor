import salesforce_monitor_backend.DataBase.database_extract_jobs as database_extract_jobs

def evaluate_main_system_health():
    metrics = database_extract_jobs.get_job_metrics()
    failed_jobs = database_extract_jobs.get_failed_jobs()

    alerts = []

    if metrics["failed"] > 5:
        alerts.append("High number of failed jobs detected")

    if metrics["total_errors"] > 20:
        alerts.append("High error volume detected")

    success_rate = 0
    if metrics["total_jobs"] > 0:
        success_rate = metrics["completed"] / metrics["total_jobs"]

    if success_rate < 0.80:
        alerts.append("Success rate below 80%")

    return metrics, alerts ,failed_jobs


# def evaluate_system_health():
#     metrics = database.get_job_metrics()

#     alerts = []

#     if metrics["failed"] > 5:
#         alerts.append("High number of failed jobs detected")

#     if metrics["total_errors"] > 20:
#         alerts.append("High error volume detected")

#     success_rate = 0
#     if metrics["total_jobs"] > 0:
#         success_rate = metrics["completed"] / metrics["total_jobs"]

#     if success_rate < 0.80:
#         alerts.append("Success rate below 80%")

#     return metrics, alerts
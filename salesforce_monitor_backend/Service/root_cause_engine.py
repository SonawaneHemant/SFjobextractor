import salesforce_monitor_backend.DataBase.database_extract_jobs as database


def identify_top_failed_classes():

    jobs = database.fetch_all_jobs()

    class_failures = {}

    for row in jobs:

        apex_class = row[7]
        status = row[8]

        if status == "Failed":

            class_failures[apex_class] = class_failures.get(apex_class, 0) + 1

    sorted_classes = sorted(
        class_failures.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return sorted_classes[:3]
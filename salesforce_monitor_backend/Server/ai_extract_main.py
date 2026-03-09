import salesforce_monitor_backend.DataBase.database_extract_jobs as database_extract_jobs
import salesforce_monitor_backend.Service.ai_metrics_engine as ai_metrics_engine
import salesforce_monitor_backend.Agent.ai_agent_main as ai_agent_main
import salesforce_monitor_backend.Service.ai_salesforce_service_main as ai_salesforce_service_main

def run_monitoring():

    # Ensure table exists
    ai_salesforce_service_main.extract_and_store_jobs()

    metrics, alerts, failed_jobs = ai_metrics_engine.evaluate_main_system_health()

    print("\n=== SYSTEM METRICS ===")
    print(metrics)

    print("\n=== ALERTS ===")
    print(alerts if alerts else "No alerts")

    print("\n=== FAILED JOBS ===")
    print(failed_jobs if failed_jobs else "No failed jobs")

    # ai_response = ai_agent_main.run_ai_analysis(metrics, alerts, failed_jobs)

    # print("\n=== AI ROOT CAUSE ANALYSIS ===")
    # print(ai_response)

    #  # Structured AI output
    # structured_report = ai_agent_main.run_ai_analysis_structured(
    #     metrics, alerts, failed_jobs
    # )

    # print("\n=== STRUCTURED AI REPORT ===")
    # print(structured_report)

    # # Structured AI output with pydentic
    # structured_report = ai_agent_main.run_ai_analysis_structured_pydentic(
    #     metrics, alerts, failed_jobs
    # )

    # print("\n=== STRUCTURED PYDENTIC AI REPORT ===")
    # print(structured_report)

    

if __name__ == "__main__":
    run_monitoring()

# def run_monitoring():

#     # Ensure table exists
#     #salesforce_service_main.extract_and_store_jobs()

#     # Step 1: Get Metrics + Alerts
#     metrics, alerts = metrics_engine.evaluate_system_health()

#     print("\n=== SYSTEM METRICS ===")
#     print(metrics)

#     print("\n=== ALERTS ===")
#     print(alerts if alerts else "No alerts")

#     # Step 2: AI Analysis
#     ai_response = ai_agent_main.run_ai_analysis(metrics, alerts)

#     print("\n=== AI ANALYSIS ===")
#     print(ai_response)


# if __name__ == "__main__":
#     run_monitoring()
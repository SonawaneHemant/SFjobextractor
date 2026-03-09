# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from salesforce-monitor-backend.Models.ai_models import SystemHealthReport
# import ai_metrics_engine
# import salesforce_monitor_backend.Agent.ai_agent_main as ai_agent_main
# import database_extract_jobs


# app = FastAPI(
#     title="Salesforce Job Monitoring API",
#     description="AI powered Salesforce job monitoring system",
#     version="1.0"
# )

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # allow React frontend
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# @app.get("/health")
# def health():
#     return {"status": "API running"}


# @app.get("/job-monitoring", response_model=SystemHealthReport)
# def job_monitoring():

#     # Step 1: Get metrics
#     metrics, alerts, failed_jobs = ai_metrics_engine.evaluate_main_system_health()

#     # Step 2: Run AI analysis
#     report = ai_agent_main.run_ai_analysis_structured_pydentic(
#         metrics,
#         alerts,
#         failed_jobs
#     )

#     return report

# @app.get("/jobs")
# def get_jobs():

#     jobs = database_extract_jobs.fetch_all_jobs()

#     result = []

#     for row in jobs:
#         result.append({
#             "job_id": row[1],
#             "created_date": row[2],
#             "job_type": row[5],
#             "apex_class_name": row[7],
#             "status": row[8],
#             "number_of_errors": row[11]
#         })

#     return {
#         "total_jobs": len(result),
#         "jobs": result
#     }

# @app.get("/failed-jobs")
# def failed_jobs():

#     jobs = database_extract_jobs.get_failed_jobs()

#     return {
#         "failed_count": len(jobs),
#         "failed_jobs": jobs
#     }

# @app.get("/job/{job_id}")
# def get_job(job_id: str):

#     job = database_extract_jobs.get_job_by_id(job_id)

#     if job is None:
#         raise HTTPException(status_code=404, detail="Job not found")

#     return job
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from salesforce_monitor_backend.Models.ai_models import SystemHealthReport
import salesforce_monitor_backend.Service.ai_metrics_engine as ai_metrics_engine
import salesforce_monitor_backend.Agent.ai_agent_main as ai_agent_main
import salesforce_monitor_backend.DataBase.database_extract_jobs as database_extract_jobs
from salesforce_monitor_backend.Agent.limit_guard_agent import LimitGuardAgent
from salesforce_monitor_backend.Service.scheduler import start_scheduler
import salesforce_monitor_backend.Service.ai_salesforce_service_main as ai_salesforce_service_main
import os
import requests
from fastapi.responses import RedirectResponse

app = FastAPI(
    title="Salesforce Job Monitoring API",
    description="AI powered Salesforce job monitoring system",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.on_event("startup")
# def start_background_scheduler():
#     start_scheduler()

@app.get("/health")
def health():
    return {"status": "API running"}


@app.get("/job-monitoring", response_model=SystemHealthReport)
def job_monitoring():

    # Step 1: Get metrics
    metrics, alerts, failed_jobs = ai_metrics_engine.evaluate_main_system_health()

    # Step 2: Run AI analysis
    report = ai_agent_main.run_ai_analysis_structured_pydentic(
        metrics,
        alerts,
        failed_jobs
    )

    return report

@app.get("/alljobs")
def get_jobs():

    jobs = database_extract_jobs.fetch_all_jobs()

    # result = []

    # for row in jobs:
    #     result.append({
    #         "job_id": row[1],
    #         "created_date": row[2],
    #         "job_type": row[5],
    #         "apex_class_name": row[7],
    #         "status": row[8],
    #         "number_of_errors": row[11]
    #     })

    # return {
    #     "total_jobs": len(result),
    #     "jobs": result
    # }

    return {
        "total_jobs": len(jobs),
        "jobs": [dict(row) for row in jobs]
    }

@app.get("/jobs")
def get_jobs():

    jobs = database_extract_jobs.fetch_all_current_jobs()

    # result = []
    # #One more way to do that
    # # result = [dict(row) for row in jobs]
    # for row in jobs:
    #     result.append({
    #         "job_id": row["job_id"],
    #         "created_date": row["created_date"],
    #         "job_type": row["job_type"],
    #         "apex_class_name": row["apex_class_name"],
    #         "status": row["status"],
    #         "number_of_errors": row["number_of_errors"]
    #     })

    # return {
    #     "total_jobs": len(result),
    #     "jobs": result
    # }

    return {
        "total_jobs": len(jobs),
        "jobs": [dict(row) for row in jobs]
    }




@app.get("/failed-jobs")
def failed_jobs():

    jobs = database_extract_jobs.get_failed_jobs()

    return {
        "failed_count": len(jobs),
        "failed_jobs": jobs
    }

@app.get("/job/{job_id}")
def get_job(job_id: str):

    job = database_extract_jobs.get_job_by_id(job_id)

    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    return job

agent = LimitGuardAgent()
@app.get("/limit-guard")
def run_limit_guard():

    result = agent.run()

    return result

@app.get("/fetchjobs")
def run_fetch_jobs():
    result=ai_salesforce_service_main.extract_and_store_jobs()
    return result

#working sf access token
# @app.get("/login")
# def login():

#     auth_url = (
#         f"{os.getenv('SF_LOGIN_URL')}/services/oauth2/authorize"
#         f"?response_type=code"
#         f"&client_id={os.getenv('SF_CLIENT_ID')}"
#         f"&redirect_uri={os.getenv('SF_REDIRECT_URI')}"
#     )

#     return {"login_url": auth_url}

# @app.get("/v1/callback")
# def oauth_callback(code: str):

#     token_url = f"{os.getenv('SF_LOGIN_URL')}/services/oauth2/token"

#     payload = {
#         "grant_type": "authorization_code",
#         "client_id": os.getenv("SF_CLIENT_ID"),
#         "client_secret": os.getenv("SF_CLIENT_SECRET"),
#         "redirect_uri": os.getenv("SF_REDIRECT_URI"),
#         "code": code
#     }

#     response = requests.post(token_url, data=payload)

#     data = response.json()

#     access_token = data["access_token"]
#     refresh_token = data["refresh_token"]
#     instance_url = data["instance_url"]

#     print("ACCESS TOKEN:", access_token)
#     print("REFRESH TOKEN:", refresh_token)

#     return data

#automated SF access token

@app.get("/login")
def login():

    auth_url = (
        f"{os.getenv('SF_LOGIN_URL')}/services/oauth2/authorize"
        f"?response_type=code"
        f"&client_id={os.getenv('SF_CLIENT_ID')}"
        f"&redirect_uri={os.getenv('SF_REDIRECT_URI')}"
    )

    return RedirectResponse(auth_url)


@app.get("/v1/callback")
def oauth_callback(code: str):

    token_url = f"{os.getenv('SF_LOGIN_URL')}/services/oauth2/token"

    payload = {
        "grant_type": "authorization_code",
        "client_id": os.getenv("SF_CLIENT_ID"),
        "client_secret": os.getenv("SF_CLIENT_SECRET"),
        "redirect_uri": os.getenv("SF_REDIRECT_URI"),
        "code": code
    }

    response = requests.post(token_url, data=payload)
    data = response.json()

    access_token = data["access_token"]
    refresh_token = data["refresh_token"]
    instance_url = data["instance_url"]

    print("ACCESS TOKEN:", access_token)
    print("REFRESH TOKEN:", refresh_token)

    # Store refresh token
    save_refresh_token(refresh_token, instance_url)

    return RedirectResponse("/connected-success")

def save_refresh_token(refresh_token, instance_url):

    with open("salesforce_token.txt", "w") as f:
        f.write(refresh_token)

    print("Refresh token saved successfully")

@app.get("/connected-success")
def success():

    return {
        "status": "Salesforce connected successfully"
    }
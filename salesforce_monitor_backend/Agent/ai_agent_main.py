import json
from langchain_ollama import OllamaLLM
from langchain_core.output_parsers import PydanticOutputParser

from salesforce_monitor_backend.Models.ai_models import SystemHealthReport

def run_ai_analysis(metrics, alerts ,failed_jobs):

    llm = OllamaLLM(
        model="qwen2.5:7b",
        temperature=0   # makes output stable
    )

    failed_jobs_text = ""

    for job in failed_jobs:
        failed_jobs_text += f"""
        Job ID: {job['job_id']}
        Job Type: {job['job_type']}
        Apex Class: {job['apex_class_name']}
        Error Count: {job['number_of_errors']}
        Error Message: {job['extended_status']}
        -------------------------
        """

    prompt = f"""
    You are a Salesforce DevOps AI Monitoring Agent.

    Overall Metrics:
    Total Jobs: {metrics["total_jobs"]}
    Completed: {metrics["completed"]}
    Failed: {metrics["failed"]}
    Total Errors: {metrics["total_errors"]}

    Alerts:
    {alerts}

    Failed Job Details:
    {failed_jobs_text}

    TASK:

    1. Provide overall system health.
    2. For each failed job:
       - Identify likely root cause
       - Suggest fix
       - Suggest prevention strategy

    Format your response clearly.
    """

    response = llm.invoke(prompt)

    return response


# 🔹 Structured AI output
def run_ai_analysis_structured(metrics, alerts, failed_jobs):

    llm = OllamaLLM(model="qwen2.5:3b", temperature=0)

    prompt = f"""
        You are a Salesforce DevOps AI monitoring system.

        You MUST fill every field in the JSON.
        
        Do NOT leave fields empty.
        
        Use these rules:
        
        System Health Rules:
        - Healthy → failure rate < 5%
        - Warning → failure rate between 5% and 15%
        - Critical → failure rate > 15%
        
        Risk Level Rules:
        - Low → system stable
        - Medium → some failures detected
        - High → frequent failures

        Metrics:
        Total Jobs: {metrics["total_jobs"]}
        Completed: {metrics["completed"]}
        Failed: {metrics["failed"]}
        Errors: {metrics["total_errors"]}

        Alerts:
        {alerts}

        Failed Jobs:
        {failed_jobs}

        JSON format:

        {{
        "system_health":"",
        "risk_level":"",
        "total_jobs":0,
        "completed_jobs":0,
        "failed_jobs":0,
        "total_errors":0,
        "failed_job_analysis":[
        {{
        "job_id":"",
        "job_type":"",
        "apex_class":"",
        "root_cause":"",
        "fix":"",
        "prevention":""
        }}
        ]
        }}
    """

    response = llm.invoke(prompt)
    print(response)

    data = json.loads(response)

    report = SystemHealthReport(**data)

    return report

def run_ai_analysis_structured_pydentic(metrics, alerts, failed_jobs):

    llm = OllamaLLM(
        model="qwen2.5:3b",
        temperature=0
    )

    # Create parser
    parser = PydanticOutputParser(
        pydantic_object=SystemHealthReport
    )

    format_instructions = parser.get_format_instructions()

    prompt = f"""
You are a Salesforce DevOps Monitoring AI.

Analyze the job metrics and failed job errors.

Metrics:
Total Jobs: {metrics["total_jobs"]}
Completed Jobs: {metrics["completed"]}
Failed Jobs: {metrics["failed"]}
Total Errors: {metrics["total_errors"]}

Alerts:
{alerts}

Failed Jobs:
{failed_jobs}

IMPORTANT:
Return ONLY the final JSON result.
DO NOT return the schema.
DO NOT explain anything.
DO NOT include markdown.

{format_instructions}
"""

    response = llm.invoke(prompt)

    # Parse response automatically
    structured_output = parser.parse(response)

    return structured_output
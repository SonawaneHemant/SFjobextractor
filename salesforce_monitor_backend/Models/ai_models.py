from pydantic import BaseModel, Field
from typing import List


class FailedJobAnalysis(BaseModel):
    job_id: str = Field(description="Salesforce Async Apex Job ID of the failed job")
    job_type: str = Field(description="Type of Salesforce job such as Batch, Queueable, Future, or Scheduled")
    apex_class: str = Field(description="Name of the Apex class that executed the job")
    root_cause: str = Field(description="Likely technical root cause of the failure")
    fix: str = Field(description="Recommended fix to resolve the job failure")
    prevention: str = Field(description="Best practice to prevent this failure in the future")


class SystemHealthReport(BaseModel):
    system_health: str = Field(description="Overall health of the system: Healthy, Warning, or Critical")
    risk_level: str = Field(description="Operational risk level: Low, Medium, or High")
    total_jobs: int = Field(description="Total number of jobs processed")
    completed_jobs: int = Field(description="Number of successfully completed jobs")
    failed_jobs: int = Field(description="Number of failed jobs")
    total_errors: int = Field(description="Total number of errors detected across jobs")
    failed_job_analysis: List[FailedJobAnalysis] = Field(
        description="Detailed analysis for each failed Salesforce job"
    )
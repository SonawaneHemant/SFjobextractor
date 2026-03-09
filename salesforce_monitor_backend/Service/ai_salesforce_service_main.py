from simple_salesforce import Salesforce
from dotenv import load_dotenv
import os
import salesforce_monitor_backend.DataBase.database_extract_jobs as database_extract_jobs

load_dotenv()

def extract_and_store_jobs():
    session_id = os.getenv("SF_SESSION_ID")
    instance_url = os.getenv("SF_INSTANCE_URL") 

    sf = Salesforce(
        instance_url=instance_url,
        session_id=session_id
    )

    query = """
    SELECT                         
            Id,
            CreatedDate,     
            CreatedById,
            CreatedBy.Name,
            JobType,
            ApexClassId,
            ApexClass.Name,
            Status,
            JobItemsProcessed,
            TotalJobItems,
            NumberOfErrors,
            CompletedDate,
            MethodName,
            ExtendedStatus,
            ParentJobId,
            LastProcessed,
            LastProcessedOffset,
            CronTriggerId
    FROM AsyncApexJob
    ORDER BY CreatedDate DESC
    """

    result = sf.query(query)
    records = result["records"]

    # # Create table first time
    database_extract_jobs.create_table()

    for job in records:

        execution_time = database_extract_jobs.calculate_execution_time(
        job.get("CreatedDate"),
        job.get("CompletedDate")
        )

        flattened_job = {
        "job_id": job.get("Id"),
        "created_date": job.get("CreatedDate"),
        "created_by_id": job.get("CreatedById"),
        "created_by_name": (job.get("CreatedBy") or {}).get("Name"),
        "job_type": job.get("JobType"),
        "apex_class_id": job.get("ApexClassId"),
        "apex_class_name": (job.get("ApexClass") or {}).get("Name"),
        "status": job.get("Status"),
        "job_items_processed": job.get("JobItemsProcessed"),
        "total_job_items": job.get("TotalJobItems"),
        "number_of_errors": job.get("NumberOfErrors"),
        "completed_date": job.get("CompletedDate"),
        "method_name": job.get("MethodName"),
        "extended_status": job.get("ExtendedStatus"),
        "parent_job_id": job.get("ParentJobId"),
        "last_processed": job.get("LastProcessed"),
        "last_processed_offset": job.get("LastProcessedOffset"),
        "cron_trigger_id": job.get("CronTriggerId"),
        "execution_time": execution_time
        }
        database_extract_jobs.insert_job(flattened_job)

        database_extract_jobs.update_job_time_stats(
        flattened_job["job_id"],
        execution_time
        )
        database_extract_jobs.update_current_job_state(flattened_job)

    
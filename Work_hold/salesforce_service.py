from simple_salesforce import Salesforce
from dotenv import load_dotenv
import os
import database

load_dotenv()

def extract_and_store_jobs():
    session_id = os.getenv("SF_SESSION_ID")
    instance_url = os.getenv("SF_INSTANCE_URL") 

    sf = Salesforce(
        instance_url=instance_url,
        session_id=session_id
    )

    query = """
    SELECT Id,
           CreatedDate,
           CreatedById,
           JobType,
           ApexClassId,
           Status,
           JobItemsProcessed,
           TotalJobItems,
           NumberOfErrors,
           CompletedDate
    FROM AsyncApexJob
    ORDER BY CreatedDate DESC
    LIMIT 5
    """

    result = sf.query(query)
    records = result["records"]

    database.create_table()

    for job in records:
        database.insert_job(job)

    print(f"{len(records)} records inserted into SQLite.")
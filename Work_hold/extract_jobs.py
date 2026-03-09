# import json
# from simple_salesforce import Salesforce
# from dotenv import load_dotenv
# import os
# import database_extract_jobs

# # Load environment variables
# load_dotenv()

# username = os.getenv("SF_USERNAME")
# password = os.getenv("SF_PASSWORD")
# security_token = os.getenv("SF_SECURITY_TOKEN")



# sf = Salesforce(
#     instance_url="https://csx-ms-demo--dev.sandbox.my.salesforce.com",
#     session_id=session_id
# )

# full_password = password + security_token
# # Connect to Salesforce

# # sf = Salesforce(
# #     username=username,
# #     password=password,
# #     security_token=security_token,
# #     domain='test'
# # )
# # #security_token=security_token,


# # print("Username:", username)
# # print("Password:", password)
# # print("Token:", security_token)

# #Get the fields info from bellow code
# # desc = sf.AsyncApexJob.describe()

# # for field in desc['fields']:
# #     print(field['name'])


# query1 = """
# SELECT Id,
#        ApexClassId,
#        Status,
#        JobType,
#        CreatedDate,
#        CompletedDate,
#        NumberOfErrors,
#        TotalJobItems,
#        JobItemsProcessed
# FROM AsyncApexJob
# ORDER BY CreatedDate DESC
# LIMIT 10
# """

# query2 = """
# SELECT                         
#         Id,
#         CreatedDate,     
#         CreatedById,
#         CreatedBy.Name,
#         JobType,
#         ApexClassId,
#         ApexClass.Name,
#         Status,
#         JobItemsProcessed,
#         TotalJobItems,
#         NumberOfErrors,
#         CompletedDate,
#         MethodName,
#         ExtendedStatus,
#         ParentJobId,
#         LastProcessed,
#         LastProcessedOffset,
#         CronTriggerId
# FROM AsyncApexJob
# ORDER BY CreatedDate DESC
# """
# #LIMIT 10


# #How To Check Scheduled Jobs (Declarative or Apex) :- CronTrigger
# #This will show:
# #Scheduled Apex
# #Scheduled Flows
# #Scheduled processes 
# cronTrigger = """
# SELECT Id,
#        CronJobDetail.Name,
#        State,
#        NextFireTime,
#        PreviousFireTime
# FROM CronTrigger
# """

# #Flows are stored as metadata in:FlowDefinition
# #Flow names
# #Active version
# #does NOT show execution history.
# flowDefinition = """
# SELECT Id, DeveloperName, ActiveVersion.VersionNumber
# FROM FlowDefinition
# """

# #Flow execution logs are stored in:FlowInterview
# flowInterview = """
# SELECT Id, FlowVersionId, InterviewStatus, CreatedDate
# FROM FlowInterview
# """

# #Approval Processes :-ProcessInstance
# processInstance = """
# SELECT Id, Status, CreatedDate
# FROM ProcessInstance
# ORDER BY CreatedDate DESC
# LIMIT 10
# """

# query = query2

# result = sf.query(query)

# records = result["records"]

# # # Create table first time
# database_extract_jobs.create_table()

# for job in records:

#     flattened_job = {
#     "job_id": job.get("Id"),
#     "created_date": job.get("CreatedDate"),
#     "created_by_id": job.get("CreatedById"),
#     "created_by_name": (job.get("CreatedBy") or {}).get("Name"),
#     "job_type": job.get("JobType"),
#     "apex_class_id": job.get("ApexClassId"),
#     "apex_class_name": (job.get("ApexClass") or {}).get("Name"),
#     "status": job.get("Status"),
#     "job_items_processed": job.get("JobItemsProcessed"),
#     "total_job_items": job.get("TotalJobItems"),
#     "number_of_errors": job.get("NumberOfErrors"),
#     "completed_date": job.get("CompletedDate"),
#     "method_name": job.get("MethodName"),
#     "extended_status": job.get("ExtendedStatus"),
#     "parent_job_id": job.get("ParentJobId"),
#     "last_processed": job.get("LastProcessed"),
#     "last_processed_offset": job.get("LastProcessedOffset"),
#     "cron_trigger_id": job.get("CronTriggerId")
#     }
#     database_extract_jobs.insert_job(flattened_job)


# # print("Data inserted into SQLite database.")

# # print("Total Jobs:", len(records))

# # print("\nReading from Database:")
# # rows = database_extract_jobs.fetch_all_jobs()

# # for row in rows:
# #     print(row)


# # print("--------------------Record 1--------------------")
# # for job in records:
# #     print("--------------------")
# #     print("Job ID:", job.get("Id"))
# #     print("Type:", job.get("JobType"))
# #     print("Status:", job.get("Status"))

# # print("--------------------Record 2--------------------")
# # for job in records:
# #     print("--------------------")
# #     for key, value in job.items():
# #         if key != "attributes":   # Ignore Salesforce metadata
# #             print(f"{key}: {value}")
            
# # print("--------------------Record 3--------------------")
# # for i, job in enumerate(records, start=1):
# #     print(f"\n---- Record {i} ----")
# #     clean_record = {k: v for k, v in job.items() if k != "attributes"}
# #     print(json.dumps(clean_record, indent=4))

# rows = database_extract_jobs.fetch_all_jobs()

# for row in rows:
#     print(row)

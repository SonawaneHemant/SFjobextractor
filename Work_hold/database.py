# import sqlite3

# DB_NAME = "salesforce_jobs.db"

# def create_connection():
#     conn = sqlite3.connect(DB_NAME)
#     return conn

# def create_table():
#     conn = create_connection()
#     cursor = conn.cursor()

#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS async_apex_jobs (
#         db_id INTEGER PRIMARY KEY AUTOINCREMENT,
#     job_id TEXT,
#     created_date TEXT,
#     created_by TEXT,
#     job_type TEXT,
#     apex_class_id TEXT,
#     status TEXT,
#     job_items_processed INTEGER,
#     total_job_items INTEGER,
#     number_of_errors INTEGER,
#     completed_date TEXT,
#     extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#     )
#     """)

#     conn.commit()
#     conn.close()

# def insert_job(job):
#     conn = create_connection()
#     cursor = conn.cursor()

#     cursor.execute("""
#         INSERT INTO async_apex_jobs (
#             job_id,
#             created_date,
#             created_by,
#             job_type,
#             apex_class_id,
#             status,
#             job_items_processed,
#             total_job_items,
#             number_of_errors,
#             completed_date
#         ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#     """, (
#         job.get("Id"),
#         job.get("CreatedDate"),
#         job.get("CreatedById"),
#         job.get("JobType"),
#         job.get("ApexClassId"),
#         job.get("Status"),
#         job.get("JobItemsProcessed"),
#         job.get("TotalJobItems"),
#         job.get("NumberOfErrors"),
#         job.get("CompletedDate")
#     ))

#     conn.commit()
#     conn.close()

# def fetch_all_jobs():
#     conn = create_connection()
#     cursor = conn.cursor()

#     cursor.execute("SELECT * FROM async_apex_jobs")
#     rows = cursor.fetchall()

#     conn.close()
#     return rows
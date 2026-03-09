from datetime import datetime
import sqlite3

DB_NAME = "main_salesforce_jobs.db"

def create_connection():
    conn = sqlite3.connect(DB_NAME)
    # This converts rows to dictionary-style objects
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS async_Main_apex_jobs (
        db_id INTEGER PRIMARY KEY AUTOINCREMENT,
        job_id TEXT,
        created_date TEXT,
        created_by_id TEXT,
        created_by_name TEXT,
        job_type TEXT,
        apex_class_id TEXT,
        apex_class_name TEXT,
        status TEXT,
        job_items_processed INTEGER,
        total_job_items INTEGER,
        number_of_errors INTEGER,
        completed_date TEXT,
        method_name TEXT,
        extended_status TEXT,
        parent_job_id TEXT,
        last_processed TEXT,
        last_processed_offset INTEGER,
        cron_trigger_id TEXT,
        execution_time INTEGER,
        extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    
    # JOB TIME STATS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS job_time_stats (

        job_id TEXT PRIMARY KEY,

        job_count INTEGER,
        first_execution_time INTEGER,
        latest_execution_time INTEGER,
        average_execution_time REAL,
        max_execution_time INTEGER,
        min_execution_time INTEGER,

        first_seen TIMESTAMP,
        last_seen TIMESTAMP
    )
    """)

    # CURRENT JOB STATE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS current_job_state (

        job_id TEXT PRIMARY KEY,

        created_date TEXT,
        created_by_id TEXT,
        created_by_name TEXT,
        job_type TEXT,
        apex_class_id TEXT,
        apex_class_name TEXT,
        status TEXT,
        job_items_processed INTEGER,
        total_job_items INTEGER,
        number_of_errors INTEGER,
        completed_date TEXT,
        method_name TEXT,
        extended_status TEXT,
        parent_job_id TEXT,
        last_processed TEXT,
        last_processed_offset INTEGER,
        cron_trigger_id TEXT,

        execution_time INTEGER,
            job_count INTEGER,
            average_execution_time REAL,

        extracted_at TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

def insert_job(job):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO async_Main_apex_jobs (
            job_id,
            created_date,
            created_by_id,
            created_by_name,
            job_type,
            apex_class_id,
            apex_class_name,
            status,
            job_items_processed,
            total_job_items,
            number_of_errors,
            completed_date,
            method_name,
            extended_status,
            parent_job_id,
            last_processed,
            last_processed_offset,
            cron_trigger_id,
            execution_time
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?)
    """, (
        job.get("job_id"),
        job.get("created_date"),
        job.get("created_by_id"),
        job.get("created_by_name"),
        job.get("job_type"),
        job.get("apex_class_id"),
        job.get("apex_class_name"),
        job.get("status"),
        job.get("job_items_processed"),
        job.get("total_job_items"),
        job.get("number_of_errors"),
        job.get("completed_date"),
        job.get("method_name"),
        job.get("extended_status"),
        job.get("parent_job_id"),
        job.get("last_processed"),
        job.get("last_processed_offset"),
        job.get("cron_trigger_id"),
        job.get("execution_time")
    ))

    conn.commit()
    conn.close()



def fetch_all_jobs():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM async_Main_apex_jobs")
    rows = cursor.fetchall()

    conn.close()
    return rows

def fetch_all_current_jobs():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM current_job_state")
    rows = cursor.fetchall()

    conn.close()
    return rows


def get_job_metrics():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            COUNT(*) as total_jobs,
            SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) as completed,
            SUM(CASE WHEN status = 'Failed' THEN 1 ELSE 0 END) as failed,
            SUM(number_of_errors) as total_errors
        FROM current_job_state
    """)

    result = cursor.fetchone()

    conn.close()

    return {
        "total_jobs": result[0] or 0,
        "completed": result[1] or 0,
        "failed": result[2] or 0,
        "total_errors": result[3] or 0
    }

def get_failed_jobs():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT job_id, job_type, apex_class_name, extended_status, number_of_errors
        FROM current_job_state 
        WHERE status = 'Failed'
        ORDER BY created_date DESC
        LIMIT 10
    """)

    rows = cursor.fetchall()
    conn.close()

    failed_jobs = []

    for row in rows:
        failed_jobs.append({
            "job_id": row[0],
            "job_type": row[1],
            "apex_class_name": row[2],
            "extended_status": row[3],
            "number_of_errors": row[4]
        })

    return failed_jobs

def get_all_failed_jobs():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT job_id, job_type, apex_class_name, extended_status, number_of_errors
        FROM async_Main_apex_jobs 
        WHERE status = 'Failed'
        ORDER BY created_date DESC
        LIMIT 10
    """)

    rows = cursor.fetchall()
    conn.close()

    failed_jobs = []

    for row in rows:
        failed_jobs.append({
            "job_id": row[0],
            "job_type": row[1],
            "apex_class_name": row[2],
            "extended_status": row[3],
            "number_of_errors": row[4]
        })

    return failed_jobs

def get_job_by_id(job_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT *
        FROM current_job_state
        WHERE job_id = ?
    """, (job_id,))
    row = cursor.fetchone()
    conn.close()
    # if not row:
    #     return None
    # return {
    #     "job_id": row[1],
    #     "created_date": row[2],
    #     "created_by_name": row[4],
    #     "job_type": row[5],
    #     "apex_class_name": row[7],
    #     "status": row[8],
    #     "job_items_processed": row[9],
    #     "total_job_items": row[10],
    #     "number_of_errors": row[11],
    #     "extended_status": row[14]
    # }
    if not row:
        return None

    # Convert sqlite Row object to dictionary
    return dict(row)

def update_job_time_stats(job_id, execution_time):

    if execution_time is None:
        return

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM job_time_stats WHERE job_id = ?", (job_id,)
    )

    row = cursor.fetchone()

    if not row:

        cursor.execute("""
        INSERT INTO job_time_stats (
            job_id,
            job_count,
            first_execution_time,
            latest_execution_time,
            average_execution_time,
            max_execution_time,
            min_execution_time,
            first_seen,
            last_seen
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        """,
        (
            job_id,
            1,
            execution_time,
            execution_time,
            execution_time,
            execution_time,
            execution_time
        ))

    else:

        # Convert NULL values to 0 safely
        job_count = (row[1] or 0) + 1
        avg_time = row[4] or 0
        max_time = row[5] or execution_time
        min_time = row[6] or execution_time

        new_avg = ((avg_time * (job_count - 1)) + execution_time) / job_count

        cursor.execute("""
        UPDATE job_time_stats
        SET job_count=?,
            latest_execution_time=?,
            average_execution_time=?,
            max_execution_time=?,
            min_execution_time=?,
            last_seen=CURRENT_TIMESTAMP
        WHERE job_id=?
        """,
        (
            job_count,
            execution_time,
            new_avg,
            max(max_time, execution_time),
            min(min_time, execution_time),
            job_id
        ))

    conn.commit()
    conn.close()

def calculate_execution_time(created_date, completed_date):

    if not created_date or not completed_date:
        return None

    try:
        start = datetime.fromisoformat(created_date.replace("Z","+00:00"))
        end = datetime.fromisoformat(completed_date.replace("Z","+00:00"))

        return int((end - start).total_seconds())

    except:
        return None

def update_current_job_state(job):

    conn = create_connection()
    cursor = conn.cursor()

     # Get job statistics
    cursor.execute("""
        SELECT job_count, average_execution_time
        FROM job_time_stats
        WHERE job_id = ?
    """, (job.get("job_id"),))

    stats = cursor.fetchone()

    job_count = None
    avg_execution_time = None

    if stats:
        job_count = stats[0]
        avg_execution_time = stats[1]

    cursor.execute("""
    INSERT INTO current_job_state (

        job_id,
        created_date,
        created_by_id,
        created_by_name,
        job_type,
        apex_class_id,
        apex_class_name,
        status,
        job_items_processed,
        total_job_items,
        number_of_errors,
        completed_date,
        method_name,
        extended_status,
        parent_job_id,
        last_processed,
        last_processed_offset,
        cron_trigger_id,
        execution_time,
        job_count,
        average_execution_time,
        extracted_at

    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)

    ON CONFLICT(job_id) DO UPDATE SET

        created_date=excluded.created_date,
        created_by_id=excluded.created_by_id,
        created_by_name=excluded.created_by_name,
        job_type=excluded.job_type,
        apex_class_id=excluded.apex_class_id,
        apex_class_name=excluded.apex_class_name,
        status=excluded.status,
        job_items_processed=excluded.job_items_processed,
        total_job_items=excluded.total_job_items,
        number_of_errors=excluded.number_of_errors,
        completed_date=excluded.completed_date,
        method_name=excluded.method_name,
        extended_status=excluded.extended_status,
        parent_job_id=excluded.parent_job_id,
        last_processed=excluded.last_processed,
        last_processed_offset=excluded.last_processed_offset,
        cron_trigger_id=excluded.cron_trigger_id,
        execution_time=excluded.execution_time,
        job_count=excluded.job_count,
        average_execution_time=excluded.average_execution_time,
        extracted_at=CURRENT_TIMESTAMP
    """,

    (
        job.get("job_id"),
        job.get("created_date"),
        job.get("created_by_id"),
        job.get("created_by_name"),
        job.get("job_type"),
        job.get("apex_class_id"),
        job.get("apex_class_name"),
        job.get("status"),
        job.get("job_items_processed"),
        job.get("total_job_items"),
        job.get("number_of_errors"),
        job.get("completed_date"),
        job.get("method_name"),
        job.get("extended_status"),
        job.get("parent_job_id"),
        job.get("last_processed"),
        job.get("last_processed_offset"),
        job.get("cron_trigger_id"),
        job.get("execution_time"),
        job_count,
        avg_execution_time
    ))

    conn.commit()
    conn.close()
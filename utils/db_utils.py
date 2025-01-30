import sqlite3

def init_db():
    conn = sqlite3.connect('app_database.db')
    cursor = conn.cursor()  # Initialize cursor here

    # Create jobs table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL
        );
    """)

    # Create job_applications table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS job_applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id INTEGER NOT NULL,
            applicant_name TEXT NOT NULL,
            resume_text TEXT,
            matching_score REAL NOT NULL,
            FOREIGN KEY (job_id) REFERENCES jobs(id)
        );
    """)

    conn.commit()
    return conn

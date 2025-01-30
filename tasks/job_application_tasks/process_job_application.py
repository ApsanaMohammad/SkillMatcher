
def process_job_application(conn, applicant_name, job_id, matching_score):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO job_applications (job_id, applicant_name, matching_score)
        VALUES (?, ?, ?)
    """, (job_id, applicant_name, matching_score))
    conn.commit()

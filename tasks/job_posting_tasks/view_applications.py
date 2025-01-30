def view_applications(db_connection, job_id):
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM applicants WHERE job_id = ? ORDER BY matching_score ASC", (job_id,))
    return cursor.fetchall()

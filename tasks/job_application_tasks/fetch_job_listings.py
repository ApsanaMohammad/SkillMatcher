def fetch_job_listings(db_connection, job_id):
    query = "SELECT * FROM jobs WHERE id = ?"
    cursor = db_connection.cursor()
    cursor.execute(query, (job_id,))
    return cursor.fetchall()

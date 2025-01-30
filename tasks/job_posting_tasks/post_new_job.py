def post_new_job(db_connection, job_id, job_title, job_description):
    cursor = db_connection.cursor()
    cursor.execute("INSERT INTO jobs (id, title, description) VALUES (?, ?, ?)", (job_id, job_title, job_description))
    db_connection.commit()

def update_job_post(db_connection, job_id, new_title, new_description):
    cursor = db_connection.cursor()
    cursor.execute("UPDATE jobs SET title = ?, description = ? WHERE id = ?", (new_title, new_description, job_id))
    db_connection.commit()

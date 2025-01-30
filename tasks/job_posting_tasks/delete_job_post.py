def delete_job_post(db_connection, job_id):
    cursor = db_connection.cursor()
    cursor.execute("DELETE FROM jobs WHERE id = ?", (job_id,))
    db_connection.commit()

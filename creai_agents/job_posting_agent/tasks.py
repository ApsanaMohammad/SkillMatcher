from tasks.job_posting_tasks import post_new_job, update_job_post, delete_job_post, view_applications

def handle_job_posting(db_connection, job_id, job_title, job_description):
    post_new_job(db_connection, job_id, job_title, job_description)

def handle_update_job(db_connection, job_id, new_title, new_description):
    update_job_post(db_connection, job_id, new_title, new_description)

def handle_delete_job(db_connection, job_id):
    delete_job_post(db_connection, job_id)

def handle_view_applications(db_connection, job_id):
    return view_applications(db_connection, job_id)

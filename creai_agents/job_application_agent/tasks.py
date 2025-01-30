from tasks.job_application_tasks import fetch_job_listings, compute_matching_score, process_job_application

def handle_job_application(db_connection, applicant_name, resume_text, job_id):
    job_desc = fetch_job_listings(db_connection, job_id)
    matching_score = compute_matching_score(resume_text, job_desc)
    process_job_application(db_connection, applicant_name, resume_text, job_id, matching_score)

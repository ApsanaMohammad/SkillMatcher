from tasks.job_posting_tasks import post_new_job, update_job_post, delete_job_post, view_applications

class JobPostingAgent:
    def __init__(self, db_connection):
        self.db_connection = db_connection
    
    def post_job(self, job_id, job_title, job_description):
        post_new_job(self.db_connection, job_id, job_title, job_description)
    
    def update_job(self, job_id, new_title, new_description):
        update_job_post(self.db_connection, job_id, new_title, new_description)
    
    def delete_job(self, job_id):
        delete_job_post(self.db_connection, job_id)
    
    def view_applications(self, job_id):
        return view_applications(self.db_connection, job_id)

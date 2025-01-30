
from tasks.job_application_tasks import compute_matching_score,fetch_job_listings,process_job_application
class JobApplicationAgent:
    def __init__(self, db_connection):
        self.db_connection = db_connection
    
    def handle_application(self, applicant_name, matching_score, job_id):
        # Fetch job description from the job listings using the job_id
        job_desc = self.fetch_job_description(job_id)
        
        # Process the job application with the applicant details, job ID, and matching score
        self.process_application(applicant_name, matching_score, job_id)
    
    def fetch_job_description(self, job_id):
        # Fetch job description from the database using the job_id
        return fetch_job_listings(self.db_connection, job_id)
    
    def process_application(self, applicant_name, matching_score, job_id):
        # Store the application in the database, along with the matching score
        process_job_application(self.db_connection, applicant_name, matching_score, job_id)

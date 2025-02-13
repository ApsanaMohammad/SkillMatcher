# Skill Matcher

Skill Matcher is a web-based platform built using Streamlit, Python, and NLP techniques. It allows job applicants to upload their resumes and match their skills with job postings based on similarity scores. Employers can post jobs, update or delete listings, and view applicant data.

## Features

### For Job Applicants:
- Upload resumes in PDF format.
- Extract text from the resume and preprocess it.
- Match skills with job descriptions using NLP-based similarity computation.
- Apply for job listings and track applications.

### For Employers:
- Post job opportunities with job ID, title, and description.
- Update or delete job postings.
- View applicants and their similarity scores.
- Visualize matching scores and experience distribution using Altair charts.

## Technologies Used
- **Frontend:** Streamlit (for UI)
- **Backend:** Python
- **Database:** SQLite (via `db_utils` module)
- **NLP Processing:** Custom preprocessing (`nlp_utils` module)
- **Data Visualization:** Altair
- **PDF Parsing:** PyPDF2

## Installation & Setup

1. Clone the repository:
   ```sh
   git clone https://github.com/your-repo/skill-matcher.git
   cd skill-matcher
   ```

2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

3. Run the application:
   ```sh
   streamlit run app.py
   ```

## Project Structure
```
skill-matcher/
│-- app.py                  # Main Streamlit app
│-- utils/
│   │-- db_utils.py         # Database initialization & queries
│   │-- nlp_utils.py        # NLP preprocessing & similarity computation
│-- requirements.txt        # Required Python packages
│-- README.md               # Project documentation
```

## Usage
### Job Applicant Portal
1. Navigate to the "Job Applicant" section.
2. Enter your name and upload your resume.
3. Once the profile is set up, view available job listings.
4. Click "Apply" to submit your application for a job.

### Job Posting Portal
1. Navigate to the "Job Posting" section.
2. Post a new job with title and description.
3. Update or delete existing job postings.
4. View applicants and analyze their matching scores & experience.

## Contribution
1. Fork the repository and create a feature branch.
2. Make changes and commit with proper messages.
3. Create a pull request with details about the changes.



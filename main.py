import streamlit as st
from utils.db_utils import init_db
from creai_agents.job_application_agent.agent import JobApplicationAgent
from creai_agents.job_posting_agent.agent import JobPostingAgent
from PyPDF2 import PdfReader
import pandas as pd
import altair as alt
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

# Initialize database connection
conn = init_db()

# Initialize agents
job_application_agent = JobApplicationAgent(conn)
job_posting_agent = JobPostingAgent(conn)

# Sidebar navigation
st.sidebar.title("Skill Matcher Platform")
page = st.sidebar.radio("Navigate", ["Job Applicant", "Job Posting"])

# Global variables for session state
if "profile_set" not in st.session_state:
    st.session_state["profile_set"] = False
    st.session_state["applicant_name"] = ""
    st.session_state["resume_text"] = ""

# Function to calculate resume matching score
def calculate_matching_score(resume_text, job_description):
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform([resume_text, job_description])
    similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])
    return similarity_matrix[0][0]

# Job Applicant Page
if page == "Job Applicant":
    st.title("Job Applicant Portal")
    st.subheader("Set up your profile once")

    if not st.session_state["profile_set"]:
        st.warning("Please set up your profile below before applying for jobs!")
        applicant_name = st.text_input("Your Name")
        uploaded_resume = st.file_uploader("Upload Resume (PDF only)", type=["pdf"])

        if st.button("Save Profile"):
            if applicant_name.strip() and uploaded_resume:
                try:
                    pdf_reader = PdfReader(uploaded_resume)
                    resume_text = " ".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])
                    
                    if not resume_text.strip():
                        st.error("Unable to extract text from the uploaded PDF. Please upload a valid resume.")
                    else:
                        st.session_state["profile_set"] = True
                        st.session_state["applicant_name"] = applicant_name
                        st.session_state["resume_text"] = resume_text
                        st.success("Profile saved successfully!")
                except Exception as e:
                    st.error(f"An error occurred while processing your resume: {e}")
            else:
                st.error("Please fill in your name and upload a valid resume.")

    if st.session_state["profile_set"]:
        st.subheader("Available Job Listings")
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, description FROM jobs")
        jobs = cursor.fetchall()
        cursor.close()

        if jobs:
            for job in jobs:
                with st.container():
                    st.markdown(f"""
                    <div style="border: 1px solid #ddd; border-radius: 10px; padding: 10px;">
                    <h3>{job[1]}</h3>
                    <p style="margin: 5px 0;">{job[2][:100]}...</p>
                    <p><strong>Job ID:</strong> {job[0]}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"Apply for {job[1]}", key=f"apply-{job[0]}"):
                        matching_score = calculate_matching_score(st.session_state["resume_text"], job[2])
                        matching_score = min(max(matching_score, 0), 1)
                        job_application_agent.handle_application(st.session_state["applicant_name"], job[0], matching_score)
                        st.success(f"Application submitted for {job[1]} with a matching score of {matching_score:.2f}")
        else:
            st.warning("No job listings available at the moment.")

# Job Posting Page
elif page == "Job Posting":
    st.title("Job Posting Portal")
    st.subheader("Post, update, or delete jobs")

    job_post_option = st.radio("Select Action", ["Post a Job", "Update Job", "Delete Job", "View Applications"])

    if job_post_option == "Post a Job":
        job_title = st.text_input("Job Title")
        job_description = st.text_area("Job Description")
        job_id = st.number_input("Job ID", min_value=1)

        if st.button("Post Job"):
            job_posting_agent.post_job(job_id, job_title, job_description)
            st.success("Job posted successfully!")

    elif job_post_option == "Update Job":
        job_id_to_update = st.number_input("Enter Job ID to update", min_value=1)
        new_title = st.text_input("New Job Title")
        new_description = st.text_area("New Job Description")

        if st.button("Update Job"):
            job_posting_agent.update_job(job_id_to_update, new_title, new_description)
            st.success("Job updated successfully!")

    elif job_post_option == "Delete Job":
        job_id_to_delete = st.number_input("Enter Job ID to delete", min_value=1)
        if st.button("Delete Job"):
            job_posting_agent.delete_job(job_id_to_delete)
            st.success("Job deleted successfully!")

    elif job_post_option == "View Applications":
        st.subheader("View Applications and Resume Matching Scores")

        job_id_filter = st.number_input("Enter Job ID to filter applications", min_value=1, value=1)
        cursor = conn.cursor()
        cursor.execute("SELECT job_id, applicant_name, matching_score FROM job_applications WHERE job_id = ?", (job_id_filter,))
        applications = cursor.fetchall()
        cursor.close()

        if applications:
            df_applications = pd.DataFrame(applications, columns=["Job ID", "Applicant Name", "Matching Score"])
            st.write(df_applications)

            if not df_applications.empty:
                bar_chart = alt.Chart(df_applications).mark_bar().encode(
                    x='Applicant Name:N',
                    y='Matching Score:Q',
                    color='Matching Score:Q',
                    tooltip=['Applicant Name', 'Matching Score']
                ).properties(
                    title=f"Resume Matching Scores for Job ID {job_id_filter}"
                )
                st.altair_chart(bar_chart, use_container_width=True)
        else:
            st.warning(f"No applications received yet for Job ID {job_id_filter}.")

import streamlit as st
from utils.db_utils import init_db
from utils.nlp_utils import preprocess_text, compute_similarity
import pandas as pd
from PyPDF2 import PdfReader
import altair as alt

# Initialize Database
conn = init_db()

# Sidebar Navigation
st.sidebar.title("Skill Matcher Platform")
page = st.sidebar.radio("Navigate", ["Job Applicant", "Job Posting"])

# Global variables for session state
if "profile_set" not in st.session_state:
    st.session_state["profile_set"] = False
    st.session_state["applicant_name"] = ""
    st.session_state["resume_text"] = ""

# Job Applicant Page
if page == "Job Applicant":
    st.title("Job Applicant Portal")
    st.subheader("Set up your profile once")

    # Profile setup section
    if not st.session_state["profile_set"]:
        st.warning("Please set up your profile below before applying for jobs!")
        applicant_name = st.text_input("Your Name")
        uploaded_resume = st.file_uploader("Upload Resume (PDF only)", type=["pdf"])

        if st.button("Save Profile"):
            if applicant_name.strip() and uploaded_resume:
                try:
                    # Extract text from resume PDF
                    pdf_reader = PdfReader(uploaded_resume)
                    resume_text = " ".join(
                        [page.extract_text() for page in pdf_reader.pages if page.extract_text()]
                    )

                    if not resume_text.strip():
                        st.error("Unable to extract text from the uploaded PDF. Please upload a valid resume.")
                    else:
                        # Save to session state
                        st.session_state["profile_set"] = True
                        st.session_state["applicant_name"] = applicant_name
                        st.session_state["resume_text"] = resume_text
                        st.success("Profile saved successfully!")
                except Exception as e:
                    st.error(f"An error occurred while processing your resume: {e}")
            else:
                st.error("Please fill in your name and upload a valid resume.")

    # Job listings and application section
    if st.session_state["profile_set"]:
        st.subheader("Available Job Listings")

        # Fetch jobs from the database
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, description FROM jobs")
        jobs = cursor.fetchall()

        if jobs:
            for job in jobs:
                with st.container():
                    st.markdown(f"""
                    <div style="border: 1px solid #ddd; border-radius: 10px; padding: 10px; margin-bottom: 15px; background-color: #f9f9f9;">
                        <h4 style="margin: 0;">{job[1]}</h4>
                        <p style="margin: 5px 0;">{job[2][:100]}...</p>
                        <p><strong>Job ID:</strong> {job[0]}</p>
                    </div>
                    """, unsafe_allow_html=True)

                    # Apply button for each job
                    if st.button(f"Apply for Job ID {job[0]}", key=f"apply_{job[0]}"):
                        try:
                            # Fetch job description
                            cursor.execute("SELECT description FROM jobs WHERE id = ?", (job[0],))
                            job_desc = cursor.fetchone()
                            if job_desc:
                                job_desc = job_desc[0]
                            else:
                                st.error("Failed to fetch the job description. Please try again later.")
                                continue

                            # Compute similarity score
                            matching_score = compute_similarity(
                                preprocess_text(job_desc), preprocess_text(st.session_state["resume_text"])
                            )

                            # Insert application into the database
                            cursor.execute(
                                """
                                INSERT INTO applicants (name, resume, job_id, matching_score, experience)
                                VALUES (?, ?, ?, ?, ?)
                                """,
                                (
                                    st.session_state["applicant_name"],
                                    st.session_state["resume_text"],
                                    job[0],
                                    matching_score,
                                    0,  # Experience placeholder
                                ),
                            )
                            conn.commit()
                            st.success(f"Application for Job ID {job[0]} submitted successfully!")
                        except Exception as e:
                            st.error(f"An error occurred while processing your application: {e}")
        else:
            st.warning("No jobs available at the moment.")

# Job Posting Page
# Inside the Job Posting Page
elif page == "Job Posting":
    st.title("Job Posting Portal")
    st.subheader("Post a New Job")

    job_id = st.number_input("Job ID (Set Manually)", min_value=1, step=1)
    job_title = st.text_input("Job Title")
    job_description = st.text_area("Job Description")

    if st.button("Post Job"):
        cursor = conn.cursor()  # Ensure cursor is defined here
        cursor.execute("INSERT INTO jobs (id, title, description) VALUES (?, ?, ?)", (job_id, job_title, job_description))
        conn.commit()
        st.success(f"Job posted successfully with Job ID: {job_id}!")

    st.subheader("Update or Delete Job Postings")
    job_id_to_modify = st.number_input("Enter Job ID to Modify", min_value=1, step=1)

    if st.button("Delete Job"):
        cursor = conn.cursor()  # Ensure cursor is defined here
        cursor.execute("DELETE FROM jobs WHERE id = ?", (job_id_to_modify,))
        conn.commit()
        st.success(f"Job ID {job_id_to_modify} deleted successfully!")

    if st.button("Update Job"):
        new_title = st.text_input("New Job Title", key="update_title")
        new_description = st.text_area("New Job Description", key="update_description")
        if st.button("Save Updates", key="save_update"):
            cursor = conn.cursor()  # Ensure cursor is defined here
            cursor.execute(
                "UPDATE jobs SET title = ?, description = ? WHERE id = ?",
                (new_title, new_description, job_id_to_modify),
            )
            conn.commit()
            st.success(f"Job ID {job_id_to_modify} updated successfully!")

    st.subheader("View Applications by Job")
    job_id_filter = st.number_input("Enter Job ID to View Applicants", min_value=1, step=1)

    if st.button("Show Applications"):
        cursor = conn.cursor()  # Ensure cursor is defined here
        cursor.execute("SELECT * FROM applicants WHERE job_id = ? ORDER BY matching_score ASC", (job_id_filter,))
        applicants = cursor.fetchall()

        if applicants:
            df = pd.DataFrame(applicants, columns=["ID", "Name", "Resume", "Job ID", "Matching Score", "Experience"])
            st.dataframe(df)
            st.info(f"Number of applicants for Job ID {job_id_filter}: {len(applicants)}")

            # Bar chart for Matching Score
            st.subheader("Matching Score Distribution")
            score_chart = alt.Chart(df).mark_bar().encode(
                x=alt.X("Name:N", sort=None),
                y="Matching Score:Q",
                tooltip=["Name", "Matching Score"],
            )
            st.altair_chart(score_chart, use_container_width=True)

            # Bar chart for Experience
            st.subheader("Experience Distribution")
            exp_chart = alt.Chart(df).mark_bar().encode(
                x=alt.X("Name:N", sort=None),
                y="Experience:Q",
                tooltip=["Name", "Experience"],
            )
            st.altair_chart(exp_chart, use_container_width=True)
        else:
            st.warning("No applications found for this job.")
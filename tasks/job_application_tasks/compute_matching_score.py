from utils.nlp_utils import preprocess_text, compute_similarity

def compute_matching_score(resume_text, job_desc):
    return compute_similarity(preprocess_text(job_desc), preprocess_text(resume_text))

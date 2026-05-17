from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer('all-MiniLM-L6-v2')


def compute_similarity(text1, text2):
    emb1 = model.encode([text1])
    emb2 = model.encode([text2])

    return float(cosine_similarity(emb1, emb2)[0][0] * 100)


def skill_match(resume_skills, job_skills):

    if not job_skills:
        return 0, []

    matched = list(set(resume_skills) & set(job_skills))
    missing = list(set(job_skills) - set(resume_skills))

    score = (len(matched) / len(job_skills)) * 100

    return float(score), missing


def final_score(similarity, skill_score):

    return (0.7 * similarity) + (0.3 * skill_score)
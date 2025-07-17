# utils/scoring.py

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer, util

def load_st_model(model_name: str = "all-MiniLM-L6-v2") -> SentenceTransformer:
    """
    Load a sentence transformer model.
    """
    return SentenceTransformer(model_name)


def compute_tfidf_score(resume_text: str, jd_text: str) -> float:
    """
    Compute TF-IDF cosine similarity score between resume and job description.
    """
    vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 3))
    vectors = vectorizer.fit_transform([resume_text, jd_text])
    return cosine_similarity(vectors[0], vectors[1])[0][0] * 100


def compute_skill_score(resume_skills: list, jd_skills: list) -> float:
    """
    Calculate skill match percentage.
    """
    if not jd_skills:
        return 0.0
    matched = set(jd_skills).intersection(set(resume_skills))
    return len(matched) / len(jd_skills) * 100


def compute_semantic_similarity(resume_text: str, jd_text: str, st_model: SentenceTransformer) -> float:
    """
    Compute semantic similarity using a SentenceTransformer model.
    """
    emb_resume = st_model.encode(resume_text, convert_to_tensor=True)
    emb_jd = st_model.encode(jd_text, convert_to_tensor=True)
    return util.cos_sim(emb_resume, emb_jd).item() * 100


def hybrid_score_tfidf_st(
    resume_text: str,
    jd_text: str,
    resume_skills: list,
    jd_skills: list,
    st_model: SentenceTransformer
) -> float:
    """
    Calculate a hybrid score based on semantic, TF-IDF, and skill match.
    Weights: 0.5 (Semantic) + 0.3 (TF-IDF) + 0.2 (Skill Match)
    """
    tfidf_score = compute_tfidf_score(resume_text, jd_text)
    skill_score = compute_skill_score(resume_skills, jd_skills)
    st_score = compute_semantic_similarity(resume_text, jd_text, st_model)

    final_score = 0.5 * st_score + 0.3 * tfidf_score + 0.2 * skill_score
    return round(final_score, 2)

# utils/scoring.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer, util

def load_st_model(model_name):
    return SentenceTransformer(model_name)

def hybrid_score_tfidf_st(resume_text, jd_text, resume_skills, jd_skills, st_model):
    # TF-IDF
    vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1,3))
    vectors = vectorizer.fit_transform([resume_text, jd_text])
    tfidf_score = cosine_similarity(vectors[0], vectors[1])[0][0]*100

    # Skills overlap
    matched = set(jd_skills).intersection(set(resume_skills))
    skill_score = (len(matched)/len(jd_skills)*100) if jd_skills else 0

    # Semantic similarity
    emb_resume = st_model.encode(resume_text, convert_to_tensor=True)
    emb_jd = st_model.encode(jd_text, convert_to_tensor=True)
    st_score = util.cos_sim(emb_resume, emb_jd).item()*100

    # Combine
    final = 0.5*st_score + 0.3*tfidf_score + 0.2*skill_score
    return round(final,2)

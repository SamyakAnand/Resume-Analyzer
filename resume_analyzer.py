import streamlit as st
import pandas as pd
import tempfile
from pdfminer.high_level import extract_text
from docx import Document
import re
import nltk
from nltk import word_tokenize, pos_tag, ne_chunk
from nltk.tree import Tree
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ✅ Download once if needed
# nltk.download('punkt')
# nltk.download('maxent_ne_chunker')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('words')

# --- Load dataset ---
@st.cache_data
def load_job_roles():
    try:
        return pd.read_csv('IT_Job_Roles_Skills.csv', encoding='utf-8')
    except UnicodeDecodeError:
        return pd.read_csv('IT_Job_Roles_Skills.csv', encoding='latin1')

job_roles_df = load_job_roles()

# --- Extract text from files ---
def extract_text_from_pdf(pdf_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
        tmp.write(pdf_file.read())
        text = extract_text(tmp.name)
    return text

def extract_text_from_docx(docx_file):
    doc = Document(docx_file)
    return "\n".join([p.text for p in doc.paragraphs])

# --- Better name extraction (ignore titles) ---
def extract_name(text):
    lines = text.strip().split('\n')
    ignore_titles = {
        'Data Scientist', 'Machine Learning Engineer', 'AI Engineer',
        'Artificial Intelligence Architect', 'Big Data Engineer',
        'AI Researcher', 'Data Analyst', 'Software Engineer'
    }
    for line in lines[:5]:
        clean_line = line.strip()
        if not clean_line or clean_line in ignore_titles:
            continue
        tokens = word_tokenize(clean_line)
        if all(token[0].isupper() and token.isalpha() for token in tokens):
            return clean_line
    # fallback: NLTK
    tokens = word_tokenize(text)
    tags = pos_tag(tokens)
    chunks = ne_chunk(tags, binary=False)
    for chunk in chunks:
        if isinstance(chunk, Tree) and chunk.label() == 'PERSON':
            return ' '.join(c[0] for c in chunk.leaves())
    return None

# --- Extract basic info ---
def extract_basic_info(text):
    name = extract_name(text)
    email_match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    phone_match = re.search(r"(\+\d{1,3}[-.\s]?)?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}", text)
    return {
        "name": name,
        "email": email_match.group() if email_match else None,
        "phone": phone_match.group() if phone_match else None
    }

# --- Resume vs JD similarity ---
def match_resume_to_jd(resume_text, jd_text):
    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform([resume_text, jd_text])
    return round(cosine_similarity(vectors[0], vectors[1])[0][0] * 100, 2)

# --- Streamlit App ---
def main():
    st.set_page_config(page_title="Automated Resume Analyzer", layout="wide")
    st.title("📄 Automated Resume Analyzer (Single or Batch, Scored & Sorted)")

    # --- Select job role ---
    job_titles = job_roles_df['Job Title'].unique().tolist()
    selected_job = st.selectbox("Select Job Role to match against:", job_titles)

    # Load skills for info (we won’t use them to score now, but can show later)
    selected_row = job_roles_df[job_roles_df['Job Title'] == selected_job].iloc[0]
    skill_list = selected_row['Skills'].split(',') if pd.notna(selected_row['Skills']) else []

    # Upload resumes
    uploaded_files = st.file_uploader("Upload one or multiple resumes (PDF/DOCX)", type=["pdf", "docx"], accept_multiple_files=True)

    # JD text
    jd_text = st.text_area("Paste the Job Description here (required to calculate score)")

    analyze = st.button("Analyze")

    if analyze:
        if not jd_text.strip():
            st.warning("⚠ Please paste the Job Description text to calculate scores.")
        elif not uploaded_files:
            st.warning("⚠ Please upload at least one resume.")
        else:
            results = []

            for file in uploaded_files:
                filename = file.name
                if filename.lower().endswith(".pdf"):
                    text = extract_text_from_pdf(file)
                elif filename.lower().endswith(".docx"):
                    text = extract_text_from_docx(file)
                else:
                    st.warning(f"Unsupported file type: {filename}")
                    continue

                info = extract_basic_info(text)
                jd_score = match_resume_to_jd(text, jd_text)

                results.append({
                    "filename": filename,
                    "name": info.get("name"),
                    "email": info.get("email"),
                    "phone": info.get("phone"),
                    "score (%)": jd_score
                })

            # Sort by score descending
            results_df = pd.DataFrame(results).sort_values(by="score (%)", ascending=False)

            st.subheader(f"📊 Results (Top scoring first):")
            st.dataframe(results_df, use_container_width=True)

    st.markdown("---")
    st.caption("Built with ❤️ using Python, NLTK, pandas, and Streamlit.")

if __name__ == "__main__":
    main()

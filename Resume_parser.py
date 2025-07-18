# Import all required libraries
import streamlit as st  # For building the UI
import os
import tempfile  # Used to temporarily store uploaded files
import re  # For text pattern matching
from datetime import datetime
from calendar import month_abbr  # For converting month names to numbers
from docx import Document  # To extract text from .docx files
from pdfminer.high_level import extract_text as extract_pdf  # To extract text from PDFs
from nltk.corpus import stopwords  # English stopwords (e.g., "the", "is", etc.)
from nltk import download  # Downloads missing NLTK resources
from sentence_transformers import SentenceTransformer, util  # Semantic similarity
from sklearn.feature_extraction.text import TfidfVectorizer  # TF-IDF vectorizer
from sklearn.metrics.pairwise import cosine_similarity  # Cosine similarity
import pandas as pd  # Data manipulation and display

# Load English stopwords (download if not found)
try:
    STOPWORDS = set(stopwords.words('english'))
except:
    download('stopwords')
    STOPWORDS = set(stopwords.words('english'))

# Load SentenceTransformer model once using Streamlit cache
@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

st_model = load_model()

# Extract text from PDF file
def extract_text_from_pdf(file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(file.read())
        tmp_path = tmp.name
    try:
        return extract_pdf(tmp_path)
    finally:
        os.unlink(tmp_path)

# Extract text from DOCX file
def extract_text_from_docx(file):
    doc = Document(file)
    return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])

# Clean text by lowering case and removing extra spaces
def clean_text(text):
    return re.sub(r'\s+', ' ', text.lower()).strip()

# Load predefined skills from a text file
def load_skills(path='skills.txt'):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return [line.strip().lower() for line in f if line.strip()]
    except:
        return []

# Extract basic info: Name, Email, Phone from resume text
def extract_basic_info(text):
    name, email, phone = '', '', ''
    lines = text.strip().split('\n')
    for line in lines:
        line = line.strip()
        if name == '' and re.match(r'^[a-zA-Z\s]{2,30}$', line):
            name = line.title()
        if not email:
            match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", line)
            if match: email = match.group()
        if not phone:
            match = re.search(r'\+?\d[\d\s\-\(\)]{7,}', line)
            if match: phone = match.group()
    return {'name': name, 'email': email, 'phone': phone}

# Extract matching skills from resume using given skills list
def extract_skills(text, skills_list):
    text = text.lower()
    found = []
    for skill in skills_list:
        if re.search(r'\b' + re.escape(skill) + r'\b', text):
            found.append(skill)
    return list(set(found))

# Extract education qualification
def extract_education(text):
    edu_patterns = [
        r"(bachelor|b\.tech|b\.sc|m\.sc|m\.tech|master|ph\.d|mba|bca|mca|diploma)\s*(of|in)?\s*[\w\s,]*",
    ]
    for pattern in edu_patterns:
        match = re.search(pattern, text.lower())
        if match:
            return match.group().title()
    return "Not Found"

# Calculate years of experience from dates in text
def extract_experience_years(text):
    date_patterns = [
        r"((jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*[\s\-]*\d{4})\s*(to|-|–)\s*((jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*[\s\-]*\d{4}|present)",
        r"(\d{4})\s*(to|-|–)\s*(\d{4}|present)"
    ]
    total_months = 0
    for pattern in date_patterns:
        matches = re.findall(pattern, text.lower())
        for match in matches:
            start = match[0]
            end = match[-1]
            s_date = parse_date(start)
            e_date = parse_date(end) if 'present' not in end else datetime.now()
            if s_date and e_date:
                months = (e_date.year - s_date.year) * 12 + (e_date.month - s_date.month)
                if months > 0:
                    total_months += months
    return round(total_months / 12, 1)

# Helper function to convert date string to datetime object
def parse_date(date_str):
    try:
        date_str = date_str.lower()
        month_map = {m.lower(): i for i, m in enumerate(month_abbr) if m}
        for name, num in month_map.items():
            if name in date_str:
                year = re.search(r'\d{4}', date_str)
                return datetime(int(year.group()), num, 1)
        if re.match(r'\d{4}', date_str):
            return datetime(int(date_str), 1, 1)
    except:
        return None
    return None

# TF-IDF based textual similarity
def compute_tfidf_score(resume, jd):
    vectorizer = TfidfVectorizer(stop_words='english')
    vec = vectorizer.fit_transform([resume, jd])
    return cosine_similarity(vec[0], vec[1])[0][0] * 100

# Semantic similarity using transformer embeddings
def compute_semantic_score(resume, jd):
    emb1 = st_model.encode(resume, convert_to_tensor=True)
    emb2 = st_model.encode(jd, convert_to_tensor=True)
    return util.cos_sim(emb1, emb2).item() * 100

# Skill matching score
def compute_skill_score(resume_skills, jd_skills):
    if not jd_skills:
        return 0
    matched = set(resume_skills).intersection(set(jd_skills))
    return len(matched) / len(jd_skills) * 100

# Final score combining TF-IDF, semantic and skill match
def compute_hybrid_score(tfidf, semantic, skill):
    return round(0.3 * tfidf + 0.5 * semantic + 0.2 * skill, 2)
  
  
  
  

# Streamlit UI starts here
st.set_page_config(page_title="AI Resume Analyzer", layout="wide")
st.title("📄 AI Resume Analyzer")
st.markdown("Upload resumes, paste JD, and get powerful similarity insights!")

# Load skills from file
skills_list = load_skills('skills.txt')

# Job description input box
jd_text = st.text_area("Paste the Job Description", height=200)

# Resume file uploader
uploaded_files = st.file_uploader(
    "Upload Resumes (PDF or DOCX)",
    type=["pdf", "docx"],
    accept_multiple_files=True
)

# Analyze button
analyze_button = st.button("🔍 Analyze")

# If analyze is clicked and JD + resumes are provided
if analyze_button and jd_text.strip() and uploaded_files:
    cleaned_jd = clean_text(jd_text)
    jd_skills = extract_skills(jd_text, skills_list)

    results = []
    for file in uploaded_files:
        filename = file.name

        # Extract text based on file type
        if filename.endswith(".pdf"):
            text = extract_text_from_pdf(file)
        elif filename.endswith(".docx"):
            text = extract_text_from_docx(file)
        else:
            st.warning(f"Unsupported file type: {filename}")
            continue

        if not text or not text.strip():
            st.warning(f"Could not extract text from {filename}")
            continue

        # Extract fields from resume
        info = extract_basic_info(text)
        resume_skills = extract_skills(text, skills_list)
        education = extract_education(text)
        years_exp = extract_experience_years(text)

        # Merge relevant text for scoring
        merged_text = clean_text(text) + ' ' + ' '.join(resume_skills) + ' ' + education

        # Compute all 3 scores
        tfidf_score = compute_tfidf_score(merged_text, cleaned_jd)
        semantic_score = compute_semantic_score(merged_text, cleaned_jd)
        skill_score = compute_skill_score(resume_skills, jd_skills)

        # Hybrid score
        final_score = compute_hybrid_score(tfidf_score, semantic_score, skill_score)

        # Store the result
        results.append({
            'Filename': filename,
            'Name': info['name'],
            'Email': info['email'],
            'Phone': info['phone'],
            'Education': education,
            'Experience (yrs)': years_exp,
            'Skills': ', '.join(resume_skills),
            'Match Score': final_score
        })

    # Sort results by score descending
    results.sort(key=lambda x: x['Match Score'], reverse=True)
    df_results = pd.DataFrame(results)

    # Display results table
    st.subheader("📊 Matching Results")
    st.dataframe(df_results, use_container_width=True)

    # Offer CSV download
    csv = df_results.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Download Results as CSV",
        data=csv,
        file_name='resume_match_results.csv',
        mime='text/csv'
    )

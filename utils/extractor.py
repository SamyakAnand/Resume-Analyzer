# utils/extractor.py
import re, tempfile
from pdfminer.high_level import extract_text
from docx import Document
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

STOPWORDS = set(stopwords.words('english'))

def load_skills(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return [line.strip().lower() for line in f if line.strip()]
    except Exception as e:
        print(f"⚠️ Could not load skills file: {e}")
        return []

def extract_text_from_pdf(file):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
            tmp.write(file.read())
            return extract_text(tmp.name)
    except Exception as e:
        print(f"PDF extract error: {e}")
        return None

def extract_text_from_docx(file):
    try:
        doc = Document(file)
        return "\n".join([p.text for p in doc.paragraphs])
    except Exception as e:
        print(f"DOCX extract error: {e}")
        return None

def clean_text(text):
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)
    return text

def extract_basic_info(text):
    lines = text.strip().split('\n')
    name = next((line.strip().title() for line in lines if len(line.strip().split())<=4 and line.strip()), '')
    email = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    phone = re.search(r'(\+?\d{1,3}[-.\s]?)?\(?\d{2,5}\)?[-.\s]?\d{3,5}[-.\s]?\d{3,5}', text)
    return {
        'name': name,
        'email': email.group() if email else '',
        'phone': phone.group() if phone else ''
    }

def extract_skills(text, skills_list):
    text_lower = text.lower()
    return list({skill for skill in skills_list if re.search(r'\b' + re.escape(skill) + r'\b', text_lower)})

def extract_education(text):
    keywords = ['bachelor', 'master', 'b.sc', 'm.sc', 'phd', 'b.tech', 'm.tech', 'mba']
    candidates = [line.strip() for line in text.split('\n') if any(k in line.lower() for k in keywords)]
    return max(candidates, key=len) if candidates else ''

def extract_experience_years(text):
    text_lower = text.lower()
    total_years = 0

    # First, prefer lines mentioning experience/employment
    exp_lines = [line for line in text_lower.split('\n')
                 if any(kw in line for kw in ['experience', 'employment', 'professional', 'work', 'career'])]
    relevant_text = "\n".join(exp_lines)

    # Try year ranges in relevant_text
    matches = re.findall(r'(\d{4})\s*[-–]\s*(\d{4}|present|current)', relevant_text)
    for start, end in matches:
        try:
            start = int(start)
            end = 2025 if end in ['present','current'] else int(end)
            if end > start:
                total_years += (end - start)
        except:
            continue

    # If still zero, check "X+ years of experience" in relevant_text
    if total_years == 0:
        num_match = re.findall(r'(\d+)\+?\s+years? of experience', relevant_text)
        if num_match:
            total_years = max([int(n) for n in num_match])

    # ✅ If still zero, fallback: search whole text for year ranges
    if total_years == 0:
        matches = re.findall(r'(\d{4})\s*[-–]\s*(\d{4}|present|current)', text_lower)
        for start, end in matches:
            try:
                start = int(start)
                end = 2025 if end in ['present','current'] else int(end)
                if end > start:
                    total_years += (end - start)
            except:
                continue

    # If still zero, skip fallback to all years (avoid wrong guesses)
    return total_years

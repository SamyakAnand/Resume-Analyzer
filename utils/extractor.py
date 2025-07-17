# utils/extractor.py
import re
import os
import tempfile
import logging
from datetime import datetime
from calendar import month_abbr
from pdfminer.high_level import extract_text
from docx import Document
from nltk import download
from nltk.corpus import stopwords

# Setup logging
logging.basicConfig(level=logging.INFO)

# Ensure stopwords are available
try:
    STOPWORDS = set(stopwords.words('english'))
except LookupError:
    download('stopwords')
    STOPWORDS = set(stopwords.words('english'))

def load_skills(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            skills = [line.strip().lower() for line in f if line.strip()]
            logging.info(f"Loaded {len(skills)} skills from {file_path}")
            return skills
    except FileNotFoundError:
        logging.warning(f"Skills file not found: {file_path}")
        return []
    except Exception as e:
        logging.error(f"Could not load skills file: {e}")
        return []

def extract_text_from_pdf(file):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
            tmp.write(file.read())
            tmp_path = tmp.name

        try:
            return extract_text(tmp_path)
        finally:
            os.unlink(tmp_path)
    except Exception as e:
        logging.error(f"PDF extract error: {e}")
        return None

def extract_text_from_docx(file):
    try:
        doc = Document(file)
        return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
    except Exception as e:
        logging.error(f"DOCX extract error: {e}")
        return None

def clean_text(text):
    return re.sub(r'\s+', ' ', text.lower()).strip() if text else ""

def extract_basic_info(text):
    if not text:
        return {'name': '', 'email': '', 'phone': ''}

    lines = [line.strip() for line in text.strip().split('\n') if line.strip()]
    name = ''
    for line in lines:
        if any(k in line.lower() for k in ['email', 'phone', 'address', 'resume', 'cv']):
            continue
        if '@' in line or re.search(r'\d{3,}', line):
            continue
        if len(line.split()) <= 4 and line.replace(' ', '').isalpha() and not line.isupper():
            name = line.title()
            break

    email = re.search(r"[\w._%+-]+@[\w.-]+\.[a-zA-Z]{2,}", text)
    phone_pattern = r'(\+?\d{1,3}[\s.-]?)?(\(?\d{2,4}\)?[\s.-]?)?\d{3,4}[\s.-]?\d{3,4}'
    phone = re.search(phone_pattern, text)

    return {
        'name': name,
        'email': email.group() if email else '',
        'phone': phone.group() if phone else ''
    }

def extract_skills(text, skills_list):
    if not text or not skills_list:
        return []

    text_lower = text.lower()
    found_skills = set()

    for skill in skills_list:
        variations = {
            skill,
            skill.replace('.', ''),
            skill.replace('-', ' '),
            skill.replace('_', ' ')
        }
        for var in variations:
            if var and re.search(rf'\b{re.escape(var)}\b', text_lower):
                found_skills.add(skill)
                break

    return list(found_skills)

def extract_institution(line):
    line = re.sub(r'\b(bachelor|master|degree|diploma|b\.?sc|m\.?sc|ph\.?d)\b', '', line.lower())
    line = re.sub(r'\b(of|in|from|at)\b', '', line)
    line = re.sub(r'\d{4}', '', line)
    line = re.sub(r'[^\w\s]', ' ', line)
    words = [w for w in line.split() if len(w) > 2]
    return ' '.join(words[:3]).title() if words else ''

def extract_education(text):
    if not text:
        return "Not Found"

    degree_patterns = [
        r'(bachelor(?:s)?(?: of (?:science|arts|engineering|business))?(?: in [\w\s]+)?)',
        r'(master(?:s)?(?: of (?:science|arts|engineering|business))?(?: in [\w\s]+)?)',
        r'(b\.?(?:sc|tech|eng|com|a)\.? in [\w\s]+)',
        r'(m\.?(:?sc|tech|eng|com|a|ba)\.? in [\w\s]+)',
        r'(ph\.?d\.? in [\w\s]+)',
        r'(doctorate in [\w\s]+)',
        r'(associate(?: degree)? in [\w\s]+)',
        r'(diploma in [\w\s]+)'
    ]

    education_info = []
    for line in text.split('\n'):
        for pattern in degree_patterns:
            match = re.search(pattern, line.lower())
            if match:
                year = re.search(r'\b(19|20)\d{2}\b', line)
                institution = extract_institution(line)
                education_info.append({
                    'degree': match.group(1).title(),
                    'year': year.group() if year else '',
                    'institution': institution,
                    'full_line': line.strip()
                })

    if education_info:
        best = max(education_info, key=lambda x: len(x['full_line']))
        return f"{best['degree']}, {best['institution']} ({best['year']})".strip(', ()')
    return "Not Found"

def parse_date(date_str):
    if not date_str:
        return None
    date_str = date_str.strip().lower()
    if date_str in ['present', 'current']:
        return datetime.now()

    try:
        if re.match(r'\d{1,2}/\d{4}', date_str):
            month, year = map(int, date_str.split('/'))
            return datetime(year, month, 1)
        if re.match(r'\d{4}', date_str):
            return datetime(int(date_str), 1, 1)

        month_map = {m.lower(): i for i, m in enumerate(month_abbr) if m}
        month_map.update({
            'january': 1, 'february': 2, 'march': 3, 'april': 4,
            'may': 5, 'june': 6, 'july': 7, 'august': 8,
            'september': 9, 'october': 10, 'november': 11, 'december': 12
        })
        year = re.search(r'\b(19|20)\d{2}\b', date_str)
        for name, num in month_map.items():
            if name in date_str:
                return datetime(int(year.group()), num, 1)
    except:
        return None

    return None

def calculate_non_overlapping_experience(ranges):
    total = 0
    ranges.sort(key=lambda x: x[0])
    end = None
    for start, finish, months in ranges:
        if not end or start > end:
            total += months
            end = finish
        elif finish > end:
            overlap = (end.year - start.year) * 12 + (end.month - start.month)
            total += max(0, months - overlap)
            end = finish
    return total

def extract_experience_section(text):
    if not text:
        return ""
    lines = text.split('\n')
    start, end = -1, len(lines)
    for i, line in enumerate(lines):
        if re.search(r'\b(experience|employment|work history|professional experience)\b', line.lower()):
            start = i
            break
    if start == -1:
        return text
    for i in range(start + 1, len(lines)):
        if re.search(r'\b(education|skills|projects|certifications)\b', lines[i].lower()):
            end = i
            break
    return '\n'.join(lines[start:end])

def extract_experience_years(text):
    if not text:
        return 0.0

    patterns = [
        r'((?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\w* \d{4})\s*[-\u2013to]+\s*((?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\w* \d{4}|present|current)',
        r'(\d{1,2}/\d{4})\s*[-\u2013to]+\s*(\d{1,2}/\d{4}|present|current)',
        r'(\d{4})\s*[-\u2013to]+\s*(\d{4}|present|current)'
    ]

    exp_text = extract_experience_section(text)
    matches = []

    for pattern in patterns:
        for start, end in re.findall(pattern, exp_text.lower()):
            s_date = parse_date(start)
            e_date = parse_date(end) if end not in ['present', 'current'] else datetime.now()
            if s_date and e_date and e_date > s_date:
                months = (e_date.year - s_date.year) * 12 + (e_date.month - s_date.month)
                matches.append((s_date, e_date, months))

    return round(calculate_non_overlapping_experience(matches) / 12, 1) if matches else 0.0

def debug_extraction(text, skills_list=None):
    logging.info("=== DEBUG EXTRACTION ===")
    if text:
        logging.info(f"Text length: {len(text)}")
        logging.info(f"Basic Info: {extract_basic_info(text)}")
        logging.info(f"Education: {extract_education(text)}")
        logging.info(f"Experience: {extract_experience_years(text)} years")
        if skills_list:
            skills = extract_skills(text, skills_list)
            logging.info(f"Skills found: {len(skills)} - {skills[:10]}")
    logging.info("=== END DEBUG ===")

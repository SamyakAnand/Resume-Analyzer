from flask import Flask, render_template, request
import tempfile
from pdfminer.high_level import extract_text
from docx import Document
import re
import nltk
from nltk import word_tokenize, pos_tag, ne_chunk
from nltk.tree import Tree
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# app
app = Flask(__name__)

# -- Text extraction --
def extract_text_from_pdf(file):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
        tmp.write(file.read())
        return extract_text(tmp.name)

def extract_text_from_docx(file):
    doc = Document(file)
    return "\n".join([p.text for p in doc.paragraphs])

# -- Extract name etc. --
def extract_name(text):
    lines = text.strip().split('\n')
    ignore_titles = {'Data Scientist', 'Machine Learning Engineer', 'AI Engineer', 'Software Engineer'}
    for line in lines[:5]:
        if line.strip() and line.strip() not in ignore_titles:
            tokens = word_tokenize(line)
            if all(token[0].isupper() and token.isalpha() for token in tokens):
                return line.strip()
    # fallback: NLTK chunking
    tokens = word_tokenize(text)
    tags = pos_tag(tokens)
    chunks = ne_chunk(tags)
    for chunk in chunks:
        if isinstance(chunk, Tree) and chunk.label() == 'PERSON':
            return ' '.join(c[0] for c in chunk.leaves())
    return None

def extract_basic_info(text):
    name = extract_name(text)
    email = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    phone = re.search(r"(\+\d{1,3}[-.\s]?)?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}", text)
    return {
        'name': name,
        'email': email.group() if email else None,
        'phone': phone.group() if phone else None
    }

# -- Similarity scoring --
def match_resume_to_jd(resume_text, jd_text):
    vectorizer = TfidfVectorizer(stop_words='english')
    vectors = vectorizer.fit_transform([resume_text, jd_text])
    return round(cosine_similarity(vectors[0], vectors[1])[0][0] * 100, 2)

# -- Routes --
@app.route('/', methods=['GET', 'POST'])
def index():
    results = []

    if request.method == 'POST':
        jd_text = request.form.get('jd_text')
        files = request.files.getlist('resumes')

        if jd_text.strip() and files:
            for file in files:
                filename = file.filename
                if filename.endswith('.pdf'):
                    text = extract_text_from_pdf(file)
                elif filename.endswith('.docx'):
                    text = extract_text_from_docx(file)
                else:
                    continue

                info = extract_basic_info(text)
                score = match_resume_to_jd(text, jd_text)

                results.append({
                    'filename': filename,
                    'name': info.get('name'),
                    'email': info.get('email'),
                    'phone': info.get('phone'),
                    'score': score
                })
            results = sorted(results, key=lambda x: x['score'], reverse=True)

    return render_template('index.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, flash
from utils import extractor, scoring
import config

app = Flask(__name__)
app.secret_key = 'dev'  # lightweight, non-secret placeholder

# Initialize once
skills_list = extractor.load_skills(config.SKILLS_FILE)
st_model = scoring.load_st_model(config.SENTENCE_TRANSFORMER_MODEL)

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    if request.method == 'POST':
        jd_text = request.form.get('jd_text', '')
        files = request.files.getlist('resumes')
        if jd_text.strip() and files:
            cleaned_jd = extractor.clean_text(jd_text)
            jd_skills = extractor.extract_skills(jd_text, skills_list)
            for file in files:
                filename = file.filename
                text = None
                if filename.endswith('.pdf'):
                    text = extractor.extract_text_from_pdf(file)
                elif filename.endswith('.docx'):
                    text = extractor.extract_text_from_docx(file)
                else:
                    flash(f"❌ Unsupported file type: {filename}", 'danger')
                    continue

                if not text or not text.strip():
                    flash(f"⚠️ Could not extract text from {filename}", 'warning')
                    continue

                info = extractor.extract_basic_info(text)
                resume_skills = extractor.extract_skills(text, skills_list)
                education = extractor.extract_education(text)
                years_exp = extractor.extract_experience_years(text)

                merged_text = extractor.clean_text(text) + ' ' + ' '.join(resume_skills) + ' ' + education

                score = scoring.hybrid_score_tfidf_st(
                    merged_text, cleaned_jd, resume_skills, jd_skills, st_model
                )

                results.append({
                    'filename': filename,
                    'name': info['name'],
                    'email': info['email'],
                    'phone': info['phone'],
                    'education': education,
                    'years_exp': years_exp,
                    'skills': ', '.join(resume_skills),
                    'score': score
                })
            results.sort(key=lambda x: x['score'], reverse=True)
    return render_template('index.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)

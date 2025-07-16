# README.md

---

# AI Resume Analyzer (Flask App)

An interactive web application that analyzes candidate resumes against a target Job Description (JD) and computes a hybrid similarity score using TF-IDF, semantic embeddings (Sentence Transformers), and skill matching. Built with Flask, NLTK, scikit-learn, and a modern UI (Bootstrap), this tool helps HR teams, recruiters, and learners rank resumes by JD relevance in seconds.

---

## ✨ Features

- Upload multiple resumes in PDF or DOCX
- Paste or type a Job Description
- Auto-extract:
  - Name, email, phone  
  - Education  
  - Skills  
  - Estimated years of experience
- Compute hybrid similarity:
  - TF-IDF + cosine similarity  
  - Semantic similarity (Sentence Transformers)  
  - Skill overlap
- Beautiful animated UI & responsive table
- Download-ready, production-friendly code structure

---

## ⚙️ Tech Stack

- **Backend:** Python (Flask)  
- **NLP:** NLTK, scikit-learn, Sentence Transformers  
- **Parsing:** pdfminer.six, python-docx  
- **Frontend:** Bootstrap 5, custom CSS, responsive table  
- **Extra:** Jinja2 templates, modular utils, config structure

---

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/SamyakAnand/ai-resume-analyzer.git
cd ai-resume-analyzer

# (Recommended) Create virtual environment
python -m venv venv
# Activate:
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## 🚀 Usage

1. Ensure a `skills.txt` file exists in the project root (one skill per line).  
2. Start the Flask server:
   ```bash
   python app.py
   ```
3. Open your browser at [http://127.0.0.1:5000](http://127.0.0.1:5000)  
4. Upload resumes & paste JD → view ranked results with:
   - Name, email, phone  
   - Education  
   - Experience (years)  
   - Skills  
   - Score (%)

---

## 🧠 How It Works

1. Parses uploaded PDF/DOCX resumes  
2. Cleans and tokenizes text (NLTK)  
3. Extracts:
   - Name, email, phone (regex)  
   - Education keywords  
   - Skills from `skills.txt`  
   - Experience years from patterns  
4. Computes:
   - TF-IDF + cosine similarity (scikit-learn)  
   - Semantic similarity (Sentence Transformers)  
   - Skill overlap percentage  
5. Combines into final weighted score → displays sorted table  

---

## 🖼 Screenshot

![Demo Screenshot](https://github.com/SamyakAnand/Resume-Analyzer/blob/main/images/Screenshot%202025-07-16%20192647.png)

---

## 🙏 Credits

Built by [Samyak Anand](https://github.com/SamyakAnand).  
Thanks to the Flask, NLTK, scikit-learn, and Sentence Transformers communities.

---

## 🤝 Connect

- GitHub: [@SamyakAnand](https://github.com/SamyakAnand)  
- LinkedIn: [@samyakanand](https://www.linkedin.com/in/samyakanand/)

- GitHub: [@Thottempudi Koushik
](https://github.com/Koushik900)  
- LinkedIn: [@Thottempudi Koushik
]( https://www.linkedin.com/in/tk-koushik-1362bb200/
)

---

## ⚖️ License

Released under the MIT License — use, modify, and share freely!

---

If you'd like:
✅ I can also generate this as a ready `README.md` with badges and an animated GIF. Just say **`yes`**! 🚀

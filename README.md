# 📄 AI Resume Analyzer (Flask App)

An interactive web app to **analyze resumes vs a job description (JD)** and calculate similarity scores.  
Built using **Flask**, **NLTK**, and **scikit-learn**, this tool helps recruiters, HR teams, or learners see which resumes best match a JD.

---

## 🚀 Features

- Upload **one or multiple resumes** (PDF or DOCX)
- Paste a **Job Description (JD)**
- Extracts:
  - Candidate name
  - Email
  - Phone number
- Calculates **similarity score** using TF-IDF + Cosine Similarity
- Sorts & displays results in a stylish, responsive table
- Modern UI built with Bootstrap and custom CSS

---

## 🛠 Tech Stack

- **Python (Flask)** – web backend
- **NLTK** – name extraction (NER)
- **scikit-learn** – TF-IDF vectorization & cosine similarity
- **pdfminer / python-docx** – read PDF/DOCX
- **Bootstrap** – responsive UI & styling

---

## 📦 Installation & Running Locally

```bash
# Clone this repository
git clone https://github.com/YourUsername/ai-resume-analyzer.git
cd ai-resume-analyzer

# (Optional) Create virtual environment
python -m venv venv
# Activate:
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install required packages
pip install -r requirements.txt

# Run the app
python app.py
Open browser and go to: http://127.0.0.1:5000

📊 How It Works
Upload one or more resumes

Paste the target JD text

App extracts text, candidate info, and computes similarity

See which resumes match the JD best

📸 Screenshot
![Demo Screenshot](https://github.com/SamyakAnand/Resume-Analyzer/blob/main/images/Screenshot%202025-07-16%20012317.png)
🙏 Credits
Made as a practice project to learn NLP + Flask

Thanks to the Python, NLTK, and scikit-learn communities ❤️

🔗 Connect
GitHub: Samyak Anand

LinkedIn: @samyakanand

✨ Built to explore practical AI & NLP ideas!
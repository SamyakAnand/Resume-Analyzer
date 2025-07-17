
# 🧠 AI Resume Analyzer

An interactive Flask web application that analyzes candidate resumes against a Job Description (JD) and computes a **hybrid similarity score** using:

* **TF-IDF vectorization**
* **Semantic embeddings** (via Sentence Transformers)
* **Skill overlap**

This tool helps **recruiters**, **HR professionals**, and **job seekers** rank resumes by relevance in seconds — with a clean UI and production-friendly backend.

---

## ✨ Features

✅ Upload **multiple resumes** (PDF/DOCX)
✅ Paste or type a **Job Description**
✅ Auto-extract:

* Name, email, phone
* Skills
* Education details
* **Estimated years of experience**

✅ Compute a **hybrid similarity score**:

* **TF-IDF cosine similarity** (on resume & JD)
* **Semantic similarity** using Sentence Transformers
* **Skill overlap percentage**

✅ Responsive UI with Bootstrap 5
✅ Fully modular codebase for easy extension

---

## 🧠 Scoring Logic

We use a **weighted hybrid scoring system** defined in [`utils/scoring.py`](./utils/scoring.py):

* `50%`: Semantic similarity (`SentenceTransformer`)
* `30%`: TF-IDF cosine similarity (`sklearn`)
* `20%`: Skill overlap ratio

This approach blends keyword relevance with contextual matching and hard skill alignment.

---

## ⚙️ Tech Stack

* **Backend**: Flask (Python)
* **Parsing**: `pdfminer.six`, `python-docx`
* **NLP**: `NLTK`, `scikit-learn`, `Sentence Transformers`
* **Frontend**: Bootstrap 5, custom CSS, Jinja2
* **Structure**: Modular utilities, configuration files, static templates

---

## 📁 Project Structure

```bash
Resume-Analyzer/
├── app.py                 # Main Flask application
├── config.py              # Configuration file (model, secret key)
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
├── templates/
│   └── index.html         # UI template (Jinja2 + Bootstrap)
├── utils/
│   ├── extractor.py       # Text parsing & field extraction
│   └── scoring.py         # Hybrid scoring logic (TF-IDF + semantic + skills)
└── skills.txt             # Custom skill keywords list (one per line)
```

---

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/SamyakAnand/Resume-Analyzer.git
cd Resume-Analyzer

# (Optional) Create virtual environment
python -m venv venv
# Activate:
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## 🚀 Usage

1. Make sure `skills.txt` exists in the project root (one skill per line).
2. Launch the Flask app:

   ```bash
   python app.py
   ```
3. Open browser at: [http://127.0.0.1:5000](http://127.0.0.1:5000)
4. Upload resumes and input a JD → view extracted info and relevance scores:

   * Name, Email, Phone
   * Education
   * Skills
   * Experience (years)
   * Score (0–100%)

---

## 📊 Example Output

![Demo Screenshot](https://github.com/SamyakAnand/Resume-Analyzer/blob/main/images/Screenshot%202025-07-16%20192647.png)

---

## 🧪 How It Works (Pipeline)

1. **Parse** uploaded resumes (`pdfminer` / `python-docx`)
2. **Clean & tokenize** text (`NLTK`)
3. **Extract**:

   * Contact info (regex)
   * Skills (from `skills.txt`)
   * Education (keywords)
   * Years of experience (pattern recognition)
4. **Score** each resume:

   * TF-IDF cosine similarity (resume ↔ JD)
   * Semantic similarity (via `SentenceTransformer`)
   * Skill match ratio
5. **Combine scores** → render sorted results table on UI

---

## 🙌 Credits

Built with ❤️ by:

* 👨‍💻 [Samyak Anand](https://github.com/SamyakAnand)
* 👨‍💻 [Thottempudi Koushik](https://github.com/Koushik900)
* 👨‍💻 [Sai Vardhan Kalvala](https://github.com/saivardhankalvala)
* 👩‍💻 [Swetha](https://github.com/swethar6232)
* 👩‍💻 [Rasmitha Ravi](https://github.com/RasmithaRavi)

Thanks to open-source contributors behind Flask, NLTK, scikit-learn, and HuggingFace 🤗.

---

## 🔗 Connect

* GitHub: [@SamyakAnand](https://github.com/SamyakAnand)
* LinkedIn: [@samyakanand](https://linkedin.com/in/samyakanand)

<details>
<summary>Other Contributors</summary>

* GitHub: [@Koushik900](https://github.com/Koushik900)
  LinkedIn: [Thottempudi Koushik](https://www.linkedin.com/in/tk-koushik-1362bb200/)

* GitHub: [@saivardhankalvala](https://github.com/saivardhankalvala)
  LinkedIn: [Sai Vardhan Kalvala](https://in.linkedin.com/in/saivardhankalvala16)

* GitHub: [@swethar6232](https://github.com/swethar6232)

* GitHub: [@RasmithaRavi](https://github.com/RasmithaRavi)

</details>

---

## ⚖️ License

Licensed under the **MIT License** — free for personal, academic, or commercial use. 🌐

---


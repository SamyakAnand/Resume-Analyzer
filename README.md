# AI Resume Analyzer (Flask App)

An interactive web application that compares candidate resumes against a target Job Description (JD) and computes a similarity score. Built with Flask, NLTK, and scikit-learn, this tool streamlines the screening process for recruiters, HR teams, and learners by ranking resumes based on how well they match the JD.

---

## Table of Contents

- [Features](#features)  
- [Tech Stack](#tech-stack)  
- [Installation](#installation)  
- [Usage](#usage)  
- [How It Works](#how-it-works)  
- [Screenshot](#screenshot)  
- [Credits](#credits)  
- [Connect](#connect)  
- [License](#license)  

---

## Features

- Upload single or multiple resumes in PDF or DOCX format  
- Paste or type in a Job Description for comparison  
- Automatic extraction of candidate name, email, and phone number  
- TF-IDF vectorization and cosine similarity calculation  
- Rank resumes by similarity score in a responsive, sortable table  
- Clean, modern UI built with Bootstrap and custom CSS  

---

## Tech Stack

- Python (Flask) for the web application backend  
- NLTK for natural language processing and named entity recognition  
- scikit-learn for TF-IDF vectorization and cosine similarity  
- pdfminer.six and python-docx for parsing PDF and DOCX documents  
- Bootstrap for responsive frontend design  

---

## Installation

```bash
# Clone the repository
git clone https://github.com/YourUsername/ai-resume-analyzer.git
cd ai-resume-analyzer

# (Optional) Create and activate a virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## Usage

1. Start the Flask server:  
   ```bash
   python app.py
   ```
2. Open your browser and navigate to `http://127.0.0.1:5000`.  
3. Upload one or more resumes and paste the target JD.  
4. View similarity scores and ranked results.  

---

## How It Works

1. The app reads uploaded files (PDF/DOCX) and extracts text.  
2. Named entity recognition identifies candidate names, emails, and phone numbers.  
3. TF-IDF vectorizer transforms both resumes and the JD into numeric feature vectors.  
4. Cosine similarity measures the closeness between each resume and the JD.  
5. Results are sorted and displayed in a responsive table for easy review.  

---

## Screenshot

![Demo Screenshot](https://github.com/SamyakAnand/Resume-Analyzer/blob/main/images/Screenshot%202025-07-16%20021852.png)

---

## Credits

This project was created as a hands-on exercise in NLP and web development. Special thanks to the Python, NLTK, and scikit-learn communities for their invaluable resources.

---

## Connect

- GitHub: [Samyak Anand](https://github.com/SamyakAnand)  
- LinkedIn: [@samyakanand](https://www.linkedin.com/in/samyakanand/)  

---

## License

This project is released under the MIT License.  
Feel free to use, modify, and distribute it in your own projects.

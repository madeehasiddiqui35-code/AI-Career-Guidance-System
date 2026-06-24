# AI Career Guidance System

An AI-powered career guidance platform built using Streamlit and Groq AI. 
The system helps students assess their career readiness, identify skill gaps, analyze resumes, prepare for interviews,
and receive personalized career recommendations.

---

## Features

### User Authentication
- User Registration
- User Login
- Logout Functionality

### Dashboard
- Student profile information
- Career goal selection
- Internship readiness score calculation
- Skill gap identification

### Career Guidance Tools
- Skill Gap Analysis
- Career Roadmap Generator
- Career Match Analyzer
- Progress Tracker
- Project Recommendations
- Learning Resources
- Certification Tracker

### Resume Analyzer
- Upload PDF Resume
- Resume Content Extraction
- AI-Based Resume Review
- Strengths and Weaknesses Analysis
- Improvement Suggestions

### Interview Coach
- Role-Based Interview Questions
- Data Science
- AI Engineer
- Software Engineer
- Web Developer

### Job Description Analyzer
- Compare Job Requirements with Current Skills
- Detect Missing Skills

### AI Career Chatbot
- Career Guidance
- Resume Tips
- Interview Preparation
- Internship Guidance
- Skill Recommendations

---

## Technologies Used

- Python
- Streamlit
- Groq API
- Llama 3.3 70B Versatile
- PyPDF2
- SQLite (Authentication Database)
- Session State Management

---

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/AI-Career-Guidance-System.git

cd AI-Career-Guidance-System
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API Key

Create:

```text
.streamlit/secrets.toml
```

Add:

```toml
GROQ_API_KEY = "your_groq_api_key"
```

---

## Run Application

```bash
streamlit run app.py
```


## Security Measures

- API keys stored using Streamlit Secrets.
- No hardcoded credentials in source code.
- Input validation implemented.
- Error handling added for API failures.

---

## Future Enhancements

- Cloud Deployment
- Advanced Authentication
- Database Integration
- Resume Score Tracking
- Personalized Learning Plans
- Job Recommendation Engine
- Career Analytics Dashboard

---

## Project Workflow

1. User Registration/Login
2. Student Information Collection
3. Career Goal Selection
4. Readiness Score Calculation
5. Skill Gap Analysis
6. Resume Analysis
7. Career Guidance Recommendations
8. AI Chatbot Support

---

## Author

Name: Madeeha Siddiqui

Project: AI Career Guidance System

Academic Project – 2026

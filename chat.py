from fastapi import APIRouter
from pydantic import BaseModel

from app.api.documents import CURRENT_RESUME

router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    conversation_id: str | None = None
    resume_context: dict | None = None


# =========================================================
# HELPERS
# =========================================================

def bullet_list(items):
    if not items:
        return "No information detected."

    return "\n".join(
        f"• {item}"
        for item in items[:15]
    )


def get_skills():
    return CURRENT_RESUME.get(
        "analysis",
        {}
    ).get(
        "skills",
        []
    )


# =========================================================
# RESUME ANALYSIS
# =========================================================

def analyze_resume_response():

    if not CURRENT_RESUME["text"]:
        return """
## 📄 Resume Analysis

No resume is currently uploaded.

Please upload your PDF or DOCX resume first.
"""

    analysis = CURRENT_RESUME["analysis"]

    skills = analysis.get("skills", [])
    education = analysis.get("education", [])
    experience = analysis.get("experience", [])
    projects = analysis.get("projects", [])
    certifications = analysis.get("certifications", [])
    achievements = analysis.get("achievements", [])

    return f"""
## 📄 Resume Analysis

### 🧠 Skills

{bullet_list(skills)}

### 🎓 Education

{bullet_list(education)}

### 💼 Experience

{bullet_list(experience)}

### 🚀 Projects

{bullet_list(projects)}

### 🏆 Certifications

{bullet_list(certifications)}

### 🥇 Achievements

{bullet_list(achievements)}

### 📊 Resume Statistics

- Resume length: {analysis.get("resume_length", 0)} characters
- Skills detected: {len(skills)}
- Education entries: {len(education)}
- Experience entries: {len(experience)}
- Projects detected: {len(projects)}
- Certifications detected: {len(certifications)}

Your resume is now available as context for the CareerAI chatbot.
"""


# =========================================================
# CAREER RECOMMENDATION
# =========================================================

def career_response():

    skills = get_skills()

    if not skills:
        return """
## 💼 Career Recommendations

Please upload your resume first so I can analyze your actual skills.
"""

    skill_text = " ".join(
        skill.lower()
        for skill in skills
    )

    careers = []

    if any(
        x in skill_text
        for x in [
            "machine learning",
            "deep learning",
            "tensorflow",
            "pytorch",
            "scikit-learn"
        ]
    ):
        careers.append("Machine Learning Engineer")

    if any(
        x in skill_text
        for x in [
            "artificial intelligence",
            "generative ai",
            "deep learning",
            "nlp"
        ]
    ):
        careers.append("AI Engineer")

    if any(
        x in skill_text
        for x in [
            "pandas",
            "numpy",
            "statistics",
            "data science"
        ]
    ):
        careers.append("Data Scientist")

    if any(
        x in skill_text
        for x in [
            "sql",
            "power bi",
            "tableau",
            "data analysis"
        ]
    ):
        careers.append("Data Analyst")

    if any(
        x in skill_text
        for x in [
            "react",
            "javascript",
            "typescript",
            "html",
            "css"
        ]
    ):
        careers.append("Frontend Developer")

    if any(
        x in skill_text
        for x in [
            "fastapi",
            "flask",
            "django",
            "node.js"
        ]
    ):
        careers.append("Backend Developer")

    if not careers:
        careers = [
            "Software Developer",
            "AI/ML Trainee",
            "Data Analyst"
        ]

    careers = list(dict.fromkeys(careers))

    return f"""
## 💼 Career Analysis

Based on the skills detected from your resume:

### Potential Career Paths

{bullet_list(careers)}

### Detected Skills

{bullet_list(skills)}

### Next Step

Ask:

**"What skills am I missing for AI Engineer?"**

or:

**"Create a roadmap based on my resume."**
"""


# =========================================================
# SKILL GAP
# =========================================================

ROLE_REQUIREMENTS = {

    "ai engineer": [
        "Python",
        "Machine Learning",
        "Deep Learning",
        "Generative AI",
        "APIs",
        "Docker",
        "Model Deployment"
    ],

    "machine learning engineer": [
        "Python",
        "Machine Learning",
        "Deep Learning",
        "Scikit-learn",
        "TensorFlow",
        "Docker",
        "MLOps"
    ],

    "data scientist": [
        "Python",
        "Pandas",
        "NumPy",
        "Statistics",
        "Machine Learning",
        "SQL"
    ],

    "data analyst": [
        "Python",
        "SQL",
        "Pandas",
        "Statistics",
        "Power BI",
        "Tableau"
    ],

    "backend developer": [
        "Python",
        "FastAPI",
        "REST API",
        "SQL",
        "Git",
        "Docker"
    ]
}


def skill_gap_response(message):

    skills = get_skills()

    if not skills:
        return """
## 🎯 Skill Gap Analysis

Please upload your resume first.
"""

    target = "ai engineer"

    if "machine learning" in message.lower():
        target = "machine learning engineer"

    elif "data scientist" in message.lower():
        target = "data scientist"

    elif "data analyst" in message.lower():
        target = "data analyst"

    elif "backend" in message.lower():
        target = "backend developer"

    requirements = ROLE_REQUIREMENTS[target]

    current = [
        skill.lower()
        for skill in skills
    ]

    matched = []
    missing = []

    for requirement in requirements:

        found = any(
            requirement.lower() in skill
            or skill in requirement.lower()
            for skill in current
        )

        if found:
            matched.append(requirement)
        else:
            missing.append(requirement)

    return f"""
## 🎯 Skill Gap Analysis

### Target Role

**{target.title()}**

### ✅ Skills You Already Have

{bullet_list(matched)}

### 📚 Skills To Develop

{bullet_list(missing)}

### 🗺️ Suggested Order

1. Strengthen your existing fundamentals.
2. Learn the missing technical skills.
3. Build practical projects.
4. Deploy at least one project.
5. Practice role-specific interviews.
"""


# =========================================================
# ROADMAP
# =========================================================

def roadmap_response():

    skills = get_skills()

    return f"""
## 🗺️ Personalized Career Roadmap

### Current Skills

{bullet_list(skills)}

### Phase 1 — Foundations

- Python
- Data Structures & Algorithms
- SQL
- Git & GitHub

### Phase 2 — AI / Data

- NumPy
- Pandas
- Statistics
- Machine Learning
- Scikit-learn

### Phase 3 — Advanced AI

- Deep Learning
- NLP
- Computer Vision
- Generative AI
- LLMs

### Phase 4 — Production

- FastAPI
- REST APIs
- Docker
- Cloud
- Model Deployment

### Phase 5 — Portfolio

Build:

- AI Resume Analyzer
- RAG Career Assistant
- AI Interview Coach
- Skill Gap Analyzer

### Phase 6 — Interview

Practice:

- Python
- DSA
- SQL
- Machine Learning
- System Design
- Project Explanation
- HR Questions
"""


# =========================================================
# INTERVIEW
# =========================================================

def interview_response():

    skills = get_skills()

    return f"""
## 🎤 Resume-Based Mock Interview

I'll use your uploaded resume to create questions.

### Detected Skills

{bullet_list(skills)}

### Question 1

**Tell me about yourself and explain your most important project.**

Answer as if you're speaking to an interviewer.

After your answer, I can continue with a follow-up question.
"""


# =========================================================
# PROJECT RECOMMENDATIONS
# =========================================================

def project_response():

    skills = get_skills()

    return f"""
## 🚀 Project Recommendations

### Your Current Skills

{bullet_list(skills)}

### Recommended Projects

**1. AI Resume Analyzer**

Resume → Extraction → Analysis → Career Recommendations

**2. RAG Career Assistant**

Documents → Retrieval → AI Answers

**3. AI Interview Coach**

Resume → Questions → Answer Evaluation

**4. Skill Gap Analyzer**

Current Skills → Target Role → Missing Skills → Roadmap

**5. Career Recommendation Engine**

Skills → Profile → Career Paths
"""


# =========================================================
# MAIN CHAT LOGIC
# =========================================================

def generate_response(message: str):

    text = message.lower().strip()

    if (
        "analyze my resume" in text
        or "analyse my resume" in text
        or text == "resume analysis"
        or text == "resume"
    ):
        return analyze_resume_response()

    if (
        "skill gap" in text
        or "missing skill" in text
        or "skills am i missing" in text
    ):
        return skill_gap_response(message)

    if (
        "career" in text
        or "job" in text
        or "career path" in text
        or "suitable role" in text
    ):
        return career_response()

    if (
        "roadmap" in text
        or "learning path" in text
        or "how do i become" in text
    ):
        return roadmap_response()

    if (
        "mock interview" in text
        or "interview" in text
    ):
        return interview_response()

    if (
        "project" in text
        or "projects" in text
    ):
        return project_response()

    if CURRENT_RESUME["text"]:

        return f"""
## 🤖 CareerAI

I have your uploaded resume available as context.

### Detected Skills

{bullet_list(get_skills())}

You can ask me:

• Analyze my resume

• What careers are suitable for me?

• What skills am I missing for AI Engineer?

• Create a roadmap for me

• Give me resume-based interview questions

• Suggest projects based on my skills
"""

    return f"""
## 👋 CareerAI

You said:

> {message}

I'm your AI Career and Interview Preparation Assistant.

Upload your resume to unlock personalized career analysis.
"""


# =========================================================
# CHAT API
# =========================================================

@router.post("/chat")
async def chat(request: ChatRequest):

    response = generate_response(
        request.message
    )

    return {
        "response": response,
        "conversation_id":
            request.conversation_id
            or "career-session"
    }

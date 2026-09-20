from pathlib import Path
import re

import fitz
from docx import Document

from fastapi import APIRouter, UploadFile, File, HTTPException

router = APIRouter()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

MAX_FILE_SIZE = 10 * 1024 * 1024

ALLOWED_EXTENSIONS = {".pdf", ".docx"}

CURRENT_RESUME = {
    "filename": None,
    "text": "",
    "pages": [],
    "analysis": {}
}


# =========================================================
# PDF EXTRACTION
# =========================================================

def extract_pdf(path: Path):
    pages = []

    pdf = fitz.open(path)

    for number, page in enumerate(pdf):
        pages.append({
            "page": number + 1,
            "text": page.get_text()
        })

    pdf.close()

    return pages


# =========================================================
# DOCX EXTRACTION
# =========================================================

def extract_docx(path: Path):
    document = Document(path)

    text = []

    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            text.append(paragraph.text)

    return [{
        "page": None,
        "text": "\n".join(text)
    }]


# =========================================================
# SKILL DATABASE
# =========================================================

SKILLS = [
    "Python",
    "C",
    "C++",
    "Java",
    "JavaScript",
    "TypeScript",
    "HTML",
    "CSS",
    "React",
    "Node.js",
    "FastAPI",
    "Flask",
    "Django",

    "SQL",
    "MySQL",
    "PostgreSQL",
    "MongoDB",

    "Pandas",
    "NumPy",
    "Matplotlib",
    "Seaborn",

    "Machine Learning",
    "Deep Learning",
    "Artificial Intelligence",
    "Natural Language Processing",
    "NLP",
    "Computer Vision",

    "TensorFlow",
    "PyTorch",
    "Keras",
    "Scikit-learn",

    "Data Science",
    "Data Analysis",
    "Statistics",

    "Git",
    "GitHub",
    "Docker",
    "Kubernetes",

    "AWS",
    "Azure",
    "Google Cloud",

    "Power BI",
    "Tableau",

    "REST API",
    "APIs",

    "Data Structures",
    "Algorithms",

    "OpenCV",
    "LangChain",
    "RAG",
    "Generative AI",
    "LLM",

    "IoT",
    "Robotics"
]


def extract_skills(text: str):
    found = []

    text_lower = text.lower()

    for skill in SKILLS:
        if skill.lower() in text_lower:
            found.append(skill)

    return sorted(set(found))


# =========================================================
# SECTION EXTRACTION
# =========================================================

SECTION_HEADERS = [
    "education",
    "experience",
    "work experience",
    "projects",
    "skills",
    "certifications",
    "achievements",
    "summary",
    "objective",
    "profile",
    "internships"
]


def extract_section(text: str, keywords):
    lines = text.splitlines()

    collected = []
    active = False

    for line in lines:
        clean = line.strip()

        if not clean:
            continue

        lower = clean.lower()

        if any(keyword in lower for keyword in keywords):
            active = True
            collected.append(clean)
            continue

        if active:
            if any(
                header in lower
                for header in SECTION_HEADERS
            ):
                if not any(
                    keyword in lower
                    for keyword in keywords
                ):
                    break

            collected.append(clean)

    return collected[:40]


# =========================================================
# RESUME ANALYSIS
# =========================================================

def analyze_resume(text: str):

    email_match = re.search(
        r"[\w\.-]+@[\w\.-]+\.\w+",
        text
    )

    phone_match = re.search(
        r"(\+?\d[\d\s\-\(\)]{8,}\d)",
        text
    )

    return {
        "skills": extract_skills(text),

        "education": extract_section(
            text,
            ["education", "academic", "degree"]
        ),

        "experience": extract_section(
            text,
            ["experience", "work experience", "internship"]
        ),

        "projects": extract_section(
            text,
            ["projects", "project"]
        ),

        "certifications": extract_section(
            text,
            ["certifications", "certification", "certificate"]
        ),

        "achievements": extract_section(
            text,
            ["achievements", "achievement", "awards"]
        ),

        "email": (
            email_match.group(0)
            if email_match
            else None
        ),

        "phone": (
            phone_match.group(0)
            if phone_match
            else None
        ),

        "resume_length": len(text)
    }


# =========================================================
# UPLOAD RESUME
# =========================================================

@router.post("/documents/upload")
async def upload_document(
    file: UploadFile = File(...)
):

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is missing."
        )

    extension = Path(
        file.filename
    ).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are supported."
        )

    content = await file.read()

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="Maximum file size is 10MB."
        )

    filename = Path(
        file.filename
    ).name

    file_path = UPLOAD_DIR / filename

    with open(file_path, "wb") as output:
        output.write(content)

    # Extract document text
    if extension == ".pdf":
        pages = extract_pdf(file_path)
    else:
        pages = extract_docx(file_path)

    full_text = "\n".join(
        item["text"]
        for item in pages
    )

    if not full_text.strip():
        raise HTTPException(
            status_code=400,
            detail="Could not extract readable text from the resume."
        )

    # Analyze
    analysis = analyze_resume(full_text)

    # Store globally for current session
    CURRENT_RESUME["filename"] = filename
    CURRENT_RESUME["text"] = full_text
    CURRENT_RESUME["pages"] = pages
    CURRENT_RESUME["analysis"] = analysis

    return {
        "filename": filename,
        "characters": len(full_text),
        "pages": pages,
        "analysis": analysis,
        "message": "Resume uploaded and analyzed successfully."
    }


# =========================================================
# CURRENT RESUME
# =========================================================

@router.get("/documents/current")
async def get_current_resume():

    if not CURRENT_RESUME["text"]:
        raise HTTPException(
            status_code=404,
            detail="No resume uploaded."
        )

    return CURRENT_RESUME


# =========================================================
# DOCUMENT CHAT
# =========================================================

@router.post("/documents/{document_id}/chat")
async def document_chat(document_id: str):

    if not CURRENT_RESUME["text"]:
        raise HTTPException(
            status_code=404,
            detail="No resume uploaded."
        )

    return {
        "document_id": document_id,
        "response": "Resume is loaded and available to CareerAI."
    }


# =========================================================
# RESUME QUESTIONS
# =========================================================

@router.post("/documents/{document_id}/questions")
async def generate_questions(document_id: str):

    if not CURRENT_RESUME["text"]:
        raise HTTPException(
            status_code=404,
            detail="No resume uploaded."
        )

    skills = CURRENT_RESUME["analysis"].get(
        "skills",
        []
    )

    questions = []

    for skill in skills[:10]:
        questions.append({
            "question": f"Explain your experience with {skill}.",
            "answer": (
                f"Prepare a practical example from your resume "
                f"where you used {skill}."
            )
        })

    if not questions:
        questions.append({
            "question": "Tell me about yourself.",
            "answer": "Prepare a concise introduction based on your resume."
        })

    return {
        "document_id": document_id,
        "questions": questions
    }

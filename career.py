from fastapi import APIRouter
from pydantic import BaseModel

from app.api.documents import CURRENT_RESUME

router = APIRouter()


class CareerRequest(BaseModel):
    resume: dict = {}
    target_role: str | None = None


ROLE_REQUIREMENTS = {

    "AI Engineer": [
        "Python",
        "Machine Learning",
        "Deep Learning",
        "Generative AI",
        "APIs",
        "Docker",
        "Model Deployment"
    ],

    "Machine Learning Engineer": [
        "Python",
        "Machine Learning",
        "Deep Learning",
        "Scikit-learn",
        "TensorFlow",
        "Docker",
        "MLOps"
    ],

    "Data Scientist": [
        "Python",
        "Pandas",
        "NumPy",
        "Statistics",
        "Machine Learning",
        "SQL"
    ],

    "Data Analyst": [
        "Python",
        "SQL",
        "Pandas",
        "Statistics",
        "Power BI",
        "Tableau"
    ],

    "Backend Developer": [
        "Python",
        "FastAPI",
        "REST API",
        "SQL",
        "Git",
        "Docker"
    ]
}


def calculate_match(skills, requirements):

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

    match = round(
        len(matched) /
        len(requirements) *
        100
    )

    return match, matched, missing


@router.post("/career/recommend")
async def recommend_roles(
    request: CareerRequest
):

    if CURRENT_RESUME["analysis"]:

        skills = CURRENT_RESUME[
            "analysis"
        ].get(
            "skills",
            []
        )

    else:

        skills = request.resume.get(
            "skills",
            []
        )

    results = []

    for role, requirements in ROLE_REQUIREMENTS.items():

        match, matched, missing = calculate_match(
            skills,
            requirements
        )

        results.append({
            "role": role,
            "match": match,
            "matched_skills": matched,
            "missing_skills": missing
        })

    results.sort(
        key=lambda item: item["match"],
        reverse=True
    )

    return {
        "roles": results,
        "resume_skills": skills
    }


@router.post("/job/analyze")
async def analyze_job(
    request: CareerRequest
):

    role = (
        request.target_role
        or "AI Engineer"
    )

    requirements = ROLE_REQUIREMENTS.get(
        role,
        ROLE_REQUIREMENTS["AI Engineer"]
    )

    if CURRENT_RESUME["analysis"]:

        skills = CURRENT_RESUME[
            "analysis"
        ].get(
            "skills",
            []
        )

    else:

        skills = request.resume.get(
            "skills",
            []
        )

    match, matched, missing = calculate_match(
        skills,
        requirements
    )

    return {
        "target_role": role,
        "match": match,
        "matched_skills": matched,
        "missing_skills": missing,
        "recommended_preparation": [
            f"Learn {skill}"
            for skill in missing
        ]
    }

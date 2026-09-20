from fastapi import APIRouter
from pydantic import BaseModel


router = APIRouter()


class InterviewRequest(BaseModel):

    role: str

    difficulty: str = "medium"

    resume: dict = {}


class AnswerRequest(BaseModel):

    question: str

    answer: str


@router.post("/interview/start")
async def start_interview(
    request: InterviewRequest
):

    return {

        "session_id":
            "demo-session-001",

        "role":
            request.role,

        "difficulty":
            request.difficulty,

        "question":
            f"Tell me about yourself and your experience related to {request.role}."

    }


@router.post("/interview/evaluate")
async def evaluate_answer(
    request: AnswerRequest
):

    return {

        "score": 8,

        "strengths": [
            "Relevant response",
            "Good explanation"
        ],

        "improvements": [
            "Use a structured answer",
            "Include a specific example"
        ],

        "follow_up_question":
            "Can you explain one technical challenge you faced and how you solved it?"

    }


@router.post("/interview/complete")
async def complete_interview():

    return {

        "practice_readiness_score": 82,

        "strengths": [
            "Technical knowledge",
            "Project understanding"
        ],

        "areas_to_improve": [
            "Answer structure",
            "Advanced concepts"
        ]

    }

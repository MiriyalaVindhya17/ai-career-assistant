from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.chat import router as chat_router
from app.api.career import router as career_router
from app.api.interview import router as interview_router
from app.api.documents import router as documents_router


app = FastAPI(
    title="CareerAI",
    description="AI Career and Interview Preparation Chatbot",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)


app.include_router(
    chat_router,
    prefix="/api"
)

app.include_router(
    career_router,
    prefix="/api"
)

app.include_router(
    interview_router,
    prefix="/api"
)

app.include_router(
    documents_router,
    prefix="/api"
)


@app.get("/")
async def root():

    return {
        "name": "CareerAI",
        "status": "running"
    }


@app.get("/api/health")
async def health():

    return {
        "status": "healthy"
    }

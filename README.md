# 🤖 CareerAI — AI Career & Resume Assistant

CareerAI is an AI-powered career assistant chatbot designed to help students and job seekers understand their resumes, identify relevant career paths, discover skill gaps, build personalized learning roadmaps, and prepare for interviews.

## 🚀 Features

- 📄 Resume Upload
- 🔍 Resume Text Extraction
- 🧠 Resume Analysis
- 🎯 Skill Extraction
- 💼 Career Path Recommendations
- 📊 Skill Gap Analysis
- 🗺️ Personalized Career Roadmaps
- 🚀 Project Recommendations
- 🎤 Resume-Based Mock Interviews
- 💬 Resume-Aware Career Chatbot
- 📑 PDF and DOCX Support
- 🌐 React + TypeScript Frontend
- ⚡ FastAPI Backend

## 🏗️ Architecture

```text
                    CareerAI
                       │
                       ▼
                Resume Upload
                       │
              ┌────────┴────────┐
              ▼                 ▼
             PDF               DOCX
              │                 │
              └────────┬────────┘
                       ▼
                Text Extraction
                       │
                       ▼
                 Resume Analysis
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
       Skills      Education     Projects
          │            │            │
          └────────────┼────────────┘
                       ▼
                Career Profile
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
       Career       Skill Gap     Roadmap
       Paths        Analysis
          │            │            │
          └────────────┼────────────┘
                       ▼
                    Chatbot

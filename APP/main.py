from pathlib import Path

from fastapi import Depends
from fastapi import FastAPI
from fastapi import Request

from fastapi.responses import HTMLResponse

from fastapi.staticfiles import StaticFiles

from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from app.ai.gemini import gemini

from app.config import get_settings

from app.database import Base
from app.database import engine
from app.database import get_db

from app.models import Interaction

from app.schemas import TextRequest
from app.schemas import QuizRequest
from app.schemas import LearningRequest

from app.services.qna import answer_question
from app.services.explanation import explain_concept
from app.services.quiz import generate_quiz
from app.services.summary import summarize_text
from app.services.learning_path import get_learning_recommendations


# --------------------------------------------------
# Configuration
# --------------------------------------------------

settings = get_settings()

BASE_DIR = Path(__file__).resolve().parent.parent


# --------------------------------------------------
# Database
# --------------------------------------------------

Base.metadata.create_all(
    bind=engine
)


# --------------------------------------------------
# FastAPI application
# --------------------------------------------------

app = FastAPI(
    title="EduGenie",
    description="Google Gemini Powered Learning Assistant",
    version="1.0.0"
)


# --------------------------------------------------
# Static files
# --------------------------------------------------

app.mount(
    "/static",
    StaticFiles(
        directory=BASE_DIR / "static"
    ),
    name="static"
)


# --------------------------------------------------
# HTML templates
# --------------------------------------------------

templates = Jinja2Templates(
    directory=BASE_DIR / "templates"
)


# --------------------------------------------------
# Helper functions
# --------------------------------------------------

def limit_text(value: str) -> str:

    return value.strip()[
        :settings.max_input_chars
    ]


def save_interaction(
    db: Session,
    task: str,
    user_input: str,
    response: str
):

    interaction = Interaction(
        task=task,
        user_input=user_input,
        response=response
    )

    db.add(interaction)

    db.commit()


# --------------------------------------------------
# Home page
# --------------------------------------------------

@app.get(
    "/",
    response_class=HTMLResponse
)
def home(request: Request):

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "app_name": settings.app_name
        }
    )


# --------------------------------------------------
# Health API
# --------------------------------------------------

@app.get("/api/health")
def health():

    return {
        "status": "ok",
        "application": "EduGenie",
        "gemini_configured": gemini.enabled,
        "model": settings.gemini_model
    }


# --------------------------------------------------
# Q&A API
# --------------------------------------------------

@app.post("/api/qa")
def qa(
    request: TextRequest,
    db: Session = Depends(get_db)
):

    text = limit_text(
        request.text
    )

    answer, source = answer_question(
        text
    )

    save_interaction(
        db,
        "qa",
        text,
        answer
    )

    return {
        "answer": answer,
        "source": source
    }


# --------------------------------------------------
# Explanation API
# --------------------------------------------------

@app.post("/api/explain")
def explain(
    request: TextRequest,
    db: Session = Depends(get_db)
):

    text = limit_text(
        request.text
    )

    explanation, source = explain_concept(
        text
    )

    save_interaction(
        db,
        "explain",
        text,
        explanation
    )

    return {
        "explanation": explanation,
        "source": source
    }


# --------------------------------------------------
# Quiz API
# --------------------------------------------------

@app.post("/api/quiz")
def quiz(
    request: QuizRequest,
    db: Session = Depends(get_db)
):

    text = limit_text(
        request.text
    )

    questions, source = generate_quiz(
        text
    )

    save_interaction(
        db,
        "quiz",
        text,
        str(questions)
    )

    return {
        "questions": questions,
        "source": source
    }


# --------------------------------------------------
# Summary API
# --------------------------------------------------

@app.post("/api/summarize")
def summarize(
    request: TextRequest,
    db: Session = Depends(get_db)
):

    text = limit_text(
        request.text
    )

    summary, source = summarize_text(
        text
    )

    save_interaction(
        db,
        "summarize",
        text,
        summary
    )

    return {
        "summary": summary,
        "source": source
    }


# --------------------------------------------------
# Learning Path API
# --------------------------------------------------

@app.post(
    "/api/learn/recommendations"
)
def learning(
    request: LearningRequest,
    db: Session = Depends(get_db)
):

    topic = request.topic.strip()

    level = request.level.strip()

    recommendations, source = (
        get_learning_recommendations(
            topic,
            level
        )
    )

    save_interaction(
        db,
        "learning_path",
        topic,
        recommendations
    )

    return {
        "recommendations": recommendations,
        "source": source
    }


# --------------------------------------------------
# History API
# --------------------------------------------------

@app.get("/api/history")
def history(
    limit: int = 20,
    db: Session = Depends(get_db)
):

    limit = min(
        max(limit, 1),
        100
    )

    rows = (
        db.query(Interaction)
        .order_by(
            Interaction.id.desc()
        )
        .limit(limit)
        .all()
    )

    return [
        {
            "id": row.id,
            "task": row.task,
            "input": row.user_input,
            "response": row.response,
            "created_at": row.created_at.isoformat()
        }

        for row in rows
    ]
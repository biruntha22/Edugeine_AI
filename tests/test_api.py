from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health():

    response = client.get(
        "/api/health"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"


def test_question_answer():

    response = client.post(
        "/api/qa",
        json={
            "text": "What is a binary tree?"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "answer" in data

    assert "source" in data


def test_explanation():

    response = client.post(
        "/api/explain",
        json={
            "text": "Explain Python"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "explanation" in data


def test_quiz():

    response = client.post(
        "/api/quiz",
        json={
            "text": (
                "A binary tree is a tree "
                "data structure where each "
                "node has at most two children."
            )
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "questions" in data

    assert len(
        data["questions"]
    ) == 3


def test_summary():

    response = client.post(
        "/api/summarize",
        json={
            "text": (
                "Python is a programming "
                "language used for many "
                "different applications."
            )
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "summary" in data


def test_learning_path():

    response = client.post(
        "/api/learn/recommendations",
        json={
            "topic": "Python",
            "level": "beginner"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "recommendations" in data
from app.ai.gemini import gemini


def answer_question(text: str) -> tuple[str, str]:

    prompt = f"""
You are EduGenie, an AI educational assistant.

Answer the student's question accurately.

Rules:

1. Use simple language.
2. Explain the answer clearly.
3. Give a small example when useful.
4. Do not invent sources.
5. Keep the answer suitable for a student.

Student question:

{text}
"""

    if gemini.enabled:

        answer = gemini.generate(
            prompt,
            temperature=0.4,
            max_output_tokens=1200
        )

        return answer, "gemini"

    answer = f"""
Demo Mode

Your question:

{text}

Gemini is not connected yet.

Add your GEMINI_API_KEY inside the .env file
to receive an AI-generated answer.
"""

    return answer.strip(), "demo"
from app.ai.gemini import gemini


def explain_concept(text: str) -> tuple[str, str]:

    prompt = f"""
You are EduGenie, a beginner-friendly educational tutor.

Explain the following concept.

Use this format:

Definition:
Give a simple definition.

Key Points:
1. Explain the first important point.
2. Explain the second important point.
3. Explain the third important point.

Example:
Give one simple real-world or programming example.

Concept:

{text}
"""

    if gemini.enabled:

        answer = gemini.generate(
            prompt,
            temperature=0.3,
            max_output_tokens=1200
        )

        return answer, "gemini"

    answer = f"""
Simple Explanation

Concept:

{text}

Gemini is not connected yet.

Add your Gemini API key in the .env file
to generate a complete AI explanation.
"""

    return answer.strip(), "demo"
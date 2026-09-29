from app.ai.gemini import gemini


def summarize_text(text: str) -> tuple[str, str]:

    prompt = f"""
You are EduGenie, an educational assistant.

Summarize the following educational material.

Requirements:

1. Keep the important facts.
2. Remove unnecessary repetition.
3. Use simple student-friendly language.
4. Use bullet points where appropriate.
5. Do not add information that is not in the original text.

Educational material:

{text}
"""

    if gemini.enabled:

        summary = gemini.generate(
            prompt,
            temperature=0.2,
            max_output_tokens=1000
        )

        return summary, "gemini"

    words = text.split()

    short_text = " ".join(
        words[:80]
    )

    if len(words) > 80:

        short_text += "..."

    answer = f"""
Demo Summary

{short_text}

Gemini is not connected yet.

Add GEMINI_API_KEY in the .env file
for an AI-generated summary.
"""

    return answer.strip(), "demo"
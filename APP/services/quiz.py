from app.ai.gemini import gemini
from app.ai.gemini import parse_json


def fallback_quiz(text: str):

    topic = text.strip().split("\n")[0][:80]

    questions = [

        {
            "question": (
                f"What is the main topic discussed in the given material? "
                f"({topic})"
            ),

            "options": [
                "The main concept",
                "An unrelated topic",
                "A random idea",
                "None of these"
            ],

            "answer": "The main concept",

            "explanation": (
                "This is a demo question. "
                "Connect Gemini for topic-specific questions."
            )
        },

        {
            "question": (
                "What is a good way to learn a new concept?"
            ),

            "options": [
                "Understand the basics and practise",
                "Skip all examples",
                "Memorize without understanding",
                "Avoid revision"
            ],

            "answer": "Understand the basics and practise",

            "explanation": (
                "Understanding and practice help reinforce learning."
            )
        },

        {
            "question": (
                "What should an educational quiz test?"
            ),

            "options": [
                "Understanding of the topic",
                "Typing speed only",
                "Computer screen size",
                "Internet speed"
            ],

            "answer": "Understanding of the topic",

            "explanation": (
                "An educational quiz should measure understanding."
            )
        }
    ]

    return questions


def generate_quiz(text: str) -> tuple[list, str]:

    prompt = f"""
You are EduGenie, an AI educational assistant.

Create exactly 3 multiple-choice questions from
the educational material below.

Each question must contain:

- question
- exactly 4 options
- answer
- explanation

The answer must exactly match one of the four options.

Return ONLY valid JSON.

Use this exact structure:

{{
    "questions": [
        {{
            "question": "Question",
            "options": [
                "Option 1",
                "Option 2",
                "Option 3",
                "Option 4"
            ],
            "answer": "Correct option",
            "explanation": "Short explanation"
        }}
    ]
}}

Educational material:

{text}
"""

    if not gemini.enabled:

        return fallback_quiz(text), "demo"

    try:

        result = gemini.generate(
            prompt,
            temperature=0.3,
            max_output_tokens=1600
        )

        data = parse_json(result)

        if not isinstance(data, dict):

            raise ValueError(
                "Invalid quiz response."
            )

        questions = data.get("questions")

        if not isinstance(questions, list):

            raise ValueError(
                "Questions are missing."
            )

        if len(questions) != 3:

            raise ValueError(
                "Exactly 3 questions are required."
            )

        for question in questions:

            options = question.get("options", [])

            answer = question.get("answer")

            if len(options) != 4:

                raise ValueError(
                    "Each question needs 4 options."
                )

            if answer not in options:

                raise ValueError(
                    "Answer must match an option."
                )

        return questions, "gemini"

    except Exception:

        return fallback_quiz(text), "fallback"from app.ai.gemini import gemini
from app.ai.gemini import parse_json


def fallback_quiz(text: str):

    topic = text.strip().split("\n")[0][:80]

    questions = [

        {
            "question": (
                f"What is the main topic discussed in the given material? "
                f"({topic})"
            ),

            "options": [
                "The main concept",
                "An unrelated topic",
                "A random idea",
                "None of these"
            ],

            "answer": "The main concept",

            "explanation": (
                "This is a demo question. "
                "Connect Gemini for topic-specific questions."
            )
        },

        {
            "question": (
                "What is a good way to learn a new concept?"
            ),

            "options": [
                "Understand the basics and practise",
                "Skip all examples",
                "Memorize without understanding",
                "Avoid revision"
            ],

            "answer": "Understand the basics and practise",

            "explanation": (
                "Understanding and practice help reinforce learning."
            )
        },

        {
            "question": (
                "What should an educational quiz test?"
            ),

            "options": [
                "Understanding of the topic",
                "Typing speed only",
                "Computer screen size",
                "Internet speed"
            ],

            "answer": "Understanding of the topic",

            "explanation": (
                "An educational quiz should measure understanding."
            )
        }
    ]

    return questions


def generate_quiz(text: str) -> tuple[list, str]:

    prompt = f"""
You are EduGenie, an AI educational assistant.

Create exactly 3 multiple-choice questions from
the educational material below.

Each question must contain:

- question
- exactly 4 options
- answer
- explanation

The answer must exactly match one of the four options.

Return ONLY valid JSON.

Use this exact structure:

{{
    "questions": [
        {{
            "question": "Question",
            "options": [
                "Option 1",
                "Option 2",
                "Option 3",
                "Option 4"
            ],
            "answer": "Correct option",
            "explanation": "Short explanation"
        }}
    ]
}}

Educational material:

{text}
"""

    if not gemini.enabled:

        return fallback_quiz(text), "demo"

    try:

        result = gemini.generate(
            prompt,
            temperature=0.3,
            max_output_tokens=1600
        )

        data = parse_json(result)

        if not isinstance(data, dict):

            raise ValueError(
                "Invalid quiz response."
            )

        questions = data.get("questions")

        if not isinstance(questions, list):

            raise ValueError(
                "Questions are missing."
            )

        if len(questions) != 3:

            raise ValueError(
                "Exactly 3 questions are required."
            )

        for question in questions:

            options = question.get("options", [])

            answer = question.get("answer")

            if len(options) != 4:

                raise ValueError(
                    "Each question needs 4 options."
                )

            if answer not in options:

                raise ValueError(
                    "Answer must match an option."
                )

        return questions, "gemini"

    except Exception:

        return fallback_quiz(text), "fallback"
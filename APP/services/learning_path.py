from app.ai.gemini import gemini


def get_learning_recommendations(
    topic: str,
    level: str
) -> tuple[str, str]:

    prompt = f"""
You are EduGenie, a personalized AI learning assistant.

Create a learning path for:

Topic:
{topic}

Learner level:
{level}

Include:

1. Fundamentals
2. Core concepts
3. Practice activities
4. Mini project
5. Advanced concepts
6. Revision

Also suggest approximate learning time
for each stage.

Recommend resource TYPES such as:

- Videos
- Articles
- Documentation
- Books
- Practice websites

Do not invent specific URLs.

Keep the plan practical and student-friendly.
"""

    if gemini.enabled:

        result = gemini.generate(
            prompt,
            temperature=0.5,
            max_output_tokens=1400
        )

        return result, "gemini"

    result = f"""
Demo Learning Path

Topic:
{topic}

Level:
{level}

Stage 1 - Fundamentals
Learn the basic concepts.

Stage 2 - Core Concepts
Study the important concepts and terminology.

Stage 3 - Practice
Solve exercises and small problems.

Stage 4 - Mini Project
Build a small project using the topic.

Stage 5 - Advanced Concepts
Move to advanced topics after understanding the basics.

Stage 6 - Revision
Revise the concepts and practise questions.

Connect Gemini using GEMINI_API_KEY
for personalized recommendations.
"""

    return result.strip(), "demo"
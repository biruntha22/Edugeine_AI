import json
import re

from typing import Any

from google import genai
from google.genai import types

from app.config import get_settings


class GeminiService:

    def __init__(self):

        self.settings = get_settings()

        if self.settings.gemini_api_key:

            self.client = genai.Client(
                api_key=self.settings.gemini_api_key
            )

        else:

            self.client = None

    @property
    def enabled(self) -> bool:

        return self.client is not None

    def generate(
        self,
        prompt: str,
        temperature: float = 0.4,
        max_output_tokens: int = 1200
    ) -> str:

        if not self.client:

            raise RuntimeError(
                "Gemini API key is not configured."
            )

        response = self.client.models.generate_content(

            model=self.settings.gemini_model,

            contents=prompt,

            config=types.GenerateContentConfig(

                temperature=temperature,

                max_output_tokens=max_output_tokens
            )
        )

        result = getattr(response, "text", None)

        if not result:

            raise RuntimeError(
                "Gemini returned an empty response."
            )

        return result.strip()


def clean_json_block(value: str) -> str:

    value = value.strip()

    value = re.sub(
        r"^```(?:json)?\s*",
        "",
        value,
        flags=re.IGNORECASE
    )

    value = re.sub(
        r"\s*```$",
        "",
        value
    )

    return value.strip()


def parse_json(value: str) -> Any:

    cleaned = clean_json_block(value)

    return json.loads(cleaned)


gemini = GeminiService()
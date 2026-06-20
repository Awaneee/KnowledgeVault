import requests


class LLMService:
    OLLAMA_URL = "http://localhost:11434/api/generate"
    MODEL = "phi3:mini"

    @classmethod
    def generate(
        cls,
        prompt: str,
        response_format: str | None = None
    ):
        payload = {
            "model": cls.MODEL,
            "prompt": prompt,
            "stream": False
        }

        if response_format:
            payload["format"] = response_format

        response = requests.post(
            cls.OLLAMA_URL,
            json=payload,
            timeout=60
        )

        response.raise_for_status()

        return response.json()["response"]

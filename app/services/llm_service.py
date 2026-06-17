import requests


class LLMService:
    OLLAMA_URL = "http://localhost:11434/api/generate"
    MODEL = "llama3:latest"

    @classmethod
    def generate(cls, prompt: str):

        response = requests.post(
            cls.OLLAMA_URL,
            json={
                "model": cls.MODEL,
                "prompt": prompt,
                "stream": False
            }
        )

        response.raise_for_status()

        return response.json()["response"]
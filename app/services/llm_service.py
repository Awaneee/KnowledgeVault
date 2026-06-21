import requests


class LLMService:
    OLLAMA_URL = "http://localhost:11434/api/generate"

    INTENT_MODEL = "phi3:mini"
    TITLE_MODEL = "phi3:mini"
    ASK_MODEL = "llama3"

    @classmethod
    def generate(
        cls,
        prompt: str,
        response_format: str | None = None,
        model: str | None = None
    ):
        selected_model = model or cls.INTENT_MODEL

        payload = {
            "model": selected_model,
            "prompt": prompt,
            "stream": False
        }

        if response_format:
            payload["format"] = response_format

        print("USING MODEL:", selected_model)

        response = requests.post(
            cls.OLLAMA_URL,
            json=payload,
            timeout=120
        )

        response.raise_for_status()

        return response.json()["response"]
import json

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

    @classmethod
    def generate_stream(
        cls,
        prompt: str,
        model: str | None = None
    ):
        """
        Token-by-token generator over Ollama's streaming API.

        Yields decoded text chunks as they arrive instead of blocking
        until the full answer is ready. Used by the Ask endpoint so the
        user sees the answer forming instead of waiting ~50s+ for a
        single response. Falls back to nothing special on error - the
        caller (StreamingResponse) will just stop if Ollama drops the
        connection; that's surfaced as a short/cut-off answer rather
        than a 500, which is generally the safer failure mode for a
        streaming endpoint that's already mid-response to the client.
        """
        selected_model = model or cls.ASK_MODEL

        payload = {
            "model": selected_model,
            "prompt": prompt,
            "stream": True
        }

        with requests.post(
            cls.OLLAMA_URL,
            json=payload,
            timeout=120,
            stream=True
        ) as response:
            response.raise_for_status()

            for line in response.iter_lines():
                if not line:
                    continue

                chunk = json.loads(line)
                token = chunk.get("response", "")

                if token:
                    yield token

                if chunk.get("done"):
                    break
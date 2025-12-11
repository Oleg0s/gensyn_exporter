import json
import random

import requests

openrouter_free_model_list = [
    "amazon/nova-2-lite-v1:free",
    # "tngtech/tng-r1t-chimera:free",
    "kwaipilot/kat-coder-pro:free",
    # "google/gemma-3n-e2b-it:free",
    # "tngtech/deepseek-r1t2-chimera:free",
    "google/gemma-3-4b-it:free",
    # "meta-llama/llama-3.3-70b-instruct:free",
    # "nousresearch/hermes-3-llama-3.1-405b:free"
]

openrouter_model_list = [
    # "openai/gpt-oss-120b",
    # "anthropic/claude-sonnet-4.5",
    "qwen/qwen-2.5-coder-32b-instruct"
]


class OpenRouterClient:
    def __init__(self, api_key: str, model: str = "deepseek/deepseek-chat"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"

    def get_chat_response(self, prompt: str) -> str:
        self.model = random.choice(openrouter_free_model_list)
        print(f"Using model: {self.model}")
        response = requests.post(
            url=self.base_url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://nuts-accountant.local",  
                "X-Title": "Gensyn Bot",
            },
            data=json.dumps({
                "model": self.model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 1,
            })
        )

        if response.status_code != 200:
            raise Exception(
                f"OpenRouter API error: {response.status_code} - {response.text}")

        result = response.json()
        return result["choices"][0]["message"]["content"]

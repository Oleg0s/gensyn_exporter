import json
import random

import requests

openrouter_free_model_list = [
    "amazon/nova-2-lite-v1:free",
    "arcee-ai/trinity-mini:free",
    "tngtech/tng-r1t-chimera:free",
    "allenai/olmo-3-32b-think:free",
    "kwaipilot/kat-coder-pro:free",
    "nvidia/nemotron-nano-12b-v2-vl:free",
    "alibaba/tongyi-deepresearch-30b-a3b:free",
    "meituan/longcat-flash-chat:free",
    "nvidia/nemotron-nano-9b-v2:free",
    "openai/gpt-oss-120b:free",
    "z-ai/glm-4.5-air:free",
    "qwen/qwen3-coder:free",
    "moonshotai/kimi-k2:free",
    "cognitivecomputations/dolphin-mistral-24b-venice-edition:free",
    "google/gemma-3n-e2b-it:free",
    "tngtech/deepseek-r1t2-chimera:free",
    "google/gemma-3n-e4b-it:free",
    "qwen/qwen3-4b:free",
    "qwen/qwen3-235b-a22b:free",
    "tngtech/deepseek-r1t-chimera:free",
    "mistralai/mistral-small-3.1-24b-instruct:free",
    "google/gemma-3-4b-it:free",
    "google/gemma-3-12b-it:free",
    "google/gemini-2.0-flash-exp:free",
    "meta-llama/llama-3.3-70b-instruct:free",
    "nousresearch/hermes-3-llama-3.1-405b:free"
]


class OpenRouterClient:
    def __init__(self, api_key: str, model: str = "deepseek/deepseek-chat"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"

    def get_chat_response(self, prompt: str) -> str:
        self.model = random.choice(openrouter_free_model_list)
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

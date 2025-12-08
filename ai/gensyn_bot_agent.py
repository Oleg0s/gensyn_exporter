from typing import Protocol
from pathlib import Path
from datetime import datetime, timedelta


class AIApi(Protocol):
    model: str
    def get_chat_response(self, prompt: str) -> str:
        ...

class GensynBotAgent:
    def __init__(self, ai_api:AIApi, propmpt_formatter, prompt_path:Path|None = None):
        self.ai_api = ai_api
        self.prompt_formatter = propmpt_formatter
        self.prompt_path = prompt_path
        if prompt_path is None:
            self.prompt_path = Path("ai/prompt.txt")
    
    def analyse_messages(self, messages_raw:list):
        system_prompt = self.prompt_formatter.format_prompt(
            self.prompt_path, system_messages=self._format_tweets(messages_raw))
        return self.ai_api.get_chat_response(system_prompt)
    
    def _format_tweets(self, messages: list) -> str:
        formatted = ""
        for message in messages:
            formatted += f"{message}\n"

        return formatted
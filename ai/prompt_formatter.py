import os
from pathlib import Path


class PromptFormatter:
    def load_prompt(self, filepath) -> str:
        path = Path(filepath) if isinstance(filepath, str) else filepath

        with path.open('r', encoding='utf-8') as f:
            return f.read().strip()

    def format_prompt(self, filepath, **kwargs) -> str:
        template = self.load_prompt(filepath)
        return template.format(**kwargs)

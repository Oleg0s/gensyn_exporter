from pathlib import Path
from ai.openrouter import OpenRouterClient
from ai.prompt_formatter import PromptFormatter
from ai.gensyn_bot_agent import GensynBotAgent
import config

if __name__ == "__main__":
    open_router = OpenRouterClient(config.openrouter_api_key, config.openrouter_model_name)
    prompt_formatter = PromptFormatter()
    agent = GensynBotAgent(open_router, prompt_formatter, Path("ai/prompt.txt"))
    a = agent.analyse_messages(["Oleg0s:ZYBf is alive!", "Pavel:P2rT is DEAD!"])
    print(a)


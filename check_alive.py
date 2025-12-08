import requests
from config import PROMETHEUS_URL, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
import time
from pathlib import Path
from ai.openrouter import OpenRouterClient
from ai.prompt_formatter import PromptFormatter
from ai.gensyn_bot_agent import GensynBotAgent
import config


def query_prometheus(query):
    response = requests.get(
        f'{PROMETHEUS_URL}/api/v1/query',
        params={'query': query}
    )
    return response.json()


def get_statuses():
    result = query_prometheus('gensyn_votes{} - gensyn_votes{} offset 4h')
    nodes = {F"{r['metric']['group']}:{r['metric']['short_id']}": r['value'][1] != '0' for r in
             result['data']['result']}

    return nodes


def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    requests.post(url, json=data)


if __name__ == "__main__":
    open_router = OpenRouterClient(config.openrouter_api_key, config.openrouter_model_name)
    prompt_formatter = PromptFormatter()
    agent = GensynBotAgent(open_router, prompt_formatter, Path("ai/prompt.txt"))

    old_status = get_statuses()
    while True:
        time.sleep(60)

        print("Checking statuses...")
        try:
            new_status = get_statuses()
        except Exception as e:
            print(f"Error checking statuses: {e}")
            continue

        messages = []
        for node, alive in new_status.items():
            if alive and (node not in old_status or not old_status[node]):
                message = f"{node} is alive!"
                print(message)
                #send_telegram_message(message)
                messages.append(message)
            if not alive and node in old_status and old_status[node]:
                message = f"{node} is DEAD!"
                print(message)
                #send_telegram_message(message)
                messages.append(message)

        if messages:
            try:
                ai_answer = agent.analyse_messages(messages)
                send_telegram_message(f"[{agent.ai_api.model}]\n{ai_answer}")
            except Exception as e:
                tmess = f"[{agent.ai_api.model}]\n" + '\n'.join(messages)
                send_telegram_message(tmess)

        old_status = new_status

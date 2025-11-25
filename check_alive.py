import requests
from config import PROMETHEUS_URL
import time


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


if __name__ == "__main__":
    old_status = get_statuses()
    while True:
        time.sleep(5)

        print("Checking statuses...")
        new_status = get_statuses()
        for node, alive in new_status.items():
            if alive and (node not in old_status or not old_status[node]):
                print(f"{node} is alive!")
            if not alive and node in old_status and old_status[node]:
                print(f"{node} is dead!")
        old_status = new_status

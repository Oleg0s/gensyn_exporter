from gensyn_contract import GensynContract, GensynOldContract
from peers import peers
import time
from config import TAG
from redis_store import RedisStore


def scan():
    rewards = {group: {peer: 0 for peer in g_peers} for group, g_peers in peers.items()}
    wins = {group: {peer: 0 for peer in g_peers} for group, g_peers in peers.items()}
    votes = {group: {peer: 0 for peer in g_peers} for group, g_peers in peers.items()}

    for c in [GensynOldContract(), GensynContract()]:
        for group, g_peers in peers.items():
            result = c.getTotalRewards(g_peers)
            print(f"Rewards scanned {group} group for {c.name}")
            for i in range(len(result)):
                rewards[group][g_peers[i]] += result[i]
        for group, g_peers in peers.items():
            for peer in g_peers:
                wins[group][peer] += c.getTotalWins(peer)
                print(f"Wins scanned {peer} for {c.name}")
        for group, g_peers in peers.items():
            for peer in g_peers:
                votes[group][peer] += c.getVoterVoteCount(peer)
                print(f"Votes scanned {peer} for {c.name}")

    redis = RedisStore()
    redis.set(f"{TAG}:rewards", rewards)
    redis.set(f"{TAG}:wins", wins)
    redis.set(f"{TAG}:votes", votes)


if __name__ == "__main__":
    while True:
        scan()
        time.sleep(600)

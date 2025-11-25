from flask import Flask, jsonify, Response
from flask_caching import Cache
from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST
from gensyn_contract import GensynContract, GensynOldContract
from peers import peers
from config import TAG
from redis_store import RedisStore

gensyn_rewards_gauge = Gauge('gensyn_rewards', 'Gensyn rewards by peer id', ['group', 'peer_id', 'short_id'])
gensyn_wins_gauge = Gauge('gensyn_wins', 'Gensyn wins by peer id', ['group', 'peer_id', 'short_id'])
gensyn_votes_gauge = Gauge('gensyn_votes', 'Gensyn votes by peer id', ['group', 'peer_id', 'short_id'])

app = Flask(__name__)
app.config['CACHE_TYPE'] = 'simple'  # for simple in-memory cache, or use 'redis', 'memcached', etc.
cache = Cache(app)

@app.route('/')
@cache.cached(timeout=60)
def home():
    return jsonify({"result": "Ok"})

@app.route('/metrics')
@cache.cached(timeout=3)
def metrics():
    gensyn_rewards_gauge.clear()
    gensyn_wins_gauge.clear()
    gensyn_votes_gauge.clear()

    redis = RedisStore()
    rewards = redis.get(f"{TAG}:rewards")
    wins = redis.get(f"{TAG}:wins")
    votes = redis.get(f"{TAG}:votes")

    for group, g_peers in peers.items():
        for peer in g_peers:
            gensyn_rewards_gauge.labels(group=group, peer_id=peer, short_id=peer[-4:]).set(rewards[group][peer])
            gensyn_wins_gauge.labels(group=group, peer_id=peer, short_id=peer[-4:]).set(wins[group][peer])
            gensyn_votes_gauge.labels(group=group, peer_id=peer, short_id=peer[-4:]).set(votes[group][peer])

    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3437)
    # gunicorn -b 0.0.0.0:3437 stats_flask:app

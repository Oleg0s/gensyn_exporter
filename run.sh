# gunicorn -b 0.0.0.0:3434 stats_flask:app

docker build -t cats/gensyn-exporter .

docker stop gensyn-exporter
docker rm gensyn-exporter
docker run -dit --restart always --name gensyn-exporter -p 3437:3437 cats/gensyn-exporter gunicorn -t 120 -w 4 -b 0.0.0.0:3437 exporter:app

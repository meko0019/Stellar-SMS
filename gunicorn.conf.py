import multiprocessing
import os

debug = os.environ.get("DEBUG", False)

loglevel = "debug" if debug else "info"

# Settings from http://docs.gunicorn.org/en/stable/settings.html#settings
port = int(os.environ.get("PORT", "8000"))
bind = f"0.0.0.0:{port}"
reuse_port = True

reload = debug
preload_app = not debug

backlog = 2048
max_requests = 2048
max_requests_jitter = 128
keepalive = 5

workers = min(multiprocessing.cpu_count() * 2 + 1, 16)
worker_class = "gevent"
worker_connections = 1000

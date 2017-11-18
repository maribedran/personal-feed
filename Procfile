web: gunicorn personal_feed.wsgi --limit-request-line 8188 --log-file -
worker: celery worker --app=personal_feed --loglevel=info

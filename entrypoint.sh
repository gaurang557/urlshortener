celery -A shortener worker &
celery -A shortener beat &
gunicorn shortener.wsgi:application --bind 0.0.0.0:8000
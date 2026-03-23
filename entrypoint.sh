celery -A shortener worker &
gunicorn shortener.wsgi:application --bind 0.0.0.0:8000
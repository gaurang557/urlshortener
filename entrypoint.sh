celery -A shortener worker --concurrency 1 &
celery -A shortener beat &
gunicorn shortener.wsgi:application --bind 0.0.0.0:8000
  --workers 1 \
  --threads 4 \
  --timeout 60
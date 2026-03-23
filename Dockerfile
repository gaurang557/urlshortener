FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt
RUN python manage.py collecstatic --noinput
# EXPOSE 8000
CMD ["gunicorn", "shortener.wsgi:application", "--bind", "0.0.0.0:8000"]
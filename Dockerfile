FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt
RUN python manage.py collectstatic --noinput
EXPOSE 8000
RUN useradd -m appuser
RUN chown -R appuser:appuser /app
RUN chmod -R 555 /app
ENTRYPOINT /app/entrypoint.sh
FROM python:3.12-alpine

WORKDIR "/app"

COPY /backend /app/backend
COPY /requirements.txt /app
COPY /alembic.ini /app

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "-m", "backend.main"]

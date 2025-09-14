FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

ENV HOST 0.0.0.0

# Run migrations before starting the app
CMD alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port 8000
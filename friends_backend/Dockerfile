FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip3 install -r /app/requirements.txt --no-cache-dir

COPY . .


CMD ["gunicorn", "friends_backend.wsgi:application", "--bind", "0:8000" ] 
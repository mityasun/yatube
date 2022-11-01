FROM python:3.9.8-slim

WORKDIR /app

COPY requirements.txt /app

RUN pip install -r /app/requirements.txt --no-cache-dir

COPY .. /app

LABEL project='yatube' version=1.0

CMD ["gunicorn", "yatube.wsgi:application", "--bind", "0:8000" ]
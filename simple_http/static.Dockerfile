FROM python:3.11-slim

WORKDIR /app

COPY static_server.py .
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir

EXPOSE 8060

CMD ["python", "static_server.py"]
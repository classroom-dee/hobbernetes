FROM python:3.11-slim

WORKDIR /app

COPY logger.py .
# maybe a pod just for the helper in the future?
COPY helper.py .

CMD ["python", "logger.py"]
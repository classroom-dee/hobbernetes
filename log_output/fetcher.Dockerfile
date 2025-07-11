FROM python:3.11-slim

WORKDIR /app

COPY fetcher.py .
COPY helper.py .

EXPOSE 8088

CMD ["python", "fetcher.py"]
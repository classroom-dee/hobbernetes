FROM python:3.11-slim


WORKDIR /app

COPY fetcher.py .
COPY helper.py .
COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

EXPOSE 8088

CMD ["python", "fetcher.py"]
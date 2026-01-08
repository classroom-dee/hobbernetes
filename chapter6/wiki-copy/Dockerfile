FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY simple_parser.py .

# hadolint ignore=DL3013
RUN pip install --no-cache-dir requests beautifulsoup4 \
  && useradd -m wiki-user

USER wiki-user

CMD ["python", "simple_parser.py"]
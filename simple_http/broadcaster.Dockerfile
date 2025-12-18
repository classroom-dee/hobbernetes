FROM python:3.11-slim

# Prevent Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Create non-root user
RUN useradd -m nootnoot

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY broadcaster.py .

USER nootnoot

CMD ["python", "-m", "broadcaster"]

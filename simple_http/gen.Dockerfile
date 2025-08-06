FROM python:3.11-slim

WORKDIR /app

COPY gen_app.py /app/
RUN pip install requests --no-cache-dir

CMD ["python", "gen_app.py"]
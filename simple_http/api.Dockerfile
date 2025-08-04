FROM python:3.11-slim

WORKDIR /app

COPY api_server.py requirements.txt api_utils.py /app/
RUN pip install -r requirements.txt --no-cache-dir

EXPOSE 8061

CMD ["python", "api_server.py"]
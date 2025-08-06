FROM python:3.11-slim

WORKDIR /app

COPY static_server.py static_utils.py requirements.txt /app/
COPY static/ /app/static/
RUN pip install -r requirements.txt --no-cache-dir

EXPOSE 8060

CMD ["python", "static_server.py"]

# Debug
# CMD ["python", "-c", "import os, sys; print(repr(os.environ.get('STATIC_CACHE_DIR')), file=sys.stderr, flush=True); import time; time.sleep(3600)"]
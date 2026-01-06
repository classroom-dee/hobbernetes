FROM python:3.11-slim


WORKDIR /app

COPY greeter.py .

EXPOSE 8088

CMD ["python", "greeter.py"]
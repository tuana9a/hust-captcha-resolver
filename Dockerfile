FROM python:3.8-slim-bullseye
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY weights-2021.04.05.pth .
COPY main.py .
COPY weights.yaml .
EXPOSE 8080
CMD uvicorn main:app --host $BIND --port $PORT
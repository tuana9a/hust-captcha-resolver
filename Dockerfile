FROM python:3.8-slim-bullseye
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY weights-2021.04.05.pth .
COPY weights.yaml .
COPY main.py .
CMD ["python", "main.py"]

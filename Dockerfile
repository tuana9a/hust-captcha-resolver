FROM python:3.8-slim-bullseye

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY weights* .

COPY main.py main.py

EXPOSE 5000

CMD python main.py
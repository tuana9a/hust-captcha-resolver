# notice the downloaded filename via wget, change it correctly in the weights.yaml file
FROM busybox as WEIGHT
WORKDIR /tmp
RUN wget https://public.tuana9a.com/hust-captcha-resolver/weights-2021.04.05.pth

FROM python:3.8-slim-bullseye
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY --from=WEIGHT /tmp/weights-2021.04.05.pth .
COPY weights.yaml .
COPY main.py .
COPY index.html .
CMD ["python", "main.py"]

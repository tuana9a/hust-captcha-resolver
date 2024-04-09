# notice the downloaded filename via wget, change it correctly in the weights.yaml file
FROM busybox as WEIGHT
RUN wget https://public.tuana9a.com/hust-captcha-resolver/weights-2021.04.05.pth -O /weights.pth

FROM python:3.8-slim-bullseye
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY --from=WEIGHT /weights.pth .
COPY weights.yaml .
COPY main.py .
COPY index.html .
USER nobody
CMD ["python", "main.py"]

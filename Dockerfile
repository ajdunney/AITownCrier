FROM python:3.8-slim-buster

WORKDIR /app

ADD . /app

RUN mkdir -p /app/src/ai_town_crier/resources

RUN pip install --no-cache-dir -r requirements.txt

ENV CLI_ARGS=""

CMD python -u /app/src/ai_town_crier/main.py --service twitter ${CLI_ARGS}

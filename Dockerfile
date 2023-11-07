FROM python:3.8-slim-buster

COPY /src/*.py /app/
COPY /data/anime_prep.csv /app/
COPY requirements.txt /app/

WORKDIR /app/

RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN pip install fastapi uvicorn

RUN python similitary.py

CMD uvicorn server:app --reload --host 0.0.0.0 --port 80

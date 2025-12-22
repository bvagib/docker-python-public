FROM python:3.10-alpine

RUN apk add gdal-dev gcc libc-dev g++ proj-dev

COPY ./requirements.txt /

RUN pip install --upgrade pip

RUN pip install -r /requirements.txt

COPY ./src /app

CMD ["sh", "-c", "python3 /app/main.py"]
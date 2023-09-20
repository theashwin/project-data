FROM python:3.10-slim

WORKDIR /

COPY requirements.txt requirements.txt

RUN apt-get update
RUN apt-get install libpq-dev python3-dev gcc -y
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY src src
COPY tests src

RUN pytest src/

CMD sleep 10
CMD ["python", "src/main.py"]

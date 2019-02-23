FROM python:3.6.4-slim

WORKDIR /app

# COPY ./pip.conf /etc/pip.conf
COPY ./requirements.txt /app/

# Do all these operations in one RUN command so that we write a smaller, single layer. Reduces container size.
# RUN apt-get update && \

RUN apt-get update && \
    apt-get install -y mysql-client curl gcc python3-lxml libffi-dev libssl-dev libmysqlclient-dev && \
    pip install -U pip && \
    pip install -r /app/requirements.txt

COPY . /app/

CMD ["python", "/app/app.py"]

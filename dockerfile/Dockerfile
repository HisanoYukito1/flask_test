FROM debian:bullseye-slim

RUN apt update && apt install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*
RUN pip3 install -U pip && pip3 install \
    flask \
    matplotlib \
    pandas
RUN mkdir /data /tmp/app
RUN export FLASK_APP=app

EXPOSE 5000

CMD [ "python3", "app.py" ]
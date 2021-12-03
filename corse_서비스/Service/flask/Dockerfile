FROM python:3.8

WORKDIR /app

ADD . /app
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install coreutils -y


CMD ["uwsgi","uwsgi.ini"]

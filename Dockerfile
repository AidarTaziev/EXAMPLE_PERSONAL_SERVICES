FROM python:3.7.6

WORKDIR /usr/projects/current
COPY requirements.txt ./
RUN pip install -r requirements.txt
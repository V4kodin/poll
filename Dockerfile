FROM python:3
ENV PYTHONUNBUFFERED 1
COPY poll/ /poll/
COPY requirements.txt /poll/
WORKDIR /poll
RUN pip install --upgrade pip && pip install -r requirements.txt

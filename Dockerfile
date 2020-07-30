FROM python:3.8.1-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH $PYTHONPATH:/migrations

RUN useradd -ms /bin/bash app

WORKDIR /home/app

RUN pip install --upgrade pip

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN pip install -r requirements.txt

RUN chown -R app:app ./
USER app

COPY ./ /home/app

EXPOSE 5000
ENTRYPOINT python main.py
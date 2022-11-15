FROM python:3.12-rc-bullseye
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
WORKDIR /home/app
COPY build/requirements.txt .
COPY src/app.py .
LABEL author="Jack Jackman"
LABEL author_contact="jack.jackman@waltoninstitute.ie"

RUN pip install -r requirements.txt

EXPOSE 5000 5007


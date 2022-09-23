FROM python:3
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
WORKDIR /home/app
COPY requirements.txt .
LABEL author="Jack Jackman"
LABEL author_contact="jack.jackman@waltoninstitute.ie"

RUN pip install -r requirements.txt

EXPOSE 5000 5007


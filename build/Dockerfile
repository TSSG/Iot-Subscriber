FROM ubuntu:lunar-20230301
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
WORKDIR /home/app
COPY build/requirements.txt .
COPY src/app.py .
LABEL author="Jack Jackman"
LABEL author_contact="jack.jackman@waltoninstitute.ie"
RUN apt-get update && \
    apt-get install -y \
    python3 \
    python3-pip
RUN pip3 install -r requirements.txt --break-system-packages
EXPOSE 5000 5007


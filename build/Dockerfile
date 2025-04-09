FROM ubuntu:noble-20250404
LABEL author="Jack Jackman"
LABEL author_contact="jack.jackman@waltoninstitute.ie"

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PY_ENV=/opt/py-venv

RUN apt-get update && \
    apt-get install -y \
    python3.12 \
    python3.12-venv \
    python3-pip

#WORKDIR /home/app
#COPY build/requirements.txt .
#COPY src/app.py .

WORKDIR /code
COPY . code/
#COPY build/requirements.txt /code/

RUN python3 -m venv $PY_ENV
ENV PATH="${PY_ENV}/bin:$PATH"
RUN pip install -r code/build/requirements.txt

#RUN pip3 install -r requirements.txt --break-system-packages
#EXPOSE 5000 5007


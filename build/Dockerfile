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

WORKDIR /code
COPY . code/

RUN python3 -m venv $PY_ENV
ENV PATH="${PY_ENV}/bin:$PATH"
RUN pip install -r code/build/requirements.txt

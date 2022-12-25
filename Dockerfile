FROM python:3.7.3
ENV PYTHONUNBUFFERED 1

WORKDIR /SWE-573.01

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install ez_setup
RUN pip install -r requirements.txt

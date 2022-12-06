FROM python:3.7.3
ENV PYTHONUNBUFFERED 1
RUN mkdir /SWE-573.01

WORKDIR /SWE-573.01

COPY . /SWE-573.01/

RUN pip install -r requirements.txt

EXPOSE 8000
ENV LC_ALL=en_US.UTF8
CMD ["python", "manage.py", "makemigrations"]
CMD ["python", "manage.py", "migrate"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

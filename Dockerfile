FROM python:3

ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY . /code
RUN pip install -r requirements.txt && cd /code/src/scheduling_system && python manage.py makemigrations && python manage.py migrate

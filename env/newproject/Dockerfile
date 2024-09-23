FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    postgresql-client


COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .


RUN python manage.py collectstatic --noinput


EXPOSE 8000


CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "newproject.asgi:application"]

FROM python:3.11-slim

WORKDIR /pytime

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

CMD python manage.py migrate \
    && python manage.py collectstatic --noinput \
    && gunicorn PyTime_Project.wsgi:application --bind 0.0.0.0:8000 --log-level info

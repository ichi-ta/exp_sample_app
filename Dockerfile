FROM python:3.11-bullseye

RUN pip install Flask==2.2.3 Flask-SQLAlchemy Flask-Migrate flask-login mysqlclient

WORKDIR /app
COPY run.py run.py
COPY test_app test_app

EXPOSE 8080

CMD ["python", "run.py"]
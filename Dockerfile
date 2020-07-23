FROM python:alpine

COPY requirements.txt /requirements.txt

RUN pip3 install -r /requirements.txt

COPY app.py /app.py

ENV PORT=5000

EXPOSE 5000

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app

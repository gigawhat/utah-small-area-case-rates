FROM python:alpine

COPY requirements.txt /requirements.txt

RUN pip3 install -r /requirements.txt

COPY main.py /main.py

ENV PORT=5000

EXPOSE 5000

CMD ["python3", "/main.py"]

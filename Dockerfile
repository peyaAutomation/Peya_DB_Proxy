FROM python:3.6.5

WORKDIR /app

RUN pip3 install uwsgi

RUN pip3 install --upgrade pip

COPY requirements.txt /app/requirements.txt

RUN pip3 install -r requirements.txt

COPY . /app/

EXPOSE 4500

CMD ["python3", "server.py"]

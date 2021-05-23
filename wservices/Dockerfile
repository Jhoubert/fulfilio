#Debian based docker image
FROM python:3.8-slim-buster

#Installing python dependencies
COPY requirements.txt /usr/src/app/requirements.txt
WORKDIR /usr/src/app
RUN pip install -r requirements.txt
COPY . /usr/src/app


CMD ["python", "/usr/src/app/app.py"]

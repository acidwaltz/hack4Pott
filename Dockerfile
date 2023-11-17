# python based on ubuntu
FROM python:3.8

# define working director inside the docker
WORKDIR /usr/src/web

# copy from here to current working DIR
COPY requirements.txt requirements.txt

# install requirments
RUN pip install --no-cache-dir -r requirements.txt

# copy everything from current to working DIR
COPY . .

CMD gunicorn -b 0.0.0.0:8000 --access-logfile - "base:create_app()"


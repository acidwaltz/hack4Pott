This runs the flask app
1- create virtual env
2- install requirements
3- run the following command :   gunicorn -b 0.0.0.0:8000 "base:create_app()"
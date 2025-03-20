# https://medium.com/@sharma39vishal/basic-python-flask-rabbitmq-celery-mysql-project-bdc3028f5f9

# brew install rabbitmq
# CONF_ENV_FILE="/opt/homebrew/etc/rabbitmq/rabbitmq-env.conf" /opt/homebrew/opt/rabbitmq/sbin/rabbitmq-server

# celery -A tasks worker --loglevel=INFO

from celery import Celery
import time

app = Celery('tasks', backend='rpc://', broker='amqp://guest:guest@localhost:5672//')

@app.task(bind=True)
def add(self, x, y):
    time.sleep(5)
    result = x + y
    return result

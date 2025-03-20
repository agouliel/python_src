# https://medium.com/exsq-engineering-hub/asynchronous-task-processing-with-celery-rabbitmq-and-flask-a-complete-guide-to-deployment-on-189d6d957d48

# brew install rabbitmq
# CONF_ENV_FILE="/opt/homebrew/etc/rabbitmq/rabbitmq-env.conf" /opt/homebrew/opt/rabbitmq/sbin/rabbitmq-server

# pip install celery
# celery -A app2.celery worker --loglevel=INFO

# flask --app app2 run
# curl -X POST http://127.0.0.1:5000/start-task -H "Content-Type: application/json" -d '{}'
# curl "http://127.0.0.1:5000/get-result/90c6cdc1-f3fb-4c42-b042-b7ade9e852b2"

# test without flask:
# from celery import Celery
# celery = Celery('app2', broker='amqp://guest:guest@localhost:5672//')
# celery.conf.update(CELERY_RESULT_BACKEND='rpc://')
# @celery.task(bind=True)
# def long_running_task(self, duration):
#    time.sleep(duration)
#    return f"Task completed after {duration} seconds."
# task = long_running_task.apply_async(args=[5])
# task.state

from flask import Flask, jsonify, request
from celery import Celery
import time

app = Flask(__name__)

# Configure Celery with RabbitMQ
app.config['CELERY_BROKER_URL'] = 'amqp://guest:guest@localhost:5672//'
app.config['CELERY_RESULT_BACKEND'] = 'rpc://'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# Celery task
@celery.task(bind=True)
def long_running_task(self, duration):
    time.sleep(duration)
    return f"Task completed after {duration} seconds."

# Start task API endpoint
@app.route('/start-task', methods=['POST'])
def start_task():
    duration = request.json.get('duration', 5)
    task = long_running_task.apply_async(args=[duration])
    return jsonify({"task_id": task.id}), 202

# Get task result API endpoint
@app.route('/get-result/<string:task_id>', methods=['GET'])
def get_result(task_id):
    task = long_running_task.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {"status": "PENDING"}
    elif task.state == 'SUCCESS':
        response = {"status": "SUCCESS", "result": task.result}
    else:
        response = {"status": "FAILURE"}

    return jsonify(response)
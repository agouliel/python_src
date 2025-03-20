from tasks import add  

# Call the 'add' task function asynchronously and store the result
#result = add.delay(4, 4)

# Check if the result is ready (completed)
#print(result.ready())

# Print the status of the result
#print(result.status)

# Print the actual result of the task (if it's completed)
#print(result.result)

# Print the result object itself (useful for debugging and introspection)
#print(result)

#------------------------------------------------------------------------

from flask import Flask, request, jsonify

# Create a Flask app instance
app = Flask(__name__)

# Create a Celery instance named 'celery_app'
#celery_app = Celery('tasks', broker='amqp://guest:guest@localhost:5672//', backend='rpc://') # instead of 'tasks' we could use app.name

# Configure Celery settings
#celery_app.conf.update(
    #CELERY_RESULT_BACKEND='rpc://',
    #CELERY_TASK_SERIALIZER='json', # Set the task serializer to JSON
    #CELERY_IGNORE_RESULT=False, # Do not ignore results (set to False)
#)

# Define a route for adding data using a POST request
@app.route('/add', methods=['POST'])
def adddata():
    try:
        # Extract data from JSON request
        # example: {"x":5,"y":1}
        # curl -X POST http://127.0.0.1:5000/add -H "Content-Type: application/json" -d '{"x":5,"y":1}'
        data = request.get_json()
        x = data['x']
        y = data['y']
        
        # Call the 'add' task asynchronously and get the result object
        result = add.delay(x, y)
        
        # Return the task ID as a JSON response
        return jsonify({'Task ID': result.id})
    except Exception as e:
        return jsonify({'error': str(e)})

# Define a route for getting the status of a task
@app.route('/getstatus/<string:task_id>')
def gettaskstatus(task_id):
    try:
        # Get the status of the task using the task ID
        # celery_app.AsyncResult was wrong
        task_status = add.AsyncResult(task_id).status
        
        return jsonify({'Task Status': task_status})
    except Exception as e:
        return jsonify({'error': str(e)})

# Define a route for getting the result of a completed task
# curl "http://127.0.0.1:5000/getdone/90c6cdc1-f3fb-4c42-b042-b7ade9e852b2"
@app.route('/getdone/<string:task_id>')
def getdone(task_id):
    try:
        # Get the result of the task using the task ID
        # celery_app.AsyncResult was wrong
        task_result = add.AsyncResult(task_id).result      
        
        return jsonify({'Task Result': task_result})
    except Exception as e:
        return jsonify({'error': str(e)})

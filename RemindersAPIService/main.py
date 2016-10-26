from flask import Flask
from flask import request
import json

from task import Task

app = Flask(__name__)

#========================================
# Task
#========================================

# List for now
tasksList = []

# Create Task
@app.route('/tasks', methods=['POST'])
def create_task():
	parsed_body = request.get_json()
	print(type(parsed_body))
	print(parsed_body)
	print(pased_body['text'])

	if 'text' in parsed_body.keys():
		task = Task(parsed_body['text'])
		tasksList.append(task)
		print(tasksList)
		return('Successfully created new task')
	else:
		return('Create new task failed, no text in body')

	return('Something went wrong')

# Index Tasks
@app.route('/tasks', methods=['GET'])
def index_tasks():
	print('Get list of all tasks')
	return('Get list of all tasks')

# Get Task
@app.route('/tasks/<id>', methods=['GET'])
def get_task():
	print('Get task')
	return('Get task')

# Delete
@app.route('tasks/<id>', methods=['DELETE'])
def delete_task():
	print('Delete task')
	return('Delete task')

# #========================================
# # List
# #========================================

# # Create List
# @app.route('/lists', methods=['POST'])
# def createList():
# 	print('Create new list')

# # Index Lists
# @app.route('/lists', methods=['GET'])
# def indexLists():
# 	print('Get list of all lists')

# # Get List
# @app.route('/lists/<id>', methods=['GET'])
# def getTask():
# 	print('Get list')

# # Delete
# @app.route('tasks/<id>', methods=['DELETE'])
# def deleteTask():
# 	print('Delete task')


if __name__ == "__main__":
    app.run()

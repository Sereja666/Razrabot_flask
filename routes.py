from flask import request, jsonify
from pydantic import ValidationError

from core.handlar import db, app

from models.schemas import TaskSchema, Task





@app.route('/tasks', methods=['POST'])
def create_task():
    try:
        task_data = TaskSchema(title=request.json['title'], description=request.json.get('description'))
        new_task = Task(**task_data.dict())
        db.session.add(new_task)
        db.session.commit()
        return task_data.json()
    except ValidationError as e:
        return jsonify({'error': e.errors()})


@app.route('/tasks', methods=['GET'])
def get_tasks():
    all_tasks = Task.query.all()
    task_list = []
    for task in all_tasks:
        task_data = TaskSchema(id=task.id, title=task.title, description=task.description, created_at=task.created_at, updated_at=task.updated_at)
        task_list.append(task_data.dict())
    return jsonify(task_list)


@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    task = Task.query.get(id)
    task_data = TaskSchema(id=task.id, title=task.title, description=task.description, created_at=task.created_at, updated_at=task.updated_at)
    return task_data.json()


@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get(id)
    try:
        task_data = TaskSchema(title=request.json.get('title', task.title), description=request.json.get('description', task.description))
        task.title = task_data.title
        task.description = task_data.description
        db.session.commit()
        return task_data.json()
    except ValidationError as e:
        return jsonify({'error': e.errors()})


@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get(id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted'})

import json

from flask import Flask, request, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from pydantic import BaseModel, ValidationError

from config import settings

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = settings.db_url
db = SQLAlchemy(app)
print("подключил БД -> ", db)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())


class TaskSchema(BaseModel):
    id: int = None
    title: str
    description: str = None
    created_at: datetime = None
    updated_at: datetime = None


class TaskCreateSchema(BaseModel):
    title: str
    description: str = None


# 1. Создание задачи
@app.route('/tasks', methods=['POST'])
def create_task():
    try:
        task_data = TaskCreateSchema(title=request.form.get('title'), description=request.form.get('description'))

        new_task = Task(**task_data.dict())

        db.session.add(new_task)
        db.session.commit()

        return {'id': new_task.id,
                "title": new_task.title,
                "description": new_task.description,
                "created_at": new_task.created_at,
                "updated_at": new_task.updated_at
                }
    except ValidationError:
        return Response(response=
                        "ValidationError",
                        status=400,
                        )


# 2. Получение списка задач
@app.route('/tasks', methods=['GET'])
def get_tasks():
    all_tasks = Task.query.all()
    task_list = []
    for task in all_tasks:
        task_data = TaskSchema(id=task.id, title=task.title, description=task.description, created_at=task.created_at,
                               updated_at=task.updated_at)
        task_list.append(task_data.dict())
    return jsonify(task_list)


# 3. Получение информации о задаче
@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    try:
        task = Task.query.get(id)
        task_data = TaskSchema(id=task.id, title=task.title, description=task.description, created_at=task.created_at,
                               updated_at=task.updated_at)
        return task_data.json()
    except AttributeError:
        return Response(response="Не найден id",
                        status=404,
                        )


# 4. Обновление задачи
@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get(id)

    task_data = TaskSchema(title=request.json.get('title', task.title),
                           description=request.json.get('description', task.description))

    task.title = task_data.title
    task.description = task_data.description
    db.session.commit()

    return {'id': task.id,
            "title": task.title,
            "description": task.description,
            "created_at": task.created_at,
            "updated_at": task.updated_at
            }



# Delete a task
@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get(id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': f'Задача {id} успешно удалена'})


if __name__ == '__main__':
    app.run(debug=True)

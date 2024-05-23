import pytest

from config import settings
from main import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = settings.db_url
    client = app.test_client()

    yield client


def test_create_task(client):
    # Positive test case
    response = client.post('/tasks', data={'title': 'Тестовая задача', 'description': 'Тестовое описание'})
    print(response.text)

    assert response.status_code == 200

    # Negative test case
    response = client.post('/tasks', data={})
    assert response.status_code == 400
#
def test_get_tasks(client):
    # Positive test case
    response = client.get('/tasks')
    print(response.text)
    assert response.status_code == 200
#
def test_get_task(client):
    # Positive test case
    response = client.get('/tasks')
    task_id = response.json[0]['id']
    response = client.get(f'/tasks/{task_id}')
    assert response.status_code == 200

    # Negative test case
    response = client.get('/tasks/10000000')
    print(response.text)
    assert response.status_code == 404
#
def test_update_task(client):
    # Positive test case

    # task_data = TaskCreateSchema(title='nbnkdas', description='sfdfsdf')
    response = client.post('/tasks', data={'title': 'тест для обновления222', 'description': '___'})

    task_id = response.json['id']
    response = client.put(f'/tasks/{task_id}', json={'title': 'тест для обновления2222', 'description': 'УСПЕХ'})
    assert response.status_code == 200


#
def test_delete_task(client):
    # Positive test case
    response = client.post('/tasks', data={'title': 'Тест задачи удаления', 'description': 'Тест задачи удаления'})
    task_id = response.json['id']
    response = client.delete(f'/tasks/{task_id}')
    assert response.status_code == 200
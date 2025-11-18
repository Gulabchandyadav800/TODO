import os
import sqlite3
import pytest
from django.conf import settings
from tasks import db

# pytest fixture: ensure DB tests start from a clean table
@pytest.fixture(autouse=True)
def init_db(tmp_path, monkeypatch):
    # Use tmp DB file for isolation
    tmp_db = tmp_path / "test_todo.sqlite3"
    monkeypatch.setattr(settings, 'DB_FILE', tmp_db)
    db.create_tasks_table()
    yield
    # cleanup file
    try:
        os.remove(str(tmp_db))
    except OSError:
        pass

def test_create_task(client):
    payload = {
        "title": "Test task",
        "description": "Testing",
        "due_date": "2025-12-31",
        "status": "pending"
    }
    resp = client.post('/api/tasks/', data=payload, content_type='application/json')
    assert resp.status_code == 201
    data = resp.json()
    assert data['title'] == payload['title']
    assert 'id' in data

def test_get_tasks_empty_then_with_item(client):
    # initially empty
    r = client.get('/api/tasks/')
    assert r.status_code == 200
    assert r.json() == []

    # create via DB helper
    tid = db.insert_task('a', 'b', '2025-01-01', 'pending')
    r2 = client.get('/api/tasks/')
    assert r2.status_code == 200
    items = r2.json()
    assert len(items) == 1
    assert items[0]['id'] == tid

def test_get_update_delete_task(client):
    tid = db.insert_task('old', 'desc', '2025-03-03', 'pending')
    # retrieve
    r = client.get(f'/api/tasks/{tid}/')
    assert r.status_code == 200
    data = r.json()
    assert data['title'] == 'old'

    # update (PUT)
    new = {
        "title": "updated",
        "description": "desc2",
        "due_date": "2025-04-04",
        "status": "in_progress"
    }
    r2 = client.put(f'/api/tasks/{tid}/', data=new, content_type='application/json')
    assert r2.status_code == 200
    assert r2.json()['title'] == 'updated'

    # patch (partial)
    r3 = client.patch(f'/api/tasks/{tid}/', data={'status': 'done'}, content_type='application/json')
    assert r3.status_code == 200
    assert r3.json()['status'] == 'done'

    # delete
    r4 = client.delete(f'/api/tasks/{tid}/')
    assert r4.status_code == 204

    # now 404
    r5 = client.get(f'/api/tasks/{tid}/')
    assert r5.status_code == 404

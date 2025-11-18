import pytest
from django.conf import settings
from tasks import db

@pytest.fixture(autouse=True)
def init_test_db(tmp_path, monkeypatch):
    tmp_db = tmp_path / "test.sqlite3"
    monkeypatch.setattr(settings, "DB_FILE", str(tmp_db))

    db.create_tasks_table()
    yield

    if tmp_db.exists():
        tmp_db.unlink()

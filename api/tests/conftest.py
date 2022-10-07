import pytest
from starlette.testclient import TestClient

from api.api import api
from api.config import get_test_database_url, get_database_url
from api.db.database import Database
from api.utils import dataset, db_filler


@pytest.fixture(scope="module")
def client():
    authors, scientometric_databases, profiles = dataset.parse()
    db = Database(get_test_database_url())
    db_filler.refill(db, authors, scientometric_databases, profiles)
    api.dependency_overrides[get_database_url] = get_test_database_url
    client = TestClient(api, base_url="http://127.0.0.1:8082")
    yield client
    db.close()

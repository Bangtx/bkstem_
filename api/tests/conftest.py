import pytest
import json
from main import app
from fastapi.testclient import TestClient
from config.setting import POSTGRES_DB, TOKEN_GENERATION_KEY
from utils import auth, cache


@pytest.fixture(scope="session")
def db():
    from config.database import db, bare_cursor

    test_database = f"{POSTGRES_DB}_test"

    db.close()
    db.database = "postgres"
    with bare_cursor(db) as cursor:
        cursor.execute(f"DROP DATABASE IF EXISTS {test_database}")
        cursor.execute(f"CREATE DATABASE {test_database}")
    db.close()

    db.database = test_database
    sql_file = open("db/01_public.sql", "r").read()
    db.execute_sql(sql_file)
    # Add a dummy member
    db.execute_sql(
        """
          INSERT INTO member(id, email) VALUES (1, 'fmbiz@test.com');
        """
    )
    yield db


@pytest.fixture(scope="session")
def token():
    key = json.loads(TOKEN_GENERATION_KEY)
    cache.set("jwks-" + key["kid"], json.dumps(key))
    # Add a fake token to bypass FastAPI's bearer validation
    token = auth.generate_token(key, email="fmbiz@test.com")
    # Add a fake userinfo in cache
    user_info = {"id": 1, "email": "fmbiz@test.com"}
    cache.set("user-info." + token, json.dumps(user_info))
    yield token


@pytest.fixture(scope="session")
def client(db, token):
    app.state._db = db
    client = TestClient(app)
    client.headers = {"Authorization": f"Bearer {token}"}
    yield client

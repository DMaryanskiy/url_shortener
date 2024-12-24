from fastapi import testclient
import pytest
import sqlmodel
from sqlmodel import pool

from src import database as db
from src import main


@pytest.fixture(name='session')
def session_fixture():
    engine = sqlmodel.create_engine('sqlite://', connect_args={"check_same_thread": False}, poolclass=pool.StaticPool)
    sqlmodel.SQLModel.metadata.create_all(engine)
    with sqlmodel.Session(engine) as session:
        yield session


@pytest.fixture(name='client')
def client_fixture(session: sqlmodel.Session):
    def get_session_override():
        return session
    
    main.app.dependency_overrides[db.get_session] = get_session_override
    client = testclient.TestClient(main.app)
    yield client
    main.app.dependency_overrides.clear()

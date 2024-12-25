from fastapi import testclient

from src import database as db
from src import main
from src import models

client = testclient.TestClient(main.app)


def test_uri_not_exists(client: testclient.TestClient):
    response = client.get(
        'api/v1/url/not-exists',
    )

    assert response.status_code == 404
    data = response.json()

    assert data == {'message': 'Short URI `not-exists` does not exist'}


def test_redirect(session: db.SessionDep, client: testclient.TestClient):
    existing_long = models.Urls(original_url='exists', shorten_url='exists')
    session.add(existing_long)
    session.commit()

    response = client.get(
        'api/v1/url/exists',
        follow_redirects=False,
    )

    assert response.status_code == 307

import os

from fastapi import testclient

from src import database as db
from src import main
from src import models

os.environ['DOMAIN'] = 'http://127.0.0.1:8000/'

client = testclient.TestClient(main.app)


def test_with_short_uri(client: testclient.TestClient):
    response = client.post(
        '/api/v1/url/shorten',
        json={
            'original_url': 'long_url',
            'shorten_url': 'short'
        },
    )

    assert response.status_code == 201
    data = response.json()

    assert data == {'shorten_url': 'http://127.0.0.1:8000/short'}


def test_long_exists(session: db.SessionDep, client: testclient.TestClient):
    existing_long = models.Urls(original_url='exists', shorten_url='exists')
    session.add(existing_long)
    session.commit()

    response = client.post(
        '/api/v1/url/shorten',
        json={
            'original_url': 'exists',
            'shorten_url': 'short'
        },
    )

    assert response.status_code == 201
    data = response.json()

    assert data == {'shorten_url': 'http://127.0.0.1:8000/exists'}


def test_with_random_short(client: testclient.TestClient):
    response = client.post(
        '/api/v1/url/shorten',
        json={
            'original_url': 'long_url',
        },
    )

    assert response.status_code == 201
    data = response.json()
    uri = data['shorten_url'].split('/')[-1]

    assert len(uri) == 12 # we generate sequence with length of 20


def test_short_exists(session: db.SessionDep, client: testclient.TestClient):
    existing_long = models.Urls(original_url='exists', shorten_url='exists')
    session.add(existing_long)
    session.commit()

    response = client.post(
        '/api/v1/url/shorten',
        json={
            'original_url': 'long',
            'shorten_url': 'exists'
        },
    )

    assert response.status_code == 400
    data = response.json()

    assert data == {'message': 'Short URL `exists` is already used for another long URL'}

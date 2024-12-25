from fastapi import testclient
import sqlmodel

from src import database as db
from src import main
from src import models

client = testclient.TestClient(main.app)


def test_with_short_uri(session: db.SessionDep, client: testclient.TestClient):
    response = client.post(
        '/api/v1/url/shorten',
        json={
            'original_url': 'long_url',
            'shorten_uri': 'short'
        },
    )

    assert response.status_code == 201
    data = response.json()

    assert data == {'shorten_uri': 'http://127.0.0.1:8000/api/v1/url/short'}

    res = session.exec(
        sqlmodel.select(models.Urls).where(models.Urls.shorten_uri == 'short')
    )
    row = res.one_or_none()
    assert row == models.Urls(original_url='long_url', shorten_uri='short', id=1)


def test_long_exists(session: db.SessionDep, client: testclient.TestClient):
    existing_long = models.Urls(original_url='exists', shorten_uri='exists')
    session.add(existing_long)
    session.commit()

    response = client.post(
        '/api/v1/url/shorten',
        json={
            'original_url': 'exists',
            'shorten_uri': 'short'
        },
    )

    assert response.status_code == 201
    data = response.json()

    assert data == {'shorten_uri': 'http://127.0.0.1:8000/api/v1/url/exists'}

    res = session.exec(
        sqlmodel.select(models.Urls).where(models.Urls.shorten_uri == 'exists')
    )
    row = res.one_or_none()
    assert row == models.Urls(original_url='exists', shorten_uri='exists', id=1)


def test_with_random_short(client: testclient.TestClient):
    response = client.post(
        '/api/v1/url/shorten',
        json={
            'original_url': 'long_url',
        },
    )

    assert response.status_code == 201
    data = response.json()
    uri = data['shorten_uri'].split('/')[-1]

    assert len(uri) == 12 # we generate sequence with length of 20


def test_short_exists(session: db.SessionDep, client: testclient.TestClient):
    existing_long = models.Urls(original_url='exists', shorten_uri='exists')
    session.add(existing_long)
    session.commit()

    response = client.post(
        '/api/v1/url/shorten',
        json={
            'original_url': 'long',
            'shorten_uri': 'exists'
        },
    )

    assert response.status_code == 400
    data = response.json()

    assert data == {'message': 'Short URI `exists` is already used for another long URL'}

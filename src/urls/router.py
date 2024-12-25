import os
import random
import string

import fastapi
from fastapi import responses
import sqlmodel

from src import database as db
from src import models as db_models
from src.urls import exceptions
from src.urls import models
from src.urls import utils

URLS_ROUTER = fastapi.APIRouter(prefix='/url')
DOMAIN = os.environ.get('DOMAIN', 'http://127.0.0.1:8000')


@URLS_ROUTER.post(
        '/shorten',
        status_code=201,
        responses={
            201: {
                'description': 'URL was shortened or found existing short uri for given long url',
                'model': models.ShortUriResponse,
                'content': {
                    'application/json': {
                        'shorten_url': 'https://example.com/short_uri',
                    }
                }
            },
            400: {
                'description': 'Given short URI already exists in a database',
                'model': models.ErrorMessage,
            },
        }
)
async def insert_url(url_body: models.ShortUriRequest, session: db.SessionDep) -> models.ShortUriResponse:
    url_by_original = session.exec(
        sqlmodel.select(db_models.Urls).where(db_models.Urls.original_url == url_body.original_url))
    row = url_by_original.one_or_none()
    if row:
        shorten_url = DOMAIN + '/api/v1/url/' + row.short_uri
        return models.ShortUriResponse(short_uri=shorten_url)
    
    if url_body.short_uri:
        uri_exists = await utils.short_uri_exists(url_body.short_uri, session)
        if uri_exists:
            raise exceptions.ShortUriAlreadyExists(url_body.short_uri)
        
        shorten_url = DOMAIN + '/api/v1/url/' + url_body.short_uri
        await utils.insert_db(url_body.original_url, url_body.short_uri, session)

        return models.ShortUriResponse(short_uri=shorten_url)
    
    short_uri = ''.join(random.choices(string.ascii_letters, k=12))

    attempt = 0
    while True:
        uri_exists = await utils.short_uri_exists(short_uri, session)
        if not uri_exists:
            break
        attempt += 1
        if attempt == 20:
            raise exceptions.ShortUriAlreadyExists(short_uri)

    shorten_url = DOMAIN + '/api/v1/url/' + short_uri
    await utils.insert_db(url_body.original_url, short_uri, session)

    return models.ShortUriResponse(short_uri=shorten_url)


@URLS_ROUTER.get(
        '/{short_uri}',
        status_code=307,
        response_class=responses.RedirectResponse,
        responses={
            307: {
                'description': 'Original URL was found and you were redirected',
            },
            404: {
                'description': 'Given short URI was not found',
                'model': models.ErrorMessage,
            },
        }
)
async def get_original_url(short_uri: str, session: db.SessionDep):
    url_by_shorten = session.exec(
            sqlmodel.select(db_models.Urls).where(db_models.Urls.short_uri == short_uri)
        )
    row = url_by_shorten.one_or_none()
    if not row:
        raise exceptions.ShortUriDoesNotExist(short_uri)
    
    return row.original_url

import random
import string

import fastapi
import sqlmodel

from src import database as db
from src import models as db_models
from src.urls import exceptions
from src.urls import models

URLS_ROUTER = fastapi.APIRouter(prefix='/url')
DOMAIN = 'http://127.0.0.1:8000/'


async def short_uri_exists(short_uri: str, session: db.SessionDep) -> bool:
    url_by_shorten = session.exec(
            sqlmodel.select(db_models.Urls).where(db_models.Urls.shorten_url == short_uri)
        )
    row = url_by_shorten.one_or_none()
    return True if row else False


@URLS_ROUTER.post(
        '/shorten',
        status_code=201,
        responses={
            201: {
                'description': 'URL was shortened or found existing short uri for given long url',
                'model': models.ShortenUrlResponse,
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
async def insert_url(url_body: models.ShortenUrlRequest, session: db.SessionDep) -> models.ShortenUrlResponse:
    url_by_original = session.exec(
        sqlmodel.select(db_models.Urls).where(db_models.Urls.original_url == url_body.original_url))
    row = url_by_original.one_or_none()
    if row:
        shorten_url = DOMAIN + row.shorten_url
        return models.ShortenUrlResponse(shorten_url=shorten_url)
    
    if url_body.shorten_url:
        uri_exists = await short_uri_exists(url_body.shorten_url, session)
        if uri_exists:
            raise exceptions.ShortenUrlAlreadyExists(short_url=url_body.shorten_url)
        
        shorten_url = DOMAIN + url_body.shorten_url
        db_url = db_models.Urls(original_url=url_body.original_url, shorten_url=shorten_url)
        session.add(db_url)
        session.commit()

        return models.ShortenUrlResponse(shorten_url=shorten_url)
    
    shorten_uri = ''.join(random.choices(string.ascii_letters, k=12))

    attempt = 0
    while True:
        uri_exists = await short_uri_exists(shorten_uri, session)
        if not uri_exists:
            break
        attempt += 1
        if attempt == 20:
            raise exceptions.ShortenUrlAlreadyExists(shorten_uri)

    shorten_url = DOMAIN + shorten_uri
    db_url = db_models.Urls(original_url=url_body.original_url, shorten_url=shorten_uri)
    session.add(db_url)
    session.commit()

    return models.ShortenUrlResponse(shorten_url=shorten_url)

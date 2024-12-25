import sqlmodel

from src import database as db
from src import models as db_models


async def insert_db(original_url: str, shorten_url: str, session: db.SessionDep) -> None:
    db_url = db_models.Urls(original_url=original_url, short_uri=shorten_url)
    session.add(db_url)
    session.commit()


async def short_uri_exists(short_uri: str, session: db.SessionDep) -> bool:
    url_by_shorten = session.exec(
            sqlmodel.select(db_models.Urls).where(db_models.Urls.short_uri == short_uri)
        )
    row = url_by_shorten.one_or_none()
    return True if row else False
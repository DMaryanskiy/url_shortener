import sqlalchemy
import sqlmodel


class Urls(sqlmodel.SQLModel, table=True):
    id: int | None = sqlmodel.Field(default=None, primary_key=True)
    original_url: str = sqlmodel.Field(unique=True)
    shorten_uri: str = sqlmodel.Field(unique=True)

    __table_args__ = (sqlalchemy.UniqueConstraint('original_url', 'shorten_uri'),)

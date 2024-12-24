import sqlmodel

from src import config


SQLITE_FILE_NAME = config.CONFIG.get("SQLITE_FILE_NAME", "")

ENGINE = sqlmodel.create_engine(f'sqlite:///{SQLITE_FILE_NAME}')


def init_db():
    sqlmodel.SQLModel.metadata.create_all(ENGINE)

def get_session():
    with sqlmodel.Session() as session:
        yield session

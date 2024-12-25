import os
import typing

import fastapi
import sqlmodel


SQLITE_FILE_NAME = os.environ.get('SQLITE_FILE_NAME', '')

ENGINE = sqlmodel.create_engine(f'sqlite:///{SQLITE_FILE_NAME}', connect_args={"check_same_thread": False})


def init_db():
    sqlmodel.SQLModel.metadata.create_all(ENGINE)

def get_session():
    with sqlmodel.Session(ENGINE) as session:
        yield session

SessionDep = typing.Annotated[sqlmodel.Session, fastapi.Depends(get_session)]

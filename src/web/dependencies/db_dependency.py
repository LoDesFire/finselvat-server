from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from settings import settings


class DBDependency:
    def __init__(self) -> None:
        self._engine = create_engine(
            url=settings.db_path,
            echo=settings.db_echo,
        )
        self._session_factory = sessionmaker(
            bind=self._engine,
            expire_on_commit=False,
            autocommit=False,
        )

    @property
    def db_session(self) -> sessionmaker[Session]:
        return self._session_factory

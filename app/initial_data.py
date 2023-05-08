import logging
from typing import Generator

from sqlmodel import Session

from app.db.init_db import init_db
from app.db.session import engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init() -> Generator:
    with Session(engine) as session:
        init_db(session)
        yield session


def main() -> None:
    logger.info('Creating initial data')
    init()
    logger.info('Initial data created')


if __name__ == '__main__':
    main()

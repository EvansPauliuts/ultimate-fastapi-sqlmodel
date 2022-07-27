import logging
from typing import Generator

from db.session import engine
from sqlmodel import Session
from tenacity import after_log
from tenacity import before_log
from tenacity import retry
from tenacity import stop_after_attempt
from tenacity import wait_fixed

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60 * 5  # 5 minutes
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def init() -> Generator:
    try:
        with Session(engine) as session:
            yield session
    except Exception as e:
        logger.error(e)
        raise e


def main() -> None:
    logger.info("Initializing service")
    init()
    logger.info("Service finished initializing")


if __name__ == "__main__":
    main()

import logging
from pathlib import Path


LOGFILE = Path("compressor.log")


def configure():
    logging.basicConfig(
        filename=LOGFILE,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        filemode="w",
        level=logging.DEBUG,
    )


def get_logger(name: str):
    return logging.getLogger(name)


configure()

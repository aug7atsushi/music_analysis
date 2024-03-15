import logging
from logging import config

import yaml

from music_analysis import REPO_ROOT


def get_module_logger(name: str):
    with open(REPO_ROOT / "logging.yaml", "r") as f:
        cfg = yaml.safe_load(f.read())
    config.dictConfig(cfg)
    logger = logging.getLogger(name)
    return logger


if __name__ == "__main__":
    logger = get_module_logger("test")
    logger.debug("debug")
    logger.info("info")
    logger.warning("warning")
    logger.error("error")
    logger.critical("critical")

import logging
import sys
from pathlib import Path
from datetime import datetime


class Logger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._setup_logger()
        return cls._instance

    def _setup_logger(self) -> None:
        self.logger = logging.getLogger("UI_Automation")
        self.logger.setLevel(logging.DEBUG)

        if self.logger.handlers:
            return

        log_dir = Path("reports/logs")
        log_dir.mkdir(parents=True, exist_ok=True)

        log_file = log_dir / f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    @property
    def get_logger(self) -> logging.Logger:
        return self.logger


def get_logger(name: str = "UI_Automation") -> logging.Logger:
    return Logger().get_logger

"""Logger module""" ""
import os
import logging

from .envars import PROJECT_ROOT, LOGS_VOLUME


class Logger:
    """Logger class""" ""

    def __init__(self, project_root, logging_folder_path):
        self.project_root = project_root
        self.logging_folder_path = logging_folder_path

        log_levels = [
            logging.DEBUG,
            logging.INFO,
            logging.WARNING,
            logging.ERROR,
            logging.CRITICAL,
        ]

        log_file_names = [
            "debug.log",
            "info.log",
            "warning.log",
            "error.log",
            "critical.log",
        ]

        handlers = [logging.StreamHandler()]

        for level, file_name in zip(log_levels, log_file_names):
            file_path = os.path.join(
                self.project_root, self.logging_folder_path, file_name
            )

            # create log folder if it does not exist
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            file_handler = logging.FileHandler(file_path)
            file_handler.setLevel(level)
            handlers.append(file_handler)

        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s %(levelname)s: %(filename)s %(message)s",
            handlers=handlers,
        )

        self.logger = logging.getLogger(__name__)


# logger = Logger(PROJECT_ROOT, LOGS_VOLUME).logger

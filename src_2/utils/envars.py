"""Environment variables"""

import os
from dotenv import load_dotenv

from .validators import is_valid_phone_number, is_valid_email_address, is_valid_path

load_dotenv()

cwd = os.getcwd()
PROJECT_ROOT = os.path.abspath(os.path.join(cwd, ".."))

RUN_MODE = os.getenv("RUN_MODE")
assert RUN_MODE in ["dev", "prod"], f"Invalid RUN_MODE: {RUN_MODE}"

AGENT_PHONE_NUMBER = os.getenv("AGENT_PHONE_NUMBER")
assert AGENT_PHONE_NUMBER is not None
assert is_valid_phone_number(AGENT_PHONE_NUMBER)

SIGNAL_CLI_VOLUME = os.getenv("SIGNAL_CLI_VOLUME")
assert SIGNAL_CLI_VOLUME is not None

LOGS_VOLUME = os.getenv("LOGS_VOLUME")
assert LOGS_VOLUME is not None
assert is_valid_path(PROJECT_ROOT, LOGS_VOLUME, create_if_not_exist=True)

MONGO_URL = os.getenv("MONGO_URL")
MONGO_VOLUME = os.getenv("MONGO_VOLUME")
assert MONGO_VOLUME is not None
assert is_valid_path(PROJECT_ROOT, MONGO_VOLUME, create_if_not_exist=True)
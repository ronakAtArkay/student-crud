from datetime import datetime
from uuid import uuid4

import bcrypt

from config import config


def generate_id():
    id = str(uuid4())
    return id


def now():
    return datetime.now()


def _create_password(password):
    password = bytes(password, "utf-8")
    password = bcrypt.hashpw(password, config["salt"])
    password = password.decode("utf-8")
    return password

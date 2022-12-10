from datetime import datetime
from uuid import uuid4


def generate_id():
    id = str(uuid4())
    return id


def date():
    return datetime.now()

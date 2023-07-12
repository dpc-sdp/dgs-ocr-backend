import uuid
from datetime import datetime


class BaseUtils:

    def get_a_unique_id():
        return str(uuid.uuid4())

    def get_timestamp():
        return datetime.today().strftime('%Y-%m-%d %H:%M:%S')

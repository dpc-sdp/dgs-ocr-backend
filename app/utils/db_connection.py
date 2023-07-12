from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import config


class DbConnection:
    db_uri = config.get_azure_form_recognizer_db_uri()

    def __init__(self):
        self.engine = create_engine(self.db_uri)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def getConnection(self):
        return self.session

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import config


class DbConnection:
    def __init__(self):
        self.engine = create_engine(self.getDbUrl())
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def getDbUrl(self):
        return config.get_db_uri()

    def getConnection(self):
        return self.session

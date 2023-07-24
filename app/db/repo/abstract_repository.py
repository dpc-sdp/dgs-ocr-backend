from abc import ABC
from typing import TypeVar, Generic
from conf.extensions import db

T = TypeVar('T')


class AbstractRepository(Generic[T], ABC):

    def __init__(self, logger):
        self.logger = logger

    def save_to_db(self, model: T) -> bool:
        self.logger.debug(f'Creating data: {model}')
        db.session.add(model)
        db.session.commit()
        self.logger.info('Data saved successfully')
        return True

    def update(self, model: T) -> bool:
        self.logger.debug(f'Updating data: {model}')
        db.session.commit()
        db.logger.info('Data updated successfully')
        return True

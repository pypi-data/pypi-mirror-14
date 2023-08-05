from mongoengine import connect
from mongoengine.connection import _get_db


class BaseTest:

    @classmethod
    def clean_db(cls):
        cls.db.connection.drop_database('test')

    @classmethod
    def setup_class(cls, config=None):
        """
        Initialize a clean test database
        """
        connect('test', host='mongodb://localhost:27017/test')
        cls.db = _get_db()
        cls.clean_db()

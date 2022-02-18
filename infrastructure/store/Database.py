
from SingletonMeta import SingletonMeta
from peewee import SqliteDatabase
from app.classes.helpers import helper
import logging

class Database(metaclass=SingletonMeta):
    """
    The Database entry point. Note that this is a singleton pattern to avoid
    implementing a container for the moment. 
    
    Remember to call TearDown when stopping the app!
    """

    def __init__(self):
        self.Database = None

        self._logger = logging.getLogger(__name__)

        self._db_path = helper.get_db_path()
        self._journal_Mode = 'wal'
        self._cache_size = -1024 * 10

        self.SetUp()

    def GetDatabase(self):
        return self.Database

    def SetUp(self):
        self._logger.info("SqlLite Database setup in progress...")

        self.Database = SqliteDatabase(self._db_path, pragmas={
            'journal_mode': self._journal_Mode,
            'cache_size': self._cache_size }
        )

        self._logger.info("SqlLite Database setup completed")

    def TearDown(self):
        self._logger.info("SqlLite Database teardown in progress...")

        self.Database = None

        self._logger.info("SqlLite Database teardown completed")

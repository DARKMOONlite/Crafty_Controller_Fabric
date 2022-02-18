from infrastructure.store.Database import Database
from peewee import Model

class BaseModel(Model):
    class Meta:
        database = Database.GetDatabase()
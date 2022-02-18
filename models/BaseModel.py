from infrastructure.store.Datastore import Datastore
from peewee import Model

class BaseModel(Model):
    class Meta:
        database = Datastore().GetDatabase()
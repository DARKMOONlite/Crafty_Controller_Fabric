from BaseModel import BaseModel


class ExecutableServer(BaseModel):
    def __init__(self):
        self.Id
        self.Version
        self.Description
        self.RemoteSource
        self.IsFabricServer
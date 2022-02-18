import logging
from models.ExecutableServer import ExecutableServer


class ExecutableServerRepository():
    def __init__(self):
        self._logger = logging.getLogger(__name__)

    def GetByVersion(self, version: int) -> ExecutableServer:
        pass

    def GetAll(self,) -> list(ExecutableServer):
        pass

    def GetWhere(self, predicate) -> list(ExecutableServer):
        pass

    def Add(self, exec) -> None:
        pass

    def AddRange(self, execs: list) -> None:
        pass

    def Delete(self, exec) -> bool:
        pass

    def DeleteRange(self, execs: list) -> bool:
        pass

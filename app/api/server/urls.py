# define endpoint mappings here

from .handlers import *

handlers = [
    (r'/force_backup', ForceServerBackup),
    (r'/start', StartServer),
    (r'/stop', StopServer),
    (r'/restart', RestartServer)
]

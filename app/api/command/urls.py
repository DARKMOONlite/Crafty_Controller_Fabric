# define endpoint mappings here

from .handlers import *

handlers = [
    (r'/send_command', SendCommand)
]

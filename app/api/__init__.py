# configure API handler module exports here!

from .server import handlers as server_handlers
from .user import handlers as user_handlers
from .log import handlers as log_handlers
from .command import handlers as command_handlers

"""
.. module:: API
    :platform: Unix, Windows
    :synopsis: Crafty Controller API
.. moduleauthor:: Albert Ferguson <albertferguson118@gmail.com>
.. moduleauthor:: Sebastian Schroder

All API route handlers live within this module.
"""

__author__ = "Albert Ferguson"
__author__ = "Sebastian Schroder"

__all__ = [
    "server_handlers",
    "user_handlers",
    "log_handlers",
    "command_handlers"
]
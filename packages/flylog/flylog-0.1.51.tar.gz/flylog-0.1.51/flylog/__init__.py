# -*- coding: utf-8 -*-

__version__ = '0.1.51'

from .api.log_handler import LogHandler
from .api.client import Client
from .agent.agent import Agent

# 向下兼容
FlyLogHandler = LogHandler

# -*- coding: utf-8 -*-

__version__ = '0.1.50'

from .api.log_handler import LogHandler
from .agent.agent import Agent

# 向下兼容
FlyLogHandler = LogHandler

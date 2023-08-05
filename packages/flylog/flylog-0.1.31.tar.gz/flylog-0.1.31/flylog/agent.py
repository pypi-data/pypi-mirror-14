#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
用来作为接受log传递的agent
通过udp通道。
"""

import json
import gevent
from gevent.server import DatagramServer
from utils import import_string
from log import logger


class FlyLogAgent(object):
    debug = False

    backend_dict = None

    def __init__(self, config=None, debug=None):
        self.config = config
        if debug is not None:
            self.debug = debug

        self.backend_dict = dict()
        for name, backend_conf in self.config.BACKENDS.items():
            _class = import_string(backend_conf['class'])
            backend = _class(**backend_conf['init_data'])

            self.backend_dict[name] = backend

    def handle_message(self, message, address):
        recv_dict = json.loads(message)

        title = u'[%s]Attention!' % recv_dict.get('source')
        content = recv_dict.get('content')

        role_list = recv_dict.get('role_list') or ('default',)

        for role in role_list:
            handler_list = self.config.ROLES.get(role)
            if handler_list is None:
                continue

            for handler in handler_list:
                gevent.spawn(self._process_handler, handler, title, content)

    def _process_handler(self, handler, title, content):
        """
        为了支持gevent.spawn，所以独立出来
        """
        backend = self.backend_dict[handler['backend']]
        params = handler['params']

        try:
            if not backend.emit(title, content, **params):
                logger.error('emit error. handler: %s, title: %s, content: %s',
                             handler, title, content)
        except:
            logger.error('exc occur. handler: %s, title: %s, content: %s',
                         handler, title, content, exc_info=True)

    def run(self, host, port):
        class UDPServer(DatagramServer):

            def handle(sub_self, message, address):
                try:
                    self.handle_message(message, address)
                except:
                    logger.error('exc occur.', exc_info=True)

        server = UDPServer((host, port))

        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
        except:
            logger.error('exc occur.', exc_info=True)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
用来作为接受log传递的agent
通过udp通道。

不使用 gevent，因为测试了 gevent 对 smtplib 似乎没法异步，还是会阻塞
"""

import json
import SocketServer
from thread import start_new_thread
from collections import defaultdict

from .utils import import_string
from .log import logger


class Agent(object):
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

        # backend_name -> params
        merged_backends = defaultdict(dict)

        for role in role_list:
            handler_list = self.config.ROLES.get(role)
            if handler_list is None:
                continue

            for handler in handler_list:
                backend_name = handler['backend']
                params = handler['params']

                merged_backends[backend_name] = self._merge_backend_params(
                    merged_backends[backend_name],
                    params
                )

        for backend_name, params in merged_backends.items():
            start_new_thread(self._process_backend_emit, (backend_name, params, title, content))

    def _merge_backend_params(self, params1, params2):
        """
        因为有可能不同role之间对应同样的发送人，为了避免重复，所以需要合并
        """

        merged_keys = set(params1.keys()) | set(params2.keys())
        merged_params = dict()

        for key in merged_keys:
            value1 = params1.get(key) or list()
            value2 = params2.get(key) or list()

            merged_params[key] = list(set(value1) | set(value2))

        return merged_params

    def _process_backend_emit(self, backend_name, params, title, content):
        """
        为了支持单独线程，所以独立出来
        """
        backend = self.backend_dict[backend_name]

        try:
            if not backend.emit(title, content, **params):
                logger.error('emit error. backend: %s, params: %s, title: %s, content: %s',
                             backend_name, params, title, content)
        except:
            logger.error('exc occur. backend: %s, params: %s, title: %s, content: %s',
                         backend_name, params, title, content, exc_info=True)

    def run(self, host, port):
        class ThreadedUDPRequestHandler(SocketServer.BaseRequestHandler):
            def handle(sub_self):
                message = sub_self.request[0]
                try:
                    self.handle_message(message, sub_self.client_address)
                except:
                    logger.error('exc occur.', exc_info=True)

        server = SocketServer.ThreadingUDPServer((host, port), ThreadedUDPRequestHandler)

        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
        except:
            logger.error('exc occur.', exc_info=True)

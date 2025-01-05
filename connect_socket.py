#! python3.13
# coding=utf8

""" Checkbutton container """

__author__ = 'Sihir'  # noqa
__copyright__ = '© Sihir 2023-2024 all rights reserved'  # noqa

from threading import Thread

from jsons import loads
from jsons import dumps

from datetime import datetime

from copy import copy as _copy

from typing import Optional

from utils.socket_support import SocketServer
from utils.socket_support import SocketClient


class ConnectSocket:
    """ use a socket for the data """

    def __init__(self, port: int):
        """ initialize the class """

        self._incoming: Optional[dict] = None
        self._outgoing: Optional[dict] = None
        self._message = None
        self._server = None
        self._port = port
        self._debug = False

        self.thread = Thread(target=self.client)
        self.thread.start()

    def close(self):
        """ close the connection """

        self.select_track('-q')

    def client(self):
        """ the socket client """

        self._server = SocketServer(port=self._port, callback=self.receive, debug=False)
        self._server.listen()

    def receive(self, message: str) -> str:
        """ received a string from the socket """

        self._message = message

        # filename
        # function
        # progress
        self._incoming = loads(message)

        # progress
        # heartbeat
        # busy
        answer = dumps(self._outgoing)
        return answer

    def poll(self, busy: int, progress: str) -> Optional[dict]:
        """ see whether something has come in """

        self._outgoing = {
            'progress': progress,
            'heartbeat': self.heartbeat,
            'busy': busy
        }

        if not self._message:
            return None

        result = _copy(self._incoming)
        self._incoming = None
        return result

    @property
    def heartbeat(self) -> str:
        """ still alive """

        return datetime.now().strftime('%Y/%m/%d %H:%M:%S')

    def select_track(self, file_name: str):
        """ send the message to myself (only works as long there is no other connection active """

        client = SocketClient(port=self._port)

        if file_name == '-q':
            message = '-q'
        else:
            data = {
                'file_name': file_name,
                'function': 'play',
                'progress': '0.0',
            }
            message = dumps(data)

        answer = client.communicate(message=message)
        if self._debug:
            print(answer)

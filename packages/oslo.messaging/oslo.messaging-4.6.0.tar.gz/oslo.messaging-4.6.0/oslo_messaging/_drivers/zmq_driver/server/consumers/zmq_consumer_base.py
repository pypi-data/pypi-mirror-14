#    Copyright 2015 Mirantis, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import abc
import logging
import threading
import time

import six

from oslo_messaging._drivers import common as rpc_common
from oslo_messaging._drivers.zmq_driver import zmq_async
from oslo_messaging._drivers.zmq_driver import zmq_names
from oslo_messaging._drivers.zmq_driver import zmq_socket
from oslo_messaging._i18n import _LE

LOG = logging.getLogger(__name__)

zmq = zmq_async.import_zmq()


@six.add_metaclass(abc.ABCMeta)
class ConsumerBase(object):

    def __init__(self, conf, poller, server):
        self.conf = conf
        self.poller = poller
        self.server = server
        self.sockets = []
        self.context = zmq.Context()

    @abc.abstractmethod
    def listen(self, target):
        """Associate new sockets with targets here"""

    @abc.abstractmethod
    def receive_message(self, target):
        """Method for poller - receiving message routine"""

    def cleanup(self):
        for socket in self.sockets:
            if not socket.handle.closed:
                socket.close()
        self.sockets = []


class SingleSocketConsumer(ConsumerBase):

    def __init__(self, conf, poller, server, socket_type):
        super(SingleSocketConsumer, self).__init__(conf, poller, server)
        self.socket = self.subscribe_socket(socket_type)

    def subscribe_socket(self, socket_type):
        try:
            socket = zmq_socket.ZmqRandomPortSocket(
                self.conf, self.context, socket_type)
            self.sockets.append(socket)
            self.poller.register(socket, self.receive_message)
            LOG.debug("Run %(stype)s consumer on %(addr)s:%(port)d",
                      {"stype": zmq_names.socket_type_str(socket_type),
                       "addr": socket.bind_address,
                       "port": socket.port})
            return socket
        except zmq.ZMQError as e:
            errmsg = _LE("Failed binding to port %(port)d: %(e)s")\
                % (self.port, e)
            LOG.error(_LE("Failed binding to port %(port)d: %(e)s"),
                      (self.port, e))
            raise rpc_common.RPCException(errmsg)

    @property
    def address(self):
        return self.socket.bind_address

    @property
    def port(self):
        return self.socket.port


class TargetsManager(object):

    def __init__(self, conf, matchmaker, host, socket_type):
        self.targets = []
        self.conf = conf
        self.matchmaker = matchmaker
        self.host = host
        self.socket_type = socket_type
        self.targets_lock = threading.Lock()
        self.updater = zmq_async.get_executor(method=self._update_targets) \
            if conf.zmq_target_expire > 0 else None
        if self.updater:
            self.updater.execute()

    def _update_targets(self):
        with self.targets_lock:
            for target in self.targets:
                self.matchmaker.register(
                    target, self.host,
                    zmq_names.socket_type_str(self.socket_type))

        # Update target-records once per half expiration time
        time.sleep(self.conf.zmq_target_expire / 2)

    def listen(self, target):
        with self.targets_lock:
            self.targets.append(target)
            self.matchmaker.register(
                target, self.host,
                zmq_names.socket_type_str(self.socket_type))

    def cleanup(self):
        if self.updater:
            self.updater.stop()
        for target in self.targets:
            self.matchmaker.unregister(
                target, self.host,
                zmq_names.socket_type_str(self.socket_type))

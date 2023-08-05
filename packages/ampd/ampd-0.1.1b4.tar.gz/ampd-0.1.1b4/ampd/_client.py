# coding: utf-8

# Asynchronous Music Player Daemon client library for Python

# Copyright (C) 2015 Itaï BEN YAACOV

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import os
import sys

from . import _request, _worker, _logger, errors


class Client(object):
    """
    Establishes connection with the MPD server.

    Keeps track of:
    - The worker groups.
    - The active queue: requests send to server and waiting for a reply.
    - The passive list: 'idle' commands waiting for some conditions to hold.
    - The execution queue: workers for which a reply has arrived.

    Do not use this -- use ClientGLib instead.
    """

    DISCONNECT_REQUESTED = 0
    DISCONNECT_RECONNECT = 1
    DISCONNECT_FAILED_CONNECT = 2
    DISCONNECT_SHUTDOWN = 3
    DISCONNECT_PASSWORD = 4
    DISCONNECT_ERROR = 5

    _DEFAULT_CODING = None if sys.version_info >= (3, 0) else 'utf-8'

    def __init__(self, scheduler, coding=_DEFAULT_CODING, coding_server='utf-8', excepthook=None):
        """
        Initialize a client.

        excepthook - override sys.excepthook for exceptions raised in workers.
        """
        self._scheduler = scheduler
        self._coding = coding
        self._coding_server = coding_server
        self._excepthook = excepthook
        self._passive_list = []
        self._execute_queue = []
        self._execute_timeout = None
        self._worker_groups = []
        self._poller = None
        self.is_connected = False
        self.protocol_version = None
        self.ampd_worker_group = _worker.WorkerGroup(self)
        self.host = self.port = self.password = None

    def close(self):
        """
        Close all workers and worker groups, disconnect from server.
        """
        _logger.debug("Closing client")
        while self._worker_groups:
            self._worker_groups[0].close()
        self._disconnect_from_server(self.DISCONNECT_SHUTDOWN)
        if self._execute_timeout:
            self._scheduler.remove_timeout(self._execute_timeout)
            self._run_execute_queue()

    def connect_to_server(self, host=None, port=6600, password=None):
        """
        host     - '[password@]hostname[:port]'.  Default to $MPD_HOST or 'localhost'.
        port     - Ignored if given in the 'host' argument.
        password - Ignored if given in the 'host' argument.
        """

        if not host:
            host = os.environ.get('MPD_HOST', 'localhost')
        if ':' in host:
            host, port = host.split(':', 1)
        if '@' in host:
            password, host = host.split('@', 1)

        self.host = host
        self.port = port
        self.password = password

        self.reconnect_to_server()

    def reconnect_to_server(self):
        """
        Connect to server with previous host / port / password.
        """
        if self._poller:
            self._disconnect_from_server(self.DISCONNECT_RECONNECT)

        self._buff_in = self._buff_out = b''
        self._is_idle = False
        self._active_queue = []
        self._connect_worker()
        self._poller = self._scheduler.connect_and_poll(self.host, self.port, self._handle_read, self._handle_write, self._handle_error)

    def disconnect_from_server(self):
        self._disconnect_from_server(self.DISCONNECT_REQUESTED)

    def _disconnect_from_server(self, reason):
        if self._poller:
            try:
                self._poller.sock.send('close')
            except:
                pass
            self._poller.close()
            self._poller = None
            self.is_connected = False
            self.protocol_version = None
            requests = self._active_queue + self._passive_list
            del self._buff_in, self._buff_out, self._active_queue
        else:
            requests = self._passive_list

        self._execute_queue = [(worker, errors.DisconnectError(reason)) for worker, reply in self._execute_queue]
        for request in requests:
            request._execute(errors.DisconnectError(reason))

    def new_worker_group(self):
        "Return a new WorkerGroup associated to the Client."
        return _worker.WorkerGroup(self)

    def connect_loop(self, connected_cb=None, disconnected_cb=None):
        return self.ampd_worker_group.connect_loop(connected_cb, disconnected_cb)

    connect_loop.__doc__ = _worker.WorkerGroup.connect_loop.__doc__

    def _execute(self, worker, reply=None):
        self._execute_queue.append((worker, reply))
        if not self._execute_timeout:
            self._execute_timeout = self._scheduler.add_timeout(0, self._run_execute_queue)

    def _run_execute_queue(self):
        while self._execute_queue:
            worker, reply = self._execute_queue.pop(0)
            if not worker._gen:
                continue
            try:
                try:
                    request = worker._gen.throw(reply) if isinstance(reply, Exception) else worker._gen.send(reply)
                except:
                    del reply  # If we threw an exception and got it back, python3 creates a reference cycle with the traceback.
                    worker._close()
                    raise
            except (StopIteration, errors.ConnectionError, errors.DisconnectError):
                continue
            except:
                (self._excepthook or sys.excepthook)(*sys.exc_info())
                continue
            try:
                request = _request.Request.new(request)
                request._setup(worker, self)
            except Exception as reply:
                self._execute(worker, reply)

        self._execute_timeout = None

        if self.is_connected and not self._is_idle and not self._active_queue:
            self._idle_worker()

    def _kill_worker(self, worker):
        worker._close()
        try:
            self._execute_queue.remove(worker)
        except:
            for request in self._passive_list:
                if request.worker == worker:
                    request._execute(None)
                    break

    def _handle_error(self, message=None):
        if self.is_connected:
            self._disconnect_from_server(self.DISCONNECT_ERROR)
        else:
            self._disconnect_from_server(self.DISCONNECT_FAILED_CONNECT)

    def _handle_write(self, sock):
        n = sock.send(self._buff_out)
        _logger.debug("Write: {}".format(self._buff_out[:n]))
        self._buff_out = self._buff_out[n:]
        return len(self._buff_out) > 0

    def _handle_read(self, sock):
        data = sock.recv(10000)
        _logger.debug("Read: {}".format(data))
        if not data:
            return False
        lines = (self._buff_in + data).split(b'\n')
        for line in lines[:-1]:
            line = line.decode(self._coding_server)
            if self._coding:
                line = line.encode(self._coding)
            if self._active_queue:
                self._active_queue[0]._process_line(line)
            else:
                raise errors.ProtocolError("Unexpected data: ", line)
        self._buff_in = lines[-1]
        return True

    @_worker.worker
    def _connect_worker(self):
        self.protocol_version = yield _request.RequestWelcome()
        self.is_connected = True
        if self.password:
            try:
                yield _request.commands_.password(self.password)
            except errors.ReplyError:
                self._disconnect_from_server(self.DISCONNECT_PASSWORD)
                return
        for request in list(self._passive_list):
            request._test(['connect'])

    @_worker.worker
    def _idle_worker(self):
        for request in self._passive_list:
            if request._test(['idle']):
                return
        _logger.debug("Going idle")
        subsystems = yield _request.RequestCommandIdle()
        for request in list(self._passive_list):
            request._test(subsystems)


class ServerProperties(object):
    """
    Keeps track of various properties of the server:
    - status
    - current_song
    - state
    - volume
    - time
    - elapsed
    - bitrate
    - option-X, for X in consume, random, repeat, single

    Assignment to volume is reflected in the server.

    Do not use this -- use ServerPropertiesGLib instead.
    """

    OPTION_NAMES = ['consume', 'random', 'repeat', 'single']

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, value):
        self._volume = value
        if not self._blocking:
            self._set_volume()

    @_worker.worker
    def _set_server_volume(self):
        if self._setting_volume:
            self._setting_volume.kill()
        self._setting_volume = yield _request.commands_._self()
        value = self.volume
        _logger.debug("Setting voume to {} at {}".format(value, id(self._setting_volume)))
        try:
            while True:
                try:
                    yield _request.commands_.setvol(value)
                except errors.ReplyError:
                    yield _request.conditions.PLAYER
                    continue
                status = yield _request.commands_.status()
                if int(status['volume']) == value:
                    break
                yield _request.conditions.PLAYER, _request.conditions.MIXER
            _logger.debug("Success")
        finally:
            self._setting_volume = None

    def __init__(self, client):
        self.ampd_worker_group = client.new_worker_group()
        self.ampd_worker_group.connect_loop(self._connected_cb, self._disconnected_cb)
        self._setting_volume = None
        self._reset()

    def _block(self):
        self._blocking = True

    def _unblock(self):
        self._blocking = False

    def _reset(self):
        self._block()
        self._error = None
        self.current_song = {}
        self.status = {}
        self.state = ''
        self.volume = -1
        self.time = 0
        self.elapsed = 0
        self.bitrate = ''
        self._unblock()

    @_worker.worker
    def _connected_cb(self):
        while True:
            self._update_status((yield _request.commands_.status()))
            yield [_request.conditions.PLAYER, _request.conditions.MIXER, _request.conditions.OPTIONS] + ([_request.conditions.TIMEOUT((int(self.elapsed + 1.5) - self.elapsed) * 1000)] if self.state == 'play' else [])

    def _update_status(self, status):
        self._block()
        self.status = status
        self.bitrate = self.status.get('bitrate')
        self.state = self.status['state']
        if self.state == 'stop':
            self.current_song = {}
        elif self.status['songid'] != self.current_song.get('id'):
            self._update_current_song()
        if not self._setting_volume and int(self.status['volume']) != -1:
            self.volume = int(self.status['volume'])
        if 'time' in self.status:
            times = self.status['time'].split(':')
            self.time = int(times[1])
            self.elapsed = float(self.status['elapsed'])
        else:
            self.time = 0
            self.elapsed = 0
        for option in self.OPTION_NAMES:
            exec('self.option_{} = value'.format(option), {'self': self, 'value': bool(int(self.status[option])), '__builtins__': {}})
        self._unblock()

    @_worker.worker
    def _update_current_song(self):
        self.current_song = yield _request.commands_.currentsong()

    def _disconnected_cb(self, reason):
        self._reset()

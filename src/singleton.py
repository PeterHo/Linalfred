#! /usr/bin/env python
import getpass
import os
import signal
import sys
import fcntl
import tempfile

import pickle

from PyQt5.QtCore import QIODevice
from PyQt5.QtCore import QSharedMemory
from PyQt5.QtCore import QTimer
from PyQt5.QtNetwork import QLocalServer
from PyQt5.QtNetwork import QLocalSocket
from PyQt5.QtWidgets import QApplication

fp = None


# 一种简单实现的单实例方式
def isSingleInstance(flavor_id=""):
    global fp
    basename = os.path.splitext(os.path.abspath(sys.argv[0]))[0].replace(
        "/", "-").replace(":", "").replace("\\", "-") + '-%s' % flavor_id + '.lock'
    lockfile = os.path.normpath(tempfile.gettempdir() + '/' + basename)

    if sys.platform == 'win32':
        try:
            if os.path.exists(lockfile):
                os.unlink(lockfile)
            fp = os.open(
                lockfile, os.O_CREAT | os.O_EXCL | os.O_RDWR)
        except OSError:
            return False

    else:  # non Windows
        fp = open(lockfile, 'w')
        try:
            fcntl.lockf(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except IOError:
            return False

    return True


class SingletonApp(QApplication):
    timeout = 1000
    instance = None

    def __init__(self, argv, application_id=None):
        QApplication.__init__(self, argv)

        self.socket_filename = os.path.expanduser("~/.ipc_%s" % self.generate_ipc_id())
        self.shared_mem = QSharedMemory()
        self.shared_mem.setKey(self.socket_filename)

        if self.shared_mem.attach():
            self.is_running = True
            return

        self.is_running = False
        if not self.shared_mem.create(1):
            print("Unable to create single instance")
            return
        # start local server
        self.server = QLocalServer(self)
        # connect signal for incoming connections
        self.server.newConnection.connect(self.receive_message)
        # if socket file exists, delete it
        if os.path.exists(self.socket_filename):
            os.remove(self.socket_filename)
        # listen
        self.server.listen(self.socket_filename)

        SingletonApp.instance = self

        # 监听关闭事件
        signal.signal(signal.SIGINT, self.onExit)
        # signal.signal(signal.SIGKILL, onExit)
        signal.signal(signal.SIGTERM, self.onExit)
        self.timer = QTimer()
        self.timer.start(500)
        self.timer.timeout.connect(lambda: None)

    def __del__(self):
        self.shared_mem.detach()
        if not self.is_running:
            if os.path.exists(self.socket_filename):
                os.remove(self.socket_filename)

    def generate_ipc_id(self, channel=None):
        if channel is None:
            channel = os.path.basename(sys.argv[0])
        return "%s_%s" % (channel, getpass.getuser())

    def send_message(self, message):
        if not self.is_running:
            raise Exception("Client cannot connect to IPC server. Not running.")
        socket = QLocalSocket(self)
        socket.connectToServer(self.socket_filename, QIODevice.WriteOnly)
        if not socket.waitForConnected(self.timeout):
            raise Exception(str(socket.errorString()))
        socket.write(pickle.dumps(message))
        if not socket.waitForBytesWritten(self.timeout):
            raise Exception(str(socket.errorString()))
        socket.disconnectFromServer()

    def receive_message(self):
        print("recv message")
        socket = self.server.nextPendingConnection()
        if not socket.waitForReadyRead(self.timeout):
            print(socket.errorString())
            return
        byte_array = socket.readAll()
        self.handle_new_message(pickle.loads(byte_array))

    def setDlg(self, dlg):
        self.dlg = dlg

    def handle_new_message(self, message):
        self.dlg.show()

    @staticmethod
    def onExit(signal, frame):
        SingletonApp.instance.__del__()
        print("exit")
        sys.exit(-1)

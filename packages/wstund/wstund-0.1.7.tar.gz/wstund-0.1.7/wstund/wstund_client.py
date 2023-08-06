# -*- coding: utf-8 -*-
import sys
import select
import config as g
from time import sleep
from subprocess import check_call
from lockfile import LockTimeout
from daemon.runner import DaemonRunner, DaemonRunnerStopFailureError
from threading import Thread
from pytun import TunTapDevice, IFF_TUN, IFF_NO_PI
from ws4py.client.threadedclient import WebSocketClient
from ws4py.exc import HandshakeError


# ## for daemon.runner
class WstundClientApp():
    def __init__(self):
        # ## for daemon.runner
        g.logger.debug('WstundClientApp __init__')
        inout = '/dev/tty' if g.config.get('wstund', 'debug').lower() == 'true' else '/dev/null'
        self.stdin_path = self.stdout_path = self.stderr_path = inout
        self.pidfile_path = g.config.get('wstund', 'pidpath')
        self.pidfile_timeout = int(g.config.get('wstund', 'pidtimeout'))
        self.reconnect_interval = int(g.config.get('client', 'reconnect.interval'))

        self.wstun_client = None
        # ## wstundClient
        # self.ws_tun_client = wstundClient()

    def __del__(self):
        g.logger.debug('WstundClientApp __del__')
        if self.wstun_client is not None:
            self.wstun_client.close()
            self.wstun_client.closed(1000, "client receive signal.SIGTERM)")

    def run(self):
        while True:
            try:
                self.url = 'ws://{}:{}/ws'.format(g.config.get('client', 'host'), g.config.get('client', 'port'))
                # self.wstun_client = WebSocketTunClient(self.url, heartbeat_freq=2.0)
                self.wstun_client = WebSocketTunClient(self.url, protocols=['http-only', 'chat'], heartbeat_freq=2.0)
                self.wstun_client.daemon = True
                self.wstun_client.connect()
                self.wstun_client.run_forever()
            except HandshakeError as e:
                self.wstun_client.close()
                self.wstun_client.closed(1000, "client receive signal.SIGTERM)")
                g.logger.info('wstund client wait {0} seconds to reconnect'.format(self.reconnect_interval))
                sleep(self.reconnect_interval)


class WebSocketTunClient(WebSocketClient):
    tun = None                  # TODO: tun device should shared in same network
    thread = None               # one thread one tun now, TODO TUN_TAP_MQ
    thread_counter = 0
    thread_closing = False

    def __init__(self, *args, **kwargs):
        super(WebSocketTunClient, self).__init__(*args, **kwargs)

    def _background_send(self):
        poller = select.epoll()
        poller.register(WebSocketTunClient.tun, select.EPOLLIN)
        while True:
            events = poller.poll(2)
            for fd, flag in events:
                if fd is WebSocketTunClient.tun.fileno():
                    buf = WebSocketTunClient.tun.read(WebSocketTunClient.tun.mtu)
                    g.logger.debug("send data len(buf) {}".format(len(buf)))
                    try:
                        self.send(buf, True)
                    except RuntimeError:
                        break

            # ## timeout then check thread_closing
            if WebSocketTunClient.thread_closing is True:
                g.logger.debug("background_send thread_closing")
                break

    def opened(self):
        g.logger.info("WebSocketTunClient opened")

        if WebSocketTunClient.tun is None:
            g.logger.debug("TunWebSocketHandler new tun")
            tun = TunTapDevice(flags=IFF_TUN | IFF_NO_PI)
            tun.addr = g.config.get('client', 'ip')
            tun.netmask = g.config.get('client', 'netmask')
            tun.mtu = int(g.config.get('client', 'mtu'))
            tun.up()
            WebSocketTunClient.tun = tun

        if WebSocketTunClient.thread is None:
            g.logger.debug("WebSocketTunClient new thread")
            WebSocketTunClient.thread = Thread(target=self._background_send)
            WebSocketTunClient.thread.daemon = True
            WebSocketTunClient.thread.start()
        WebSocketTunClient.thread_counter += 1

        if g.config.get('client', 'script.up') is not None:
            check_call(g.config.get('client', 'script.up'), shell=True)

    def closed(self, code, reason=None):
        g.logger.info(("WebSocketTunClient closed", code, reason))
        g.logger.debug("WebSocketTunClient closing thread")
        WebSocketTunClient.thread_counter -= 1
        if WebSocketTunClient.thread_counter == 0:
            WebSocketTunClient.thread_closing = True
            WebSocketTunClient.thread.join()
            WebSocketTunClient.tun.down()
            g.logger.debug("WebSocketTunClient closed thread")
            WebSocketTunClient.thread = None
            WebSocketTunClient.thread_closing = False
            WebSocketTunClient.tun = None

        if g.config.get('client', 'script.down') is not None:
            check_call(g.config.get('client', 'script.down'), shell=True)

    def received_message(self, m):
        if m is not None:
            if m.is_binary:
                g.logger.debug("received_message: bin len {}".format(len(m)))
                WebSocketTunClient.tun.write(m.data)
            else:
                g.logger.debug("received_message: msg {}".format(m))
        """
        if m is not None:
            g.logger.debug("incoming len(m) {0}".format(len(m)))
            try:
                self.tun.write(m.data)
            except RuntimeError as e:
                pass
        """

"""
class wstundClient():
    def __init__(self):
        # g.logger.debug('YMK in wstundClient __init__')
        self.tun = None
        self.ws = None
        self.thread = None
        self.running = False

    def outgoing(self):
        # while True:
        #     g.logger.debug('YMK in wstundClient outgoing')
        #     sleep(1)
        self.thread_closing = False
        self.count = 0
        poller = select.epoll()
        poller.register(self.tun, select.EPOLLIN)
        while True:
            # sleep(0.50)
            if self.thread_closing is True:
                break
            events = poller.poll(2)
            for fd, flag in events:
                if fd is self.tun.fileno():
                    buf = self.tun.read(self.tun.mtu)
                    # print("data len(buf) {1} [{0}]".format(hexlify(buf), len(buf)))
                    g.logger.debug("outgoing len(buf) {0}".format(len(buf)))
                    self.count += 1
                    self.ws.send(buf, True)

    def start(self):
        self.running = True
        # ## tuntap
        if self.tun is None:
            self.tun = TunTapDevice(flags=IFF_TUN | IFF_NO_PI)
        g.logger.debug(self.tun.name)
        self.tun.addr = g.config.get('client', 'ip')
        # self.tun.dstaddr = '10.10.0.1'
        self.tun.netmask = g.config.get('client', 'netmask')
        self.tun.mtu = int(g.config.get('client', 'mtu'))
        self.tun.up()

        # ## websocket
        # ws = PingClient('ws://{0}:{1}/ws'.format(args.host, args.port), protocols=['http-only', 'chat'])
        self.url = 'ws://{0}:{1}/ws'.format(g.config.get('client', 'host'), g.config.get('client', 'port'))
        self.ws = WebSocketTunClient(self.url, protocols=['http-only', 'chat'], heartbeat_freq=2.0)
        try:
            self.ws.daemon = True
            self.ws.connect()
        except:
            return

        # ## thread
        if self.thread is None:
            self.thread = Thread(target=self.outgoing)
            self.thread.daemon = True
            self.thread.start()

        # ## run forever
        self.run()

    def stop(self):
        if self.running is False:
            return
        self.thread_closing = True
        if self.thread is not None:
            self.thread.join()
            self.thread = None
        if self.ws is not None and not self.ws.terminated:
            self.ws.close()
            self.ws.closed(1000, "client receive signal.SIGTERM)")
            self.ws = None
        if self.tun is not None:
            self.tun.down()
        self.running = False

    def run(self):
        self.ws.run_forever()
        # while True:
        #     g.logger.debug('YMK in wstundClient run')
        #    sleep(1)
"""


def main():
    daemon_runner = DaemonRunner(WstundClientApp())
    try:
        daemon_runner.daemon_context.files_preserve = [h.stream for h in g.logger.handlers]
        daemon_runner.do_action()
    except (DaemonRunnerStopFailureError, LockTimeout) as e:
        g.logger.error(e)
        sys.exit(e)

# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai

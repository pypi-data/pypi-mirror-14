# -*- coding: utf-8 -*-
import config as g
from os.path import abspath, join, dirname
import sys
import random
import select
import logging
import cherrypy
from time import sleep
from lockfile import LockTimeout
from daemon.runner import DaemonRunner, DaemonRunnerStopFailureError
from subprocess import check_call
from threading import Thread
from pytun import TunTapDevice, IFF_TUN, IFF_NO_PI
# from ws4py import configure_logger
from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool
from ws4py.websocket import WebSocket
from ws4py.messaging import TextMessage


class TunWebSocketHandler(WebSocket):
    tun = None                  # TODO: tun device should shared in same network
    thread = None               # one thread one tun now, TODO TUN_TAP_MQ
    thread_counter = 0
    thread_closing = False

    def __init__(self, *args, **kwargs):
        super(TunWebSocketHandler, self).__init__(*args, **kwargs)

    def _background_send(self):
        poller = select.epoll()
        poller.register(TunWebSocketHandler.tun, select.EPOLLIN)
        while True:
            events = poller.poll(2)
            for fd, flag in events:
                if fd is TunWebSocketHandler.tun.fileno():
                    buf = TunWebSocketHandler.tun.read(TunWebSocketHandler.tun.mtu)
                    g.logger.debug("websocket-broadcast data len(buf) {}".format(len(buf)))
                    cherrypy.engine.publish('websocket-broadcast', buf, True)
                    # self.send(buf, True)

            # ## timeout then check thread_closing
            if TunWebSocketHandler.thread_closing is True:
                g.logger.debug("background_send thread_closing")
                break

    def opened(self):
        g.logger.debug("TunWebSocketHandler opened")

        if TunWebSocketHandler.tun is None:
            g.logger.debug("TunWebSocketHandler new tun")
            tun = TunTapDevice(flags=IFF_TUN | IFF_NO_PI)
            tun.addr = g.config.get('server', 'ip')
            # tun.dstaddr = '10.10.0.2'
            tun.netmask = g.config.get('server', 'netmask')
            tun.mtu = int(g.config.get('server', 'mtu'))
            tun.up()
            TunWebSocketHandler.tun = tun

        if TunWebSocketHandler.thread is None:
            g.logger.debug("TunWebSocketHandler new thread")
            TunWebSocketHandler.thread = Thread(target=self._background_send)
            TunWebSocketHandler.thread.daemon = True
            TunWebSocketHandler.thread.start()
        TunWebSocketHandler.thread_counter += 1

        if g.config.get('server', 'script.up') is not None:
            check_call(g.config.get('server', 'script.up'), shell=True)

    def received_message(self, m):
        if m is not None:
            if m.is_binary:
                g.logger.debug("received_message: bin len {}".format(len(m)))
                TunWebSocketHandler.tun.write(m.data)
            else:
                g.logger.debug("received_message: msg {}".format(m))

    def closed(self, code, reason="A client drop it's connection"):
        g.logger.debug("TunWebSocketHandler closed")
        cherrypy.engine.publish('websocket-broadcast', TextMessage(reason))
        g.logger.debug("TunWebSocketHandler closing thread")
        TunWebSocketHandler.thread_counter -= 1
        if TunWebSocketHandler.thread_counter == 0:
            TunWebSocketHandler.thread_closing = True
            TunWebSocketHandler.thread.join()
            TunWebSocketHandler.tun.down()
            g.logger.debug("TunWebSocketHandler closed thread")
            TunWebSocketHandler.thread = None
            TunWebSocketHandler.thread_closing = False
            TunWebSocketHandler.tun = None

        if g.config.get('server', 'script.down') is not None:
            check_call(g.config.get('server', 'script.down'), shell=True)


class Root(object):
    def __init__(self, host, port, ssl=False):
        self.host = host
        self.port = port
        self.scheme = 'wss' if ssl else 'ws'

    @cherrypy.expose
    def index(self):
        return """<html>
    <head>
      <script type='application/javascript' src='https://ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js'></script>
      <script type='application/javascript' src='js/cbuffer.js'></script>
      <script type='application/javascript'>
        $(document).ready(function() {

          // websocket = '%(scheme)s://%(host)s:%(port)s/ws';
          websocket = '%(scheme)s://' + window.location.host + '/ws';
          console.log(window.location);
          if (window.WebSocket) {
            ws = new WebSocket(websocket);
          }
          else if (window.MozWebSocket) {
            ws = MozWebSocket(websocket);
          }
          else {
            console.log('WebSocket Not Supported');
            return;
          }

          var Packet = function (src, dst, size, time) {
            this.src = src;
            this.dst = dst;
            this.size = size;
            this.time = time;
          }
          var pcbuffs = CBuffer(10);

          window.onbeforeunload = function(e) {
            ws.close(1000, 'wstund monitor leave');

            if(!e) e = window.event;
            e.stopPropagation();
            e.preventDefault();
          };
          ws.onmessage = function (evt) {
             // console.log("ws.onmessage packet size " + evt.data.size);
             var reader = new FileReader();
             reader.onload = function(event) {
                arrayBufferNew = this.result;
                pdata  = new Uint8Array(this.result);
                // console.log("data length " + pdata.length);
                /* for (i = 0; i < pdata.length; i++) {
                    console.log("data[ " + i + "] " + pdata[i]);
                } */

                src_ip = pdata[12] + '.' + pdata[13] + '.' + pdata[14] + '.' + pdata[15];
                dst_ip = pdata[16] + '.' + pdata[17] + '.' + pdata[18] + '.' + pdata[19];
                // console.log("src " + src_ip + " dst " + dst_ip);
                pcbuffs.push(new Packet(src_ip, dst_ip, pdata.length, Date.now()));
                // console.log("pcbuffs last " + pcbuffs.last().time);

                $('#pcbs').empty();
                for (i = 0; i < pcbuffs.length; i++) {
                    var p = pcbuffs.get(i);
                    if (p == undefined)
                        break;
                    var d = new Date(p.time);
                    var appstr = "<tr><td>" + p.src + "</td><td>";
                    appstr += p.dst + "</td><td>" + p.size + "</td><td>";
                    appstr += d + "</td></tr>";
                    $('#pcbs').append(appstr);
                }
             }
             reader.readAsArrayBuffer(evt.data)
          };
          ws.onopen = function() {
             // ws.send("%(username)s entered the room");
             console.log("ws.onopen could send messages");
             $('#status').text("wstund status: CONNECTED");
          };
          ws.onclose = function(evt) {
             $('#status').text("wstund status: DISCONNECTED");
          };
        });
      </script>
    </head>
    <body>
    <h2>wstund monitor (%(scheme)s://%(host)s:%(port)s)</h2>
    <h3 id='status'>wstund status: </h3>
    <table>
    <thead><tr><th>src</th><th>dst</th><th>len</th><th>time</th></tr></thead>
    <tbody id='pcbs'>
    </tbody>
    </table>
    </body>
    </html>
    """ % {'username': "wstund", 'host': self.host, 'port': self.port, 'scheme': self.scheme}

    @cherrypy.expose
    def ws(self):
        g.logger.debug("Handler created: {}".format(repr(cherrypy.request.ws_handler)))


# ## for daemon.runner
class WstundServertApp():
    def __init__(self):
        # ## for daemon.runner
        inout = '/dev/tty' if g.config.get('wstund', 'debug').lower() == 'true' else '/dev/null'
        self.stdin_path = self.stdout_path = self.stderr_path = inout
        self.pidfile_path = g.config.get('wstund', 'pidpath')
        self.pidfile_timeout = int(g.config.get('wstund', 'pidtimeout'))
        self.host = g.config.get('server', 'host')
        self.port = int(g.config.get('server', 'port'))

    def run(self):
        g.logger.info('server running at {}:{}'.format(self.host, self.port))
        # ## fro cherrypy
        # configure_logger(level=logging.DEBUG)
        cherrypy.config.update({'server.socket_host': self.host,
                                'server.socket_port': self.port,
                                'tools.staticdir.root': abspath(join(dirname(__file__), 'static'))})
        WebSocketPlugin(cherrypy.engine).subscribe()
        cherrypy.tools.websocket = WebSocketTool()

        cherrypy.quickstart(Root(self.host, self.port), '', config={
            '/ws': {
                'tools.websocket.on': True,
                'tools.websocket.handler_cls': TunWebSocketHandler
            },
            '/js': {
                'tools.staticdir.on': True,
                'tools.staticdir.dir': 'js'
            }
        })


def main():
    daemon_runner = DaemonRunner(WstundServertApp())
    try:
        daemon_runner.daemon_context.files_preserve = [h.stream for h in g.logger.handlers]
        daemon_runner.do_action()
    except (DaemonRunnerStopFailureError, LockTimeout) as e:
        g.logger.error(e)
        sys.exit(e)

# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai

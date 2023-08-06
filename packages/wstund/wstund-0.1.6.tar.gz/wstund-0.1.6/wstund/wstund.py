#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import os
import sys
import logging
import logging.handlers
import argparse
import ConfigParser
# from config import config, version, logger
import config as g

import wstund_client
import wstund_server


def load_default_config():
    # global config
    g.config = ConfigParser.RawConfigParser()
    g.config.add_section('wstund')
    g.config.add_section('client')
    g.config.add_section('server')
    g.config.set('wstund', 'role', 'server')
    g.config.set('wstund', 'debug', 'false')
    g.config.set('wstund', 'logfile', '/var/log/wstund.log')
    g.config.set('wstund', 'loglevel', 'INFO')
    g.config.set('wstund', 'tundev', '/dev/net/tun')
    g.config.set('wstund', 'pidpath', '/run/wstund.pid')
    g.config.set('wstund', 'pidtimeout', '5')
    g.config.set('client', 'host', '127.0.0.1')
    g.config.set('client', 'port', '5000')
    g.config.set('client', 'ip', '10.10.0.4')
    g.config.set('client', 'netmask', '255.255.255.0')
    g.config.set('client', 'mtu', '1450')
    g.config.set('client', 'reconnect.interval', '5')
    g.config.set('client', 'script.up', None)
    g.config.set('client', 'script.down', None)
    g.config.set('server', 'host', '0.0.0.0')
    g.config.set('server', 'port', '5000')
    g.config.set('server', 'ip', '10.10.0.1')
    g.config.set('server', 'netmask', '255.255.255.0')
    g.config.set('server', 'mtu', '1450')
    g.config.set('server', 'script.up', None)
    g.config.set('server', 'script.down', None)


def load_config(args=None):
    load_default_config()

    if args.config is not None:
        g.config.read(args.config)

    if args.debug is not None:
        g.config.set('wstund', 'debug', 'true' if args.debug else 'false')

    levels = {k: getattr(logging, k) for k in ['CRITICAL', 'FATAL', 'ERROR',
                                               'WARNING', 'INFO', 'DEBUG']}
    lvl = g.config.get('wstund', 'loglevel').upper()
    lvl = levels[lvl] if lvl in levels else None
    lvl = lvl if args.verbose is None else max([logging.DEBUG,
                                                logging.ERROR - (args.verbose * 10)])
    set_logging_level(lvl)


def dump_config(role_only=False):
    role = g.config.get('wstund', 'role')
    for s in g.config.sections():
        if s not in ['wstund', role]:
            continue
        print("[{}]".format(s))
        for o in g.config.options(s):
            print("  {}: {}".format(o, g.config.get(s, o)))


def set_logging_level(plevel=None):
    lvl = logging.ERROR if plevel is None else plevel     # default logging level
    g.logger = logging.getLogger('wstund')              # global logger
    g.logger.setLevel(lvl)
    formatter = logging.Formatter('%(asctime)s %(name)s:%(levelname)s %(message)s')
    logs = [logging.handlers.RotatingFileHandler(g.config.get('wstund', 'logfile'),
                                                 maxBytes=1024*1024, backupCount=10)]
    if g.config.get('wstund', 'debug').lower() == 'true':
        logs.append(logging.StreamHandler())
    map(lambda l: l.setFormatter(formatter), logs)
    map(lambda l: g.logger.addHandler(l), logs)


def main():
    parser = argparse.ArgumentParser(description='websocket tunnel daemon')
    parser.add_argument('-c', '--config', nargs='?', default='/etc/wstund.conf',
                        help='specify config file')
    parser.add_argument('-r', '--role', default=None, choices=['server', 'client'],
                        help='specify role setting')
    parser.add_argument('-H', '--host', default=None, nargs='?',
                        help='specify host to listen/connect')
    parser.add_argument('-p', '--port', default=None, nargs='?',
                        help='specify port to listen/connect')
    parser.add_argument('-d', '--debug', action='store_true', default=None,
                        help='debug print out to current tty')
    parser.add_argument('-s', '--show_config', action='store_true', default=None,
                        help='show current configuration')
    parser.add_argument('-v', '--verbose', action='count', default=None,
                        help='increase log level, more times more logs')
    parser.add_argument('-V', '--version', action='version',
                        version='{}'.format(g.version),
                        help='show version infomation')

    args = parser.parse_known_args()[0]
    load_config(args)

    role = args.role if args.role is not None else g.config.get('wstund', 'role')
    if role not in ['server', 'client']:
        print("Please specify which role for wstund [server|client]")
        return
    g.config.set('wstund', 'role', role)

    def _set_args_configs(k):
        v = getattr(args, k)
        if v is not None:
            g.config.set(role, k, v)
    map(_set_args_configs, ['host', 'port'])
    g.logger.info('main role [{}]'.format(g.config.get('wstund', 'role')))

    if args.show_config is not None and args.show_config:
        dump_config(role_only=True)
        return

    main_role = wstund_client.main if role == 'client' else wstund_server.main
    main_role()


def sudo_main():
    if os.getuid() != 0:
        os.execvp("sudo", ["sudo", "python2"] + sys.argv)
    main()


if __name__ == "__main__":
    sudo_main()

# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai

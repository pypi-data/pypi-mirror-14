#!/usr/bin/env python
#
"""
Main program
"""
from __future__ import print_function
from __future__ import unicode_literals
from fnmatch import fnmatchcase
from io import TextIOWrapper
from random import randint

from future import standard_library
from ipcalc import Network
from jw.util.python3hell import Open

standard_library.install_aliases()
from builtins import object
from _socket import SOCK_DGRAM, herror
from datetime import timedelta
import json
import logging
import sys
from argparse import ArgumentParser, Action

from dnslib import DNSRecord, RR, QTYPE, A, SOA
from gevent.pool import Pool
from gevent.socket import socket, gethostbyaddr
from gevent.monkey import patch_all
from pkg_resources import get_distribution
from urllib.request import urlopen
import time

patch_all()

__version__ = get_distribution('jw.badipsrbl').version
__author__ = "Johnny Wezel"

LOG_DEBUG2 = 9
LOG_DEBUG3 = 8

logging.addLevelName(LOG_DEBUG2, 'DEBUG2')
logging.addLevelName(LOG_DEBUG3, 'DEBUG3')
Logger = logging.getLogger(__name__)

VERSION = ("""
badipsrbl version {}
Copyright (c) 2015 {}
License: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>.
This is free software. You are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
""".strip().format(__version__, __author__)
)
LOG_LEVELS = logging._nameToLevel if sys.version_info[:2] > (3, 3) else logging._levelNames
INITIAL_LOG_LEVEL = logging.WARNING
DEFAULT_LOG_FILE = '/var/log/badipsrbl'

PERIOD = 3600 * 24 * 30 * 6  # 6 months
BIG_SPACE = 40 * ' '

RESERVED_IPS = (
    ((0, 0, 0, 0), (0, 255, 255, 255)),
    ((10, 0, 0, 0), (10, 255, 255, 255)),
    ((100, 64, 0, 0), (100, 127, 255, 255)),
    ((127, 0, 0, 0), (127, 255, 255, 255)),
    ((169, 254, 0, 0), (169, 254, 255, 255)),
    ((172, 16, 0, 0), (172, 31, 255, 255)),
    ((192, 0, 0, 0), (192, 0, 0, 255)),
    ((192, 0, 2, 0), (192, 0, 2, 255)),
    ((192, 88, 99, 0), (192, 88, 99, 255)),
    ((192, 168, 0, 0), (192, 168, 255, 255)),
    ((198, 18, 0, 0), (198, 19, 255, 255)),
    ((198, 51, 100, 0), (198, 51, 100, 255)),
    ((203, 0, 113, 0), (203, 0, 113, 255)),
    ((224, 0, 0, 0), (239, 255, 255, 255)),
    ((240, 0, 0, 0), (255, 255, 255, 254)),
)

RBL_BLOCKED = '127.0.0.2'
RBL_BAD_IP = '127.0.0.3'
FEW_REPORTS = 3

class Version(Action):
    def __call__(self, *args, **kwargs):
        print(VERSION)
        sys.exit(0)

class Program(object):
    """
    Program
    """

    def __init__(self):
        # Set up argument parsing
        argp = ArgumentParser(fromfile_prefix_chars='@')
        argp.add_argument('arg', nargs='*')
        argp.add_argument(
            '--port', '-p',
            action='store',
            type=int,
            default=53,
            help='specify port (default: 53)'
        )
        argp.add_argument(
            '--log-level',
            '-L',
            action='store',
            default='INFO',
            choices=('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'),
            type=lambda s: s.upper(),
            help='set log level (default INFO)'
        )
        argp.add_argument(
            '--log-file',
            '-l',
            action='store',
            default=DEFAULT_LOG_FILE,
            help='set log file (default: %s)' % DEFAULT_LOG_FILE
        )
        rGroup = argp.add_mutually_exclusive_group()
        rGroup.add_argument('--report', '-r', action='store_true', help='report all bad IPs')
        rGroup.add_argument('--report-domain', '-R', action='store', nargs='*', help='report bad IPs for these query domains')
        argp.add_argument('--host', '-H', action='store', nargs='*', help='accept requests only from these hostnames')
        argp.add_argument('--ip', '-I', action='store', nargs='*', help='accept requests only from these IPs')
        argp.add_argument('--exclude', '-x', action='store', type=Network, nargs='*', help='mark networks as "good"')
        argp.add_argument('--version', '-V', nargs=0, action=Version, help='display version and exit')
        # Parse arguments
        self.args = argp.parse_args()
        # Set up logging
        level = LOG_LEVELS[self.args.log_level]
        logging.basicConfig(
            stream=Open(self.args.log_file, 'a'),
            level=level,
            format='%(asctime)s %(levelname)-8s %(name)s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        Logger.debug('Arguments: %s', self.args)
        # Initialize program data
        self.pool = Pool()
        self.socket = socket(type=SOCK_DGRAM)
        try:
            categories = json.loads(
                TextIOWrapper(urlopen('https://www.badips.com/get/categories')).read()
            )['categories']
        except Exception as e:
            Logger.critical('Could not read categories from badips.com')
            raise
        self.mailCategories = {c['Name'] for c in categories if c.get('Parent') == 'mail'} | {'default'}

    def run(self):
        """
        Run program
        """
        self.socket.bind(('', self.args.port))
        # Request loop
        while True:
            request, address = self.socket.recvfrom(4096)
            self.handleRequest(address, request)

    def handleRequest(self, address, request):
        """
        Handle request

        :param address: adress (IP, port) tuple
        :type address: tuple
        :param request: DNS request blob
        :type request: bytes
        """
        for _ in ['once']:  # Pseudo block
            requester = address[0]
            reply = None
            try:
                dnsRequest = DNSRecord.parse(request)
            except Exception as e:
                Logger.critical('From DNSRecord.parse(): %s', e)
                break
            name = dnsRequest.get_q().get_qname().idna()
            # TODO: define base domain name and make parsing dependent on that
            sname = name.split('.')[3::-1]
            qname = '.'.join(sname)
            dname = '.'.join(p for p in name.split('.')[4:] if p)
            Logger.debug('dname="%s"', dname)
            reply = dnsRequest.reply()
            # Get requester's hostname
            try:
                rhostname = gethostbyaddr(requester)[0]
                rhost = '%s (%s)' % (requester, rhostname)
            except Exception as e:
                rhostname = ''
                rhost = '%s (%s)' % (requester, e)
            Logger.info('<- Query %s from %s', name, rhost)
            # Check for valid requester IP
            if self.args.ip and requester not in self.args.ip:
                if self.args.exclude and any(requester in x for x in self.args.exclude):
                    Logger.warning('-> Invalid requester IP, but white-listed: %s', rhost)
                    break
                Logger.warning('-> Invalid requester IP: %s', rhost)
                self.reportBadIp(requester, dname)
                self.returnRandomIp(name, reply)
                break
            # Check for valid requester hostname
            if self.args.host and not any(fnmatchcase(rhostname, h) for h in self.args.host):
                if self.args.exclude and any(requester in x for x in self.args.exclude):
                    Logger.warning('-> Invalid requester hostname, but white-listed: %s', rhostname)
                    break
                Logger.warning('-> Invalid requester hostname: %s', rhostname)
                self.reportBadIp(requester, dname)
                self.returnRandomIp(name, reply)
                break
            # Check for valid request
            if len(sname) != 4:
                # Invalid IP in request
                Logger.warning('-> Invalid IP (not 4 elements): "%s"', qname)
                self.reportBadIp(requester, dname)
                self.returnRandomIp(name, reply)
                break
            try:
                ip = tuple(int(b) for b in sname)
            except ValueError:
                # Invalid IP in request
                Logger.warning('-> Invalid IP (non-integers): "%s"', qname)
                self.reportBadIp(requester, dname)
                self.returnRandomIp(name, reply)
                break
            if any(l <= ip <= u for l, u in RESERVED_IPS):
                # Ignore reserved IPs
                Logger.warning('-> Reserved IP: %s', qname)
                reply.add_answer(RR(name, QTYPE.A, rdata=A(RBL_BAD_IP), ttl=60))
                break
            try:
                qhost = '%s (%s)' % (qname, gethostbyaddr(qname)[0])
            except Exception as e:
                qhost = '%s (%s)' % (qname, e)
                if isinstance(e, herror) and e.errno == 1:
                    if self.args.exclude and any(qname in x for x in self.args.exclude):
                        Logger.warning('-> %s has no hostname, but white-listed', qname)
                    else:
                        # No hostname for IP --> bad guy
                        Logger.warning('-> %s has no hostname', qname)
                        self.reportBadIp(qname, dname)
                        reply.add_answer(RR(name, QTYPE.A, rdata=A(RBL_BLOCKED), ttl=60))
                else:
                    Logger.critical('From gethostbyaddr("%s"), getting IP for request: %s', qname, e)
                break
            # Ignore white-listed IP
            if self.args.exclude and any(qname in x for x in self.args.exclude):
                Logger.info('-> %s is white-listed', qhost)
                break
            # Get info about IP from badips.com
            try:
                data = json.loads(TextIOWrapper(urlopen('https://www.badips.com/get/info/%s' % qname)).read())
                Logger.debug('From badips.com: %s', data)
            except:
                Logger.exception('Querying %s:', qhost)
                break
            # Ignore IP if not listed
            if not data['Listed']:
                Logger.info('-> %s not listed', qhost)
                break
            # Ignore IP if there are only mail-based reports, because it could hit big mail providers
            if all(c in self.mailCategories for c in data['Categories']):
                Logger.info('-> %s only reported in mail categories', qhost)
                break
            # Get count and last report time
            reportCount = data['ReporterCount']['sum']
            reportTime = max(data['LastReport'].values())
            Logger.debug('count: %s, time: %s', reportCount, time.strftime('%F %T', time.localtime(reportTime)))
            # Ignore IP if last report time too old
            if time.time() - reportTime > PERIOD:
                Logger.info('-> %s reported more than %s ago', qhost, timedelta(0, PERIOD))
                break
            # Ignore IP if not a lot of reports and reported before limited period
            if reportCount <= FEW_REPORTS and (time.time() - reportTime) > reportCount * 3600 * 24 * 7:
                Logger.info(
                    '-> %s reported %(count)d times and reported more than %(count)d weeks ago',
                    qhost,
                    dict(count=reportCount)
                )
                break
            # Positive: return IP as bad buy and report it to badips.com
            reply.add_answer(RR(name, QTYPE.A, rdata=A(RBL_BLOCKED), ttl=60))
            Logger.info('-> %s bad guy', qhost)
            self.reportBadIp(qname, dname)
            break
        # Add result reply
        if reply:
            reply.add_auth(
                RR(
                    dname,
                    QTYPE.SOA,
                    ttl=60,
                    rdata=SOA(
                        dname,
                        'admin.wezel.info',
                        (int(time.time()), 60, 60, 60, 60)
                    )
                )
            )
            Logger.debug('Reply sent: \n%s', '\n'.join(BIG_SPACE + l for l in str(reply).split('\n')))
            try:
                self.socket.sendto(reply.pack(), address)
            except Exception:
                Logger.exception('While sending DNS reply:')

    def returnRandomIp(self, name, reply):
        """
        Report a random IP to an illegal requester for fun

        :param name: request
        :type name: str
        :param reply: DNS record
        :type reply: DNSRecord
        """
        reply.add_answer(RR(name, QTYPE.A, rdata=A('.'.join(str(randint(0, 255)) for _ in range(4))), ttl=60))

    def reportBadIp(self, ip, domain=None, category='badbots'):
        """
        Report IP to badips.com

        :param ip: IP
        :type ip: str
        :param domain: query base domain
        :type domain: str
        :param category: category to report IP in
        :type category: str

        Report `ip` as bad if ``--report`` given or ``--report-domain`` given and query base domain matches some of the domains
        mentioned in the option.
        """
        if self.args.report or self.args.report_domain and domain and domain in self.args.report_domain:
            try:
                Logger.info(
                    'Reported %s as %s -> %s',
                    ip,
                    category,
                    TextIOWrapper(urlopen('https://www.badips.com/add/%s/%s' % (category, ip))).read()
                )
            except:
                Logger.exception('Reporting spammer %s as %s', ip, category)

def Main():
    program = Program()
    sys.exit(program.run())

if __name__ == '__main__':
    Main()

"""
Test handleRequest()
"""
from dnslib import DNSQuestion
from dnslib import DNSRecord
import sys

from jw.badips import main


def NewRequest(query):
    return DNSRecord(q=DNSQuestion(query)).pack()

class test10_HandleRequest:

    def test10_GoodReqest(self):
        sys.argv = ['program', '-l/dev/stdout', '-LDEBUG']
        program = main.Program()
        program.handleRequest(('127.0.0.1', 55555), NewRequest('8.8.8.8.rbl.wezel.info'))

    def test10_ShortRequest(self):
        sys.argv = ['program', '-l/dev/stdout']
        program = main.Program()
        program.handleRequest(('127.0.0.1', 55555), NewRequest('8.8.8.rbl.wezel.info'))

    def test10_BadIpReqest(self):
        sys.argv = ['program', '-l/dev/stdout']
        program = main.Program()
        program.handleRequest(('127.0.0.1', 55555), NewRequest('x8.x8.x8.x8.rbl.wezel.info'))

    def test10_ReservedIpReqest(self):
        sys.argv = ['program', '-l/dev/stdout']
        program = main.Program()
        program.handleRequest(('127.0.0.1', 55555), NewRequest('1.0.0.127.rbl.wezel.info'))

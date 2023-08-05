# -*- coding: utf-8 -*-

__version__ = '0.1.19'

import re
import sys
import logging

from supervisor import childutils


class SVDog(object):
    def __init__(self, logger_name, processes=None, excludes=None):
        self.processes = processes
        self.excludes = excludes
        self.stdin = sys.stdin
        self.stdout = sys.stdout
        self.logger = logging.getLogger(logger_name or __name__)

    def run(self):
        while True:
            headers, payload = childutils.listener.wait(self.stdin, self.stdout)

            if not payload.endswith('\n'):
                payload = payload + '\n'

            pheaders, pdata = childutils.eventdata(payload)

            process_name = pheaders.get('processname')

            if process_name and self.excludes and filter(lambda x: re.match(x, process_name), self.excludes):
                childutils.listener.ok(self.stdout)
                continue

            if process_name and self.processes and not filter(lambda x: re.match(x, process_name), self.processes):
                childutils.listener.ok(self.stdout)
                continue

            self.logger.fatal('%s\n%s', headers, payload)
            childutils.listener.ok(self.stdout)

#!/usr/bin/env python
#234567891123456789212345678931234567894123456789512345678961234567897123456789
# encoding: utf-8

import colorlog
import logging
import os
import sys

# get root logger
log = logging.getLogger()
log.setLevel(logging.DEBUG)

# console handler gets all log entries
ch = logging.StreamHandler() # defaults to sys.stderr

log.addHandler(ch)

formatstr = '%(asctime)s [%(levelname)-.4s] %(message)s'
colorFormatter = colorlog.ColoredFormatter(
    '%(log_color)s' + formatstr
)

formatter = logging.Formatter(
    formatstr
)


log.notice = log.info


if sys.stdout.isatty():
    ch.setFormatter(colorFormatter)
else:
    ch.setFormatter(formatter)

# log to syslog if env var is setup
if os.environ.get('LOG_TO_SYSLOG',False):

    # default to UDP if no socket found
    address = ('localhost', 514)
   
    from logging.handlers import SysLogHandler

    locations = [
        "/var/run/syslog",  # osx
        "/dev/log",         # linux
        "/var/run/log"      # freebsd
    ]

    for p in locations:
        if os.path.exists(p):
            address = p

    slh = SysLogHandler(address=address)
    syslogFormatter = logging.Formatter('%(message)s')
    slh.setFormatter(syslogFormatter)
    log.addHandler(slh)

def panic(msg):
    log.critical(msg)
    sys.exit(1)

log.panic = panic
log.die = panic

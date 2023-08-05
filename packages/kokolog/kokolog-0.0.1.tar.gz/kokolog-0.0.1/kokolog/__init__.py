#!/usr/bin/python
# coding=utf8

"""
    
"""

__import__('pkg_resources').declare_namespace(__name__)
__version__ = '0.0.1'
__author__ = 'hk'

import sys
import logging
from logging import Logger
from logging import Handler, LogRecord

CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
NOTSET = 0

try:
    unicode
    _unicode = True
except NameError:
    _unicode = False


class MyLocal(object):

    def __init__(self, **kwargs):
        self.__dict__.update(**kwargs)


class KokologHandler(Handler, object):

    def __init__(self):
        self._name = ''
        Handler.__init__(self)

    def emit(self, record):
        pass


class KokologRecord(LogRecord):
    def __init__(self, name, level, fn, lno, msg, args, kwargs, exc_info, func=None):
        self.kwargs = kwargs
        super(KokologRecord, self).__init__(name, level, fn, lno, msg, args, exc_info, func)


class KokologLogger(Logger):
    def debug(self, msg, *args, **kwargs):
        if self.isEnabledFor(DEBUG):
            self._log(DEBUG, msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        if self.isEnabledFor(INFO):
            self._log(INFO, msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        if self.isEnabledFor(WARNING):
            self._log(WARNING, msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        if self.isEnabledFor(ERROR):
            self._log(ERROR, msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        if self.isEnabledFor(CRITICAL):
            self._log(CRITICAL, msg, *args, **kwargs)

    def log(self, level, msg, *args, **kwargs):
        if not isinstance(level, int):
            if raiseExceptions:
                raise TypeError("level must be an integer")
            else:
                return
        if self.isEnabledFor(level):
            self._log(level, msg, *args, **kwargs)


    def _log(self, level, msg, *args, **kwargs):
        if logging._srcfile:
            try:
                fn, lno, func = self.findCaller()
            except ValueError:
                fn, lno, func = "(unknown file)", 0, "(unknown function)"
        else:
            fn, lno, func = "(unknown file)", 0, "(unknown function)"
        exc_info = kwargs.get('exc_info')
        extra = kwargs.get('extra')
        if exc_info:
            if not isinstance(exc_info, tuple):
                exc_info = sys.exc_info()
        record = self.makeRecord(self.name, level, fn, lno, msg, args, kwargs, exc_info, func, extra)
        self.handle(record)

    def makeRecord(self, name, level, fn, lno, msg, args, kwargs, exc_info, func=None, extra=None):
        addition = [one for one in kwargs.keys() if not one in ('exc_info', 'extra', 'printlevel')]
        if not '%s' in msg:
            msg = msg + ' '.join(['%s' for one in args])
        for one in addition:
            msg = msg + '\n' + one + ':  %s'
        args = tuple([str(one) for one in args] + [str(kwargs[one]) for one in addition])
        rv = KokologRecord(name, level, fn, lno, msg, args, kwargs, exc_info, func)
        if extra is not None:
            for key in extra:
                if (key in ["message", "asctime"]) or (key in rv.__dict__):
                    raise KeyError("Attempt to overwrite %r in LogRecord" % key)
                rv.__dict__[key] = extra[key]
        return rv

Logger.manager.setLoggerClass(KokologLogger)
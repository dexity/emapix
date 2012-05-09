import logging
import logging.handlers
from django.conf import settings

class Logger(object):
    @classmethod
    def get(cls, name, format=None, filename=None, filesize=None, filecount=None, datefmt=None):
        ''' Factory function to get loggers. Uses settings from settings.py unless explicitly passed. '''
        # only log errors unless debug is on
        level = logging.ERROR
        if settings.DEBUG:
            level = logging.DEBUG
        if format is None:
            format = settings.LOG_FORMAT
        if filename is None:
            filename = settings.LOG_FILENAME
        if filesize is None:
            filesize = settings.LOG_FILESIZE
        if filecount is None:
            filecount = settings.LOG_FILECOUNT
        if datefmt is None:
            datefmt = settings.LOG_DATEFMT
        logger = logging.getLogger(name)
        logger.setLevel(level)
        handler = logging.handlers.RotatingFileHandler(filename, maxBytes=filesize, backupCount=filecount)
        formatter = logging.Formatter(format, datefmt=datefmt)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger
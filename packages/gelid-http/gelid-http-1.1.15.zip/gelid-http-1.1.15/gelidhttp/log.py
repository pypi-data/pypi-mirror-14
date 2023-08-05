# -*- coding: UTF-8 -*-
# lvjiyong on 2015/6/13.

import logging
import logging.config
import sys
from gelidhttp import settings


log_console = logging.StreamHandler(sys.stderr)
formatter = logging.Formatter("%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s")
log_console.setFormatter(formatter)
logger = logging.getLogger('gelid')
logger.setLevel(logging.DEBUG)
logger.addHandler(log_console)


def setLogLevel(log_level):
    global logger
    logger.setLevel(log_level)
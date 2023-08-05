# -*- coding: UTF-8 -*-
# lvjiyong on 2015/6/7.

"""
一些静态配置信息，后期将支持动态加载
"""
import logging

REQUEST_TIMEOUT = 60

HTTP_HEADER = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:34.0) Gecko/20100101 Firefox/34.0',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Language': 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
               'Accept-Encoding': 'gzip'
               }

LOG_LEVEL = logging.DEBUG
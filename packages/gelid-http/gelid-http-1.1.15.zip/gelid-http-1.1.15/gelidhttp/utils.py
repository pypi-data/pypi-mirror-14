# -*- coding: UTF-8 -*-
# lvjiyong on 2015/6/7.

"""
提取代码中的常用代码封装成函数形式方便调整
"""

__all__ = ['match_encoding', 'search_cookie', 'http_headers']

import re
from urlparse import urlparse
from gelidhttp.settings import HTTP_HEADER


def match_encoding(html):
    """
    从文本中获取charset编码
    >>> match_encoding('<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />')
    'utf-8'
    >>> match_encoding('<meta charset="utf-8"/>')
    'utf-8'
    >>> match_encoding('application/javascript; charset=GB2312')
    'GB2312'
    """
    pattern_str = 'text/html;\s*charset=([a-z\d-]{2,10})| charset="?([a-z\d-]{2,10})"?'
    pattern_com = re.compile(pattern_str, re.IGNORECASE | re.MULTILINE)
    match = re.search(pattern_com, html)
    if match:
        return match.group(1) or match.group(2)


def search_cookie(html):
    """
    搜索内容中的cookie
    :param html:
    :return:
    """
    if 'cookie' in html:
        pattern_com = re.compile('cookie=[\'"](.+?)[\'"]', re.I | re.M)
        cookie = re.match(pattern_com, html)
        if cookie:
            return cookie.group(1)


def http_headers(url, **kwargs):
    """
    初使化请求header
    >>> header = http_headers('https://github.com')
    >>> header['Accept']
    'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    >>> header_2 = http_headers('https://github.com', Accept='text/html')
    >>> header['Accept']
    'text/html'

    >>> header = http_headers('http://feed.mix.sina.com.cn/api/roll/get?pageid=51&lid=740')
    >>> header['Referer']
    'http://sina.com.cn'

    >>> header = http_headers('http://mix.sina.com.cn/api/roll/get?pageid=51&lid=740')
    >>> header['Referer']
    'http://sina.com.cn'

    >>> header = http_headers('http://www.sina.com.cn/api/roll/get?pageid=51&lid=740')
    >>> header['Referer']
    'http://www.sina.com.cn'

    >>> header = http_headers('http://sina.com.cn/api/roll/get?pageid=51&lid=740')
    >>> header['Referer']
    'http://sina.com.cn'

    """
    url_parse = urlparse(url)
    header = HTTP_HEADER.copy()

    host = url_parse.hostname
    if host:
        hosts = host.split('.')
        if len(hosts) > 3 and hosts[-4] != 'www':
            host = '.'.join(hosts[-3:])

    header['Referer'] = "http://{0}".format(host)
    header['Accept-Encoding'] = 'gzip'

    for k, v in kwargs.iteritems():
        header[k] = v

    return header


if __name__ == "__main__":
    import doctest

    doctest.testmod()

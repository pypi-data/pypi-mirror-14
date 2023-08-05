# -*- coding: UTF-8 -*-
# lvjiyong on 2015/6/7.

"""
简单装了python-gelid可能用到的http请求
request_with_header：带有较完整的http请求及返回
request：简单返回内容
request：简单返回可能是图片或文件的数据，如果不是则返回空
"""
import socket
import re
import time
from gelidhttp.log import logger

__all__ = ['request_with_header', 'request', 'request_file']

from StringIO import StringIO
import gzip
import urllib2
from urlparse import urljoin
from gelidhttp import utils, settings
from gelidhttp.parameter import Parameter

_dns_cache = {}


def _set_dns_cache():
    def cache_address(*args, **kwargs):
        global _dns_cache
        if args in _dns_cache:
            return _dns_cache[args]
        else:
            _dns_cache[args] = getattr(socket, 'cache_address')(*args, **kwargs)
            return _dns_cache[args]

    if not hasattr(socket, 'cache_address'):
        setattr(socket, 'cache_address', socket.getaddrinfo)
        setattr(socket, 'getaddrinfo', cache_address)


def request_with_header(url, **kwargs):
    """
    获取请求内容，返回内容与header
    >>> page = request_with_header('http://www.163.com/')
    >>> '163.com' in page[0]
    True
    >>> page[1].getcode()
    200
    >>> page[1].headers.get('Content-Encoding')
    'gzip'
    """

    logger.debug('request url:%s' % url)
    params = Parameter(kwargs)
    params.max_request = params.max_request or 0
    timeout = params.timeout or settings.REQUEST_TIMEOUT
    auto_cookie_request = params.auto_cookie_request or False
    content = None
    page = Parameter()

    # logger.debug('kwargs:%s' % kwargs)
    # logger.debug('params.headers:%s' % params.headers)

    if not params.headers:
        params.headers = utils.http_headers(url)
        # logger.debug('params.headers:%s' % params.headers)
    try:
        _set_dns_cache()
        if params.proxy:
            opener = urllib2.build_opener(urllib2.ProxyHandler(params.proxy))
            urllib2.install_opener(opener)

        # logger.debug('开始下载:%s' % url)
        # logger.debug('下载参数:%s' % params)

        req = urllib2.Request(url=url, headers=params.headers, data=params.data)
        page = urllib2.urlopen(req, timeout=timeout)
        # 如果gzip则解压缩
        if page.info().get('Content-Encoding') == 'gzip':
            buf = StringIO(page.read())
            body = gzip.GzipFile(fileobj=buf)
            content = body.read()
        else:
            content = page.read()
        # 如果有跳转且标识，则进行跳转
        logger.debug('redirect %s :%s' % (params.no_redirect, params.max_request))
        if not params.no_redirect and params.max_request < 2:
            # logger.debug('content:%s' % content)
            redirected_url = None
            if page.getcode() in [301, 302, 303, 307] and 'Location' in page.headers:
                redirected_url = urljoin(url, page.headers['location'])
            else:
                # <META HTTP-EQUIV="REFRESH" CONTENT="0; URL=html/2015-08/21/node_33.htm"></head>
                meta_refresh = 'content="\d+;\s*URL=\'?(.+?)\'?">'
                meta_refresh_compile = re.compile(meta_refresh, re.I|re.M)
                match = re.search(meta_refresh_compile, content)
                if match:
                    meta_url = match.group(1)
                    redirected_url = urljoin(url, meta_url)
            if redirected_url:
                page.close()
                params.max_request += 1
                logger.debug('redirected_url:%s' % url)
                return request_with_header(redirected_url, **params)

        page.close()
        # 如果内容少于200字且标记为自动设置cookie重请求
        if len(content) < 200 and auto_cookie_request and params.max_request < 2:
            cookie_regex = utils.search_cookie(content)
            if cookie_regex:
                page_cookie = cookie_regex
            elif page.headers.get('Set-Cookie'):
                page_cookie = page.headers['Set-Cookie']
            else:
                page_cookie = None
            if page_cookie:
                params.headers['Cookie'] = page_cookie
                params.max_request += 1
                page.close()
                logger.debug('cookie redirected_url:%s' % url)
                return request_with_header(url, **params)
        url = page.geturl()

    except Exception as e:
        if params.error_callback:
            params.error_callback(e)
        else:
            raise e

    return content, page, url


def request(url, **kwargs):
    """
    获取网页内容
    >>> page = request('http://www.163.com/')
    >>> '163.com' in page
    True
    """
    return request_with_header(url, **kwargs)[0]


def request_file(url, **kwargs):
    """
    获取内容，只下载header中的Content-Type有image或stream标记的
    >>> page = request_file('http://www.163.com/')
    >>> page

    >>> page = request_file('https://www.baidu.com/favicon.ico')
    >>> len(page) > 3000
    True
    """
    file_object = None
    error_callback = kwargs.get('error_callback')
    message = None
    if url and str(url).startswith('http'):
        http_request = request_with_header(url, **kwargs)
        if http_request[0]:
            content_type = http_request[1].headers.get('Content-Type')
            # 只获取文件头含有image或stream的内容
            if content_type and ('image' in content_type or 'stream' in content_type):
                file_object = http_request[0]
            else:
                message = 'Content-Type:%s' % content_type
    else:
        message = u'文件地址错误'
    if error_callback:
        error_callback(message)

    return file_object


if __name__ == "__main__":
    import doctest

    doctest.testmod()
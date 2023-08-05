# -*- coding: UTF-8 -*-
# lvjiyong on 2015/6/7.

"""
封装Http Request，结果以Response输出
"""
__all__ = ['Request']

import chardet
from gelidhttp import http, utils
from gelidhttp.response import Response
from gelidhttp.parameter import Parameter
from log import logger


class Request(Parameter):
    """
    封装http请求，输出response等
    >>> page = Request('http://www.163.com/')
    >>> '163.com' in page.response.body
    True
    >>> page.response.encoding
    'gb18030'

    >>> response = Request('http://ent.qq.com/a/20150825/042914.hdBigPic.js').response
    >>> response.encoding
    'gb18030'

    >>> response = Request(url='http://nhwb.cnjxol.com/',).response
    >>> 'enpproperty' in response.body_as_unicode()
    True
    """

    def set_response(self, url, **kwargs):
        self.url = url
        params = Parameter(kwargs)
        self.headers = params.headers or {}
        self.cookies = params.cookies
        if url and str(url).startswith('http'):
            content, info, url = http.request_with_header(url, **kwargs)
            self.status = info.getcode()
            params.headers = self.headers
            params.body = content
            params.cookies = info.headers.get('Set-Cookie')
            params.headers['Content-Type'] = info.headers.get('Content-Type')
            #
            # logger.debug(info.headers.get('Content-Type'))

            response = Response(url=url, **params)

            # 获取编码方式并解码
            encoding = self.encoding
            if not encoding:
                encoding = utils.match_encoding(response.body)
                if not encoding:
                    encoding = utils.match_encoding(params.headers.get("Content-Type", ""))
                if not encoding:
                    encoding = 'utf-8'

            if encoding.lower() in ('gbk', 'gb2312'):
                encoding = 'gb18030'
            try:
                response.encoding = encoding
                response._body_as_unicode = response.body.decode(response.encoding, 'ignore')
            except:
                response.encoding = chardet.detect(response.body).get('encoding')
                response._body_as_unicode = response.body.decode(response.encoding, 'ignore')
            response.url = url
            response.headers = info.headers
            self.response = response


    def __init__(self, url, **kwargs):
        super(Request, self).__init__(**kwargs)
        # try:
        self.url = url
        self.response = None
        self.headers = None
        self.status = 0
        self.cookies = None
        self.set_response(url=url, **kwargs)
        self.encoding = kwargs.get('encoding') or 'utf-8'
        callback = kwargs.get('callback')
        if callback:
            call = callback(self.response)
            if hasattr(call, 'next'):
                call.next()
        # except Exception as e:
        #     if self.error_callback:
        #         self.error_callback(e)
        #     else:
        #         raise e


if __name__ == "__main__":
    import doctest

    doctest.testmod()
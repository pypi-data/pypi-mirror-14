# -*- coding: UTF-8 -*-
# lvjiyong on 2015/6/7.

"""
封装了Request输出的基本内容格式
"""

__all__ = ['Response']

from gelidhttp.parameter import Parameter


class Response(Parameter):
    """
    封装输出
    >>> response = Response(url='http://www.163.com')
    >>> response.url
    'http://www.163.com'
    >>> response = Response('http://www.163.com', encoding='gbk')
    >>> response.encoding
    'gbk'
    >>> response.body_as_unicode()

    """

    def __init__(self, seq=None, **kwargs):

        self.encoding = kwargs.get('encoding') or 'utf-8'
        self.body = kwargs.get('body')
        self.cookies = kwargs.get('cookies') or {}
        self.headers = {}
        self.url = None
        if not self.meta:
            self.meta = {}
        super(Response, self).__init__(**kwargs)

    def body_as_unicode(self):
        return self._body_as_unicode

    def __hash__(self):
        return hash(self._body_as_unicode)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
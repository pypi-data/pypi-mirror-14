# @Author: BingWu Yang <detailyang>
# @Date:   2016-03-30T17:00:32+08:00
# @Email:  detailyang@gmail.com
# @Last modified by:   detailyang
# @Last modified time: 2016-03-30T20:50:11+08:00
# @License: The MIT License (MIT)


import re


optionpattern = re.compile('--[qhb](.*)=(.*)')


class ESLNode:
    """ Abstract base class for AST nodes.
    """
    def children(self):
        pass


class RequestNode(ESLNode):
    def __init__(self, method, left, right):
        self.method =method
        self.left = left
        self.right = right

    def children(self):
        nodelist = []
        if self.left is not None:
                nodelist.append(("left", self.left))
        if self.right is not None:
                nodelist.append(("right", self.right))
        return tuple(nodelist)


class MethodNode(ESLNode):
    def __init__(self, method):
        self.method = method.upper() or 'GET'


class URLNode(ESLNode):
    def __init__(self, url):
        self.url = url


class HeaderNode(ESLNode):
    def __init__(self, header):
        r = optionpattern.match(header)
        self.key = r.group(1)
        self.value = r.group(2)


class QueryStringNode(ESLNode):
    def __init__(self, qs):
        r = optionpattern.match(qs)
        self.key = r.group(1)
        self.value = r.group(2)


class BodyNode(ESLNode):
    def __init__(self, body):
        r = optionpattern.match(body)
        self.key = r.group(1)
        self.value = r.group(2)


class OptionListNode(ESLNode):
    def __init__(self, options):
        self.options = options or []

    def children(self):
        nodelist = []
        for i, child in enumerate(self.options or []):
            nodelist.append(('options[%d]' % i, child))
        return tuple(nodelist)

    def append(self, option):
        self.options.append(option)
        return self


class OptionNode(ESLNode):
    def __init__(self, option):
        self.option = option

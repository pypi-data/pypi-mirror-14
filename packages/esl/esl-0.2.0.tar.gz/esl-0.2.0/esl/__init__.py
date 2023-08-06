# @Author: BingWu Yang <detailyang>
# @Date:   2016-03-30T20:49:47+08:00
# @Email:  detailyang@gmail.com
# @Last modified by:   detailyang
# @Last modified time: 2016-04-10T23:43:46+08:00
# @License: The MIT License (MIT)


import requests
import sys

from eslyacc import parse
from eslast import *
from eslgenerator import ESLGenerator
from eslyacc import parse
from eslast import QueryStringNode, HeaderNode, BodyNode, ValueNode, ShellNode

__version__ = '0.2.0'


def esl():
    _map = {
        'GET': requests.get,
        'POST': requests.post,
        'DELETE': requests.delete,
        'PUT': requests.put
    }
    ast = parse(' '.join(sys.argv[1:]))
    url = ast.left.url
    method = ast.method.name
    params = {}
    headers = {}
    body = {}
    for option in ast.right.options if ast.right else []:
        if isinstance(option.key, QueryStringNode):
            if isinstance(option.value, ValueNode):
                params[option.key.key] = option.value.value
            elif isinstance(option.value, ShellNode):
                params[option.key.key] = commands.getstatusoutput(option.value.value)[1]
            elif isinstance(option.key, HeaderNode):
                headers[option.key.key] = option.value.value
            elif isinstance(option.key, BodyNode):
                body[option.key.key] = option.value.value
    try:
        r = _map[method](url, data=body, params=params, headers=headers)
        print(r.text)
    except requests.exceptions.MissingSchema as e:
        print(e)

def eslgo():
    ast = parse(' '.join(sys.argv[1:]))
    if ast is not None:
        generator = ESLGenerator(ast)
        print(generator.to_go())

def eslpython():
    ast = parse(' '.join(sys.argv[1:]))
    if ast is not None:
        generator = ESLGenerator(ast)
        print(generator.to_python())

def eslcurl():
    ast = parse(' '.join(sys.argv[1:]))
    if ast is not None:
        generator = ESLGenerator(ast)
        print(generator.to_curl())

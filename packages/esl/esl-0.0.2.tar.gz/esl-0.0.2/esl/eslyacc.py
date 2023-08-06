# @Author: BingWu Yang <detailyang>
# @Date:   2016-03-29T17:47:44+08:00
# @Email:  detailyang@gmail.com
# @Last modified by:   detailyang
# @Last modified time: 2016-03-30T20:53:10+08:00
# @License: The MIT License (MIT)


import ply.yacc as yacc
import eslast as ast

from esllexer import ESLLexer


tokens = ESLLexer.tokens

# expression: URL
#           | URL METHOD
#           | URL METHOD OPTIONS
# OPTIONS:    empty
#           | OPTIONS OPTION
# OPTION:     HEADER
#           | QUERYSTRING
#           | BODY

def p_request(p):
    '''request : URL
           | URL METHOD
           | URL METHOD OPTIONS'''
    if len(p) == 2:
        p[0] = ast.RequestNode(ast.MethodNode('GET'), ast.URLNode(p[1]), None)
    elif len(p) == 3:
        p[0] = ast.RequestNode(ast.MethodNode(p[2]), ast.URLNode(p[1]), None)
    else:
        p[0] = ast.RequestNode(ast.MethodNode(p[2]), ast.URLNode(p[1]), p[3])

def p_options(p):
    '''OPTIONS :
              | OPTION
              | OPTIONS OPTION'''
    if len(p)  == 2:
        p[0] = ast.OptionListNode([p[1]])
    else:
        p[0] = p[1].append(p[2])

def p_option_empty(p):
    ' OPTION :   empty '
    p[0] = p[1]

def p_option_header(p):
    ' OPTION :   HEADER '
    p[0] = ast.HeaderNode(p[1])

def p_option_querystring(p):
    ' OPTION :  QUERYSTRING '
    p[0] = ast.QueryStringNode(p[1])

def p_option_body(p):
    ' OPTION : BODY '
    p[0] = ast.BodyNode(p[1])

def p_empty(p):
    'empty :'
    p[0] = []

def p_error(p):
    print "Syntax error in input!"

def parse(text):
    parser = yacc.yacc()
    ast = parser.parse(text, ESLLexer().build())
    return ast

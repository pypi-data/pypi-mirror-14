# @Author: BingWu Yang <detailyang>
# @Date:   2016-03-29T17:46:26+08:00
# @Email:  detailyang@gmail.com
# @Last modified by:   detailyang
# @Last modified time: 2016-03-31T10:42:10+08:00
# @License: The MIT License (MIT)


from ply.lex import TOKEN
import re
import ply.lex as lex


digit            = r'([0-9])'
nondigit         = r'([_A-Za-z])'
variable         = r'[a-zA-Z0-9\[\]\-_]+'
header           = r'--h' + variable + r'=' + variable
querystring = r'--q' + variable + r'=' + variable
body = r'--b' + variable + r'=' + variable


class ESLLexer:
    # List of token names.   This is always required
    tokens = (
       'URL',
       'METHOD',
       'HEADER',
       'QUERYSTRING',
       'BODY'
    )

    # Regular expression rules for simple tokens
    # t_HEADER = r'--h' + variable + r'=' + variable
    # t_QUERYSTRING = r'--q' + variable + r'=' + variable
    # t_BODY = r'--b' + variable + r'=' + variable
    def t_URL(self, t):
        r'^[^ ]+'
        return t

    def t_METHOD(self, t):
        r'(GET|get|POST|post|DELETE|delete|OPTIONS|options|CONNECT|connect)'
        t.value = t.value
        return t

    @TOKEN(header)
    def t_HEADER(self, t):
        return t

    @TOKEN(querystring)
    def t_QUERYSTRING(self, t):
        return t

    @TOKEN(body)
    def t_BODY(self, t):
        return t

    # Define a rule so we can track line numbers
    def t_newline(self,t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # A string containing ignored characters (spaces and tabs)
    t_ignore  = ' \t'

    # Error handling rule
    def t_error(self,t):
        print "unkonw character '%s'" % t.value[0]
        t.lexer.skip(1)

    # Build the lexer
    def build(self,**kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    # Test it output
    def test(self,data):
        self.lexer.input(data)
        while True:
             tok = self.lexer.token()
             if not tok: break
             print tok

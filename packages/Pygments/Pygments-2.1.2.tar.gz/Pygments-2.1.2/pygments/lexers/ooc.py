# -*- coding: utf-8 -*-
"""
    pygments.lexers.ooc
    ~~~~~~~~~~~~~~~~~~~

    Lexers for the Ooc language.

    :copyright: Copyright 2006-2015 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from pygments.lexer import RegexLexer, bygroups, words
from pygments.token import Text, Comment, Operator, Keyword, Name, String, \
    Number, Punctuation

__all__ = ['OocLexer']


class OocLexer(RegexLexer):
    """
    For `Ooc <http://ooc-lang.org/>`_ source code

    .. versionadded:: 1.2
    """
    name = 'Ooc'
    aliases = ['ooc']
    filenames = ['*.ooc']
    mimetypes = ['text/x-ooc']

    tokens = {
        'root': [
            (words((
                'class', 'interface', 'implement', 'abstract', 'extends', 'from',
                'this', 'super', 'new', 'const', 'final', 'static', 'import',
                'use', 'extern', 'inline', 'proto', 'break', 'continue',
                'fallthrough', 'operator', 'if', 'else', 'for', 'while', 'do',
                'switch', 'case', 'as', 'in', 'version', 'return', 'true',
                'false', 'null'), prefix=r'\b', suffix=r'\b'),
             Keyword),
            (r'include\b', Keyword, 'include'),
            (r'(cover)([ \t]+)(from)([ \t]+)(\w+[*@]?)',
             bygroups(Keyword, Text, Keyword, Text, Name.Class)),
            (r'(func)((?:[ \t]|\\\n)+)(~[a-z_]\w*)',
             bygroups(Keyword, Text, Name.Function)),
            (r'\bfunc\b', Keyword),
            # Note: %= and ^= not listed on http://ooc-lang.org/syntax
            (r'//.*', Comment),
            (r'(?s)/\*.*?\*/', Comment.Multiline),
            (r'(==?|\+=?|-[=>]?|\*=?|/=?|:=|!=?|%=?|\?|>{1,3}=?|<{1,3}=?|\.\.|'
             r'&&?|\|\|?|\^=?)', Operator),
            (r'(\.)([ \t]*)([a-z]\w*)', bygroups(Operator, Text,
                                                 Name.Function)),
            (r'[A-Z][A-Z0-9_]+', Name.Constant),
            (r'[A-Z]\w*([@*]|\[[ \t]*\])?', Name.Class),

            (r'([a-z]\w*(?:~[a-z]\w*)?)((?:[ \t]|\\\n)*)(?=\()',
             bygroups(Name.Function, Text)),
            (r'[a-z]\w*', Name.Variable),

            # : introduces types
            (r'[:(){}\[\];,]', Punctuation),

            (r'0x[0-9a-fA-F]+', Number.Hex),
            (r'0c[0-9]+', Number.Oct),
            (r'0b[01]+', Number.Bin),
            (r'[0-9_]\.[0-9_]*(?!\.)', Number.Float),
            (r'[0-9_]+', Number.Decimal),

            (r'"(?:\\.|\\[0-7]{1,3}|\\x[a-fA-F0-9]{1,2}|[^\\"])*"',
             String.Double),
            (r"'(?:\\.|\\[0-9]{1,3}|\\x[a-fA-F0-9]{1,2}|[^\\\'\n])'",
             String.Char),
            (r'@', Punctuation),  # pointer dereference
            (r'\.', Punctuation),  # imports or chain operator

            (r'\\[ \t\n]', Text),
            (r'[ \t]+', Text),
        ],
        'include': [
            (r'[\w/]+', Name),
            (r',', Punctuation),
            (r'[ \t]', Text),
            (r'[;\n]', Text, '#pop'),
        ],
    }

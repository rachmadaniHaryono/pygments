"""
    pygments.lexers.typst
    ~~~~~~~~~~~~~~~~~~~~~

    Lexers for Typst language.

    :copyright: Copyright 2006-2024 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from pygments.lexer import RegexLexer, words, bygroups, include
from pygments.token import Comment, Keyword, Name, String, Punctuation, \
    Whitespace, Generic, Operator, Number, Text, Literal

__all__ = ['TypstLexer']


class TypstLexer(RegexLexer):
    """
    For Typst code.
    """

    name = 'Typst'
    aliases = ['typst']
    filenames = ['*.typ']
    mimetypes = ['text/x-typst']
    url = 'https://typst.app'
    version_added = '2.18'

    MATH_SHORTHANDS = (
        "[|", "|]", "||", "*", ":=", "::=", "...", "'", "-", "=:", "!=", ">>",
        ">=", ">>>", "<<", "<=", "<<<", "*", "->", "|->", "=>", "|=>", "==>",
        "-->", "~~>", "~>", ">->", "->>", "<-", "<==", "<--", "<~~", "<~",
        "<-<","<<-","<->","<=>","<==>","<-->",
    )

    tokens = {
        'root': [
            include('markup'),
        ],
        # common cases going from math/markup into code mode
        'into_code': [
            (words(('#let', '#set', '#show'), suffix=r'\b'), Keyword.Declaration, 'inline_code'),
            (words(('#import', '#include'), suffix=r'\b'), Keyword.Namespace, 'inline_code'),
            (r'#\{', Punctuation, 'code'),
            (r'(#[a-zA-Z_][a-zA-Z0-9_-]*)(\[)', bygroups(Name.Function, Punctuation), 'markup'),
            (r'(#[a-zA-Z_][a-zA-Z0-9_-]*)(\()', bygroups(Name.Function, Punctuation), 'inline_code'),
            (r'#[a-zA-Z_][a-zA-Z0-9_]*', Name.Variable),
        ],
        'markup': [
            include('comment'),
            (r'^\s*=+.*$', Generic.Heading),
            (r'[*][^*]*[*]', Generic.Strong),
            (r'_[^_]*_', Generic.Emph),
            (r'\$', Punctuation, 'math'),
            (r'`[^`]*`', String.Backtick),  # inline code
            (r'^\s*-', Punctuation),  # unnumbered list
            (r'^\s*\+', Punctuation),  # numbered list
            (r'^\s*[0-9]+\.', Punctuation),  # numbered list variant
            (r'^(\s*/\s+)([^:]+)(:)', bygroups(Punctuation, Name.Variable, Punctuation)),  # definitions
            (r'<[a-zA-Z_][a-zA-Z0-9_-]*>', Name.Label),  # label
            (r'@[a-zA-Z_][a-zA-Z0-9_-]*', Name.Label),  # reference
            (r'\\#', Text), # escaped
            include('into_code'),
            (r'```(?:.|\n)*?```', String.Backtick),  # code block
            (r'https?://[0-9a-zA-Z~/%#&=\',;.+?]*', Generic.Emph),  # links
            (words(('---', '\\', '~', '--', '...'), suffix=r'\B'), Punctuation),  # special chars shorthand
            (r'\\\[', Punctuation),  # escaped
            (r'\\\]', Punctuation),  # escaped
            (r'\[', Punctuation, '#push'),
            (r'\]', Punctuation, '#pop'),
            (r'[ \t]+\n?|\n', Whitespace),
            (r'((?![*_$`/<@\\#\] ]|https?://).)+', Text),
        ],
        'math': [
            include('comment'),
            (words(('\\_', '\\^', '\\&')), Text), # escapes
            (words(('_', '^', '&')), Punctuation),
            (words(('+', '-', '*', '/', '=') + MATH_SHORTHANDS), Operator),
            (r'\\', Punctuation), # line break
            (r'\\\$', Punctuation),  # escaped
            (r'\$', Punctuation, '#pop'),  # end of math mode
            include('into_code'),
            (r'([a-zA-Z_][a-zA-Z0-9_-]*)(\s*)(\()', bygroups(Name.Function, Whitespace, Punctuation)),
            (r'([a-zA-Z][a-zA-Z0-9-]*)', Name.Variable), # both variables and symbols (_ isn't supported for variables)
            (r'[0-9]+(\.[0-9]+)?', Number),
            (r'\.{1,3}|\(|\)|,', Punctuation),
            (r'"[^"]*"', String.Double),
            (r'[ \t\n]+', Whitespace),
        ],
        'comment': [
            (r'//.*$', Comment.Single),
            (r'/[*](.|\n)*?[*]/', Comment.Multiline),
        ],
        'code': [
            include('comment'),
            (r'\[', Punctuation, 'markup'),
            (r'\(|\{', Punctuation, 'code'),
            (r'\)|\}', Punctuation, '#pop'),
            (r'"[^"]*"', String.Double),
            (r',|\.{1,2}', Punctuation),
            (r'=', Operator),
            (words(('and', 'or', 'not'), suffix=r'\b'), Operator.Word),
            (r'=>|<=|==|!=|>|<|-=|\+=|\*=|/=|\+|-|\\|\*', Operator), # comparisons
            (r'([a-zA-Z_][a-zA-Z0-9_-]*)(:)', bygroups(Name.Variable, Punctuation)),
            (r'([a-zA-Z_][a-zA-Z0-9_-]*)(\()', bygroups(Name.Function, Punctuation), 'code'),
            (words(('as', 'break', 'export', 'continue', 'else', 'for', 'if',
                    'in', 'return', 'while'), suffix=r'\b'),
             Keyword.Reserved),
             (words(('import', 'include'), suffix=r'\b'), Keyword.Namespace),
            (words(('auto', 'none', 'true', 'false'), suffix=r'\b'), Keyword.Constant),
            (r'([0-9.]+)(mm|pt|cm|in|em|fr|%)', bygroups(Number, Keyword.Reserved)),
            (r'[0-9]+', Number),
            (words(('let', 'set', 'show'), suffix=r'\b'), Keyword.Declaration),
            # FIXME: make this work
            ## (r'(import|include)( *)(")([^"])(")',
            ##  bygroups(Keyword.Reserved, Text, Punctuation, String.Double, Punctuation)),
            (r'([a-zA-Z_][a-zA-Z0-9_-]*)', Name.Variable),
            (r'[ \t\n]+', Whitespace),
            (r':', Punctuation), # from imports like "import a: b" or "show: text.with(..)"
        ],
        'inline_code': [
            (r';\b', Punctuation, '#pop'),
            (r'\n', Whitespace, '#pop'),
            include('code'),
        ],
    }

# -*- coding: utf-8 -*-
from django.template import Lexer, TOKEN_TEXT
from django.utils.encoding import force_text
from django_babel.extract import extract_django
from django.utils import six
from markey import underscore
from markey.tools import TokenStream
from markey.machine import tokenize, parse_arguments


def extract(fileobj, keywords, comment_tags, options):
    """Extracts translation messages from underscore template files.

    This method does also extract django templates. If a template does not
    contain any django translation tags we always fallback to underscore extraction.

    This is a plugin to Babel, written according to
    http://babel.pocoo.org/docs/messages/#writing-extraction-methods

    :param fileobj: the file-like object the messages should be extracted
                    from
    :param keywords: a list of keywords (i.e. function names) that should
                     be recognized as translation functions
    :param comment_tags: a list of translator tags to search for and
                         include in the results
    :param options: a dictionary of additional options (optional)
    :return: an iterator over ``(lineno, funcname, message, comments)``
             tuples
    :rtype: ``iterator``
    """
    encoding = options.get('encoding', 'utf-8')

    original_position = fileobj.tell()

    text = fileobj.read().decode(encoding)

    # TODO: There must be another way. Find a way to fix the ordering
    # in babel directly!
    vars = [token.token_type != TOKEN_TEXT for token in Lexer(text, None).tokenize()]
    could_be_django = any(list(vars))

    if could_be_django:
        fileobj.seek(original_position)
        iterator = extract_django(fileobj, keywords, comment_tags, options)
        for lineno, funcname, message, comments in iterator:
            yield lineno, funcname, message, comments
    else:
        # Underscore template extraction
        comments = []

        fileobj.seek(original_position)

        for lineno, line in enumerate(fileobj, 1):
            funcname = None

            stream = TokenStream.from_tuple_iter(tokenize(line, underscore.rules))
            while not stream.eof:
                if stream.current.type == 'gettext_begin':
                    stream.expect('gettext_begin')
                    funcname = stream.expect('func_name').value
                    args, kwargs = parse_arguments(stream, 'gettext_end')

                    strings = []
                    for arg in args:
                        try:
                            arg = int(arg)
                        except ValueError:
                            pass
                        if isinstance(arg, six.string_types):
                            strings.append(force_text(arg))
                        else:
                            strings.append(None)

                    for arg in kwargs:
                        strings.append(None)

                    if len(strings) == 1:
                        strings = strings[0]
                    else:
                        strings = tuple(strings)

                    yield lineno, funcname, strings, []

                stream.next()

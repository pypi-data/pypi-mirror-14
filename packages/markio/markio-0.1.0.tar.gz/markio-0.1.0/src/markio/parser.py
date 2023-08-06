from collections import OrderedDict
import warnings
import re
import configparser
import mistune
from markio.types import Markio
from markio.constants import (PROGRAMMING_LANGUAGES_CODES,
                              COUNTRY_CODES, LANGUAGE_CODES)


markdown = mistune.Markdown(escape=True)
blocklexer = mistune.BlockLexer()


def parse(file, extra=None):
    """Parse the given markio file.

    If it is a real file in the filesystem, the parser will look for
    supplementary data in adjacent files such as answer keys, lang files, etc.

    Parameters
    ----------

    file:
        A string with a path to a markio file or a file object.
    extra:
        A dictionary mapping fragment paths to files (or file paths) that hold
        that data.

    """

    if isinstance(file, str):
        with open(file) as F:
            return parse_string(F.read(), {})

    return parse_string(file.read(), {})


def parse_string(text, extra={}):
    # Process mistune parse tree and create an hierarchical DOM-like dictionary
    # in which section names are keys and section contents are values.
    def DOM(tree):
        current = []
        root = OrderedDict({None: current})
        levels = [D['level'] for D in tree if D['type'] == 'heading']
        if levels:
            level = min(levels)
        else:
            return tree

        for node in tree:
            if node['type'] == 'heading' and node['level'] == level:
                root[node['text']] = current = []
            else:
                current.append(node)

        return {k: DOM(v) for (k, v) in root.items()}

    mistune_tree = blocklexer(text)
    dom = DOM(mistune_tree)
    del dom[None]

    # Verify if it starts with h1-level heading
    first_node = mistune_tree[0]
    if not(first_node['type'] == 'heading' and first_node['level'] == 1):
        raise SyntaxError('Document should start with a H1-level heading')
    if len(dom) != 1:
        raise SyntaxError('Only one H1-level title is allowed for the whole '
                          'document')

    # Create return node
    title, body = dom.popitem()
    markio = Markio(title=title)

    # Process metadata block
    block = body.pop(None, [])
    if block and block[0]['type'] == 'code':
        meta = block.pop(0)['text']
        cfg = configparser.ConfigParser()
        cfg.read_string('[DEFAULT]\n' + meta)
        cfg = {k: dict(v) for (k, v) in cfg.items()}
        default = cfg.pop('DEFAULT')

        # Get default parameters and process them
        for attr in ['author', 'slug', 'timeout']:
            setattr(markio, attr, default.pop(attr, None))
        if markio.timeout is not None:
            markio.timeout = parse_time(markio.timeout)
        markio.tags = parse_tags(default.pop('tags', ''))
        markio.meta = cfg

        if default:
            key = next(iter(default))
            raise SyntaxError('invalid meta information: %r' % key)

    # Check if short description is available
    if len(block) == 1:
        markio.short_description = block[0]['text']
    elif len(block) > 1:
        raise SyntaxError('expect a single paragraph after metadata section')

    # Combine keys and extract description information
    body = combine_keys(body, lambda x: x.lower())

    def get_description(descr):
        return '\n\n'.join(block['text'] for block in descr)

    descriptions = body.pop('description', {})
    markio.description = get_description(descriptions.get(None, []))
    for lang, descr in descriptions.items():
        lang = normalize_language(lang)
        markio[lang].description = get_description(descr).strip()

    # Extract tests
    tests = body.pop('tests', {})
    markio.tests = tests.pop(None, [{'text': ''}])[0]['text'].strip()
    if tests:
        raise ValueError('invalid test subsession: Tests (%s)' %
                         next(iter(tests)))

    # Extract answer keys
    def get_code_block(k, x):
        if len(x) != 1:
            raise SyntaxError('expect to find a single block of code at answer '
                              'key %s' % k)
        return x[0]['text'].strip()

    if None in body.get('answer key', {}):
        raise SyntaxError('must provide language for Answer Key')

    markio.answer_key = {
        normalize_computer_language(k): get_code_block(k, v)
            for (k, v) in body.pop('answer key', {}).items()
    }

    # Extract all examples
    examples = body.pop('example', {})
    markio.example = examples.get(None, [{'text': None}])[0]['text'].strip()
    for lang, item in examples.items():
        lang = normalize_language(lang)
        markio[lang].example = item[0]['text'].strip()

    # Extract placeholder information
    placeholders = body.pop('placeholder', {})
    by_i18n = {None: {}}
    for k, v in placeholders.items():
        source = v[0]['text'].strip()

        if k is None:
            D = by_i18n[None]
            D[None] = source
        else:
            # Specify both programming language and i18n
            if ',' in k:
                raise NotImplementedError('placeholder: %s' % k)

            else:
                match = country_code_re.match(k)

                # It is a lang/country code
                if match:
                    lang, country = match.groups()
                    if lang not in LANGUAGE_CODES:
                        warnings.warn("unsupported language code: %r" % lang)
                    if country not in COUNTRY_CODES:
                        warnings.warn("unsupported country code: %r" % country)

                    k = '%s-%s' % (lang, country.upper())
                    D = by_i18n.setdefault(k, {})
                    D[None] = source

                # It is a programming language
                else:
                    if k not in PROGRAMMING_LANGUAGES_CODES:
                        warnings.warn("unknown programming language: %r" % k)
                    D = by_i18n[None]

                    D[k] = source

    markio.placeholder = by_i18n.pop(None)
    for lang, item in by_i18n.items():
        lang = normalize_language(lang)
        markio[lang].placeholder = item.strip()

    # Assure there is no invalid sections
    if body:
        raise SyntaxError('invalid section: %s' % next(iter(body)))

    return markio


def parse_tags(tags):
    """Parse a string full of tags.

    Example
    -------

    >>> parse_tags('#foo #bar #MyFooBarTag')
    ['foo', 'bar', 'MyFooBarTag']
    """
    tags = tags.split()
    if not all(tag.startswith('#') for tag in tags):
        raise SyntaxError('tags must start with an "#"')
    return [tag[1:] for tag in tags]


def parse_time(st):
    """Parse a string that represents a time interval (e.g.: st = '1s') and
    return a float value representing this duration in seconds."""

    st = st.replace(' ', '').lower()
    try:
        return float(st)
    except ValueError:
        pass

    for ending, mul in [('second', 1), ('seconds', 1), ('sec', 1), ('s', 1),
                        ('minute', 60), ('minutes', 60), ('min', 60), ('m', 60)]:
        if st.endswith(ending):
            try:
                return float(st[:-len(ending)]) * mul
            except ValueError:
                break
    raise ValueError('invalid duration: %r' % st)


def combine_keys(D, keytrans=lambda x: x, dict=dict):
    """Combine keys in a dictionary so section like 'foo (bar)' and 'foo (baz)'
    are merged into foo: {'bar': ..., 'baz': ...}.

    Parameters
    ----------

    D : mapping
        Input dictionary
    keytrans : callable
        Function that is applied to normalize the keys of the output dictionary.
    dict : type
        A callable that returns an empty mapping object. Useful, for instance
        if the user wants to return merged OrderedDict's rather than regular
        dictionaries.
    """
    out = {}
    for (k, v) in D.items():
        k = k.strip()
        pre, sep, tail = k.partition('(')
        if sep:
            k = pre.strip()
            if tail[-1] != ')':
                raise SyntaxError('expect closing parenthesis')
            part = tail[:-1].strip()
        else:
            part = None
        dic = out.setdefault(keytrans(k), dict())
        dic[None if part is None else keytrans(part)] = v
    return out


def normalize_language(x):
    """Normalize accepted lang codes to ISO format."""

    return x


def normalize_computer_language(x):
    """Normalize accepted computer language strings."""

    x = x.lower()
    return PROGRAMMING_LANGUAGES_CODES.get(x, x)


#
# Re matches
#
country_code_re = re.compile(
    r'^\w*([a-zA-Z][a-zA-Z])(-|_)([a-zA-Z][a-zA-Z])?\w*$')
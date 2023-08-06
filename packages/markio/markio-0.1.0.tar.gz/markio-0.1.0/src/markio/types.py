import copy
import pprint


class Markio:
    class __Literal(str):
        """A string-like object whose repr() is equal to str()"""

        def __repr__(self):
            return str(self)

    _valid_attrs = {
        # Basic values
        'title', 'author', 'slug', 'tags', 'timeout'

        # Sections
        'answer_key', 'description',
    }

    def __init__(self, **kwds):
        parent = kwds['parent'] = kwds.pop('parent', None)
        if parent is None:
            kwds['tags'] = dict(kwds.pop('tags', []))
        else:
            if 'tags' in kwds:
                kwds['tags'] = list(kwds['tags'])

        kwds['translations'] = {}
        self.__dict__.update(kwds)

    def __getattr__(self, attr):
        if attr not in self._valid_attrs:
            raise AttributeError(attr)

        if self.parent is None:
            return None
        else:
            return getattr(self.parent, attr)

    def __getitem__(self, key):
        if key is None:
            return self
        try:
            return self.translations[key]
        except KeyError:
            self.translations[key] = out = Markio(parent=self)
            return out

    def __contains__(self, lang):
        return lang in self.translations

    def __iter__(self):
        return iter(self.translations)

    def iter_translations(self):
        """Iterate over all pairs of (lang, markio)."""

        yield (None, self)
        for trans in sorted(self.translations):
            yield (trans, self[trans])

    def source(self):
        """Renders the source code equivalent to the markio structure."""

        # Title
        lines = [self.title, '=' * len(self.title), '']

        # Meta info
        for meta in ['author', 'slug', 'timeout']:
            value = getattr(self, meta)
            if value is not None:
                lines.append('    %s: %s' % (meta.title(), value))
        if self.tags:
            tag_data = ' '.join('#%s' % tag for tag in self.tags)
            lines.append('    Tags: %s' % tag_data)

        if self.short_description:
            lines.extend(['', self.short_description])

        # Description and examples
        for (lang, obj) in self.iter_translations():
            add_description = True
            add_example = True

            if lang is None and obj.description:
                lines.append('')
                title = 'Description'
            elif not obj.description or obj.description == self.description:
                add_description = False
            else:
                title = 'Description (%s)' % lang

            if add_description:
                lines.extend(['', title, '-' * len(title), '', obj.description])

            # Examples
            if lang is None and obj.example:
                title = 'Example'
            elif not obj.example or obj.example == self.example:
                add_example = False
            else:
                title = 'Example (%s)' % lang

            if add_example:
                lines.extend(['', title, '-' * len(title), '',
                              indent(obj.example)])

        # Tests
        if self.tests:
            lines.extend(['', 'Tests', '-----', '', indent(self.tests)])

        # Answer keys
        lines.append('')
        for comp_lang, source in sorted(self.answer_key.items()):
            title = 'Answer Key (%s)' % comp_lang
            source = indent(source)
            lines.extend(['', title, '-' * len(title), '', source])

        # Default placeholder, if it exists
        lines.append('')
        for lang, obj in self.iter_translations():
            placeholders = list(obj.placeholder)
            placeholders.remove(None)
            placeholders.sort()
            placeholders.insert(0, None)

            for comp_lang in placeholders:
                value = obj.placeholder[comp_lang]
                if not value:
                    continue
                value = indent(value)

                if lang is None and comp_lang is None:
                    lines.extend(['\nPlaceholder', '-' * 11, '', value])
                    continue

                if lang is None:
                    title = 'Placeholder (%s)' % comp_lang
                elif comp_lang is None:
                    title = 'Placeholder (%s)' % lang
                else:
                    title = 'Placeholder (%s, %s)' % (lang, comp_lang)

                if lang is None or value != self.placeholder.get(comp_lang, None):
                    lines.extend(['', title, '-' * len(title), '', value])

        # Finished collecting lines: return
        return '\n'.join(lines)

    def pprint(self, file=None, **kwds):
        """Pretty print Markio structure."""

        data = pprint.pformat(self._json(), **kwds)
        print(data, file=file)

    def _json(self):
        """JSON-like expansion of the AST.

        All linear node instances are expanded into dictionaries."""

        D = {(k[1:] if k.startswith('_') else k): v
             for (k, v) in vars(self).items()}

        memo = dict()

        def json(x):
            obj_id = id(x)

            if obj_id in memo and memo[obj_id] > 5:
                if isinstance(x, list):
                    return self.__Literal('[...]')
                elif isinstance(x, (set, dict)):
                    return self.__Literal('{...}')

            if hasattr(type(x), '__contains__'):
                memo[obj_id] = memo.get(obj_id, 0) + 1

            if isinstance(x, (list, tuple)):
                return [json(y) for y in x]
            elif isinstance(x, Markio):
                return x._json()
            elif isinstance(x, dict):
                return {k: json(v) for (k, v) in x.items()}
            else:
                return x

        return {k: json(v) for (k, v) in D.items()}

    def copy(self):
        """Return a deep copy."""

        return copy.deepcopy(self)


def indent(txt):
    """Indent text with 4 spaces."""

    return '\n'.join(('    ' + x if x else '') for x in txt.splitlines())
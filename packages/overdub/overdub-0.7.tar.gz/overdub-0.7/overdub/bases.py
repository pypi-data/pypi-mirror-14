try:   # pragma: no cover
    from collections.abc import Mapping
except ImportError:   # pragma: no cover
    # python < 3.0
    from collections import Mapping
from copy import deepcopy


def merge_recursively(base, data):
    dest = deepcopy(base)
    for key, value in data.items():
        orig = base.get(key, None)
        if isinstance(orig, Mapping) and isinstance(value, Mapping):
            value = merge_recursively(orig, value)
        dest[key] = value
    return dest


class Overdub(Mapping):
    """Access mapping as a layer.

    When possible, keys will be accessed as attributes.

    For example:

    >>> overdub = Overdub({'foo': 1, 'bar': {'baz': 'qux'}})
    >>> overdub.foo
    1
    >>> overdub['foo']
    1
    """

    def __init__(self, data=None):
        self._ = data or {}

    def __getitem__(self, key):
        try:
            value = self._[key]
        except KeyError:
            raise KeyError('Key %r is not defined' % key)
        if isinstance(value, Mapping):
            value = self.__class__(value)
        return value

    def __iter__(self):
        return iter(self._)

    def __len__(self):
        return len(self._)

    def __getattr__(self, name):
        """
        Fallback to current data key if attr is not setted.
        """

        try:
            return self.__getitem__(name)
        except KeyError:
            raise AttributeError("%r object has no attribute %r" % (
                self.__class__.__name__, name
            ))


class MutableOverdub(Overdub):
    """An Overdub with mutability abilities.
    """

    def update(self, data):
        """Update data

        >>> a = {'foo': 1, 'bar': {'baz': 2}}
        >>> b = {'bar': {'baz': 4}, 'qux': {'one': 1}}
        >>> o = MutableOverdub(a)
        >>> o.update(b)
        >>> assert o == {'foo': 1, 'bar': {'baz': 4}, 'qux': {'one': 1}}

        Parameters:
            data (Mapping): data to be updated
        """
        return self._.update(data)

    def merge(self, data):
        """Merge data recursively

        >>> a = {'foo': {'one': 1}, 'bar': 1}
        >>> b = {'foo': {'two': 2}, 'bar': 2}
        >>> o = MutableOverdub(a)
        >>> o.merge(b)
        >>> assert o == {'foo': {'one': 1, 'two': 2}, 'bar': 2}

        Parameters:
            data (Mapping): data to be merged
        """
        data = merge_recursively(self._, data)
        return self._.update(data)

    def rebase(self, data):
        """Rebase data

        >>> a = {'foo': {'one': 1}, 'bar': 1}
        >>> b = {'foo': {'two': 2}, 'bar': 2}
        >>> o = MutableOverdub(a)
        >>> o.rebase(b)
        >>> assert o == {'foo': {'one': 1, 'two': 2}, 'bar': 2}

        Parameters:
            data (Mapping): data to be rebased
        """
        data = merge_recursively(data, self._)
        return self._.update(data)

    def frozen(self):
        """Froze data

        >>> a = MutableOverdub()
        >>> b = a.frozen()
        >>> isinstance(b, Overdub)
        >>> not isinstance(b, MutableOverdub)

        Returns:
            Overdub: the frozen data
        """
        return Overdub(self._)

    def unbound(self):
        """unbound the data of Overdub layer

        >>> a = MutableOverdub()
        >>> b = a.unbound()
        >>> not isinstance(b, Overdub)
        >>> not isinstance(b, MutableOverdub)

        Returns:
            Mapping: the data without magic
        """
        cls = self._.__class__
        def export(v):
            if isinstance(v, MutableOverdub):
                return v.unbound()
            return v
        return cls((k, export(v)) for k, v in self._.items())

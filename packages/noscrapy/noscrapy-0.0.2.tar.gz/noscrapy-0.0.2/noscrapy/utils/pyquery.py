from pyquery import pyquery
from itertools import chain

__all__ = 'PyQuery',

class flexible_property(object):
    """Property to allow a flexible API."""
    def __init__(self, pget, pset=pyquery.no_default, pdel=pyquery.no_default,
                 pdir=pyquery.no_default):
        self.pget = pget
        self.pset = pset
        self.pdel = pdel
        self.pdir = pdir

    def __get__(self, instance, klass):
        class _element(object):
            """real element to support set/get/del attr and item and js call
            style"""
            def __call__(prop, *args, **kwargs):  # @NoSelf
                return self.pget(instance, *args, **kwargs)
            __getattr__ = __getitem__ = __setattr__ = __setitem__ = __call__

            def __delitem__(prop, name):  # @NoSelf
                if self.pdel is not pyquery.no_default:
                    return self.pdel(instance, name)
                else:
                    raise NotImplementedError()
            __delattr__ = __delitem__

            def __repr__(prop):  # @NoSelf
                return '<flexible_element %s>' % self.pget.__name__

            def __dir__(prop):  # @NoSelf
                if self.pdir:
                    return self.pdir(instance) + super().__dir__()
                return super().__dir__()

        return _element()

class PyQuery(pyquery.PyQuery):
    def map_items(self, func, selector=None):
        results = []
        items = self.items(selector)
        count = len(items)
        argcount = pyquery.func_code(func).co_argcount
        for index, item in enumerate(items):
            args = item, index, count
            result = func(*args[:argcount])
            if result is None:
                continue
            if isinstance(result, list):
                results.extend(result)
                continue
            results.append(result)
        return self.__class__(results, **dict(parent=self))

    def attr(self, *args, **kwargs):
        """Attributes manipulation"""
        def mapped(name):
            name = name.replace('_', '-')
            if name.endswith('-'):
                name = name[:-1]
            return name

        attr = value = pyquery.no_default
        length = len(args)
        if length == 1:
            attr = args[0]
            attr = mapped(attr)
        elif length == 2:
            attr, value = args
            attr = mapped(attr)
        elif kwargs:
            attr = {}
            for k, v in kwargs.items():
                attr[mapped(k)] = v
        else:
            raise ValueError('Invalid arguments %s %s' % (args, kwargs))

        if not self:
            return None
        elif isinstance(attr, dict):
            for tag in self:
                for key, value in attr.items():
                    tag.set(key, value)
        elif value is pyquery.no_default:
            return self[0].get(attr)
        elif value is None or value == '':
            return self.remove_attr(attr)
        else:
            for tag in self:
                tag.set(attr, value)
        return self

    def _attrs(self):
        return sorted(set(a.replace('-', '_')
                          for a in chain.from_iterable(t.attrib.keys() for t in self)))

    attrs = property(_attrs)
    attr = flexible_property(pget=attr, pdel=pyquery.PyQuery.remove_attr, pdir=_attrs)

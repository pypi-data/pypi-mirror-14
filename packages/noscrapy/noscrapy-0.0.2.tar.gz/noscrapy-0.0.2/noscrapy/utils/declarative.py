from collections import OrderedDict
from itertools import chain

__all__ = 'Class', 'Field', 'Type'

NOTSET = object()

class Field(object):
    """Class descriptor which enables declarative configuration.

        default: Value returned attr is not in instance dict.
        name: Name/title for display of the field, same as attr if not set.
        desc: Description for display of the field, same as name if not set.
        attr: Gets set by metaclass to the attribute name on the class.
        readonly: Flag to disallow setting the instance value.

    """
    def __init__(self, default=NOTSET, name=NOTSET, desc=NOTSET, attr=NOTSET, readonly=False):
        self.default = default
        self.name = name
        self.desc = desc
        self.attr = attr
        self.readonly = readonly
        self.cls = None

    def _setup(self, cls, attr=NOTSET, default=NOTSET, base=NOTSET):
        self.cls = cls
        def setfattr(fattr, *values):
            for value in (v for v in values if v is not NOTSET):
                setattr(self, fattr, value)
                break

        setfattr('attr', self.attr, attr, getattr(base, 'attr', NOTSET))
        setfattr('default', self.default, default, getattr(base, 'default', NOTSET))
        setfattr('name', self.name, getattr(base, 'name', NOTSET), self.attr)
        setfattr('desc', self.desc, getattr(base, 'desc', NOTSET), self.name)
        return self

    def __get__(self, obj, cls=None):
        if obj is None:
            return self
        value = obj.__dict__.get(self.attr, self.default)
        if value is NOTSET:
            raise ValueError('No default value given for Field %s' % self.attr)
        if callable(value):
            value = value(obj)
        return value

    def __set__(self, obj, value):
        if self.readonly:
            raise AttributeError('can not set attribute %s' % self.attr)
        obj.__dict__[self.attr] = value

    def __delete__(self, obj):
        if self.readonly or self.attr not in obj.__dict__:
            raise AttributeError('can not delete attribute %s' % self.attr)
        del obj.__dict__[self.attr]

    def clone(self, cls, attr=NOTSET, default=NOTSET, base=NOTSET):
        return type(self)(self.default, self.name, self.desc, self.attr, self.readonly
                          )._setup(cls, attr, default, base)

class Type(type):
    """Type to add __attrs__ and __fields__ attributes."""
    @classmethod
    def __prepare__(cls, name, bases):
        return OrderedDict()

    def __new__(cls, name, bases, classdict):
        self = type.__new__(cls, name, bases, dict(classdict))

        attrs_lists = [b.__dict__.get('__attrs__', ()) for b in bases] + [classdict]
        # use ordered dict like an ordered set
        self.__attrs__ = tuple(OrderedDict.fromkeys(chain.from_iterable(attrs_lists)))

        base_fields = {}
        for base in bases:
            for attr in getattr(base, '__fields__', ()):
                if attr not in base_fields:
                    base_fields[attr] = getattr(base, attr).clone(self)

        fields = {}
        for attr, value in list(classdict.items()):
            if attr.startswith('__'):
                continue
            if isinstance(value, Field):
                fields[attr] = value._setup(self, attr, base=base_fields.get(attr, NOTSET))
            elif attr in fields:
                fields[attr] = base_fields[attr].clone(self, default=value)

        for attr, base_field in base_fields.items():
            if attr not in fields:
                fields[attr] = base_field.clone(self)

        for attr, field in fields.items():
            setattr(self, attr, field)

        self.__fields__ = tuple(a for a in self.__attrs__ if a in fields)
        return self

class Class(metaclass=Type):
    """Class with extra attributes:

        __attrs__ contains all attribute names in order of assignment.
        __fields__ contains only the names of Field descriptor instances.
    """
    pass

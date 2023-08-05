# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import collections
import inspect
import re
import sys
import six
try:
    from django.utils.encoding import force_text
except ImportError:
    force_text = six.text_type

__all__ = ("Enum", "Option")

# TODO: add support for checked values (e.g. all must be integers)
# TODO: add support for auto-numbered values, i.e. no value supplied creates an incremented value

_no_value = object()


class Option(object):
    """
    Enumeration option
    """
    _counter = 0

    def __init__(self, value=_no_value, **kwargs):
        """
        Create an enumeration option.
        :param value: pass in a value for this enumeration option, defaults to enumeration key name
        :param kwargs: pass in additional parameters to store alongside
        """
        self.value = value
        self.kwargs = kwargs

        self._counter = Option._counter
        Option._counter += 1


class InternalOption(object):
    _mutable = True

    def __init__(self, enum, key, value, **kwargs):
        self.enum = enum
        self.key = key
        self.value = value
        self.kwargs = kwargs
        self._mutable = False

    def __repr__(self):
        return "<%s.%s=%s %s>" % (self.enum.__name__, self.key, repr(self.value), " ".join("%s=%s" % (k, repr(v)) for k, v in six.iteritems(self.kwargs)))

    def __get__(self, instance, owner):
        # instance is always None, owner is the Enum subclass
        return self.value

    def __setattr__(self, key, value):
        if self._mutable:
            return super(InternalOption, self).__setattr__(key, value)
        raise TypeError("%s cannot be mutated" % self.enum.__name__)

    def __delattr__(self, item):
        if self._mutable:
            return super(InternalOption, self).__delattr__(item)
        raise TypeError("%s cannot be mutated" % self.enum.__name__)

    @property
    def description(self):
        """
        Returns the 'description' kwarg if one exists, a text representation of the value otherwise.
        Mainly for Django choices compatability.
        """
        return self.kwargs.get("description", force_text(self.value))

    @property
    def choice(self):
        """
        Django choices tuple
        """
        return self.value, self.description


class EnumBase(type):
    """
    Enumeration meta class
    """
    _mutable = True

    def __new__(mcs, name, bases, attrs):
        super_new = super(EnumBase, mcs).__new__

        # make the new class
        new_class = super_new(mcs, name, bases, attrs)

        # ensure it's mutable for further subclasses
        type.__setattr__(new_class, "_mutable", True)

        # enforce docs attribute
        if "__doc__" not in attrs:
            setattr(new_class, "__doc__", None)

        # keys must follow a specific pattern
        re_key = re.compile(r"^[A-Z][0-9A-Z_]*$")

        def key_check(key):
            if not isinstance(key, six.string_types) or not re_key.match(key):
                raise KeyError("Enum key %s is not allowed" % key)
            return key

        # value checking method
        value_set = set()

        def value_check(opt):
            if opt.value in value_set:
                raise ValueError("Enum value %s is not unique (%s.%s)" % (repr(opt.value), name, opt.key))
            value_set.add(opt.value)
            return opt

        # collect enumeration options from superclasses up to Enum
        options = []
        setattr(new_class, "options", options)
        key_set = set()
        for cls in new_class.__bases__:
            if cls is EnumBase:
                break
            if hasattr(cls, "options"):
                options.extend(map(value_check, cls.options))
                current_key_count = len(key_set)
                new_keys = [option.key for option in cls.options]
                key_set.update(new_keys)
                if len(key_set) != len(new_keys) + current_key_count:
                    raise KeyError("Duplicate keys found in parent classes of %s" % name)

        # collect enumeration options from this class
        new_options = inspect.getmembers(new_class, lambda attr: isinstance(attr, Option))
        new_options = sorted(new_options, key=lambda o: o[1]._counter)
        for option_name, option in new_options:
            option_name = key_check(six.text_type(option_name))
            if option_name in key_set:
                raise KeyError("Duplicate key found '%s' in %s" % (option_name, name))
            key_set.add(option_name)
            new_option = InternalOption(new_class, option_name, option_name if option.value is _no_value else option.value, **option.kwargs)
            if value_check is not None:
                value_check(new_option)

            setattr(new_class, option_name, new_option)
            options.append(new_option)

        # make it immutable as the last step
        setattr(new_class, "_mutable", False)

        return new_class

    def __repr__(self):
        return "<%s {%s}>" % (self.__name__, ", ".join(map(lambda o: repr(o.value), self.options)))

    def __setattr__(self, key, value):
        if self._mutable:
            return super(EnumBase, self).__setattr__(key, value)
        raise TypeError("%s cannot be mutated" % self.__name__)

    def __delattr__(self, item):
        if self._mutable:
            return super(EnumBase, self).__delattr__(item)
        raise TypeError("%s cannot be mutated" % self.__name__)

    def __hash__(self):
        # taken from collections.Set
        max_i = sys.maxint
        mask = 2 * max_i + 1
        n = len(self)
        h = 1927868237 * (n + 1)
        h &= mask
        for x in self:
            hx = hash(x)
            h ^= (hx ^ (hx << 16) ^ 89869747) * 3644798167
            h &= mask
        h = h * 69069 + 907133923
        h &= mask
        if h > max_i:
            h -= mask + 1
        if h == -1:
            h = 590923713
        return h

    def __eq__(self, other):
        """
        Tests for quality based only on *values*
        """
        if not issubclass(other, Enum):
            return False
        if self.__len__() != len(other):
            return False
        for value in self:
            if value not in other:
                return False
        return True

    def __len__(self):
        """
        The number of options in this enumeration
        """
        return len(self.options)

    def __iter__(self):
        """
        Iterates over the option *values* in this enumeration
        """
        return iter(map(lambda o: o.value, self.options))

    def __contains__(self, item):
        """
        Checks whether an option *value* exists in this enumeration
        """
        for option in self.options:
            if option.value == item:
                return True
        return False

    def __getitem__(self, item):
        """
        Looks up the option object based on its value
        e.g. Enum[Enum.OPTION] would return the full option object
        """
        for option in self.options:
            if option.value == item:
                return option
        raise KeyError("No option with value %s found" % repr(item))

    def __add__(self, other):
        """
        Union of two enumerations based on value, preserving order. Keys are taken from this enumeration first,
        non-option attributes are lost.
        Raises a ValueError if duplicate values are found, KeyError if duplicate keys are found.
        """
        if not issubclass(other, Enum):
            raise TypeError("%s cannot be added to %s" % (self.__name__, repr(other)))
        attrs = dict((option.key, Option(option.value, **option.kwargs)) for option in self.options)
        for option in other.options:
            key = option.key
            if key in attrs:
                raise KeyError("Duplicate key '%s' while attempting to add" % key)
            if option.value in self:
                raise ValueError("Duplicate value '%s' while attempting to add" % option.value)
            attrs[key] = Option(option.value, **option.kwargs)
        return EnumBase(str("Enum"), (Enum,), attrs)

    def __sub__(self, other):
        """
        Difference of two enumerations based on value, preserving order. Non-option attributes are lost.
        """
        if not issubclass(other, Enum):
            raise TypeError("%s cannot be subtracted %s" % (self.__name__, repr(other)))
        attrs = dict((option.key, Option(option.value, **option.kwargs)) for option in self.options if option.value not in other)
        return EnumBase(str("Enum"), (Enum,), attrs)

    def __and__(self, other):
        """
        Intersection of two enumerations based on value. Keys and kwargs are taken first from this enumeration,
        non-option attributes are lost.
        """
        if not issubclass(other, Enum):
            raise TypeError("Cannot create intersection of %s and %s" % (self.__name__, repr(other)))
        attrs = dict((option.key, Option(option.value, **option.kwargs)) for option in self.options if option.value in other)
        return EnumBase(str("Enum"), (Enum,), attrs)

    def __or__(self, other):
        """
        Union of two enumerations based on value. Keys and kwargs are taken first from this enumeration,
        non-option attributes are lost.
        Raises KeyError if duplicate keys are found. Does not raise errors if duplicate values are found.
        """
        if not issubclass(other, Enum):
            raise TypeError("Cannot create union of %s and %s" % (self.__name__, repr(other)))
        attrs = dict((option.key, Option(option.value, **option.kwargs)) for option in self.options)
        for option in other.options:
            if option.value in self:
                continue
            key = option.key
            if key in attrs:
                raise KeyError("Duplicate key '%s' while attempting to create union" % key)
            attrs[option.key] = Option(option.value, **option.kwargs)
        return EnumBase(str("Enum"), (Enum,), attrs)

    def __xor__(self, other):
        """
        Exclusive disjunction of two enumerations based on value. Non-option attributes are lost.
        """
        if not issubclass(other, Enum):
            raise TypeError("Cannot create exclusive disjunction of %s and %s" % (self.__name__, repr(other)))
        return (self | other) - (self & other)

    def isdisjoint(self, other):
        """
        Return True if two enumerations have a null intersection.
        """
        if not issubclass(other, Enum):
            raise TypeError("Cannot check if enumeration %s is disjoint from %s" % (self.__name__, repr(other)))
        for value in other:
            if value in self:
                return False
        return True


class Enum(six.with_metaclass(EnumBase)):
    """
    Enumeration type base class. Enumeration must be subclassed and cannot be instantiated. These subclasses are perfect
    for use with Django field choices. Additional attributes and methods (decorated with @classmethod) are allowed.

    Options in the enumeration have a key (determined by attribute name) and value (set in subclass or defaults to be
    the same as the key). Additional arguments can also be attached to options.

    Arithmetic and binary operations on enumerations are based on the value. Non-option attributes are lost in the
    process.
    """

    def __init__(self):
        raise TypeError("%s cannot be instantiated" % self.__name__)

    @classmethod
    def get_choices(cls):
        """
        Returns a list of key, value tuple pairs, for use in Django field choices.
        """
        return [option.choice for option in cls.options]

    @classmethod
    def get_default(cls):
        """
        Returns the first value, for use as the default value in Django field choices.
        """
        if cls.options:
            return cls.options[0].value
        raise ValueError("No options")

    @classmethod
    def lookup_description(cls, value):
        """
        Look up the option's description
        """
        return cls[value].description if value in cls else None


collections.Set.register(Enum)

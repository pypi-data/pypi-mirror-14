# lib imports
from itertools import combinations


class dotteddict(dict):
    """
    A convenience mapping providing access by-attribute in addition to by-key.

    A `dotteddict` provides something much like a dictionary except with the
    added benefit of having some clever ways to access the contents in the
    dictionary.

    For example:

        data = {"people": {"bob": {"status": True}, "john": {"status": False}}}
        dotted = dotteddict(data)
        dotted.people.bob.status
        dotted["people.john.status"]

    This is in contrast to using defaults:

        dotted["people"]["john"]["status"]
    """

    def __init__(self, data=None):
        """
        Class constructor
        """
        # pylint: disable=W0231
        #         __init__ method from base class 'dict' is not called
        if data:
            keys = data.keys()
            overlapped_keys = self._has_overlapped(keys)
            if overlapped_keys:
                raise ValueError(
                    "Dictionary has values with the following "
                    "overlapped keys: {}".format(overlapped_keys)
                )
            for key in data:
                value = data[key]
                # If the value is a dict, turn it into a dotteddict instance
                if isinstance(value, dict):
                    self[key] = dotteddict(value)
                else:
                    self[key] = value

    @staticmethod
    def _has_overlapped(items, separator="."):
        """
        Determine and return overlapping of iterable `items`.

        args:
            items(list[str])
            separator(Optional(str)): key must include this symbol at the end for it to be
                considered a member of an overlapping set of names.
        returns:
            tuple[str, str] or tuple[]: pair where one has another as part
        """
        combinations_ = combinations(sorted(items), 2)
        found = ((k1, k2) for k1, k2 in combinations_ if k2.startswith(k1 + separator))
        return next(found, ())

    def get(self, key, default=None):
        """
        Override to support dotted path directly as a dictionary:

            d.get('key1.key2.key3', default)
        """
        if '.' in key:
            head, tail = key.split('.', 1)

            # Get the head value from super so we don't go through this logic
            # again and blow the stack
            val = super(dotteddict, self).get(head, default)

            if val is not None and tail:
                dict_value = (
                    # If we have a dotteddict for a value, we can recursively
                    # call it with the tail of the path
                    val if isinstance(val, dotteddict)
                    # When value stored in Mapping but not in dotteddict
                    else super(dotteddict, self))
                return dict_value.get(tail, default)
            return val
        return super(dotteddict, self).get(key, default)

    def __getitem__(self, key):
        """
        Override to reuse the logic in ``get`` to traverse the key.
        """
        # Use a new object to test whether or not the default value is used.
        # None can't be used here because None is a legitimate value that might
        # be in a dictionary.
        default = object()

        val = self.get(key, default)

        if val is default:
            raise KeyError(key)
        else:
            return val

    def __getattr__(self, key):
        """
        Override of attribute accessor magic method.

        This adds the ability to use dotted accessor on this dictionary.

            val = d.key1.key2.key3

        This just passes off to `__getitem__` so that we may use the same
        logic as a `dict`.
        """
        try:
            return self.__getitem__(key)
        except KeyError:
            raise AttributeError("type object '%s' has no attribute '%s'" % (
                self.__class__.__name__, key))

    def __setattr__(self, key, value):
        """
        Override so that we can handle dotted assignments.

            d.key1.key2.key3 = val

        This just passes off to `__setitem__` so that we use the same logic
        as a `dict`.
        """
        try:
            self.__setitem__(key, value)
        except KeyError:
            raise AttributeError("type object '%s' has no attribute '%s'" % (
                self.__class__.__name__, key))

    def __setitem__(self, key, value):
        """
        Override this to support a dotted key.

            d['key1.key2.key3'] = val

        Which is equivalent to:

            d.key1.key2.key3 = val

        This ultimately just delagates to the super so that we maintain the
        same underlying logic as a real `dict`.
        """
        # convert any incoming dict into a dotteddict
        if isinstance(value, dict):
            value = dotteddict(value)

        if '.' in key:
            head, tail = key.split('.', 1)
            # we are interested only in a valid dotted pair
            # where parent and child are separated by dot
            if head and tail:
                if head not in self:
                    self[head] = dotteddict()
                self[head][tail] = value
            else:
                raise ValueError("Malformed key specified: '{}'".format(key))
        else:
            super(dotteddict, self).__setitem__(key, value)

    def __contains__(self, key):
        """
        Override for the `in` operator to handle dotted keys.

            if 'key1.key2.key3' in d:
                pass

        This ultimately ends up delegating to the super so that we use the
        same underlying logic as a real `dict`.
        """
        if '.' in key:
            key_list = key.split('.')
            (head, tail) = key_list[0], key_list[1:]
            if super(dotteddict, self).__contains__(head):
                return '.'.join(tail) in self[head]
            else:
                return False
        else:
            return super(dotteddict, self).__contains__(key)

# -*- coding: utf-8 -*-
# vim:set ts=4 sw=4 et ft=python:

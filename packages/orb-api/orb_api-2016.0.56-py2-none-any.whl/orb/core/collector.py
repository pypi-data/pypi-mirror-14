import projex.text

from projex.enum import enum
from projex.lazymodule import lazy_import

orb = lazy_import('orb')


class Collector(object):
    Flags = enum('Unique', 'Private')

    def __json__(self):
        output = {
            'name': self.__name,
            'flags': self.Flags.toSet(self.__flags)
        }
        return output

    def __init__(self, name='', flags=0):
        self.__name = self.__name__ = name
        self.__schema = None
        self.__preload = None
        self.__getter = None
        self.__flags = self.Flags.fromSet(flags) if isinstance(flags, set) else flags

    def __call__(self, record, useGetter=True, **context):
        if self.__getter and useGetter:
            return self.__getter(record, **context)
        else:
            if not record.isRecord():
                return orb.Collection()
            else:
                collection = self.collect(record, **context)
                cache = record.preload(projex.text.underscore(self.name()))
                collection.preload(cache, **context)

                if self.testFlag(self.Flags.Unique):
                    return collection.first()
                else:
                    return collection

    def copy(self):
        out = type(self)(name=self.__name, flags=self.__flags)
        out.setSchema(self.schema())
        return out

    def collect(self, record, **context):
        raise NotImplementedError

    def collectExpand(self, query, parts, **context):
        raise NotImplementedError

    def getter(self, function):
        self.__getter = function
        return function

    def flags(self):
        return self.__flags

    def name(self):
        return self.__name

    def schema(self):
        return self.__schema

    def setName(self, name):
        self.__name = self.__name__ = name

    def setSchema(self, schema):
        self.__schema = schema

    def setFlags(self, flags):
        self.__flags = flags

    def testFlag(self, flag):
        return (self.__flags & flag) > 0

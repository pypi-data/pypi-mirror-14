# napper -- A REST Client for Python
# Copyright (C) 2016 by Yann Kaiser and contributors.
# See AUTHORS and COPYING for details.
import asyncio
import json
import collections.abc
from functools import partial

from . import request
from .util import requestmethods, m, rag, getattribute_dict


@asyncio.coroutine
def convert_json(request, response):
    return upgrade_object(
        json.loads((yield from response.text()),
                   object_hook=partial(ResponseObject, origin=request)),
        request)


def upgrade_object(val, origin):
    if isinstance(val, str):
        return PermalinkString(val, origin=origin)
    elif isinstance(val, list):
        return ResponseList(val, origin=origin)
    else:
        return val


class ResponseList(collections.abc.Sequence):
    def __init__(self, val, origin):
        self.origin = origin
        self.val = val

    def __repr__(self):
        return repr(self.val)

    def __getitem__(self, i):
        return self.val[i]

    def __len__(self):
        return len(self.val)

    async def __aiter__(self):
        return ResponseListIterator(self)


class ResponseListIterator:
    def __init__(self, val):
        self.ito = iter(val)

    async def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            return next(self.ito)
        except StopIteration as exc:
            raise StopAsyncIteration from exc


@requestmethods
class PermalinkString(str):
    def __new__(cls, *args, origin, **kwargs):
        ret = super().__new__(cls, *args, **kwargs)
        ret.origin = origin
        return ret

    def request(self, method, *args, **kwargs):
        site = rag(self.origin, 'site')
        return request.Request(site, method, self)


class ResponseObject(dict):
    def __new__(cls, *args, origin, **kwargs):
        return super().__new__(cls, *args, **kwargs)

    def __init__(self, *args, origin, **kwargs):
        super().__init__(*args, **kwargs)
        self.origin = origin

    @getattribute_dict
    def __getattribute__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __getitem__(self, name):
        return upgrade_object(super().__getitem__(name), m(self).origin)

from functools import wraps
from re import match
from fanza.exceptions.fanza_exception import ExtractException

def checkdate(regex):
    def decorator(func):
        @wraps(func)
        def after(*args, **kwargs):
            ret = func(*args, **kwargs)
            if ret is None or match(regex, ret) is None:
                return None
            return ret
        return after
    return decorator

def checkvideolen(func):
    def after(*args, **kwargs):
        ret = func(*args, **kwargs)
        if not ret.isdigit():
            raise ExtractException('illegal video length: %s', ret)
        return ret
    return after

def collect(func):
    def after(*args, **kwargs):
        res = dict()
        for id, name in func(*args, **kwargs):
            res[id] = name
        return res
    return after

def notnull(func):
    def after(*args, **kwargs):
        ret = func(args, **kwargs)
        if ret is None:
            raise ExtractException('%s returned null value', func.__name__)
        return ret
    return after
        
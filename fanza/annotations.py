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
            return ret.replace('/', '-')
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
        ids, names = func(*args, **kwargs)
        n = len(ids) if len(ids) < len(names) else len(names)
        for i in range(0, n):
            if not ids[i].isdigit():
                continue
            res[ids[i]] = names[i]
        return res
    return after

def notnull(func):
    def after(*args, **kwargs):
        ret = func(*args, **kwargs)
        if ret is None:
            raise ExtractException('returned null value')
        return ret
    return after

def notempty(func):
    def after(*args, **kwargs):
        ret = func(*args, **kwargs)
        if len(ret) == 0:
            raise ExtractException('returned empty value')
        return ret
    return after
        
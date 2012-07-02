import uuid
from collections import namedtuple

def genid():
    return str(uuid.uuid4())

def dict_to_namedtuple(name, d):
    keylist = " ".join(d.keys())
    tc = namedtuple(name, keylist)
    return tc(**d)

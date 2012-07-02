import logging

class Monad(object):
    def __init__(self, value):
        self.value = value
    def __rshift__(self, func):
       return func(self.value)
    def __repr__(self):
        return "Monad(%r)" % (self.value,)

def unpack(v):
    return v

def mreturn(v):
    return Monad(v)

def do(fn):
       # if you want the decorator take arguments, see below link:
       # http://www.artima.com/weblogs/viewpost.jsp?thread=240845

       def invoker(*args, **kwargs):
           logging.debug("Invoker called:")
           print "args", args
           print "args 1 and above", args[1:]
           print "fn", fn
           gen = fn(*args, **kwargs)

           rv = {}
           def send(v):
               try:
                   m = gen.send(v)
                   rv['v'] = m
                   return m >> send
               except StopIteration:
                   #return mreturn(m)
                   return rv['v']

           return send(None)

       return invoker


class Either(Monad):
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return "Either(%r)" % (self.value,)

class Left(Either):

    def __rshift__(self, func):
        return self

    def __repr__(self):
        return "Left(%r)" % (self.value,)

class Right(Either):
    def __rshift__(self, func):
       return func(self.value)
                                                                    
    def __repr__(self):
     return "Right(%r)" % (self.value,)

class Maybe(Monad):
    def __repr__(self):
     return "Maybe(%r)" % (self.value,)

class Just(Maybe):
    def __init__(self, value):
        self.value = value

    def __rshift__(self, func):
        return func(self.value)

    def __repr__(self):
     return "Just(%r)" % (self.value,)

class Nothing(Maybe):
    def __init__(self):
        super(Nothing, self).__init__(None)

    def __rshift__(self, func):
        return self

    def __repr__(self):
        return "Nothing()"



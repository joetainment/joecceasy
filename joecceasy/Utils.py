
## not really needed since we use metaclasses instead
def callInitCls( cls ):
    cls.InitCls()
    return cls


## classproperty only works for getters
## to make read/write work use @property properties
## on a metaclass instead 
class classproperty(property):
        def __get__(self, obj, objtype=None):
            return super(classproperty, self).__get__(objtype)
        def __set__(self, obj, value):
            super(classproperty, self).__set__(type(obj), value)
        def __delete__(self, obj):
            super(classproperty, self).__delete__(type(obj))

class Object(object):
    pass


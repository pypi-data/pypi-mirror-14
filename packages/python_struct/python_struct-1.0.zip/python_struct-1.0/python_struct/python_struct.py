# Copyright (c) Chai Nunes 2016
class __StructType__(object):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __setattr__(self, key, value):
        if hasattr(self, key):
            super(__StructType__, self).__setattr__(key, value)
        else:
            getattr(self, key) # Trigger AttributeError

    def __repr__(self):
        return repr(self.__dict__)

    def addattr(self, key="", value=None):
        if not hasattr(self, key):
            check = Struct(self.__class__.__name__, (" ".join(self.__dict__.keys()) + " " + key))()
            self.__class__ = check.__class__
            del check
        setattr(self, key, value)

    def edit(self, typename="", field_names=""):
        if not typename == "":
            self.__class__.__name__ = typename
        ret = Struct(self.__class__.__name__, field_names)()
        self.__class__ = ret.__class__

def Struct(typename="Struct", field_names=""):
    fields = dict.fromkeys(field_names.split() if isinstance(field_names, str) else field_names)
    return type(typename, (__StructType__,), fields)

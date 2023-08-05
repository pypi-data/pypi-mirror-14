import json


class Generic(object):
    def __init__(self,object):
        self.__dict__.update(object)
        self.__original__=object

    def __repr__(self):
        rep='<'+self.__class__.__name__+' {'
        first=True
        for attrib in dir(self):
            if not attrib.startswith('__'):
                if first:
                    first=False
                else:
                    rep=rep+','
                rep=rep+attrib
        return rep+'}>'

    def pretty(self):
        return json.dumps(self.__original__,indent=3)

    def get(self,key):
        return self.__dict__.get(key)

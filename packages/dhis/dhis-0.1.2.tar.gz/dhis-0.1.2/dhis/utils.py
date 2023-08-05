from collections import namedtuple
import json

class Utils:
    def cmpT(t1, t2):
        """

        :rtype : bool
        """
        return sorted(t1) == sorted(t2)


    def json_object_hook(d):
        return namedtuple('X', d.keys())(*d.values())


    def json2obj(data):
        return json.loads(data, object_hook=json_object_hook)
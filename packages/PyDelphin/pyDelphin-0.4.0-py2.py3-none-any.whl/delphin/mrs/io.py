
class XmrsSerializer(object):
    def load(self, f, errors='strict', **kwargs):
        if hasattr(f, 'read'):
        pass
    def loads(self, s, errors='strict', **kwargs):
        pass
    def dump(self, x, f, errors='strict', **kwargs):
        pass
    def dumps(self, x, errors='strict', **kwargs):
        pass

    def serialize(x, **kwargs):
        raise NotImplementedError()

    def deserialize(s, **kwargs):
        raise NotImplementedError()

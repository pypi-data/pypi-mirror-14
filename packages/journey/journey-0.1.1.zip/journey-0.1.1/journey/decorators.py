def plugin(cls):
    def _outer(method):
        setattr(cls, method.__name__, method)
        return method
    return _outer
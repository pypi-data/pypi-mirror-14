def plugin(cls):
    def _outer(method):
        cls.PLUGINS.add(method)
        return method
    return _outer
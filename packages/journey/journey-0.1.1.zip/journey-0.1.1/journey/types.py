class DataType:
    def __init__(self, name, fields, formatter=None):
        self.__name__ = name
        self._formatter = formatter
        for fld in fields:
            setattr(self, fld, None)

    def __str__(self):
        return self._formatter(self) if self._formatter else repr(self)
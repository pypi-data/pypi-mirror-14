
__all__ = [
    'ParameterNotFound', 'FilterNotFound', 'ImagineError', 'OriginalKeyDoesNotExist'
]


class ImagineError(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self)
        self.args = args
        self.code = kwargs.pop('code', None)
        self.msg = kwargs.pop('msg', None)

    def __str__(self): # pragma: no cover
        if self.code is not None:
            return '%(code)s: %(msg)s' % self.__dict__
        return Exception.__str__(self)


class ParameterNotFound(ImagineError):
    """
    Parameter not found in config
    """


class FilterNotFound(ImagineError):
    """
    Filter not found in config
    """


class OriginalKeyDoesNotExist(ImagineError):
    """
    Original key does not exist in bucket
    """

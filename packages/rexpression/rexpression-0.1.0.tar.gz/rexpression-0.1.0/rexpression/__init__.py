__all__ = ('regex')

import re

class regex(str):
    class pattern(object):
        def __init__(self, pattern):
            self.pattern = re.compile(pattern)
        def __eq__(self, other):
            return self.pattern.search(other) is not None
        def __ne__(self, other):
            return self.pattern.search(other) is None
    def __invert__(self):
        return self.__class__.pattern(self)
    def __hash__(self):
        return super(regex, self).__hash__()


from .common import Common
from .utils import Utils


class Peka(object):
    def __init__(self, arg):
        self._arg = arg
        self._common = Common()
        self._utils = Utils()

    def printer(self):
        print(self._arg)
        print(self._common.printer())
        print(self._utils.printer())

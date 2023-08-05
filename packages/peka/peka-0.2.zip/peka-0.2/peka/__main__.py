import os
from .base import Peka


os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


# if __name__ == '__main__':
# print os.getcwd()
p = Peka('peka')
p.printer()

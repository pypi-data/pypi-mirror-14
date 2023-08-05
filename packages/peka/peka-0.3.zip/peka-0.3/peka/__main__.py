import os
from .base import Peka


os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


def main():
    print os.getcwd()
    p = Peka('peka')
    p.printer()


if __name__ == '__main__':
    main()

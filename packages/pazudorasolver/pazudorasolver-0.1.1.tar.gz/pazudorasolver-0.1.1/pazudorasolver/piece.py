from abc import ABCMeta, abstractproperty
from termcolor import colored


class Piece(object):
    __metaclass__ = ABCMeta

    def __init__(self, r, c):
        self._row = r
        self._column = c

    def __repr__(self):
        return colored(self.symbol, self.color)

    @property
    def location(self):
        return (self._row, self._column)

    @abstractproperty
    def symbol(self):
        pass

    @abstractproperty
    def color(self):
        pass

    @abstractproperty
    def matchable(self):
        pass


class Fire(Piece):
    symbol = 'R'
    color = 'red'
    matchable = True


class Wood(Piece):
    symbol = 'G'
    color = 'green'
    matchable = True


class Water(Piece):
    symbol = 'B'
    color = 'blue'
    matchable = True


class Dark(Piece):
    symbol = 'P'
    color = 'magenta'
    matchable = True


class Light(Piece):
    symbol = 'Y'
    color = 'yellow'
    matchable = True


class Heart(Piece):
    symbol = 'H'
    color = 'cyan'
    matchable = True


class Poison(Piece):
    symbol = '@'
    color = 'white'
    matchable = True


class Jammer(Piece):
    symbol = '#'
    color = 'white'
    matchable = True


class Unknown(Piece):
    symbol = '?'
    color = 'grey'
    matchable = False

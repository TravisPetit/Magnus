class Symbol:
    """ Immutable representation of a symbol """

    def __init__(self, symbol, inverted=False):
        symbol = symbol.replace(" ", "")
        self.__symbol = symbol
        self.__inverted = inverted

    @property
    def symbol(self):
        return self.__symbol

    @property
    def unsigned_symbol(self):
        return self.__symbol.replace("I", "")

    @property
    def inverted(self):
        return self.__inverted

    def negate(self):
        return Symbol(self.unsigned_symbol, not self.inverted)

    def __str__(self):
        return self.symbol + ("I" if self.inverted else "")

    def __eq__(self, other):
        return self.symbol == other.symbol and self.inverted == other.inverted

    def is_inverse_of(self, other):
        return self.symbol == other.symbol and self.inverted != other.inverted

    def __repr__(self):
        return str(self)

    def repeat(self, n):
        s = [self for _ in range(n)]
        return Word(*s)

    def __add__(self, other):
        if isinstance(other, Word):
            return Word(self) + other

        if isinstance(other, Symbol):
            return Word(self, other)

        raise Exception("Invalid type for " + other)

class Word:
    """ Immutable representation of a word """

    def __init__(self, *symbols):
        self.__symbols = list(symbols)
        self.__reduce()

    @property
    def symbols(self):
        return self.__symbols

    def __len__(self):
        return len(self.symbols)

    def __reduce(self):
        keep_going = True
        while keep_going:
            keep_going = False
            for i in range(len(self) - 1):
                if self.symbols[i].is_inverse_of(self.symbols[i+1]):
                    del self.symbols[i:i+2]
                    keep_going = True
                    break


    def compare(self, other):
        for i in range(len(self)):
            try:
                other.symbols[i]
            except IndexError:
                return False

            if self.symbols[i] != other.symbols[i]:
                return False
        return True

    def __str__(self):
        s = "[ "
        for w in self.symbols:
            s += str(w) + " "
        return s + "]"

    @property
    def str_for_gen(self):
        s = ""
        for w in self.symbols:
            s += str(w) + ", "
        return s[:-2]

    @property
    def str_for_rel(self):
        s = ""
        for w in self.symbols:
            s += str(w) + "*"
        return s[:-1]

    def __add__(self, other):
        if isinstance(other, Word):
            s = self.symbols + other.symbols
            return Word(*s)

        if isinstance(other, Symbol):
            return self + Word(other)
        raise Exception("Invalid type for " + str(type(other)))

    @staticmethod
    def from_string(s):
        s = s.split(" ")
        symbols = []
        for q in s:
            q = q.split("I")
            if len(q) == 1:
                symbols.append(Symbol(q[0]))
            else:
                symbols.append(Symbol(q[0], True))
        return Word(*symbols)


class ORG:
    """ One relator group """
    def __init__(self, generators, relator):
        self.generators = generators
        self.relator = relator

    def __str__(self):
        return "< " + self.generators.str_for_gen + " | " + self.relator.str_for_rel + " >"


class FreeSymbolWithIndex(Symbol):
    def __init__(self, symbol, index):
        symbol_str = symbol.unsigned_symbol + "_" + str(index)

        self.__original = symbol
        self.__index = index
        super().__init__(symbol_str, symbol.inverted)

    @property
    def index(self):
        return self.__index

    @property
    def original(self):
        return self.__original



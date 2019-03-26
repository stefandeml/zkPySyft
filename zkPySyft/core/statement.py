from collections import namedtuple

from zkPySyft.io.pysyft import read_pysyft_plan


class Statement(namedtuple('_Statement', ('lhs rhs res ins'))):
    "Wrapped to add more class features over time"
    pass


class StatementStore(object):
    def __init__(self, path):
        statements = []
        for s in read_pysyft_plan(path):
            statements.append(s)
        self.statements = statements

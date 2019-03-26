from collections import namedtuple

from zkPySyft.io.pysyft import read_pysyft_plan


class AddInstruction:
    def __init__(self, out, lhs, rhs):
        self.out = out
        self.lhs = lhs
        self.rhs = rhs

    def to_zokrates(self):
        return "v{} = v{} + v{}".format(self.out, self.lhs, self.rhs)

class MulInstruction:
    def __init__(self, out, lhs, rhs):
        self.out = out
        self.lhs = lhs
        self.rhs = rhs

    def to_zokrates(self):
        return "v{} = v{} * v{}".format(self.out, self.lhs, self.rhs)

class DivCInstruction:
    DIVISION_CONSTANT = 42

    def __init__(self, out, lhs, rhs=DIVISION_CONSTANT):
        self.out = out
        self.lhs = lhs
        self.rhs = rhs

    def to_zokrates(self):
        return "v{} = v{} / {}".format(self.out, self.lhs, self.rhs)

class Gt0Instruction:
    def __init__(self, out, val):
        self.out = out
        self.val = val

    def to_zokrates(self):
        return "v{} = if v{} == 0 then 0 else 1 fi".format(out, val)


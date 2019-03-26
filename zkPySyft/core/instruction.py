class Instruction:
    def __init__(self, out, lhs, rhs):
        self.out = out
        self.lhs = lhs
        self.rhs = rhs

class AddInstruction(Instruction):
    def __repr__(self):
        return self.to_zokrates()

    def to_zokrates(self):
        return "field v{} = v{} + v{}".format(self.out, self.lhs, self.rhs)

class MulInstruction(Instruction):
    def __repr__(self):
        return self.to_zokrates()

    def to_zokrates(self):
        return "field v{} = v{} * v{}".format(self.out, self.lhs, self.rhs)

class DivCInstruction(Instruction):
    def __repr__(self):
        return self.to_zokrates()

    def to_zokrates(self):
        return "field v{} = v{} / {}".format(self.out, self.lhs, self.rhs)

class GtCInstruction(Instruction):
    def __repr__(self):
        return self.to_zokrates()

    def to_zokrates(self):
        if int(self.rhs) != 0:
            raise NotImplementedError("Greater than instruction currently "
                                      "support only comparison with 0")
        return "field v{} = if v{} == {} then 0 else 1 fi".format(self.out, self.lhs, self.rhs)


import ast
import csv

from zkPySyft.core.instruction import AddInstruction, MulInstruction, \
    DivCInstruction, Gt0Instruction


ADD_INSTRUCTION = b"__add__"
MUL_INSTRUCTION = b"__mul__"
DIVC_INSTRUCTION = b"__divC__"
GT0_INSTRUCTION = b"__gt0__"
FACTORIES = {
    ADD_INSTRUCTION: AddInstruction,
    MUL_INSTRUCTION: MulInstruction,
    DIVC_INSTRUCTION: DivCInstruction,
    GT0_INSTRUCTION: Gt0Instruction
}


def read_pysyft_inputs(path):
    with open(path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row

def read_pysyft_plan(path):
    with open(path, "r") as f:
        for line in f:
            if line:
                yield parse_instruction(line)

def parse_instruction(line):
    parts = ast.literal_eval(line)
    ins = parts[0]

    if ins in { MUL_INSTRUCTION, ADD_INSTRUCTION, DIVC_INSTRUCTION }:
        assert len(parts) == 4, "Malformed {} instruction: {}".format(ins, line)
        return FACTORIES[ins](parts[1], parts[2], parts[3])
    elif ins == GT0_INSTRUCTION:
        assert len(parts) == 3, "Malformed __gt0__ instruction: {}".format(line)
        return FACTORIES[ins](parts[1], parts[2])
    else:
        raise ValueError("Unsupported instruction {}, line {}".format(ins, line))

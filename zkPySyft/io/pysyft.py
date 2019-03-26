import ast
import csv

from zkPySyft.core.instruction import AddInstruction, MulInstruction, \
    DivCInstruction, GtCInstruction


ADD_INSTRUCTION = b"__add__"
MUL_INSTRUCTION = b"__mul__"
DIVC_INSTRUCTION = b"__divC__"
GTC_INSTRUCTION = b"__gtC__"
FACTORIES = {
    ADD_INSTRUCTION: AddInstruction,
    MUL_INSTRUCTION: MulInstruction,
    DIVC_INSTRUCTION: DivCInstruction,
    GTC_INSTRUCTION: GtCInstruction
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
    try:
        parts = ast.literal_eval(line)
        ins = parts[0]
    except ValueError:
        raise ValueError("Malformed instruction: {}".format(line))

    if ins in { MUL_INSTRUCTION, ADD_INSTRUCTION, DIVC_INSTRUCTION, GTC_INSTRUCTION }:
        assert len(parts) == 4, "Malformed {} instruction: {}".format(ins, line)
        return FACTORIES[ins](parts[1], parts[2], parts[3])
    else:
        raise ValueError("Unsupported instruction {}, line {}".format(ins, line))

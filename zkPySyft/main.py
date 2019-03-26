import tempfile
import sys

from zkPySyft.io.pysyft import read_pysyft_inputs, read_pysyft_plan
from zkPySyft.core.zokrates import ZoKrates

# TODO: Check if this is the best place for defining the consntants
SCENARIO_1 = 0
SCENARIO_2 = 1
SCENARIO_3 = 2

# TODO: fix scenarios
def process_pysyft_input(scenario, path):
    for row in read_pysyft_inputs(path):
        if scenario == SCENARIO_1:
            pass
        if scenario == SCENARIO_2:
            pass
        if scenario == SCENARIO_3:
            pass
        yield row


def main(pysyft_plan_file, pysyft_input_file, scenario):
    instructions = read_pysyft_plan(pysyft_plan_file)
    inputs = process_pysyft_input(scenario, pysyft_input_file)

    zokrates = ZoKrates(instructions, inputs)
    zokrates.run("zokrates.code")


if __name__ == "__main__":
    print(sys.argv)
    assert len(sys.argv) == 4, \
        "You must specify a plan file, an input file and a scenario"
    main(sys.argv[1], sys.argv[2], sys.argv[3])

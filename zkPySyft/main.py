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


def main():
    path = "21"
    statements = read_pysyft_plan(path)
    inputs = process_pysyft_input(SCENARIO_3, path)
    path_out = "3123"

    zokrates = ZoKrates(statements, inputs)
    zokrates.compile(path_out)
    zokrates.synthesize()
    zokrates.setup()
    zokrates.compute_witness()
    zokrates.generate_proof()

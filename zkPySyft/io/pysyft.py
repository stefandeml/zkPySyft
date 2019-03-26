import csv
from zkPySyft.core.statement import Statement
from zkPySyft.util import take, get_re_group1


def read_pysyft_inputs(path):
    with open(path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row


def read_pysyft_plan(path):
    with open(path, "r") as file:
        # TODO: Consider using the CSV reader from above
        for line in file:
            ins, res, lhs, rhs = line.split(",")
            yield Statement(lhs, rhs, res, ins)

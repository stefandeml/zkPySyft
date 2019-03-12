import csv
from zkPySyft.core.statement import Statement
import re
from zkPySyft.util import take, get_re_group1

def read_pysyft_inputs(path):
    with open(path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row 

re_ins = re.compile(r"__([a-z]+)__")
re_operands = re.compile(r"\[\d+, (\d+), \d+, .*, .*\]")
re_res = re.compile(r"(\d+)\]\]\)\)")

def read_pysyft_plan(path):
    with open(path, "r") as file:  
        for line in file:
            match = re.search(re_ins, line)
            if match:
                ins = match.group(1)
                operands = take(3, file)

                lhs = get_re_group1(re_operands, operands[0])
                rhs = get_re_group1(re_operands, operands[1])
                res = get_re_group1(re_res, operands[2])

                s = Statement(
                    lhs,
                    rhs,
                    res,
                    ins
                )

                yield s

from itertools import islice
import re

def take(n, iterable):
    "Return next n items of the iterable as a list"
    return list(islice(iterable, n))

def get_re_group1(regex, string):
    "Return the first matched group"
    match = re.search(regex, string)
    if match:
        res = match.group(1)
        return res
    else:
        return None

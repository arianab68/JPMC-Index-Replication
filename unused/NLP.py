import pandas as pd
import numpy as np
import re
import itertools
from word2number import w2n

def extract_number(inp):
    res = re.findall(r'\d+', inp)
    if len(res) > 0:
        res = [int(res[0])]
    #if it comes here that means the input doesn't have a numeric form and probably word format
    if not res:
        for w in inp.split():
            if not res:
                try:
                    res = [w2n.word_to_num(w)]
                except:
                    res = []
    return res


def extract_mathematical(inp):
    #dictionary of key words for inequalities
    d = {
        "=": ["only", "exactly"],
        ">=": ["at least", "minimum", "no less than", "no fewer than", "greater than or equal to"],
        "<=": ["at most", "maximum", "no more than", "not above", "does not exceed", "less than or equal to"],
        ">": ["more than", "exceeds", "over", "above", "greater than"],
        "<": ["under", "below", "fewer than", "beneath", "less than"]
    }
    res = []
    for key, value in d.items():
        for w in value:
            if w in inp.lower():
                res.append(key)
    return res

#NEED TO ADD CATEGORICAL EXTRACTION CODE




def extraction(inp):
    res = []
    mth = extract_mathematical(inp)
    num = extract_number(inp)
    #we don't have categorical extract function yet for sector
    cat = False
    if len(mth) > 0:
        res.append((mth[0], 'mth'))
    else:
        res.append(("None", "mth"))
    if len(num) > 0:
        res.append((num[0], 'num'))
    else:
        res.append(("None", "num"))
    if cat:
        res.append((cat, "cat"))
    else:
        res.append(("None", "cat"))
    return res



if __name__ == "__main__":
    print(extraction("I want 3 tech stocks"))
    print(extraction("I want 3 tech stocks"))
    print(extraction("I want 3 tech stocks"))
    print(extraction("I want 3 tech stocks"))
    print(extraction("I want 3 tech stocks"))
    print(extraction("I want 3 tech stocks"))
    print(extraction("I want 3 tech stocks"))
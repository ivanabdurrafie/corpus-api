from ast import Return
from collections import Counter


def countWord(list):
    freq = Counter(list)
    return freq

def mostCommon(list):
    freq = Counter(list)
    return freq.most_common(10)

from pathlib import Path
import re
import numpy as np
import math


def rms(values, value):
    if not values:
        return 0
    sum_of_squares = sum((x - value) ** 2 for x in values)
    mean_of_squares = sum_of_squares / len(values)
    return math.sqrt(mean_of_squares)
class LightValues:
    def __init__(self, lv=None, rv=None):
        self.lv = lv
        self.rv = rv

def get_lines(path):
    condition = not (Path(path).exists())
    if condition:
        return 0
    rexp = [r'\d{1,2}\.\d{1,2}\%|\d\%', r'\d{3,5}\.\d{1,6}']
    lines = []

    lvpack = []
    rv = 0
    flag = False
    with open(path, 'r') as f:
        for line in f:
            if ('Probe' in line) and not (' 0' in line):
                flag = False
                lvpack = [float(x) for x in lvpack]
                lines.append(LightValues(rv=rv, lv=np.array(lvpack)))
                lvpack = []
                rv = 0
            if flag is True:
                lvpack += re.findall(rexp[1], line)
            if 'Concentration' in line:
                flag = True
                try:
                    rv = re.findall(rexp[0], line)[0]
                    rv = float(rv[:-1])
                except Exception:
                    rv = None
        lvpack = [float(x) for x in lvpack]
        lines.append(LightValues(rv=rv, lv=np.array(lvpack)))
    return lines

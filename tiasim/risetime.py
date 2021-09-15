import numpy as np


# Step Resonse Tools
def get_signal_start_end(data, n=8):
    low = np.mean(data[:n])
    high = np.mean(data[-n:])
    return low, high

def get_percent_value(data, percent, n=8):
    start, end = get_signal_start_end(data, n)
    return np.abs(start - end)*percent/100. + min([start, end])

def get_first_higher_value(value, x, data):
    for xp, p in zip(x, data):
        if p > value:
            return xp
    raise UserWarning("get_first_higher_value Failed")

def get_slew_by_mode(mode, x, data, percents=(10,90)):
    ninetyPercent = get_percent_value(data, max(percents))
    tenPercent = get_percent_value(data, min(percents))
    assert(ninetyPercent > tenPercent)

    if mode == 'RISING':
        tenPercentPos = get_first_higher_value(tenPercent, x, data)
        ninetyPercentPos = get_first_higher_value(ninetyPercent, x, data)
    elif mode == 'FALLING':
        tenPercentPos = get_first_higher_value(tenPercent, x[::-1], data[::-1])
        ninetyPercentPos = get_first_higher_value(ninetyPercent, x[::-1], data[::-1])
    else:
        raise UserWarning('unknown mode %s'%mode)

    return (ninetyPercentPos, ninetyPercent), (tenPercentPos, tenPercent)

def find_rise_time(x, y):
    mode = 'FALLING'
    if y[-1] > y[0]:
        mode = 'RISING'
    (ninetyPercentPos, ninetyPercent), (tenPercentPos, tenPercent) = get_slew_by_mode(mode, x, y)
    return abs(ninetyPercentPos - tenPercentPos)

def calc_slew_rate(x, y):
    mode = 'FALLING'
    if y[-1] > y[0]:
        mode = 'RISING'
    (sixtyPercentPos, sixtyPercent), (fortyPercentPos, fortyPercent) = get_slew_by_mode(mode, x, y, percents=[40, 60])
    average_slew_rate = abs(sixtyPercent-fortyPercent)/float(sixtyPercentPos-fortyPercentPos)
    return average_slew_rate

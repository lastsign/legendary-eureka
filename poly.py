import numpy as np
import random

alpha = 'ЕЖЗИЙК'
val = ['11000101', '11000110', '11000111', '11001000', '11001001', '11001010']
dlv = {k: v for k, v in zip(alpha, val)}
dvl = {v: k for k, v in zip(alpha, val)}
g = [1, 1, 0, 1, 1, 1]
n = 13
k = 8


def shift(poly):
    p_shift = np.zeros(n)
    for i, v in enumerate(poly):
        p_shift[i] = v
    return p_shift


def generate(info):
    shifted = shift(info)
    _, remain = np.polydiv(shifted, g)
    remain = np.mod(remain, np.ones_like(remain) * 2)
    remain = np.concatenate([np.zeros(n - len(remain)), remain])
    poly = [int(x) for x in shifted != remain]
    return poly


def find_synd(code):
    _, synd = np.polydiv(code, g)
    synd = np.mod(synd, np.ones_like(synd) * 2)
    return synd


for l, v in dlv.items():
    print(l, ': ', v)
    code = generate(v)
    print(code, 'cyclic code')
    er = random.randint(0, len(code) - 1)
    code[er] = 0 if code[er] == 1 else 1
    print(code, 'cyclic code with one error')
    synd = find_synd(code)
    if all(synd == 0):
        print('None syndrome')
    else:
        print(f'Syndrome is {synd}')

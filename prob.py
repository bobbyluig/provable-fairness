import hashlib
import os
import random

import numpy as np
import itertools
import hmac
from matplotlib import pyplot as plt
from scipy import stats


def roll(seed):
    offset = 0

    while True:
        number = int(seed[offset: offset + 5], 16)

        if number < 1000000:
            return number % 10000

        offset += 5


def test(count):
    bins = [0] * 10000

    # m = hashlib.sha512()
    # m.update(os.urandom(64).hex().encode())
    m = hmac.new(os.urandom(64).hex().encode())

    for i in range(count):
        m_prime = m.copy()
        m_prime.update(str(i).encode())
        bins[roll(m_prime.hexdigest())] += 1
        # bins[random.randint(0, 9999)] += 1

    expected = count / 10000
    return sum((y - expected) ** 2 / expected for y in bins)


def test2():
    m = hashlib.sha256()
    m.update(os.urandom(32).hex().encode())

    m_first = m.copy()
    m_first.update(b'0')
    first = roll(m_first.hexdigest())

    m_second = m.copy()
    m_second.update(b'1')
    second = roll(m_second.hexdigest())

    return abs(first - second)


def hamming(n1, n2):
    x = n1 ^ n2
    set_bits = 0

    while x > 0:
        set_bits += x & 1
        x >>= 1

    return set_bits


def test3(seed, count):
    numbers = [0] * count

    m = hashlib.sha256()
    m.update(seed)

    for i in range(count):
        m_prime = m.copy()
        m_prime.update(str(i).encode())

        # numbers[i] = roll(m_prime.hexdigest())
        numbers[i] = random.randint(0, 9999)

    return numbers


y = []

for i in range(1000):
    p = stats.chi2.sf(test(10000), 9999)
    print(i, p)
    y.append(p)

plt.hist(y)
plt.show()


def autocorr(x, t=1):
    return np.corrcoef(np.array([x[:-t], x[t:]]))


def test4(count):
    numbers = [0] * count

    m = hashlib.sha512()
    m.update(os.urandom(64).hex().encode())
    m.update(b',6857,')
    # random.seed(os.urandom(64).hex().encode())

    for i in range(count):
        m_prime = m.copy()
        m_prime.update(str(i).encode())

        numbers[i] = roll(m_prime.hexdigest()) > 4999
        # numbers[i] = random.randint(0, 9999) > 4999

    # return np.var(list(sum(1 for _ in l) for n, l in itertools.groupby(numbers)))
    # return len(list(itertools.groupby(numbers)))
    # return sum(numbers[i] > numbers[i - 1] for i in range(1, len(numbers)))
    return numbers[0] != numbers[1]


def test5(count):
    numbers = [0] * count

    m = hmac.new(os.urandom(64).hex().encode())
    # random.seed(os.urandom(64).hex().encode())

    for i in range(count):
        m_prime = m.copy()
        m_prime.update(str(i).encode())

        numbers[i] = roll(m_prime.hexdigest()) > 4999
        # numbers[i] = random.randint(0, 9999) > 4999

    # return np.var(list(sum(1 for _ in l) for n, l in itertools.groupby(numbers)))
    return len(list(itertools.groupby(numbers)))
    # return sum(numbers[i] > numbers[i - 1] for i in range(1, len(numbers)))
    # return numbers[0] != numbers[1]


# y = []
#
# for i in range(100000):
#     data = test5(100)
#     y.append(data)
#
# print(np.mean(y), np.var(y), np.max(y))

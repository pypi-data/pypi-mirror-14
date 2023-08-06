from itertools import izip_longest


def grouper(n, iterable, padvalue=None):
    "grouper(3, 'abcdefg', 'x') --> ('a','b','c'), ('d','e','f'), ('g','x','x')"
    return izip_longest(*[iter(iterable)]*n, fillvalue=padvalue)


def bouncy_hex_decode(hex):
    return "".join(map(lambda pair: chr(int("".join(pair), 16)), grouper(2, hex)))
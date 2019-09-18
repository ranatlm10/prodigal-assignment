import sys
from prime_numbers import library_method
import random


def generate_files(quantity):
    for id in range(0, quantity):
        f = open(("tmp/file_%d.txt"%id), "w+")
        f.write("%r" % sorted(random.choices(library_method(100), k=5)))
        f.close()


generate_files(int(sys.argv[1]))

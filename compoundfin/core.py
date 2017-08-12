import argparse

import sys

"""
Interface with user
Switch between data acquisition or query running modes
"""


def run():
    print("Hello")
    for arg in sys.argv[1:]:
        print(arg)


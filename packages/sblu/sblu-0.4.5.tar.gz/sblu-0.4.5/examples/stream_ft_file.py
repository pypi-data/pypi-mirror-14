#!/usr/bin/env python
"""
A simple example that just streams an ft file from cluspro and prints it
to stdout.
"""
from sblu.cluspro import ClusproClient
from sblu.config import config
import sys


cluspro_id = int(sys.argv[1])

with ClusproClient(config) as client:
    with client.ftfile(cluspro_id, 0) as ftfile:
        for line in ftfile:
            print(line)

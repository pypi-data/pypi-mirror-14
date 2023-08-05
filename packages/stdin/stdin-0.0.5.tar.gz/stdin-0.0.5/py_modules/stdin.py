#!/usr/bin/env python
__all__ = ["STDIN"]
import os
import sys

STDIN = None
if os.fstat(sys.stdin.fileno()).st_size > 0:
    STDIN = sys.stdin.read()

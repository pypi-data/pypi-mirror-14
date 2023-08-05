# -*- coding: utf-8 -*-

import uuid
import math

#-----------------------------------------------------------------------------
# Classes and functions
#-----------------------------------------------------------------------------

def tolerant_equals(a, b, atol=10e-7, rtol=10e-7):
    return math.fabs(a - b) <= (atol + rtol * math.fabs(b))


def isint(num):
    return isinstance(num, int)

def isnumber(num):
    return isinstance(num, (int, float))

def generate_uuid():
    return uuid.uuid4().hex

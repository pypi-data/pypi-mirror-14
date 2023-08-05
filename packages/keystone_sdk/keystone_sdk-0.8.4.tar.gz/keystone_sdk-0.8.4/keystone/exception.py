# -*- coding: utf-8 -*-

class KSEndTimeReachedException(Exception):
    def __str__(self):
        return "Reach End Time"
    
class KSStopLineReachedException(Exception):
    def __str__(self):
        return "Reach Stop Line"
    
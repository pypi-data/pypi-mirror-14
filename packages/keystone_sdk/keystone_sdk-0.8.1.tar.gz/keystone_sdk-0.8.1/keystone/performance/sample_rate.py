# -*- coding: utf-8 -*-

import numpy as np
from datetime import datetime, timedelta

class KSSampleRate():
    '''
    KSSampleRate store all the informations that need to annulize daily return,
    such as `sample rate`, `trading days` and `trading hours`.
    All of this informations are class properties
    '''

    MONTH = "MONTH"
    DAY = "DAY"
    HOUR = "HOUR"
    MINUTE = "MINUTE"
    SECOND = "SECOND"

    # default rate is DAY
    rate = "DAY"
    tradingDays = 250
    tradingHours = 4
    @classmethod
    def datetimeOffset(cls, rate = None):
        if rate is None:
            rate = cls.rate
        if rate == cls.DAY:
            return timedelta(days = 1)
        elif rate == cls.HOUR:
            return timedelta(hours = 1)
        elif rate == cls.MINUTE:
            return timedelta(minutes = 1)
        elif rate == cls.SECOND:
            return timedelta(seconds = 1)
        else:
            return timedelta(0)

    @classmethod
    def getAnnulizedMultiplier(cls, rate = None, tradingDays = None, tradingHours = None, squared = False):
        if rate is None:
            rate = cls.rate
        if tradingDays is None:
            tradingDays = cls.tradingDays
        if tradingHours is None:
            tradingHours = cls.tradingHours
            
        if rate == KSSampleRate.MONTH:
            multiplier = 12
        elif rate == KSSampleRate.DAY:
            multiplier = tradingDays
        elif rate == KSSampleRate.HOUR:
            multiplier = tradingDays * tradingHours
        elif rate == KSSampleRate.MINUTE:
            multiplier = tradingDays * tradingHours * 60
        elif rate == KSSampleRate.SECOND:
            multiplier = tradingDays * tradingHours * 3600
        else:
            raise ValueError('rate error, rate MUST be ["MONTH", "DAY", "HOUR", "MINUTE", "SECOND"]')
        if squared:
            multiplier = np.sqrt(multiplier)

        return multiplier

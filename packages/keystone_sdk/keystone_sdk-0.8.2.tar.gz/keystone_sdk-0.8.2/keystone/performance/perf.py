# -*- coding: utf-8 -*-

from copy import copy
from six import with_metaclass
import abc
import numpy as np
from datetime import datetime, timedelta
from collections import deque

from keystone.performance import risk
from keystone.performance.analyzer import KSAnalyzer
from keystone.performance.sample_rate import KSSampleRate
from keystone.parameters import DEFAULT_BENCHMARK_COLUMN
from keystone.constant import SIGNAL_DATA_SID_COLUMNS

class PeriodReturn(object):
    benchmark_sid = SIGNAL_DATA_SID_COLUMNS
    benchmark_column = DEFAULT_BENCHMARK_COLUMN
    def __init__(self):
        self.algoPeriodStartingValue = None
        self.algoPeriodEndingValue = None
        self.benchmarkPeriodStartingValue = None
        self.benchmarkPeriodEndingValue = None

        self.algoReturn = 0.0
        self.benchmarkReturn = 0.0

        # save this two for faster calculate cumulative return
        self.algoStartingValue = None
        self.benchmarkStartingValue = None

    def to_dict(self):
        fields = copy(self.__dict__)
        return fields

    def __str__(self):
        return self.to_dict().__str__()

    def __repr__(self):
        return self.to_dict().__repr__()

    @classmethod
    def setBenchmark(cls, sid, column):
        cls.benchmark_sid = sid
        cls.benchmark_column = column

    def rollover(self):
        self.algoPeriodStartingValue = self.algoPeriodEndingValue
        self.benchmarkPeriodStartingValue = self.benchmarkPeriodEndingValue
        self.algoReturn = 0.0
        self.benchmarkReturn = 0.0

    def calculateReturn(self):
        pnl = self.algoPeriodEndingValue - self.algoPeriodStartingValue
        self.algoReturn = 0.0
        if self.algoPeriodStartingValue != 0:
            self.algoReturn = pnl / self.algoPeriodStartingValue

        benchmarkPnl = self.benchmarkPeriodEndingValue - self.benchmarkPeriodStartingValue
        self.benchmarkReturn = 0.0
        if self.benchmarkPeriodStartingValue != 0:
            self.benchmarkReturn = benchmarkPnl / self.benchmarkPeriodStartingValue

    def update(self, dataEvent, context):
        if self.algoPeriodStartingValue is None:
            self.algoPeriodEndingValue = context.portfolio.value()
            try:
                self.benchmarkPeriodEndingValue = dataEvent.query(self.benchmark_sid, self.benchmark_column)
            except Exception as e:
                self.benchmarkPeriodEndingValue = np.nan
            self.algoStartingValue = context.portfolio.startingCash()
            self.benchmarkStartingValue = self.benchmarkPeriodEndingValue
            self.rollover()
            return

        self.algoPeriodEndingValue = context.portfolio.value()
        try:
            self.benchmarkPeriodEndingValue = dataEvent.query(self.benchmark_sid, self.benchmark_column)
        except Exception as e:
            self.benchmarkPeriodEndingValue = np.nan

        # take care of nan benchmark starting value
        if np.isnan(self.benchmarkStartingValue):
            self.benchmarkStartingValue = self.benchmarkPeriodEndingValue

class ReturnTracker(object):
    def __init__(self):
        self.algoReturns = deque()
        self.benchmarkReturns = deque()

        self.algoCumulativeReturns = deque()
        self.benchmarkCumulativeReturns = deque()

        self.algoMeanReturns = deque()
        self.benchmarkMeanReturns = deque()

        self.algoAnnulizedMeanReturns = deque()
        self.benchmarkAnnulizedMeanReturns = deque()

    def to_dict(self):
        fields = copy(self.__dict__)
        return fields

    def __str__(self):
        return self.to_dict().__str__()

    def __repr__(self):
        return self.to_dict().__repr__()

    '''
    calculateCumulativeReturn is deprecated. TOO SLOW
    '''
    def calculateCumulativeReturn(self, returns):
        return (1. + np.array(returns)).prod() - 1
        # return np.prod([1. + x for x in returns]) - 1

    def calculateAnnulizedReturn(self, returns):
        return KSSampleRate.getAnnulizedMultiplier(squared = False) * returns

    def update(self, period):
        '''
        period: a PeriodReturn instance
        '''
        self.algoReturns.append(period.algoReturn)
        self.benchmarkReturns.append(period.benchmarkReturn)
        numTradingUnits = len(self.algoReturns)

        '''
        self.algoCumulativeReturns.append(\
            self.calculateCumulativeReturn(self.algoReturns))
        self.benchmarkCumulativeReturns.append(\
            self.calculateCumulativeReturn(self.benchmarkReturns))
        '''
        self.algoCumulativeReturns.append(\
            (period.algoPeriodEndingValue - period.algoStartingValue) / period.algoStartingValue)
        self.benchmarkCumulativeReturns.append(\
            (period.benchmarkPeriodEndingValue - period.benchmarkStartingValue) / period.benchmarkStartingValue)

        self.algoMeanReturns.append(self.algoCumulativeReturns[-1] / numTradingUnits)
        self.benchmarkMeanReturns.append(self.benchmarkCumulativeReturns[-1] / numTradingUnits)

        self.algoAnnulizedMeanReturns.append(\
            self.calculateAnnulizedReturn(self.algoMeanReturns[-1]))
        self.benchmarkAnnulizedMeanReturns.append(\
            self.calculateAnnulizedReturn(self.benchmarkMeanReturns[-1]))

class KSPerformance(object):
    def __init__(self):
        self.period = PeriodReturn()
        self.lastdt = None
        self.nextdt = None

    def to_dict(self):
        fields = copy(self.__dict__)
        return fields

    def __repr__(self):
        return self.to_dict().__repr__()

    def __str__(self):
        return self.to_dict().__str__()

    def initialize(self):
        self.returnTracker = ReturnTracker()
        KSAnalyzer.returnTracker = self.returnTracker

    ''' deprecated methods
    def setSampleRate(self, rate):
        self.sampleRate = rate

    def setRiskless(self, riskless):
        self.riskless = riskless

    def setTradingDays(self, days):
        self.tradingDays = days

    def setTradingHours(self, hours):
        self.tradingHours = hours
    '''

    def getNextDate(self):
        if KSSampleRate.rate == KSSampleRate.MONTH:
            nextdt = self.lastdt
            current_month = nextdt.month
            while nextdt.month == current_month:
                nextdt += timedelta(days = 1)
            return nextdt
        else:
            return self.lastdt + KSSampleRate.datetimeOffset()

    '''
    def calculateMaxDrawdown(self):
        if len(self.algoCumulativeReturns) == 0:
            return self.currentDrawdown

        # The drawdown is defined as: (high - low) / high
        # The above factors out to: 1.0 - (low / high)
        drawdown = 1.0 - (1.0 + self.algoCumulativeReturns[-1])/(1.0 + self.currentMaxReturn)
        if self.currentDrawdown > drawdown:
            return self.currentDrawdown
        else:
            return drawdown

    def calculateSharpe(self):
        """
        http://en.wikipedia.org/wiki/Sharpe_ratio
        """
        assert len(self.volatility) == len(self.algoAnnulizedMeanReturns)
        return risk.sharpe_ratio(
            self.algoAnnulizedMeanReturns[-1],
            self.riskless,
            self.volatility[-1])

    def calculateSortino(self):
        """
        http://en.wikipedia.org/wiki/Sortino_ratio
        """
        assert len(self.downsideRisk) == len(self.algoAnnulizedMeanReturns)
        return risk.sortino_ratio(
            self.algoAnnulizedMeanReturns[-1],
            self.riskless,
            self.downsideRisk[-1])

    def calculateInformation(self):
        """
        http://en.wikipedia.org/wiki/Information_ratio
        """
        assert len(self.volatility) == len(self.algoAnnulizedMeanReturns)
        return risk.information_ratio(
            self.algoAnnulizedMeanReturns[-1],
            self.benchmarkAnnulizedMeanReturns[-1],
            self.volatility[-1])

    def calculateAlpha(self):
        """
        http://en.wikipedia.org/wiki/Alpha_(investment)
        """
        assert len(self.beta) == len(self.algoAnnulizedMeanReturns)
        return risk.alpha(
            self.algoAnnulizedMeanReturns[-1],
            self.riskless,
            self.benchmarkAnnulizedMeanReturns[-1],
            self.beta[-1])

    def calculateVolatility(self, returns):
        if len(returns) <= 1:
            return 0.0
        # return np.std(returns, ddof=1) * math.sqrt(252)
        return np.std(returns, ddof=1) * self.getAnnulizedMultiplier(squared = True)

    def calculateDownsideRisk(self):
        """
        https://en.wikipedia.org/wiki/Downside_risk
        """
        return risk.downside_risk(self.algoReturns,
                             self.algoMeanReturns,
                             self.getAnnulizedMultiplier())

    def calculateBeta(self):
        """
        http://en.wikipedia.org/wiki/Beta_(finance)
        """
        return risk.beta(self.algoReturns, self.benchmarkReturns)

    def calculatePerformance(self):
        # max drawdown
        self.currentMaxReturn = np.max((self.currentMaxReturn, self.algoCumulativeReturns[-1]))
        self.currentDrawdown = self.calculateMaxDrawdown()
        self.maxDrawdown.append(self.currentDrawdown)

        # volatility
        self.volatility.append(self.calculateVolatility(self.algoReturns))
        self.benchmarkVolatility.append(self.calculateVolatility(self.benchmarkReturns))

        # beta
        self.beta.append(self.calculateBeta())

        # downside risk
        self.downsideRisk.append(self.calculateDownsideRisk())

        # alpha
        self.alpha.append(self.calculateAlpha())

        # information ratio
        self.informationRatio.append(self.calculateInformation())

        # sortino ratio
        self.sortinoRatio.append(self.calculateSortino())

        # sharp ratio
        self.sharpeRatio.append(self.calculateSharpe())
    '''

    def update(self, dataEvent, context):
        self.period.update(dataEvent, context)
        # first day
        if self.lastdt is None:
            self.lastdt = dataEvent.time()
            self.nextdt = self.getNextDate()
            self.initialize()
            return

        if self.nextdt <= dataEvent.time():
            # update period return
            self.period.calculateReturn()

            # update all returns
            self.returnTracker.update(self.period)

            # rollover
            self.period.rollover()
            self.nextdt = self.getNextDate()

            
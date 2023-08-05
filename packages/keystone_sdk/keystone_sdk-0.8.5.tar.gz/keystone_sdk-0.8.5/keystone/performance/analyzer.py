# -*- coding: utf-8 -*-

from six import with_metaclass
import abc
import sys
import numpy as np
import math
from datetime import datetime, timedelta
from copy import copy

from keystone.performance import risk
from keystone.performance.sample_rate import KSSampleRate
from keystone.riskless import Riskless
from keystone.utils import numpy_utils


class KSAnalyzer(with_metaclass(abc.ABCMeta)):

    '''
    Abstract class of analyzer.

    Class properties:
    returnTracker: ReturnTracker instance, shared by all analyzer
    '''
    returnTracker = None

    def getAnnulizedMultiplier(self, squared=True):
        return KSSampleRate.getAnnulizedMultiplier(squared=squared)

    def update(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def value(self, *args, **kwargs):
        pass


class KSReturn(KSAnalyzer):

    @property
    def value(self, *args, **kwargs):
        if self.returnTracker is None or len(self.returnTracker.algoCumulativeReturns) <= 1:
            return 0.0
        return self.returnTracker.algoCumulativeReturns[-1]


class KSBenchmarkReturn(KSAnalyzer):

    @property
    def value(self, *args, **kwargs):
        if self.returnTracker is None or len(self.returnTracker.benchmarkCumulativeReturns) <= 1:
            return 0.0
        return self.returnTracker.benchmarkCumulativeReturns[-1]


class KSVolatility(KSAnalyzer):

    def __init__(self):
        self.std = numpy_utils.nanstd(ddof=1)

    @property
    def value(self, *args, **kwargs):
        return self.std.value * self.getAnnulizedMultiplier(squared=True)

    def update(self, *args, **kwargs):
        if self.returnTracker is not None and len(self.returnTracker.algoReturns) > 0:
            self.std.update(self.returnTracker.algoReturns[-1])


class KSBeta(KSAnalyzer):

    """
    http://en.wikipedia.org/wiki/Beta_(finance)
    """

    def __init__(self):
        self.cov = numpy_utils.nancov(ddof=1)

    @property
    def value(self, *args, **kwargs):
        algorithm_covariance = self.cov.value[0, 1]
        benchmark_variance = self.cov.value[1, 1]
        return algorithm_covariance / benchmark_variance

    def update(self, *args, **kwargs):
        if self.returnTracker is not None and len(self.returnTracker.algoReturns) > 0:
            self.cov.update(
                self.returnTracker.algoReturns[-1], self.returnTracker.benchmarkReturns[-1])


class KSDownsideRisk(KSAnalyzer):

    """
    https://en.wikipedia.org/wiki/Downside_risk
    """

    def __init__(self):
        self.std = numpy_utils.nanstd(ddof=1)

    @property
    def value(self, *args, **kwargs):
        return self.std.value * self.getAnnulizedMultiplier(squared=True)

    def update(self, *args, **kwargs):
        if self.returnTracker is not None and len(self.returnTracker.algoReturns) > 0:
            rets = np.round(self.returnTracker.algoReturns[-1], 8)
            mar = np.round(self.returnTracker.algoMeanReturns[-1], 8)
            if rets < mar:
                self.std.update(rets - mar)

class KSAlpha(KSAnalyzer):

    """
    http://en.wikipedia.org/wiki/Alpha_(investment)
    """

    def __init__(self):
        self.beta = KSBeta()

    @property
    def value(self, *args, **kwargs):
        if self.returnTracker is None or len(self.returnTracker.algoReturns) < 1:
            return np.nan
        return risk.alpha(
            self.returnTracker.algoAnnulizedMeanReturns[-1],
            Riskless.value,
            self.returnTracker.benchmarkAnnulizedMeanReturns[-1],
            self.beta.value)

    def update(self, *args, **kwargs):
        self.beta.update(args, kwargs)

class KSInformationRatio(KSAnalyzer):
    """
    http://en.wikipedia.org/wiki/Information_ratio
    """

    def __init__(self):
        self.volatility = KSVolatility()

    @property
    def value(self, *args, **kwargs):
        if self.returnTracker is None or len(self.returnTracker.algoReturns) <= 1:
            return np.nan

        return risk.information_ratio(
            self.returnTracker.algoAnnulizedMeanReturns[-1],
            self.returnTracker.benchmarkAnnulizedMeanReturns[-1],
            self.volatility.value)

    def update(self, *args, **kwargs):
        self.volatility.update(args, kwargs)

class KSSortinoRatio(KSAnalyzer):
    """
    http://en.wikipedia.org/wiki/Sortino_ratio
    """
    def __init__(self):
        self.downsideRisk = KSDownsideRisk()

    @property
    def value(self, *args, **kwargs):
        if self.returnTracker is None or len(self.returnTracker.algoReturns) <= 1:
            return np.nan

        return risk.sortino_ratio(
            self.returnTracker.algoAnnulizedMeanReturns[-1],
            Riskless.value,
            self.downsideRisk.value)

    def update(self, *args, **kwargs):
        self.downsideRisk.update(args, kwargs)


class KSSharpRatio(KSAnalyzer):
    """
    http://en.wikipedia.org/wiki/Sharpe_ratio
    """
    def __init__(self):
        self.volatility = KSVolatility()

    @property
    def value(self, *args, **kwargs):
        if self.returnTracker is None or len(self.returnTracker.algoReturns) <= 1:
            return np.nan

        return risk.sharpe_ratio(
            self.returnTracker.algoAnnulizedMeanReturns[-1],
            Riskless.value,
            self.volatility.value)

    def update(self, *args, **kwargs):
        self.volatility.update(args, kwargs)

class KSMaxDrawdown(KSAnalyzer):

    def __init__(self):
        KSAnalyzer.__init__(self)
        self.currentMaxReturn = -np.inf
        self.currentDrawdown = -np.inf

    @property
    def value(self, *args, **kwargs):
        if self.returnTracker is None or len(self.returnTracker.algoCumulativeReturns) == 0:
            return 0.0

        self.currentMaxReturn = np.nanmax(
            (self.currentMaxReturn, self.returnTracker.algoCumulativeReturns[-1]))
        # The drawdown is defined as: (high - low) / high
        # The above factors out to: 1.0 - (low / high)
        drawdown = 1.0 - \
            (1.0 +
             self.returnTracker.algoCumulativeReturns[-1]) / (1.0 + self.currentMaxReturn)
        if self.currentDrawdown < drawdown:
            self.currentDrawdown = drawdown

        return self.currentDrawdown


class KSDefaultAnalyzer(KSAnalyzer):

    def __init__(self):
        KSAnalyzer.__init__(self)
        self.benchmark = KSBenchmarkReturn()
        self.returns = KSReturn()
        self.alpha = KSAlpha()
        self.beta = KSBeta()
        self.volatility = KSVolatility()
        self.maxDrawdown = KSMaxDrawdown()
        self.downsideRisk = KSDownsideRisk()
        self.sharpeRatio = KSSharpRatio()
        self.sortinoRatio = KSSortinoRatio()
        self.informationRatio = KSInformationRatio()

    def update(self, *args, **kwargs):
        self.alpha.update(args, kwargs)
        self.beta.update(args, kwargs)
        self.volatility.update(args, kwargs)
        self.downsideRisk.update(args, kwargs)
        self.sharpeRatio.update(args, kwargs)
        self.sortinoRatio.update(args, kwargs)
        self.informationRatio.update(args, kwargs)

    def value(self, *args, **kwargs):
        ret = {
            'return': self.returns.value,
            'benchmark': self.benchmark.value,
            'alpha': self.alpha.value,
            'beta': self.beta.value,
            'volatility': self.volatility.value,
            'max_drawdown': self.maxDrawdown.value,
            'downside_risk': self.downsideRisk.value,
            'sharpe_ratio': self.sharpeRatio.value,
            'sortino_ratio': self.sortinoRatio.value,
            'information_ratio': self.informationRatio.value
        }
        return ret


class KSCumulativeAnalyzer(KSAnalyzer):

    def __init__(self):
        self.returns = []
        self.benchmark = []
        self.alpha = []
        self.beta = []
        self.volatility = []
        self.max_drawdown = []
        self.downside_risk = []
        self.sharpe_ratio = []
        self.sortino_ratio = []
        self.information_ratio = []

        self.count = 0
        self.defaultAnalyzer = KSDefaultAnalyzer()

    def value(self, *args, **kwargs):
        fields = copy(self.__dict__)
        return fields

    def update(self, *args, **kwargs):
        self.count += 1
        if self.count > 2:
            self.returns.append(self.defaultAnalyzer.returns.value)
            self.benchmark.append(self.defaultAnalyzer.benchmark.value)
            self.alpha.append(self.defaultAnalyzer.alpha.value)
            self.beta.append(self.defaultAnalyzer.beta.value)
            self.volatility.append(self.defaultAnalyzer.volatility.value)
            self.max_drawdown.append(self.defaultAnalyzer.maxDrawdown.value)
            self.downside_risk.append(
                self.defaultAnalyzer.downsideRisk.value)
            self.sharpe_ratio.append(self.defaultAnalyzer.sharpeRatio.value)
            self.sortino_ratio.append(
                self.defaultAnalyzer.sortinoRatio.value)
            self.information_ratio.append(
                self.defaultAnalyzer.informationRatio.value)

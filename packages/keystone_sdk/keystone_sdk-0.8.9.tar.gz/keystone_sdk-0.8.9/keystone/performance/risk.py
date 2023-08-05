# -*- coding: utf-8 -*-

import math
import numpy as np
from keystone.utils.math_utils import tolerant_equals

############################
# Risk Metric Calculations #
############################


def sharpe_ratio(algorithm_return, treasury_return, algorithm_volatility):
    """
    http://en.wikipedia.org/wiki/Sharpe_ratio
    Args:
        algorithm_volatility (float): Algorithm volatility.
        algorithm_return (float): Algorithm return percentage.
        treasury_return (float): Treasury return percentage.
    Returns:
        float. The Sharpe ratio.
    """
    if tolerant_equals(algorithm_volatility, 0):
        return np.nan

    return (algorithm_return - treasury_return) / algorithm_volatility


def downside_risk(algorithm_returns, mean_returns, normalization_factor):
    rets = np.round(algorithm_returns, 8)
    mar = np.round(mean_returns, 8)
    mask = rets < mar
    downside_diff = rets[mask] - mar[mask]
    if len(downside_diff) <= 1:
        return 0.0
    return np.nanstd(downside_diff, ddof=1) * math.sqrt(normalization_factor)


def sortino_ratio(algorithm_return, treasury_return, mar):
    """
    http://en.wikipedia.org/wiki/Sortino_ratio
    Args:
        algorithm_returns (np.array-like):
            Returns from algorithm lifetime.
        algorithm_period_return (float):
            Algorithm return percentage from latest period.
        mar (float): Minimum acceptable return.
    Returns:
        float. The Sortino ratio.
    """
    if tolerant_equals(mar, 0):
        return np.nan

    return (algorithm_return - treasury_return) / mar


def information_ratio(algorithm_return, benchmark_return, algo_volatility):
    """
    http://en.wikipedia.org/wiki/Information_ratio
    Args:
        algorithm_returns (np.array-like):
            All returns during algorithm lifetime.
        benchmark_returns (np.array-like):
            All benchmark returns during algo lifetime.
    Returns:
        float. Information ratio.
    """
    if tolerant_equals(algo_volatility, 0):
        return np.nan

    # The square of the annualization factor is in the volatility,
    # because the volatility is also annualized,
    # i.e. the sqrt(annual factor) is in the volatility's numerator.
    # So to have the the correct annualization factor for the
    # Sharpe value's numerator, which should be the sqrt(annual factor).
    # The square of the sqrt of the annual factor, i.e. the annual factor
    # itself, is needed in the numerator to factor out the division by
    # its square root.
    return (algorithm_return - benchmark_return) / algo_volatility


def alpha(algorithm_returns, treasury_return,
          benchmark_returns, beta):
    """
    http://en.wikipedia.org/wiki/Alpha_(investment)
    Args:
        algorithm_period_return (float):
            Return percentage from algorithm period.
        treasury_period_return (float):
            Return percentage for treasury period.
        benchmark_period_return (float):
            Return percentage for benchmark period.
        beta (float):
            beta value for the same period as all other values
    Returns:
        float. The alpha of the algorithm.
    """
    return algorithm_returns - \
        (treasury_return + beta *
         (benchmark_returns - treasury_return))

def beta(algorithm_returns, benchmark_returns):
    """
    .. math::
        \\beta_a = \\frac{\mathrm{Cov}(r_a,r_p)}{\mathrm{Var}(r_p)}
    http://en.wikipedia.org/wiki/Beta_(finance)
    """
    # it doesn't make much sense to calculate beta for less than two
    # values, so return none.
    if len(algorithm_returns) < 2:
        return 0.0

    returns_matrix = np.vstack([algorithm_returns,
                                benchmark_returns]).T
    returns_matrix = returns_matrix[~np.isnan(returns_matrix).any(axis=1)].T
    if returns_matrix.shape[1] < 2:
        return 0.0

    C = np.cov(returns_matrix, ddof=1)
    algorithm_covariance = C[0][1]
    benchmark_variance = C[1][1]
    beta = algorithm_covariance / benchmark_variance

    return beta
###########################
# End Risk Metric Section #
###########################
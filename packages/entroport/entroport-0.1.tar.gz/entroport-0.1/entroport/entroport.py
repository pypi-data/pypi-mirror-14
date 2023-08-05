from __future__ import division, absolute_import
from scipy.optimize import minimize
import pandas as pd
import numpy as np
import statsmodels.api as sm

from entroport.utils import window
from entroport.utils import arrmap 

MAX_OPT_ATTEMPTS = 10

def _kernel(theta, R):
    """ theta : [N,] ndarray, R : [T, N] ndarray
    """
    return np.exp(np.sum(theta * R, axis=1))

def _goalfun(theta, *args):
    R = args[0]
    comm = _kernel(theta, R)
    fun = np.sum(comm)
    grad = np.sum(comm * R.T, axis=1)

    return fun, grad

def _get_thetas(R, pcached_startval):
    Nassets = R.shape[1]
    success = False
    i = 0
    # Quirky but works, if the solver failed, some numerical 
    # imprecision caused some tolerance level not to be met, increasing 
    # iterations, etc. won't remedy this. Restart and try again.
    # The alernative would be a convex solver that is "guaranteed" to hit 
    # the global minimim, but this is much slower (tried with `cvxpy`).
    # With this setup 'BFGS' is fast and performs well
    while not success and i < MAX_OPT_ATTEMPTS:
        optres = minimize(fun=_goalfun,
                          x0=pcached_startval,
                          args=R,
                          jac=True,
                          method='BFGS')
        success = optres.success
        # if this run was unsuccessful reset the start values
        pcached_startval[:] = np.random.rand(Nassets)
        i += 1

    if not success:
        raise RuntimeError("fmin failed", optres.message)

    theta = optres.x
    pcached_startval[:] = theta # Cleaner way to do this?

    return theta

def _get_weights(R, theta):
    sdf_is = _kernel(theta, R)
    reg = sm.OLS(sdf_is, sm.add_constant(R)).fit()
    weights = reg.params[1:]
    weights /= np.sum(weights)

    return weights

class EntroPort(object):
    """ Portfolio allocation with relative entropy minimization

    Estimates portfolio weights on a rolling out of sample basis by projecting
    past returns on an estimated stochastic discount factor. 

    Parameters
    ----------
    df : DataFrame
        Portfolio time series, net log (excess) returns

    estlength : int
        Length of the moving estimation window

    step : int 
        The number of observations in the out of sample
        estimation window (default is 1) - a step size of for ex. 10 would 
        be the same as a 10 period rebalancing.

    Attributes
    ----------
    theta_ : DataFrame
        Estimated thetas
    
    weights_ : DataFrame
        Estimated weights
    
    pfs_ : DataFrame
        The time series of the estimated stochastic discount factor and
        'information portfolio'

    References
    ----------
    .. [1] A One Factor Benchmark Model for Asset Pricing' by
    Ghosh, Julliard, and Taylor (2015 wp)
    """

    def __init__(self, df, estlength, step=1):
        self.df = df
        self.estlength = estlength
        self.step = step

        self.Nobs = df.shape[0]
        assert step < estlength < self.Nobs
        self.estidx = list(window(range(self.Nobs), estlength, step))
        self.oosidx = map(lambda x: range(x[-1] + 1, x[-1] + 1 + step),
                          self.estidx)

        # Taking care of the last estimation and out of sample indices
        self.oosidx[-1] = list(set(self.oosidx[-1]).intersection(range(self.Nobs)))
        if not self.oosidx[-1]:
            self.oosidx.pop()
            self.estidx.pop()
        
        self._pcached_startval = np.random.rand(df.shape[1])

    def _fit_one_period(self, idx):
        estwindow = self.estidx[idx]
        ooswindow = self.oosidx[idx]

        R = self.df.iloc[estwindow].values

        theta = _get_thetas(R, self._pcached_startval)
        weights = _get_weights(R, theta)

        # b/c not necessarily equal to `self.step` in the last period
        reps = len(ooswindow) 

        return np.tile(theta, (reps, 1)), np.tile(weights, (reps, 1))

    def fit(self):
        theta, weights = arrmap(self._fit_one_period, range(len(self.estidx)))
        
        index = self.df.index[self.oosidx[0][0]:self.Nobs]
        colnames = self.df.columns.tolist()

        self.thetas_ = pd.DataFrame(theta, index=index, columns=colnames)
        self.weights_ = pd.DataFrame(weights, index=index, columns=colnames)

        sdf = map(lambda theta, R: _kernel(theta, R[None, :])[0],
                  theta, self.df.loc[index].values)
        ip = (weights * self.df.loc[index]).sum(axis=1)

        self.pfs_ = pd.DataFrame({'sdf': sdf, 'ip': ip})

        return self


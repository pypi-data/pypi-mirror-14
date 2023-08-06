
import cvxpy as cp
import numpy as np
import epopt as ep
import scipy.sparse as sp

def create(m, n):
    np.random.seed(0)
    X = np.random.randn(m,n);
    X = X*sp.diags([1 / np.sqrt(np.sum(X**2, 0))], [0])
    y = X.dot(10*np.random.randn(n))

    k = max(m/50, 1)
    idx = np.random.randint(0, m, k)
    y[idx] += 100*np.random.randn(k)

    D = ep.sqdist(X, X)
    sigma = np.median(D)
    K = np.exp(-0.5*D/sigma**2)

    lam = 1
    alpha = cp.Variable(m)
    f = cp.norm1(K*alpha - y) + lam*cp.quad_form(alpha, K)
    return cp.Problem(cp.Minimize(f))

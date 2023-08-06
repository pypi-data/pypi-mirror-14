#!/usr/bin/env python

import argparse
import logging
import sys
import time

from epopt.problems import *
from epopt.problems.problem_instance import ProblemInstance

PROBLEMS = {
    "liblinear": [
        ProblemInstance("hinge_l1", hinge_l1.create, dict(m=1500, n=5000, rho=0.01)),
        ProblemInstance("hinge_l1_sparse", hinge_l1.create, dict(m=1500, n=50000, rho=0.01, mu=0.1)),
        ProblemInstance("hinge_l2", hinge_l2.create, dict(m=5000, n=1500)),
        ProblemInstance("hinge_l2_sparse", hinge_l2.create, dict(m=10000, n=1500, mu=0.1)),
    ],

    "glmnet": [
        ProblemInstance("lasso", lasso.create, dict(m=1500, n=5000, rho=0.01)),
        ProblemInstance("lasso_sparse", lasso.create, dict(m=1500, n=50000, rho=0.01, mu=0.1)),
        ProblemInstance("logreg_l1", logreg_l1.create, dict(m=1500, n=5000, rho=0.01)),
        ProblemInstance("logreg_l1_sparse", logreg_l1.create, dict(m=1500, n=50000, rho=0.01, mu=0.1)),
    ],

    "gurobi": [
        ProblemInstance("lp", lp.create, dict(m=800, n=1000)),
        ProblemInstance("qp", qp.create, dict(n=1000)),
    ],

    "quic": [
        ProblemInstance("covsel", covsel.create, dict(m=100, n=200, lam=0.1)),
    ],
}

def run_benchmarks():
    for method, problems in PROBLEMS.iteritems():
        for problem in problems:
            t0 = time.time()
            cvxpy_prob = problem.create()
            t1 = time.time()
            logging.debug("creation time %f seconds", t1-t0)

            print method, problem.name


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    run_benchmarks()

else:
    args = argparse.Namespace()

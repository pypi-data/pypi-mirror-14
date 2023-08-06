"""Benchmark against liblinear problem instances.

Run with:

PYTHONPATH=$HOME/liblinear/python python -m epopt.problems.benchmark_liblinear
"""

import argparse
import logging
import time

import liblinear
import liblinearutil
import numpy as np
import scipy.sparse as sp

from epopt.problems import hinge_l1
from epopt.problems import hinge_l2
from epopt.problems import problem_util

from epopt.problems.problem_instance import ProblemInstance

PROBLEMS = [
    ("-q -s 5", ProblemInstance("hinge_l1", hinge_l1.create, dict(m=1500, n=5000, rho=0.01))),
    ("-q -s 5", ProblemInstance("hinge_l1_sparse", hinge_l1.create, dict(m=1500, n=50000, rho=0.01, mu=0.1))),
    ("-q -s 1", ProblemInstance("hinge_l2", hinge_l2.create, dict(m=5000, n=1500))),
    ("-q -s 1", ProblemInstance("hinge_l2_sparse", hinge_l2.create, dict(m=10000, n=1500, mu=0.1)))
]

def convert_data(A):
    if isinstance(A, np.ndarray):
        logging.debug("converting dense matrix")
        return A.tolist()

    if sp.issparse(A):
        logging.debug("converting sparse matrix")
        A = sp.coo_matrix(A)
        data = [{}]*A.shape[0]
        for i, j, v in zip(A.row, A.col, A.data):
            data[i][j] = v
        return data

    raise ValueError("unknown data type " + repr(A))

def benchmark_liblinear(param_str, problem):
    np.random.seed(0)

    logging.debug("creating problem")
    A, b = problem_util.create_classification(**problem.kwargs)

    logging.debug("converting to liblinear input")
    prob = liblinear.problem(b, convert_data(A))
    param = liblinear.parameter(param_str)

    t0 = time.time()
    model = liblinearutil.train(prob, param)
    t1 = time.time()

    print problem.name, t1 - t0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    for param_str, problem in PROBLEMS:
        benchmark_liblinear(param_str, problem)

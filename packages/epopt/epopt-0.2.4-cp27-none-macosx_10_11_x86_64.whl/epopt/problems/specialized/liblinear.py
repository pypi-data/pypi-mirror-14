"""Benchmark against liblinear problem instances."""

import time

from epopt.problems import hinge_l1
from epopt.problems import hinge_l2

from epopt.problems.problem_instance import ProblemInstance

PROBLEMS = [
    ProblemInstance("hinge_l1", hinge_l1.create, dict(m=1500, n=5000, rho=0.01)),
    # ProblemInstance("hinge_l1_sparse", hinge_l1.create, dict(m=1500, n=50000, rho=0.01, mu=0.1)),
    # ProblemInstance("hinge_l2", hinge_l2.create, dict(m=5000, n=1500)),
    # ProblemInstance("hinge_l2_sparse", hinge_l2.create, dict(m=10000, n=1500, mu=0.1)),
]


if __name__ == "__main__":
    for problem in PROBLEMS:
        cvxpy_prob = problem.create()
        benchmark_liblinear(cvxpy_prob)

# This file provides an example problem for testing the DOT wrapper provided
# in dot.py.  The example problem contained in this file is the first
# example problem from the dot.pdf manual.
#
# Created by:
# Gerhard Venter
# August 21, 2019
#
# Modified by:
# CamelCMA
# February 27, 2020
#------------------------------------------------------------------------------
from dot import Dot
import numpy as np
import math

#------------------------------------------------------------------------------
# Define your own function to evaluate the objective function and constraints
# This function can be name anything, but the arguments must be as shown below.
#
# Input:  x     - The current design variable vector obtained from DOT to
#               evaluate.  This is a numpy array of length nDvar.
#         obj   - The objective function value that will be evaluated and set
#               here.
#         g     - The constraint vector that will be evaluated and set here.
#               This is a numpy array of length nCon.
#         param - An optional numpy array with parameter values that the user
#               can specify when setting up the DOT parameters.  These
#               optional parameters will be passed to this evaluate function
#               unchanged by DOT.
# Return: Nothing
#------------------------------------------------------------------------------


def myEvaluate(x, obj, g, param):

    # Optional step to map the design variable array to local variables that
    # are easier to work with
    h, w, d = x[0], x[1], x[2]

    # Evaluate the objective function value and use the ".value" notation to
    # update this new value in the calling function, which is DOT in this
    # case
    obj.value = 2.0 * (h * w + h * d + 2.0 * w * d) + 1.25 * h / 12.0

    # Evaluate the constraints and update the constraint vector.  Since this
    # is a numpy object, the values will be updated in the calling function
    g[0] = 1.0 - h * w * d / 2.


nDvar = 3  # Number of design variables
nCons = 1  # Number of constraints

# Set the initial values and upper and lower bounds for the design variables
x = np.ones(nDvar, float) * 1.0
xl = np.ones(nDvar, float) * 0.001
xu = np.ones(nDvar, float) * 100.00

# Append different DOT instances into a list
models = []
models.append(Dot(nMethod=1, nPrint=3))
models.append(Dot(nMethod=2, nPrint=3))
models.append(Dot(nMethod=3, nPrint=3))

for model in models:
    # model.print_init()
    model.fit(x=x, xl=xl, xu=xu, nCons=nCons, evalfunc=myEvaluate)
    model.print_info()

for model in models:
    model.plot_fig(is_savefig=True)

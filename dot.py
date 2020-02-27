# Wrapper to call DOT from Python
#
# Will work on both Linux and Windows platforms.  There
# should not be any need to change this file.
# ---------------------------------------------------------
import platform
import numpy as np
import ctypes as ct
import math
from ctypes import byref as B
import matplotlib.pyplot as plt


class Dot:
    """
    Define the Python wrapper to the DOT shared library as a Python class
    """

    # Initialize the class - this loads the DOT shared library
    # according to the platform detected at run time
    def __init__(self, *, nInfo=0, nMethod=0, nPrint=0, nMinMax=0, nMaxInt=20000000, nmParam=np.empty(1, float),
                 nmRPRM=np.zeros(20, float), nmIPRM=np.zeros(20, int)):

        self.systemName = platform.system()

        # Load the shared library on Linux
        if (self.systemName == 'Linux'):
            self.dotlib = ct.cdll.LoadLibrary("libDOT2.so")

        # Load the shared library on Windows
        elif (self.systemName == 'Windows'):
            self.dotlib = ct.windll.LoadLibrary("DOT.dll")

        # Else throw an exception to indicate that no supported
        # platform was found
        else:
            raise ValueError(
                'Unsupported Operating System: ' + self.systemName)

        self.nInfo = nInfo
        self.nMethod = nMethod
        self.nPrint = nPrint
        self.nMinMax = nMinMax
        self.nMaxInt = nMaxInt
        self.nmParam = nmParam
        self.nmRPRM = nmRPRM
        self.nmIPRM = nmIPRM

    def print_init(self):
        print(
            f'self.nInfo = {self.nInfo}, type = {type(self.nInfo)}')
        print(
            f'self.nMethod = {self.nMethod}, type = {type(self.nMethod)}')
        print(
            f'self.nPrint = {self.nPrint}, type = {type(self.nPrint)}')
        print(
            f'self.nMinMax = {self.nMinMax}, type = {type(self.nMinMax)}')
        print(
            f'self.nMaxInt = {self.nMaxInt}, type = {type(self.nMaxInt)}')
        print(
            f'self.nmParam = {self.nmParam}, type = {type(self.nmParam)}')
        print(
            f'self.nmRPRM = {self.nmRPRM}, type = {type(self.nmRPRM)}')
        print(
            f'self.nmIPRM = {self.nmIPRM}, type = {type(self.nmIPRM)}')

    # Allocate memory by DOT510
    def alloc_mem(self, x, xl, xu, nCons, evalfunc):
        # Init
        self.x = x
        self.xl = xl
        self.xu = xu
        self.nCons = nCons
        self.evalfunc = evalfunc

        # Initailize all array types
        self.nDvar = self.x.shape[0]
        self.ctDVAR = ct.c_double * self.nDvar
        self.ctCONS = ct.c_double * self.nCons
        self.ctRPRM = ct.c_double * 20
        self.ctIPRM = ct.c_int * 20

        # Initialize all arrays
        self.RPRM = self.ctRPRM(*(self.nmRPRM))  # Tells dot to use defaults
        self.IPRM = self.ctIPRM(*(self.nmIPRM))  # Tells dot to use defaults
        self.X = self.ctDVAR(*(self.x))  # Initial values
        self.XL = self.ctDVAR(*(self.xl))  # Lower bounds
        self.XU = self.ctDVAR(*(self.xu))  # Upper bounds
        self.G = self.ctCONS(*([0.0] * self.nCons))  # Constraints

        # Initialize constants
        self.METHOD = ct.c_int(self.nMethod)
        self.NDV = ct.c_int(self.nDvar)
        self.NCON = ct.c_int(self.nCons)
        self.IPRINT = ct.c_int(self.nPrint)
        self.MINMAX = ct.c_int(self.nMinMax)
        self.INFO = ct.c_int(self.nInfo)
        self.OBJ = ct.c_double(0.0)
        self.MAXINT = ct.c_int(self.nMaxInt)

        # Call DOT510 to determine memory requirements for DOT and allocate the memory
        # in the work arrays
        self.NRWK = ct.c_int()
        self.NRWKMN = ct.c_int()
        self.NRIWD = ct.c_int()
        self.NRWKMX = ct.c_int()
        self.NRIWK = ct.c_int()
        self.NSTORE = ct.c_int()
        self.NGMAX = ct.c_int()
        self.IERR = ct.c_int()

        if (self.systemName == 'Linux'):
            self.dotlib.dot510_(B(self.NDV), B(self.NCON), B(self.METHOD), B(self.NRWK), B(self.NRWKMN), B(self.NRIWD), B(
                self.NRWKMX), B(self.NRIWK), B(self.NSTORE), B(self.NGMAX), B(self.XL), B(self.XU), B(self.MAXINT), B(self.IERR))
        elif (self.systemName == 'Windows'):
            self.dotlib.DOT510(B(self.NDV), B(self.NCON), B(self.METHOD), B(self.NRWK), B(self.NRWKMN), B(self.NRIWD), B(
                self.NRWKMX), B(self.NRIWK), B(self.NSTORE), B(self.NGMAX), B(self.XL), B(self.XU), B(self.MAXINT), B(self.IERR))

        self.ctRWK = ct.c_double * self.NRWKMX.value
        self.ctIWK = ct.c_int * self.NRIWK.value
        self.IWK = self.ctIWK(*([0] * self.NRIWK.value))
        self.WK = self.ctRWK(*([0.0] * self.NRWKMX.value))

    # Call DOT itself
    def fit(self, *, x, xl, xu, nCons, evalfunc):

        self.alloc_mem(x, xl, xu, nCons, evalfunc)

        self.OBJ_value_list,  self.Max_G_list, self.X_list, self.count = [], [], [], 0

        while (True):
            if (self.systemName == 'Linux'):
                self.dotlib.dot_(B(self.INFO), B(self.METHOD), B(self.IPRINT), B(self.NDV),  B(self.NCON), B(self.X), B(self.XL), B(
                    self.XU), B(self.OBJ), B(self.MINMAX), B(self.G), B(self.RPRM), B(self.IPRM), B(self.WK), B(self.NRWKMX), B(self.IWK), B(self.NRIWK))
            elif (self.systemName == 'Windows'):
                self.dotlib.DOT(B(self.INFO), B(self.METHOD), B(self.IPRINT), B(self.NDV),  B(self.NCON), B(self.X), B(self.XL), B(
                    self.XU), B(self.OBJ), B(self.MINMAX), B(self.G), B(self.RPRM), B(self.IPRM), B(self.WK), B(self.NRWKMX), B(self.IWK), B(self.NRIWK))

            if (self.INFO.value == 0):
                break
            else:
                self.evalfunc(self.X, self.OBJ, self.G, self.nmParam)
                self.OBJ_value_list.append(self.OBJ.value)

                if self.nCons != 0:
                    self.Max_G_list.append(max(self.G))

                self.X_list.append(list(self.X))
                self.count += 1

        self.X_array = np.array(self.X_list)

        return self.OBJ_value_list, self.Max_G_list, self.X_list, self.X_array, self.count

    def print_info(self):

        print(
            f'-----nMinMax = {self.nMinMax} , nMethod = {self.nMethod}-----')
        print(f'Function calls = {self.count}')
        print(f'Initial Objective Function = {self.OBJ_value_list[0]:1.5e}')
        print(
            f'Optimum Objective function = {self.OBJ.value:1.5e}')

        if self.Max_G_list:
            print(f'Initial MAX G = {self.Max_G_list[0]:1.5e}')
            print(f'Optimum MAX G = {max(self.G):1.5e}')
        else:
            print('Unconstrained Problem(nCons=0)')

        print('Initial X')
        for i in range(self.nDvar):
            print(f'X[{i}] = {self.X_list[0][i]:1.5e}')

        print('Optimum X')
        for i in range(self.nDvar):
            print(f'X[{i}] = {self.X[i]:1.5e}')

        print('--------------E N D-----------------', end='\n\n')

    def plot_fig(self, is_savefig=False, dpi=150):

        self.is_savefig = is_savefig
        self.dpi = dpi

        plt.style.use('seaborn')
        fig, ax = plt.subplots(2, 2)
        fig.suptitle(
            f'nMinMax = {self.nMinMax} , nMethod = {self.nMethod}', fontsize=12)
        fig.text(0.5, 0.04, 'Function calls',
                 ha='center', va='center', fontsize=12)
        fig.text(0.04, 0.5, 'Value', ha='center',
                 va='center', fontsize=12, rotation=90)

        ax[0, 0].plot(range(1, self.count + 1), self.OBJ_value_list)
        ax[0, 0].set(title='OBJ', xlim=[1, self.count])

        ax[0, 1].plot(range(1, self.count + 1), self.Max_G_list)
        ax[0, 1].set(title='Max G', xlim=[1, self.count])

        gs = ax[1, 0].get_gridspec()
        for ax_x in ax[1, :]:
            ax_x.remove()
        ax_X = fig.add_subplot(gs[1, :])

        self.Xname = []
        for i in range(self.X_array.shape[1]):
            self.Xname.append(f'X{i+1}')
            ax_X.plot(range(1, self.count + 1), self.X_array[:, i])

        ax_X.legend(self.Xname, loc=0)
        ax_X.set(title='X', xlim=[1, self.count])
        plt.show()

        if self.is_savefig:
            fig.savefig(
                f'nMinMax_{self.nMinMax}_nMethod_{self.nMethod}', dpi=self.dpi)

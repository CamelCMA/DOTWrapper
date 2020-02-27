# About
This repository is forked from [MODRG/DOTWrapper](https://github.com/MODRG/DOTWrapper), created by Prof Gerhard Venter on 21 August 2019. The user is recommended to go through its README file first.

# Requirements
- The DOT optimizer itself (commercially available form [VR&D](https://www.vrand.com)). A Python wrapper for DOT is provided that will allow the user to call the DOT shared library from Python. **It should be noted DOT is a commercial optimizer, a license is required to use it.**
- [NumPy](http://www.numpy.org/) & [Matplotlib ](https://matplotlib.org/) Python library

# File description
| File        | Description  |
| ------------- |-------------|
| [dot.py](https://github.com/CamelCMA/DOTWrapper/blob/master/dot.py)  | The Python wrapper for DOT |
| [dot.pdf](https://github.com/CamelCMA/DOTWrapper/blob/master/dot.pdf) | The DOT manual |
| [sec4_2_BoxDesign.py](https://github.com/CamelCMA/DOTWrapper/blob/master/sec4_2_BoxDesign.py) | The first example problem from the DOT manual, using the provided wrapper |

### Figure for model 1
![nMinMax_0_nMethod_1](https://github.com/CamelCMA/DOTWrapper/blob/master/nMinMax_0_nMethod_1.png)

### Figure for model 2
![nMinMax_0_nMethod_2](https://github.com/CamelCMA/DOTWrapper/blob/master/nMinMax_0_nMethod_2.png)

### Figure for model 3
![nMinMax_0_nMethod_3](https://github.com/CamelCMA/DOTWrapper/blob/master/nMinMax_0_nMethod_3.png)

# Modification
Reconstruct the dot.py file and implement the following methods to call:
* `print_init` can be used to check the input parameters.
* `fit` calls DOT to resolve the problem.
* `print_info` prints the following values to screen.
    * Objective function value
    * Max violated constraint value
    * Design variable values
* `plot_fig` plots the following values as figures. A flag `is_savefig=True` can be used to save the figures and a flag `dpi` can be used to set the resolution of the figures.
    * Objective function value
    * Max violated constraint value
    * Design variable values

# Problem-defined steps
4 steps to complete the setting for a optimization problem:
1. Define the problem in `myEvaluate` function.
2. Define `nDvar` & `nCons` as integer.
3. Define `x`, `xl`, `xu` as numpy ndarray.
4. Configure the model(s) with corresponding method(s) to call.

_Typically, the user is recommended to explore the solution by setting different nMethod value. Sometimes, interesting outcomes could be observed._

# Acknowledgement
* Thanks for Prof Gerhard Venter constructing the original dot.py file.
* Thanks for [VR&D](https://www.vrand.com/) sponsoring the trial license of DOT.

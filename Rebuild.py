'''
XOR problem:
    - Two inputs
    - Each input can either be a 0 or a 1
    - If the two inputs are identical, output must be 0. i.e. if inputs are 1 and 1, output is expected to be 0
    - If the two inputs are different, output must be 1. i.e. if inputs are 0 and 1, output is expected to be 1
'''

import random as rnd
import numpy as np
import copy

from Brain_class import Brain


#Determines population size at start.
pop_size = 50

#Number of input neurons
input_N = 2 #A bias neuron will be automatically added to the input neurons.

output_N = 1 #Number of output neurons 

hidden_N = 1 #Number of hidden neurons at start (This is likely to change as generations go by)

percent_conn = 1 #number of initial activated connections 

import os 
import torch
import torch.nn as nn
import torch.nn.functional as F

# HYPER PARAMS

N_KERNEL = 128
N_RESIDUAL_BLOCK = 16
STATE_SHAPE = (3, 3, 2) 
N_ACTIONS = 9

class ConvLayer(nn.Module):
    def __init__(self, x):
        super().__init__()
        pass

    def forward(self, x):
        return x

class ResidualBlock(nn.Module):
    def __init__(self, depth):
        super().__init__()
        pass

    def forward(self, x):
        return x
    
class Network(nn.Module):
    def __init__(self, n_residual_block, input_shape, n_actions):
        super().__init__()
        self.n_residual_block = n_residual_block
        self.input_shape = input_shape
        self.n_actions = n_actions

        self.policy_linear = nn.Linear(xxxxx, self.n_actions)
        self.value_linear = nn.Linear(xxxxx, 1)

    def forward(self, x):

        p, v = self.policy_linear(x), self.value_linear(x)

        return p, v
    

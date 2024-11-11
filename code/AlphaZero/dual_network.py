import torch.nn as nn
import torch.nn.functional as F

# HYPER PARAMS

N_KERNEL = 128
N_RESIDUAL_BLOCK = 16
STATE_SHAPE = (3, 3, 2) 
N_ACTIONS = 9

class ConvLayer(nn.Module):
    def __init__(self, n_kernel):
        super().__init__()
        self.conv = nn.Conv2d(2, n_kernel, kernel_size=3, padding=1, bias=False)
        self.bn = nn.BatchNorm2d(n_kernel)

    def forward(self, x):
        x = self.conv(x)
        x = self.bn(x)
        x = F.relu(x)
        return x

class ResidualBlock(nn.Module):
    def __init__(self, n_kernel):
        super().__init__()
        self.conv1 = nn.Conv2d(n_kernel, n_kernel, kernel_size=3, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(n_kernel)
        self.conv2 = nn.Conv2d(n_kernel, n_kernel, kernel_size=3, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(n_kernel)

    def forward(self, x):
        residual = x

        x = self.conv1(x)
        x = self.bn1(x)
        x = F.relu(x) # double check 
        x = self.conv2(x)
        x = self.bn2(x)

        x += residual
        x = F.relu(x)

        return x
    
class Network(nn.Module):
    def __init__(self, n_residual_block, n_kernel, input_shape, n_actions):
        super().__init__()
        self.n_residual_block = n_residual_block
        self.n_kernel = n_kernel
        self.input_shape = input_shape
        self.n_actions = n_actions
        self.n_fc_nodes = 0 # 수정

        self.conv_layer = ConvLayer(self.n_kernel)
        self.residual_blocks = nn.Sequential(*[ResidualBlock(self.n_kernel) for _ in range(self.n_residual_block)])
        self.global_pooling = nn.AdaptiveAvgPool2d(1)

        self.policy_head = nn.Linear(self.n_fc_nodes, self.n_actions)
        self.value_head = nn.Linear(self.n_fc_nodes, 1)
        self.softmax = nn.Softmax(dim=-1)

    def forward(self, x):
        x = self.conv_layer(x)
        x = self.residual_blocks(x)
        x = self.global_pooling(x)
        x = x.view(x.size(0), -1)

        p, v = self.policy_head(x), self.value_head(x)
        p = self.softmax(p)

        return p, v
    

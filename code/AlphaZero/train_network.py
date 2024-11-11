from dual_network import * # Network, N_KERNEL, N_RESIDUAL_BLOCK, STATE_SHAPE, N_ACTIONS

import torch.nn.functional as F
import torch.optim as optim

model = Network()

class TrainNetwork:
    def __init__(self, model, episode_memory, batch_size, learning_rate):
        # define 
        self.model = model
        self.learning_rate = learning_rate
        self.losses = [] # elements : ( p_loss, v_loss )

        # define loss ftn
        self.mse_loss = F.mse_loss()
        self.cross_entropy_loss = F.cross_entropy() 

        # memory
        self.episode_memory = episode_memory
        self.batch_size = batch_size

        # Optimizer & Scheduler
        self.optimizer = optim.Adam(self.model.parameters(), lr=self.learning_rate, eps=1e-4, weight_decay=1e-4) # 체크

        self._train()

    def _train(self):
        sample = self.episode_memory.sample(self.batch_size)
        state, target_policy, target_value = zip(*sample)
        
        # 데이터 차원 맞추기
        # -------------
        # kokokara
        # -------------

        self.model.train()

        policy, value = self.model(state)

        p_loss = self.cross_entropy_loss(value, target_value)
        v_loss = self.mse_loss(policy, target_policy)

        total_loss = p_loss + v_loss

        p_running_loss, v_running_loss = p_loss.item(), v_loss.item()

        self.losses.append((p_running_loss, v_running_loss))

        self.optimizer.zero_grad()
        total_loss.backward()
        self.optimizer.step()
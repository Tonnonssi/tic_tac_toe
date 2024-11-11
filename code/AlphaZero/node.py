from math import sqrt
import numpy as np
import torch

class Node:
    def __init__(self, state, p):
        self.state = state 
        self.p = p # prior prob
        self.n = 0 # n_visit
        self.w = 0 # cum weight 
        self.child_nodes = []

    def evaluate_value(self):
        if self.state.is_done():
            # judge current value 
            value = -1 if self.state.is_lose() else 0 # 패배 혹은 무승부 

            # update 
            self.n += 1
            self.w += value

            return value 
        
        # When child node does not exist.
        if len(self.child_nodes) != 0:
            policies, value = predict(self.state) # by using nn

            # update
            self.n += 1
            self.w += value 

            # expand 
            for policy, action in zip(self.state.available_actions, policies):
                self.child_nodes.append(Node(self.state.next(action), policy))

            return value
        
        # When child node exist
        else:
            value = select_next_child_node(self.state)

            # update
            self.n += 1
            self.w += value 

            return value

def get_n_child(child_nodes):

    child_n = []

    for node in child_nodes:
        child_n.append(node.n)
        
    return child_n
    
def predict(model, state):
    _, row, col = state.shape

    x = torch.tensor(state.board) 
    channel = torch.tensor(np.full([row, col], 1 if state.is_first_player() else 0))
    x = torch.stack([x, channel], axis=0).reshape(1, *state.shape)

    model.eval()

    with torch.no_grad():
        policies, value = model(x)
        policies, value = policies.detach().numpy(), value.detach().numpy()
    
    # take legal policy 
    legal_policy = policies[state.available_actions]
    legal_policy /= sum(legal_policy) if sum(legal_policy) else 1

    return legal_policy, value

def select_next_child_node(state):
    # PUCT 알고리즘을 사용

    C_PUCT = 1.0 # 탐험의 정도 
    total_visit = sum(get_n_child(state.child_nodes))
    values = []

    for node in state.child_nodes:
        node_value = node.w / node.n + C_PUCT * node.p * sqrt(total_visit) / (1 + node.n)
        values.append(node_value)

    return state.child_nodes[np.argmax(values)]
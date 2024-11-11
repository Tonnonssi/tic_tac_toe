from node import *
from dual_network import *

import random 

PV_EVALUATE_COUNT = 1600 

class MCTS:
    def __init__(self, model):
        self.model = model 

    def get_policy(self, state, temp):
        # define root node 
        root_node = Node(state, 0)

        for _ in range(PV_EVALUATE_COUNT):
            root_node.evaluate_value()

        # 
        childs_n = get_n_child(state.child_nodes)

        if temp == 0:
            action = np.argmax(childs_n)
            policy = np.zeros(len(childs_n))
            policy[action] = 1

        else:
            # by Boltzmann
            policy = self.boltzmann_dist(childs_n, temp)

        return policy
    
    def boltzmann_dist(self, x_lst, temp):
        x_lst = [x ** (1/temp) for x in x_lst]
        return [x/sum(x_lst) for x in x_lst]


    def get_action(self, state, temp=0):
        policy = self.get_policy(state, temp)
        action = random.choice(state.legal_actions(), policy)
        return action 
    
    def get_n_child(self, child_nodes):

        child_n = []

        for node in child_nodes:
            child_n.append(node.n)
            
        return child_n

    def select_next_child_node(self, state):
        # PUCT 알고리즘을 사용

        C_PUCT = 1.0 # 탐험의 정도 
        total_visit = sum(get_n_child(state.child_nodes))
        values = []

        for node in state.child_nodes:
            node_value = node.w / node.n + C_PUCT * node.p * sqrt(total_visit) / (1 + node.n)
            values.append(node_value)

        return state.child_nodes[np.argmax(values)]



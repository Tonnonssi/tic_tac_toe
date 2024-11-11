from state import *
from mcts import MCTS

SP_GAME_COUNT = 500
SP_TEMPERATURE = 1.0  # 볼츠만 분포의 온도 파라미터

class SelfPlay:
    def __init__(self, n_games, model, temp):
        self.n_games = n_games
        self.model = model
        self.temp = temp
        self.history = []
        self.mcts = MCTS()

    def get_first_player_value(self, ended_state):
        # 1: 선 수 플레이어 승리, -1: 선 수 플레이어 패배, 0: 무승부
        if ended_state.is_lose():
            return -1 if ended_state.is_first_player() else 1
        return 0

    def single_play(self):
        
        history = []
        final_policy = np.zeros([state.n_action]) # init value 

        state = State()

        while True:
            if state.is_done():
                break

            policy = self.mcts.get_policy(self.model, state, self.temp)

            final_policy[state.available_actions] = policy
            history.append([state.board[0], state.board[1], final_policy, None]) # my board, enemy board, policy, value

            action = np.random.choice(state.available_actions, policy)

            state = state.next(action)

        # end state를 기준으로 값을 업데이트
        value = self.get_first_player_value(state)

        for i in range(history):
            history[i][-1] = value
            value = -value
        
        return history

    def self_play(self):
        for i in range(SP_GAME_COUNT):
            single_history = self.self_play()
            self.history.extend(single_history)

            print(f"self play {i+1} / {SP_GAME_COUNT}")

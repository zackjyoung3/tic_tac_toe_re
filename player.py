import numpy as np
import pickle

# defining the dimensions of the board to be played on
# tic tac toe is played on a 3 rows x 3 column board
num_rows = 3
num_cols = 3


# the player is going to represent the agent
# the agent is able to choose actions based on current estimation of the states, record all of the states of the game,
# update states-value estimation after each game as well as save and load policies
class Player:
    # initialise a dict storing state-value pair and update the estimates at the end of each game
    # note that the default value for exploration ratre is 0.3 => the player will take the greedy
    # action 70% of the time and random, exploratory action 30%
    def __init__(self, name, exp_rate=0.3):
        self.name = name
        # where all the positions that are taken by a player during a game
        self.states = []
        self.lr = 0.2
        self.exp_rate = exp_rate
        self.decay_gamma = 0.9
        # where values for the corresponding states are updated
        self.states_value = {}

    def get_hash(self, board):
        board_hash = str(board.reshape(num_cols * num_rows))
        return board_hash

    # method that will determine what action is to be taken by the agent
    def choose_action(self, positions, current_board, symbol):
        # note that we wish to make a random exploratory move with rate exp_rate
        # thus, we can accomplish this by picking a rand num [0,1) note that np.random.uniform(0, 1) includes lower
        # bound but excludes upper thus cardinality 0 to exp_rate-1 / cardinality 0 to 0.99 = exp_rate
        if np.random.uniform(0, 1) < self.exp_rate:
            # take a random action
            idx = np.random.choice(len(positions))
            action = positions[idx]
        # otherwise take the greedy action
        else:
            value_max = -999
            for p in positions:
                next_board = current_board.copy()
                next_board[p] = symbol
                next_board_hash = self.get_hash(next_board)
                if self.states_value.get(next_board_hash) is None:
                    value = 0
                else:
                    value = self.states_value.get(next_board_hash)
                # store the action that will result in the maximum value of the next state
                if value >= value_max:
                    value_max = value
                    action = p

        return action

    # append a hash state
    def add_state(self, state):
        self.states.append(state)

    # To update the value estimation of the states, apply value iteration
    def feed_reward(self, reward):
        for st in reversed(self.states):
            if self.states_value.get(st) is None:
                self.states_value[st] = 0
            self.states_value[st] += self.lr * (self.decay_gamma * reward - self.states_value[st])
            reward = self.states_value[st]

    # reset the player
    def reset(self):
        self.states = []

    # at the end of training our agent is able to learn its policy that is stored in the states value dict
    # save the policy to enable play against human player
    def save_policy(self, difficulty=''):
        # save to the default location of for the player
        fw = open('policy_' + str(self.name), 'wb')
        # if specified as a difficulty, save the appropriate difficulty as well
        if difficulty != '':
            fw = open(str(difficulty) + '_agent', 'wb')
        pickle.dump(self.states_value, fw)
        fw.close()


    def load_policy(self, file):
        fr = open(file, 'rb')
        self.states_value = pickle.load(fr)
        fr.close()

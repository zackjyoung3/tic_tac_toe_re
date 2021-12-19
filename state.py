import numpy as np
import pickle

# defining the dimensions of the board to be played on
# tic tac toe is played on a 3 rows x 3 column board
num_rows = 3
num_cols = 3


# the state of this game is the board state of both the agent as well as its opponent
class State:
    # method that will initialize a tic tac toe playing board
    def __init__(self, p1, p2):
        # note that the board is initially all zeroes and 0 val will indicate open board space
        self.board = np.zeros((num_rows, num_cols))
        self.p1 = p1
        self.p2 = p2
        self.isEnd = False
        self.boardHash = None
        # initialize the player that will play first
        # in my implementation p1 will play first
        self.playerSymbol = 1

    # method that will obtain the unique hash of the board state
    # enables us to store the current board state in the state-value dictionary
    def get_hash(self):
        self.boardHash = str(self.board.reshape(num_cols * num_rows))
        return self.boardHash

    # method that will return the available positions on the current board ie those with val = 0
    def available_positions(self):
        positions = []
        for i in range(num_rows):
            for j in range(num_cols):
                if self.board[i, j] == 0:
                    # need to be tuple
                    positions.append((i, j))
        return positions

    # method that will be used to update the state of the board based on the player that made the move
    def update_state(self, position):
        # mark the position passed in appropriately depending on the payer
        self.board[position] = self.playerSymbol
        # switch to the other player
        self.playerSymbol *= -1

    # method that will be invoked to determine if the game has ended or not
    def winner(self):
        # determine if either of the agents won via row win
        for i in range(num_rows):
            if sum(self.board[i, :]) == 3:
                self.isEnd = True
                return 1
            if sum(self.board[i, :]) == -3:
                self.isEnd = True
                return -1

        # determine if either of the agents won via column win
        for i in range(num_cols):
            if sum(self.board[:, i]) == 3:
                self.isEnd = True
                return 1
            if sum(self.board[:, i]) == -3:
                self.isEnd = True
                return -1

        # determine if either of the agents won via diagonal win
        diag_sum1 = sum([self.board[i, i] for i in range(num_cols)])
        diag_sum2 = sum([self.board[i, num_cols - i - 1] for i in range(num_cols)])
        diag_sum = max(abs(diag_sum1), abs(diag_sum2))
        if diag_sum == 3:
            self.isEnd = True
            if diag_sum1 == 3 or diag_sum2 == 3:
                return 1
            else:
                return -1

        # if we haven't returned at this point and there are no available positions => the game resulted in a tie
        if len(self.available_positions()) == 0:
            self.isEnd = True
            return 0

        # if no winner and there exist available spaces continue playing
        self.isEnd = False
        return None

    # once the game has ended assign the reward to the player
    def give_reward(self):
        # obtain the player that has one
        result = self.winner()
        # backpropagate reward
        # note that we give the winner reward of 1
        if result == 1:
            self.p1.feed_reward(1)
            self.p2.feed_reward(0)
        elif result == -1:
            self.p1.feed_reward(0)
            self.p2.feed_reward(1)
        # if tie give p1 smaller reward because draw is still a negative result
        else:
            self.p1.feed_reward(0.1)
            self.p2.feed_reward(0.5)

    # reset the board to the original state
    def reset(self):
        self.board = np.zeros((num_rows, num_cols))
        self.boardHash = None
        self.isEnd = False
        self.playerSymbol = 1

    # method that will allow two players to play against one another
    def play_agent(self, rounds=100):
        for i in range(rounds):
            if i % 1000 == 0:
                print("Rounds {}".format(i))
            while not self.isEnd:
                # Player 1
                # first, look for available positions in the board
                positions = self.available_positions()
                # choose the appropriate action for the agent
                p1_action = self.p1.choose_action(positions, self.board, self.playerSymbol)
                # take action and update board state
                self.update_state(p1_action)
                board_hash = self.get_hash()
                self.p1.add_state(board_hash)

                # determine if there is a winner
                win = self.winner()
                if win is not None:
                    # ended with p1 either win or draw
                    self.give_reward()
                    self.p1.reset()
                    self.p2.reset()
                    self.reset()
                    break

                else:
                    # Player 2
                    # first, look for available positions in the board
                    positions = self.available_positions()
                    # choose the appropriate action for the agent
                    p2_action = self.p2.choose_action(positions, self.board, self.playerSymbol)
                    # take action and update board state
                    self.update_state(p2_action)
                    board_hash = self.get_hash()
                    self.p2.add_state(board_hash)

                    # determine if there is a winner
                    win = self.winner()
                    if win is not None:
                        # self.showBoard()
                        # ended with p2 either win or draw
                        self.give_reward()
                        self.p1.reset()
                        self.p2.reset()
                        self.reset()
                        break

    # method that will permit the agent to play with a human
    def play_human(self):
        while not self.isEnd:
            # Player 1 is still the agent
            # first, look for available positions in the board
            positions = self.available_positions()
            # choose the appropriate action for the agent
            p1_action = self.p1.choose_action(positions, self.board, self.playerSymbol)
            # take action and update board state
            self.update_state(p1_action)
            self.show_board()
            # check board status if it is end
            win = self.winner()
            if win is not None:
                if win == 1:
                    print(self.p1.name, "wins!")
                else:
                    print("tie!")
                self.reset()
                break

            else:
                # Player 2 is the human
                positions = self.available_positions()
                p2_action = self.p2.choose_action(positions)

                self.update_state(p2_action)
                self.show_board()
                win = self.winner()
                if win is not None:
                    if win == -1:
                        print(self.p2.name, "wins!")
                    else:
                        print("tie!")
                    self.reset()
                    break

    def show_board(self):
        # p1: x  p2: o
        for i in range(0, num_rows):
            print('-------------')
            out = '| '
            for j in range(0, num_cols):
                if self.board[i, j] == 1:
                    token = 'x'
                if self.board[i, j] == -1:
                    token = 'o'
                if self.board[i, j] == 0:
                    token = ' '
                out += token + ' | '
            print(out)
        print('-------------')
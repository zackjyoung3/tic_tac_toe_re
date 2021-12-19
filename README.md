Reinforcement Learning Project with tic tac toe

State- the state of the game in this context is the board state of the agent as well as its opponent. Note that the State class enables play both between agents for
learning and then play against a human player. Records the board state of both players and updates when either takes an action. Also note that empty cell in board
is indicated by 0 and player marks represented by + or -1. 

action- the action that is to be taken by the player given the current board state

reward- between 0 and 1 and given at the end of a game. Note that in my implemenation for p1 the reward for a draw is 0.1. Also note that I applied value iteration
to update the value of states

Player- the Player class represents the agent. Note that I set exploratory rate to 0.3 and thus, the agent will exploit the knowledge that it already knows taking
the greedy action 70% of the time and will take random exploratory moves 30% of the time. Has save_policy to save the policy obtained from training and load_policy
to load the policy obtained in training.

Main:
In main, I created a dynamic interface that will enable the user to either create additional agents under the name they specified
and with the number of training rounds that they specified, or to play one of the agents that have already been defined.

Agents I made:
The easy_agent has been was trained in 100 training rounds and as one could observe is very easy to beat and almost randomly selects actions.
The medium_agent has was trained in 2000 rounds and resembles the play of an actual human more than the easy_agent. It will select the correct move some of the 
time, but the agent will miss oppurtunities to win and not block the human player from obtaining 3 in a row and thus, winning the game.
The hard_agent was trained over 50,000 rounds and from what I have observed, will always select the move that that will win the game when presented and 
always select the appropriate move that will prevent the human player from winning. If the human player plays correctly, the result will always be a tie.

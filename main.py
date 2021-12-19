from state import State
from player import Player
from human_player import HumanPlayer
import os


# method for if the user specified that they wanted to perform training to create a newly trained agent
def train():
    # training
    p1 = Player("p1")
    p2 = Player("p2")

    # loop until the user enters a value that can be converted to an int
    can_convert = False
    while not can_convert:
        num_rounds = input('Please enter the number of rounds to train agent:')
        print()
        try:
            num_rounds = int(num_rounds)
            can_convert = True
        except ValueError:
            can_convert = False

    # loop until a name has been obtained
    name_obtained = False
    while not name_obtained:
        # get the name that the user wishes for the new agent
        agent_name = input("Please enter the name of that you wish the agent to be saved under:")
        print()

        # if the agent is already defined prompt the user if they wish to override
        if (str(agent_name) + "_agent") in os.listdir():
            while True:
                prompt_override = input("Do you wish to override " + str(agent_name)
                                        + "_agent that already exists? (yes/no) :")
                print()
                if prompt_override == 'yes':
                    print('override')
                    name_obtained = True
                    break
                elif prompt_override == 'no':
                    # send back to new name
                    break
                # user must enter either yes or no to override question
                else:
                    print('the input must be \'yes\' or \'no\'')
                    print()
        else:
            name_obtained = True

    st = State(p1, p2)
    print("training...")
    st.play_agent(num_rounds)
    print('training for ' + str(num_rounds) + ' completed')

    # save policies
    p1.save_policy()
    p2.save_policy()
    # save new agent
    p1.save_policy(agent_name)


# method that will print all of the agents that have been trained and stored in the directory
def print_names():
    print('Agent List...')
    # all of the trained agents
    for file_name in os.listdir():
        if file_name.endswith("_agent"):
            print(file_name)


# method where the user will play an agent
def play():
    valid_name = False
    while not valid_name:
        print_names()
        entered_agent = input("Please enter the agent that you wish to play against from list above: ")
        print()
        if entered_agent in os.listdir():
            valid_name = True
        else:
            print("The name entered must exactly match one of the agents listed")
            print()

    playing = True
    while playing:
        # play with human
        p1 = Player("computer", exp_rate=0)
        p1.load_policy(entered_agent)

        p2 = HumanPlayer("human")

        st = State(p1, p2)
        st.play_human()
        while True:
            prompt_play = input("Do you wish to play " + str(entered_agent)
                                    + " again? (yes/no) :")
            print()
            if prompt_play == 'yes':
                print('play again\n')
                name_obtained = True
                break
            elif prompt_play == 'no':
                # done playing
                playing = False
                break
            # user must enter either yes or no to override question
            else:
                print('the input must be \'yes\' or \'no\'')
                print()


# method that will obtain the settings for the game that the user wishes to play
def get_user_settings():
    running = True
    while running:
        option = input("Please enter \'train\' if you want to train a new agent or \'play\' to play a trained agent:")
        print()
        if option == 'train':
            train()
        elif option == 'play':
            play()
        else:
            print('Invalid input, must be either \'train\' or \'play\'')
            print()

        quitting_time = input('Enter \'quit\' if you are done playing or training or any other key to continue:')
        print()
        if quitting_time == 'quit':
            running = False


# main
if __name__ == '__main__':
    get_user_settings()

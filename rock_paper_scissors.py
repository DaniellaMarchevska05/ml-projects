import random

def play(player1, player2, num_games, verbose=False):
    p1_prev_play = ""
    p2_prev_play = ""
    results = {"p1": 0, "p2": 0, "tie": 0}

    for _ in range(num_games):
        p1_play = player1(p2_prev_play)
        p2_play = player2(p1_prev_play)

        if p1_play == p2_play:
            results["tie"] += 1
            winner = "Tie."
        elif (p1_play == "P" and p2_play == "R") or (
                p1_play == "R" and p2_play == "S") or (p1_play == "S"
                                                       and p2_play == "P"):
            results["p1"] += 1
            winner = "Player 1 wins."
        elif p2_play == "P" and p1_play == "R" or p2_play == "R" and p1_play == "S" or p2_play == "S" and p1_play == "P":
            results["p2"] += 1
            winner = "Player 2 wins."

        if verbose:
            print("Player 1:", p1_play, "| Player 2:", p2_play)
            print(winner)
            print()

        p1_prev_play = p1_play
        p2_prev_play = p2_play

    games_won = results['p2'] + results['p1']

    if games_won == 0:
        win_rate = 0
    else:
        win_rate = results['p1'] / games_won * 100

    print("Final results:", results)
    print(f"Player 1 win rate: {win_rate}%")

    return (win_rate)


def quincy(prev_play, counter=[0]):

    counter[0] += 1
    choices = ["R", "R", "P", "P", "S"]
    return choices[counter[0] % len(choices)]


def mrugesh(prev_opponent_play, opponent_history=[]):
    opponent_history.append(prev_opponent_play)
    last_ten = opponent_history[-10:]
    most_frequent = max(set(last_ten), key=last_ten.count)

    if most_frequent == '':
        most_frequent = "S"

    ideal_response = {'P': 'S', 'R': 'P', 'S': 'R'}
    return ideal_response[most_frequent]


def kris(prev_opponent_play):
    if prev_opponent_play == '':
        prev_opponent_play = "R"
    ideal_response = {'P': 'S', 'R': 'P', 'S': 'R'}
    return ideal_response[prev_opponent_play]


def abbey(prev_opponent_play,
          opponent_history=[],
          play_order=[{
              "RR": 0,
              "RP": 0,
              "RS": 0,
              "PR": 0,
              "PP": 0,
              "PS": 0,
              "SR": 0,
              "SP": 0,
              "SS": 0,
          }]):

    if not prev_opponent_play:
        prev_opponent_play = 'R'
    opponent_history.append(prev_opponent_play)

    last_two = "".join(opponent_history[-2:])
    if len(last_two) == 2:
        play_order[0][last_two] += 1

    potential_plays = [
        prev_opponent_play + "R",
        prev_opponent_play + "P",
        prev_opponent_play + "S",
    ]

    sub_order = {
        k: play_order[0][k]
        for k in potential_plays if k in play_order[0]
    }

    prediction = max(sub_order, key=sub_order.get)[-1:]

    ideal_response = {'P': 'S', 'R': 'P', 'S': 'R'}
    return ideal_response[prediction]


def human(prev_opponent_play):
    play = ""
    while play not in ['R', 'P', 'S']:
        play = input("[R]ock, [P]aper, [S]cissors? ")
        print(play)
    return play


def random_player(prev_opponent_play):
    return random.choice(['R', 'P', 'S'])


def player(prev_play, opponent_history=[], play_order={}):
    # If there is no previous play (i.e., it's the first move), default to 'R' (Rock)
    if not prev_play:
        prev_play = 'R'

    # Append the previous play to the opponent's history
    opponent_history.append(prev_play)

    # Default prediction is 'P' (Paper)
    prediction = 'P'

    # If there are more than 4 moves in the opponent's history, analyze the last 5 moves
    if len(opponent_history) > 4:
        # Get the last 5 moves as a string
        last_five = "".join(opponent_history[-5:])

        # Update the play_order dictionary with the frequency of this 5-move sequence
        play_order[last_five] = play_order.get(last_five, 0) + 1

        # Generate potential next moves based on the last 4 moves plus each possible move ('R', 'P', 'S')
        potential_plays = [
            "".join([*opponent_history[-4:], v])
            for v in ['R', 'P', 'S']
        ]

        # Create a sub-order dictionary containing only the potential plays that exist in play_order
        sub_order = {
            k: play_order[k]
            for k in potential_plays if k in play_order
        }

        # If there are any entries in sub_order, predict the most frequent next move
        if sub_order:
            prediction = max(sub_order, key=sub_order.get)[-1:]

    # Define the ideal response to the predicted move
    ideal_response = {'P': 'S', 'R': 'P', 'S': 'R'}

    # Return the ideal response based on the prediction
    return ideal_response[prediction]


    def test_player_vs_quincy(self):
        print("Testing game against quincy...")
        actual = play(player, quincy, 1000) >= 60
        self.assertTrue(
            actual,
            'Expected player to defeat quincy at least 60% of the time.')

    def test_player_vs_abbey(self):
        print("Testing game against abbey...")
        actual = play(player, abbey, 1000) >= 60
        self.assertTrue(
            actual,
            'Expected player to defeat abbey at least 60% of the time.')

    def test_player_vs_kris(self):
        print("Testing game against kris...")
        actual = play(player, kris, 1000) >= 60
        self.assertTrue(
            actual, 'Expected player to defeat kris at least 60% of the time.')

    def test_player_vs_mrugesh(self):
        print("Testing game against mrugesh...")
        actual = play(player, mrugesh, 1000) >= 60
        self.assertTrue(
            actual,
            'Expected player to defeat mrugesh at least 60% of the time.')


play(player, quincy, 1000)
play(player, abbey, 1000)
play(player, kris, 1000)
play(player, mrugesh, 1000)

# Uncomment line below to play interactively against a bot:
#play(human, abbey, 20, verbose=True)

# Uncomment line below to play against a bot that plays randomly:
#play(human, random_player, 1000)


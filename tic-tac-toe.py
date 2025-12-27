import random
import time

# Class that stores information about the players:


class Player:
    def __init__(self, username, symbol):
        self.username = username
        self.symbol = symbol


# Class that creates the board and translates user inputs into moves:


class Board:
    winning_moves = (
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),
        (2, 4, 6),
    )

    def __init__(self):
        self.moves = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    # Printing the board:

    def print_board(self):
        print("\n     |     |     ")
        print(f"  {self.moves[0]}  |  {self.moves[1]}  |  {self.moves[2]}  ")
        print("_____|_____|_____")
        print("     |     |     ")
        print(f"  {self.moves[3]}  |  {self.moves[4]}  |  {self.moves[5]}  ")
        print("_____|_____|_____")
        print("     |     |     ")
        print(f"  {self.moves[6]}  |  {self.moves[7]}  |  {self.moves[8]}  ")
        print("     |     |     \n")

    # Transforming the user's (validated) input into a move:

    def translate_user_move(self, player, move):
        self.moves[move - 1] = player.symbol

    # Checking if any of the players won:

    def check_win(self):
        for winning_move in Board.winning_moves:
            if (
                self.moves[winning_move[0]]
                == self.moves[winning_move[1]]
                == self.moves[winning_move[2]]
            ):
                return True
        return False

    # Checking for ties:

    def check_tie(self):
        for move in self.moves:
            if move not in ("X", "O"):
                return False
        return True

    # Resetting the board:

    def reset_board(self):
        self.moves = [1, 2, 3, 4, 5, 6, 7, 8, 9]


# Class that handles the players' scores:


class ScoreBoard:
    def __init__(self, player1, player2):
        self.scores = {player1.symbol: 0, player2.symbol: 0}

    def add_score(self, winner):
        self.scores[winner.symbol] += 1

    def get_score(self, player):
        return self.scores[player.symbol]


# Class that handles UI and orchestrates the game:


class TicTacToe:

    # Creating the board and scoreboard instances:

    def __init__(self):
        self.board = Board()
        self.scoreboard = None

    # Asking the users if they want to play:

    def play(self):
        play = (
            input(
                "Hey there! Do you want to play a game of TicTacToe for 2 players? [y/n]: "
            )
            .lower()
            .strip()
        )

        while True:
            if play in ["y", "yes"]:
                self.run()
                break
            elif play in ["n", "no"]:
                print("\nWhat a pity :(")
                break
            else:
                play = (
                    input(f"\n'{play}' is an invalid input, please enter 'y' or 'n': ")
                    .lower()
                    .strip()
                )

    # What happens when the game is run:

    def run(self):
        self.introduction()
        self.set_players()
        while True:
            self.play_round()
            if self.play_again():
                self.reset()
            else:
                break
        self.print_results()

    # How every round runs:

    def play_round(self):
        while True:
            move = self.get_player_move(
                self.players[0]
            )  # Getting the user input for the move
            self.board.translate_user_move(
                self.players[0], move
            )  # Translating it into a move on the board
            self.board.print_board()  # Printing what the board looks like after the move

            # Checking for any possible wins:
            if self.board.check_win():
                self.scoreboard.add_score(self.players[0])
                print(f"\n{self.players[0].username} won this round!")
                break

            # Checking for a possible tie:
            if self.board.check_tie():
                print(f"\nIt's a tie!")
                break

            self.players.reverse()

    # What the players see at the beginning of the match:

    def introduction(self):
        print("\nPerfect, this is the board you will be playing with:")
        self.board.print_board()
        print(
            "At the start of each turn, I’ll ask you to choose a number from 1 to 9 to place your X or O. The program will randomly assign 'X' and 'O' at the start of the game. At the beginning of each new round, the player who went second in the previous round will get to start first..."
        )

    # Creating the players:

    def set_players(self):

        print("\nBut before we begin, I need your usernames!")

        # Getting the players' usernames:
        username1 = input("\nPlayer_1, please input your preferred username: ")
        username2 = input("Player_2, please input your preferred username: ")

        print(f"\nUsernames saved as '{username1}' and '{username2}'.")

        # Randomly deciding who begins:
        usernames = [username1, username2]
        random.shuffle(usernames)

        # Creating the player instances:
        self.player1 = Player(usernames[0], "X")
        self.player2 = Player(usernames[1], "O")
        self.players = [self.player1, self.player2]

        # Creating the scoreboard instance:
        self.scoreboard = ScoreBoard(self.player1, self.player2)

        input("\nWhen you are both ready, press Enter and I will begin the game: ")

        # Visual countdown for who begins:
        print(f"\nDeciding who gets to begin", end="", flush=True)

        for _ in range(5):
            print(".", end="", flush=True)
            time.sleep(0.8)

        print(f"\n\n{self.player1.username} is X and {self.player2.username} is O!")

    # Getting and validating players' moves:

    def get_player_move(self, player):
        while True:
            move = input(
                f"\n{player.username}, input your {player.symbol} between 1 and 9: "
            )

            # Checking if the input is a number:
            try:
                move = int(move)
            except ValueError:
                print(f"\n'{move}' is not a number! Please try again.")
                continue

            # Checking if the input is in range 1-9:
            if move not in range(1, 10):
                print(f"\n'{move}' is not in range 1-9! Please try again.")
                continue

            # Checking if the player's choice is not already taken:
            if self.board.moves[move - 1] in ["X", "O"]:
                print(
                    f"\n'{move}' is already taken by {self.board.moves[move - 1]}! Please try again."
                )
                continue

            break

        return move

    # Determining whether the players want to play again:

    def play_again(self):
        response = input("\nDo you want to play again? [y/n]: ").lower().strip()

        while True:
            if response in ["y", "yes"]:
                return True
            elif response in ["n", "no"]:
                return False
            else:
                response = (
                    input(
                        f"\n'{response}' is not a valid input, please input 'y' or 'n': "
                    )
                    .lower()
                    .strip()
                )

    # What happens when the players want to play again:

    def reset(self):
        # Reversing the players:
        self.players.reverse()

        # Resetting the board:
        self.board.reset_board()
        print("\nPerfect, the board has been reset!")
        self.board.print_board()

        print(f"{self.players[0].username} gets to start now!")

    # Printing the final results:

    def print_results(self):
        player1_score = self.scoreboard.get_score(self.player1)
        player2_score = self.scoreboard.get_score(self.player2)

        print(
            f"\n{self.player1.username} won {player1_score} times and {self.player2.username} won {player2_score} times."
        )

        # Checking who the winner of the whole game is:
        if player1_score > player2_score:
            print(f"\n{self.player1.username} is the winner!")

        elif player1_score < player2_score:
            print(f"\n{self.player2.username} is the winner!")

        else:
            print("\nWhat a tie!")

        print("\nThank you for playing :)")


if __name__ == "__main__":
    game = TicTacToe()
    game.play()

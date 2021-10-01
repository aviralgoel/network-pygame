# Game class
# an object of class Game is an instance of a game session running
# with two players connected to it
# it contains all the information about the Game session between those two connected players
# (and the rounds they play, during that game session)
# terminology - two players (player 1 and player 2) connect to the server
# the server starts a Game session between them (object of this class)
# during that session multiple rounds of the rock, paper and scissors are played
class Game:
    def __init__(self, id):  # constructor
        self.p1Went = False  # has player 1 selected his move for the round?
        self.p2Went = False  # has player 2 selected his move for the round?
        self.ready = False  # is this game session ready to be started?
        self.id = id  # unique ID of this game session
        # (note: the sever will manage multiple game sessions and each session will be able to
        # accommodate multiple rounds of RPS
        self.moves = [None, None]  # moves decided by player 1 and player 2 for the latest round
        self.wins = [0, 0]  # win count of player 1 and player 2 throughout the session
        self.ties = 0  # number of ties throughout the session

    # this function takes the ID of the player (player 1 (ID:0) or player 2 (ID:1)) and returns what move that player
    # has decided
    def get_player_move(self, p):
        """
        :param p: [0,1]
        :return: Move
        """
        return self.moves[p]

    # this function takes the ID of the player (0 or 1) along with the move decided, it updates that move and marks
    # the player as move played: true
    def play(self, player, move):
        self.moves[player] = move
        if player == 0:
            self.p1Went = True
        else:
            self.p2Went = True

    # return: is the game session ready to be started?
    def connected(self):
        return self.ready

    # return: has both players played their own moves or not?
    def bothWent(self):
        return self.p1Went and self.p2Went

    # game logic
        # 1. Get the moves of the players
        # 2. Decide the winner (or tie) based on the rules of the game.
        # 3. returns the verdict (0 = Player 1 won, 1 = Player 2 won, -1 = tie)

    def winner(self):

        p1 = self.moves[0].upper()[0]
        p2 = self.moves[1].upper()[0]

        winner = -1
        if p1 == "R" and p2 == "S":
            winner = 0
        elif p1 == "S" and p2 == "R":
            winner = 1
        elif p1 == "P" and p2 == "R":
            winner = 0
        elif p1 == "R" and p2 == "P":
            winner = 1
        elif p1 == "S" and p2 == "P":
            winner = 0
        elif p1 == "P" and p2 == "S":
            winner = 1

        return winner

    # reset both player move status, i.e prepare them for next round
    def resetWent(self):
        self.p1Went = False
        self.p2Went = False

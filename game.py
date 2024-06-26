"""
File for comparing information between the clients.
"""


class Game:
    def __init__(self, id):
        self.p1Submit = False
        self.p2Submit = False
        self.ready = False
        self.id = id
        self.scores = [None, None]

    def get_player_score(self, p):
        """
        :param p: [0,1]
        :return: score
        """
        return self.scores[p]

    def submitted(self, player, score):
        """Define when a player has submitted a score."""
        self.scores[player] = score
        if player == 0:
            self.p1Submit = True
        else:
            self.p2Submit = True

    def connected(self):
        """Defines when client is successfully connected."""
        return self.ready

    def both_submitted(self):
        """Define when both players have submitted their scores."""
        # If both have gone, function returns True.
        return self.p1Submit and self.p2Submit

    # Logic behind who wins the current game.
    def winner(self):
        """
        Pickle can only compile str-type data, so to compare numbers,
        must convert the strings back into int-type data.
        """
        p1 = int(self.scores[0])
        p2 = int(self.scores[1])

        # If player 1's score is higher, they win.
        if p1 > p2:
            winner = 0
        elif p1 < p2:
            winner = 1
        # If they have the same score, tie.
        else:
            winner = -1

        return winner

    def reset_submits(self):
        """Used to restart the game."""
        self.p1Submit = False
        self.p2Submit = False

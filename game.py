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
        self.scores[player] = score
        if player == 0:
            self.p1Submit = True
        else:
            self.p2Submit = True

    def connected(self):
        return self.ready

    def both_submitted(self):
        return self.p1Submit and self.p2Submit

    def winner(self):

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

    # When called,
    def reset_submits(self):
        self.p1Submit = False
        self.p2Submit = False

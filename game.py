class Game:
    def __init__(self, id):
        self.p1Went = False
        self.p2Went = False
        self.ready = False
        self.id = id
        self.scores = [None, None]
        self.wins = [0,0]
        self.ties = 0

    def get_player_score(self, p):
        """
        :param p: [0,1]
        :return: score
        """
        return self.scores[p]

    def play(self, player, score):
        self.scores[player] = score
        if player == 0:
            self.p1Went = True
        else:
            self.p2Went = True

    def connected(self):
        return self.ready

    def bothWent(self):
        return self.p1Went and self.p2Went

    def winner(self):

        p1 = int(self.scores[0])
        p2 = int(self.scores[1])

        if p1 > p2:
            winner = 0
        elif p1 < p2:
            winner = 1
        else:
            winner = -1

        return winner

    def resetWent(self):
        self.p1Went = False
        self.p2Went = False

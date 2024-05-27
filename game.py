class Game:
    def __init__(self, id):
        self.p1Went = False
        self.p2Went = False
        self.ready = False
        self.id = id
        self.hits = [None, None]
        self.wins = [0,0]
        self.ties = 0

    def get_player_hit(self, p):
        """
        :param p: [0,1]
        :return: Move
        """
        return self.hits[p]

    # asdasd
    def get_player_miss(self, p):
        """
        :param p: [0,1]
        :return: Move
        """
        return self.misses[p]

    def play(self, player, hit, miss):
        self.hits[player] = hit
        self.misses[player] = miss
        if player == 0:
            self.p1Went = True
        else:
            self.p2Went = True

    def connected(self):
        return self.ready

    def bothWent(self):
        return self.p1Went and self.p2Went

    def winner(self):

        p1 = int(self.hits[0])
        p2 = int(self.hits[1])

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

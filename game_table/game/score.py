
#Score-Class
class Score(object):
    def __init__(self, points, lives):
        self.points = points
        self.lives = lives

    def ClearPoints(self):
        self.points = 0

    def IncreasePoints(self):
        self.points += 1

    def SetLives(self, lives):
        self.lives = lives
    
    def DecreaseLives(self):
        self.lives -= 1
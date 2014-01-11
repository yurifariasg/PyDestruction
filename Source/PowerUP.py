

class PowerUP(object):

    def __init__(self, lives = 0, speed = 0, bombs = 0, range = 0):
        self.attributes = {}
        self.attributes['lives'] = lives
        self.attributes['speed'] = speed
        self.attributes['bombs'] = bombs
        self.attributes['range'] = range
    
    
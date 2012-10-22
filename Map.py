import Settings
import random
from Block import Block

class Map(object):

    def __init__(self):
        self.walls = []
        self.bombs = []
        self.fire = []
        self.powerups = []
        self.players = []
        
        self.Y_POSITIONS = [32, 64, 96, 128, 160, 192, 224, 256, 288, 320, 352, 384, 416, 448, 480]
        self.X_POSITIONS = [32, 64, 96, 128, 160, 192, 224, 256, 288, 320, 352, 384, 416, 448, 480, 512, 544, 544+32, 544+64, 544+96, 544+128, 544+160,544+192]
        
        self.coord = []
        
    def init(self):
        # Fill all possible pairs
        for x in self.X_POSITIONS:
            for y in self.Y_POSITIONS:
                self.coord.append((x,y))
        
        # Remove Initial Player Positions
        self.coord.remove((self.X_POSITIONS[0], self.Y_POSITIONS[0])) # Initial Position for Player 1
        self.coord.remove((self.X_POSITIONS[0], self.Y_POSITIONS[1]))
        self.coord.remove((self.X_POSITIONS[1], self.Y_POSITIONS[0]))
        self.players[0].rect.x, self.players[0].rect.y = (self.X_POSITIONS[0], self.Y_POSITIONS[0])
        
        self.coord.remove((self.X_POSITIONS[-1], self.Y_POSITIONS[-1])) # Initial Position for Player 2
        self.coord.remove((self.X_POSITIONS[-2], self.Y_POSITIONS[-1]))
        self.coord.remove((self.X_POSITIONS[-1], self.Y_POSITIONS[-2]))
        self.players[1].rect.x, self.players[1].rect.y = (self.X_POSITIONS[-1], self.Y_POSITIONS[-1])
        
        if len(self.players) > 2:
            self.coord.remove((self.X_POSITIONS[0], self.Y_POSITIONS[-1])) # Initial Position for Player 3
            self.coord.remove((self.X_POSITIONS[0], self.Y_POSITIONS[-2]))
            self.coord.remove((self.X_POSITIONS[1], self.Y_POSITIONS[-1]))
            self.players[2].rect.x, self.players[2].rect.y = (self.X_POSITIONS[0], self.Y_POSITIONS[-1])
            
            if len(self.players) > 3:
                self.coord.remove((self.X_POSITIONS[-1], self.Y_POSITIONS[0])) # Initial Position for Player 4
                self.coord.remove((self.X_POSITIONS[-2], self.Y_POSITIONS[0]))
                self.coord.remove((self.X_POSITIONS[-1], self.Y_POSITIONS[1]))
                self.players[3].rect.x, self.players[3].rect.y = (self.X_POSITIONS[-1], self.Y_POSITIONS[0])
            
        x = y = 0 # Building the Map
        for row in Settings.MAP:
            for col in row:
                if col == "W": # Middle Blocks
                    if (x,y) in self.coord:
                        self.coord.remove((x,y))
                    self.walls.append(Block((x,y), Block.FIXED))
                if col == "Z": # Border Block
                    if (x,y) in self.coord:
                        self.coord.remove((x,y))
                    self.walls.append(Block((x,y), Block.BORDER))
                x += 32
            y += 32
            x = 0

        # Randomly Add 100 Destructable Blocks
        count = 0
        while count < 100:
            position = random.choice(self.coord)
            self.coord.remove(position)
            self.walls.append(Block(position, Block.DESTRUCTABLE))
            count += 1
    
    def animate(self):
        pass
    
    def perform_physics(self):
        pass
    
    def render(self, screen):
        
        for wall in self.walls:
            wall.render(screen)
            
        for player in self.players:
            player.render(screen)
        
        
    
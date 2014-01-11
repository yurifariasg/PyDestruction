import Settings
import random
import math
import pygame
import Enemy
import Bomb
from Block import Block
import PathNode

class Map(object):
    
    Y_POSITIONS = [32, 64, 96, 128, 160, 192, 224, 256, 288, 320, 352, 384, 416, 448, 480]
    X_POSITIONS = [32, 64, 96, 128, 160, 192, 224, 256, 288, 320, 352, 384, 416, 448, 480, 512, 544, 544+32, 544+64, 544+96, 544+128, 544+160,544+192]


    def __init__(self):
        self.walls = []
        self.bombs = []
        self.fire = []
        self.powerups = []
        self.players = []
        self.coord = []
        self.pathNodes = []
        self.blockyMap = []
        
    def init(self):
        # Fill all possible pairs
        for x in Map.X_POSITIONS:
            for y in Map.Y_POSITIONS:
                self.coord.append((x,y))
        
        # Remove Initial Player Positions
        self.coord.remove((Map.X_POSITIONS[0], Map.Y_POSITIONS[0])) # Initial Position for Player 1
        self.coord.remove((Map.X_POSITIONS[0], Map.Y_POSITIONS[1]))
        self.coord.remove((Map.X_POSITIONS[1], Map.Y_POSITIONS[0]))
        self.players[0].rect.x, self.players[0].rect.y = (Map.X_POSITIONS[0], Map.Y_POSITIONS[0])
        
        self.coord.remove((Map.X_POSITIONS[-1], Map.Y_POSITIONS[-1])) # Initial Position for Player 2
        self.coord.remove((Map.X_POSITIONS[-2], Map.Y_POSITIONS[-1]))
        self.coord.remove((Map.X_POSITIONS[-1], Map.Y_POSITIONS[-2]))
        self.players[1].rect.x, self.players[1].rect.y = (Map.X_POSITIONS[-1], Map.Y_POSITIONS[-1])
        
        if len(self.players) > 2:
            self.coord.remove((Map.X_POSITIONS[0], Map.Y_POSITIONS[-1])) # Initial Position for Player 3
            self.coord.remove((Map.X_POSITIONS[0], Map.Y_POSITIONS[-2]))
            self.coord.remove((Map.X_POSITIONS[1], Map.Y_POSITIONS[-1]))
            self.players[2].rect.x, self.players[2].rect.y = (Map.X_POSITIONS[0], Map.Y_POSITIONS[-1])
            
            if len(self.players) > 3:
                self.coord.remove((Map.X_POSITIONS[-1], Map.Y_POSITIONS[0])) # Initial Position for Player 4
                self.coord.remove((Map.X_POSITIONS[-2], Map.Y_POSITIONS[0]))
                self.coord.remove((Map.X_POSITIONS[-1], Map.Y_POSITIONS[1]))
                self.players[3].rect.x, self.players[3].rect.y = (Map.X_POSITIONS[-1], Map.Y_POSITIONS[0])
                
        self.buildBlocks()
        
        i = 0
        # Randomly Add 100 Destructible Blocks
        count = 0
        while count < Settings.DESTRUCTIBLE_BLOCKS_COUNT:
            position = random.choice(self.coord)
            self.coord.remove(position)
            self.walls.append(Block(position, Block.DESTRUCTABLE))
            blockyCoords = self.convertRealCoordinatesToBlockyCoordinates(position)
            block = self.blockyMap[blockyCoords[1]][blockyCoords[0]] # First Y then X
            assert(isinstance(block, PathNode.PathNode)) # Must be a PathNode
            assert(not block.isBlocked()) # Must not be blocked
            block.setIsBlocked(True)
            
            count += 1
    
    def getPathNodeAt(self, realWorldPos):
        pos = self.convertRealCoordinatesToBlockyCoordinates(realWorldPos)
        return self.blockyMap[pos[1]][pos[0]]
    
    @classmethod
    def convertRealCoordinatesToBlockyCoordinates(cls, pos):
        return [int(math.floor(float(pos[0]) / Settings.BLOCK_SIZE)), 
                int(math.floor(float(pos[1]) / Settings.BLOCK_SIZE))]
    
    def getPlayerPosition(self):
        return [self.players[0].rect.centerx, self.players[0].rect.centery]
    
    def buildBlocks(self):
        map = []
        for row in Settings.MAP:  
            map.append(list(row))
        
        x = y = 0 # Building the Map
        for row_i in range(len(map)):
            for col_i in range(len(map[row_i])):
                col = map[row_i][col_i]
                if col == "W": # Middle Blocks
                    if (x,y) in self.coord:
                        self.coord.remove((x,y))
                    block = Block((x,y), Block.FIXED)
                    self.walls.append(block)
                    map[row_i][col_i] = block
                elif col == "Z": # Border Block
                    if (x,y) in self.coord:
                        self.coord.remove((x,y))
                    block = Block((x,y), Block.BORDER)
                    self.walls.append(block)
                    map[row_i][col_i] = block
                else:
                    pathnode = PathNode.PathNode(pygame.Rect(x, y, Settings.BLOCK_SIZE, Settings.BLOCK_SIZE))
                    self.pathNodes.append(pathnode)
                    map[row_i][col_i] = pathnode
                x += 32
            y += 32
            x = 0
        
        x = y = None
        # Link Pathnodes
        for y in range(1, len(map) - 1): # Skip Borders
            for x in range(1, len(map[y]) - 1):
                block = map[y][x]
                if isinstance(block, PathNode.PathNode): # if it is a PathNode
                    self.addBlockToPathNode(block, map[y - 1][x]) # Left Block
                    self.addBlockToPathNode(block, map[y + 1][x]) # Right Block
                    self.addBlockToPathNode(block, map[y][x - 1]) # Top Block
                    self.addBlockToPathNode(block, map[y][x + 1]) # Bottom Block
        
        self.blockyMap = map
    
    def addBlockToPathNode(self, pathnode, block):
        if isinstance(block, PathNode.PathNode):
            pathnode.addAdjacentNode(block)
                
            
    
    def add_player_bomb(self, player):
        if player.current_status.get('bombs', 0) < 1:
            return
        
        rect = self.get_nearest_block((player.rect.x,
                                        player.rect.y))
        colliders = []
        for otherPlayer in self.players:
            if rect.colliderect(otherPlayer.rect):
                colliders.append(otherPlayer)
        
        if self.get_bomb_at(player.rect.center) == None:
            player.current_status['bombs'] -= 1
            self.bombs.append(Bomb.Bomb(colliders,
                                        player.current_status.get('range'),
                                        3,
                                        self.get_nearest_block((player.rect.x,
                                        player.rect.y)),
                                        player))
            
            
            blockyCoords = self.convertRealCoordinatesToBlockyCoordinates(rect.center)
            self.blockyMap[blockyCoords[1]][blockyCoords[0]].setIsBlocked(True)
            
    def get_players_at(self, position):
        rect = pygame.Rect(position[0], position[1], Settings.BLOCK_SIZE, Settings.BLOCK_SIZE)
        collided = []
        for player in self.players:
            if rect.colliderect(player.rect):
                collided.append(player)
        return collided
    
    def get_wall_at(self, position):
        for wall in self.walls:
            if [wall.rect.x, wall.rect.y] == position:
                return wall
        return None
    
    def get_bomb_at(self, position):
        for bomb in self.bombs:
            if bomb.rect.collidepoint(position):
                return bomb
        return None
        
    def get_nearest_block(self, position): # redo: time complexity
        """
        indexClosestX = 0
        for i in range(1, len(Map.X_POSITIONS)):
            if math.fabs(position[0] - Map.X_POSITIONS[i]) < math.fabs(position[0] - Map.X_POSITIONS[indexClosestX]):
                indexClosestX = i
        
        indexClosestY = 0
        for i in range(1, len(Map.Y_POSITIONS)):
            if math.fabs(position[1] - Map.Y_POSITIONS[i]) < math.fabs(position[1] - Map.Y_POSITIONS[indexClosestY]):
                indexClosestY = i
        """
        
        bPos = self.convertRealCoordinatesToBlockyCoordinates(position)
        
        return pygame.Rect(bPos[0] * Settings.BLOCK_SIZE, bPos[1] * Settings.BLOCK_SIZE,
                           Settings.BLOCK_SIZE, Settings.BLOCK_SIZE)
    
    def update_bots(self):
        for player in self.players:
            if isinstance(player, Enemy.Enemy):
                player.update(self)
    
    def render(self, screen):
        
        for wall in self.walls:
            wall.render(screen)
            
        for bomb in self.bombs:
            bomb.render(screen)
            
        for fire in self.fire:
            fire.render(screen)
            
        for player in self.players:
            player.render(screen)
        
        
    
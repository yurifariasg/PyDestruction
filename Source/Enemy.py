import Bomberman
import PathNode
#import Map
import math
import random
from time import time

class BotState(object):
    IDLE = 0
    CHASING = 1
    AVOIDING = 2
    PLACING_BOMB = 3 # Add more if needed

class Enemy(Bomberman.Bomberman):
    def __init__(self, name, initial_data, initial_pos, animation_images):
        super(Enemy, self).__init__(name, initial_data, initial_pos, animation_images)
        self.map = None
        self.current_node = None
        self.target_node = None
        self.last_think_time = 0
        self.last_placed_bomb_time = 0
        self.last_position = None
    
    def shouldThinkAt(self, pathnode):
        if math.fabs(time() - self.last_think_time) > 0.1: # Times Passed
            return True
        return self.current_node == None or (pathnode != self.current_node and self.isOnCenter(pathnode))
    
    def update(self, map):
        self.map = map
        current_node = self.getCurrentPathNode()
        if self.shouldThinkAt(current_node): # Checks if it is time or moment to Think
            # Think what you gonna do
            self.last_think_time = time()
            self.current_node = current_node
            
            if self.isInDanger():
                path = self.getPathTowardsSafePosition(self.current_node)
            else:
                path = self.getPathTowardsPlayer(self.current_node, self.map.getPlayerPosition())
                
            if len(path) > 1:
                self.target_node = path[1]
            
            if self.current_node == self.target_node and \
                    self.last_think_time - self.last_placed_bomb_time > 3:
                self.plantBomb()
                self.last_placed_bomb_time = self.last_think_time
        
        # Non-Thinking Commands
        self.setMovementsTowardNode(self.target_node)
    
    def isInDanger(self):
        for bomb in self.map.bombs:
            if self.current_node.isInRangeOfBomb(bomb):
                return True
        return False
        
    
    def getPathTowardsSafePosition(self, initial_node):
        
        self.resetParenthood()
        path = []
        def retracePath(c):
            path.insert(0,c)
            if c.parent == None:
                return
            retracePath(c.parent)
        
        # First: Try to get one without passing by any unsafe block
        frontier = []
        visited = set()
        frontier.append(initial_node)
        
        while (len(frontier) != 0):
            current_node = frontier.pop(0)
            if not current_node.isInRangeOfBombs(self.map.bombs):
                retracePath(current_node)
                break
                
            adjacents = current_node.getAdjacentNodes()
            for node in adjacents:
                if node not in visited and node not in frontier:
                    node.parent = current_node
                    frontier.append(node)
            
            visited.add(current_node)
        
        return path
    
    def isOnCenter(self, node):
        
        newrect = self.rect.union(node.rect)
        
        if newrect.x == node.rect.x and newrect.y == node.rect.y and \
            newrect.width == node.rect.width and newrect.height == node.rect.height:
            return True
        return False
    
    def plantBomb(self):
        self.map.add_player_bomb(self)
    
    def getPathTowardsPlayer(self, initial_node, final_position):
        self.resetParenthood()
        finalBlockyCoords = self.map.convertRealCoordinatesToBlockyCoordinates(final_position)
        return self.aStar(initial_node, self.map.blockyMap[finalBlockyCoords[1]][finalBlockyCoords[0]])
    
    def resetParenthood(self):
        for y in range(1, len(self.map.blockyMap) - 1): # Skip Borders
            for x in range(1, len(self.map.blockyMap[y]) - 1):
                self.map.blockyMap[y][x].parent = None
    
    """
         A* Algorithm - Return path to the final node or closest path to it (using heuristic [distance])
         -> All nodes of the path must not be in range of any bomb
    """
    def aStar(self, current_node, final_node):
        frontier = set()
        visited_list = set()
        path = []
    
        def retracePath(c):
            path.insert(0,c)
            if c.parent == None:
                return
            retracePath(c.parent)
    
        frontier.add(current_node)
        while len(frontier) is not 0:
            current_node = min(frontier,
                               key=lambda node:PathNode.PathNode.dist(node.rect.center,
                                                                      final_node.rect.center))
            if current_node == final_node:
                retracePath(current_node)
                break
            frontier.remove(current_node)
            visited_list.add(current_node)
            for node in current_node.getAdjacentNodes(filterFromBombs=self.map.bombs):
                if node not in visited_list and node not in frontier:
                    frontier.add(node)
                    node.parent = current_node
        
        if len(path) == 0:
            closest_node = min(visited_list,
                               key=lambda node:PathNode.PathNode.dist(node.rect.center,
                                                                      final_node.rect.center))
            retracePath(closest_node)
        
        return path
    
    def validatePosition(self, pathnode):
        if (isinstance(pathnode, PathNode.PathNode)):
            return not pathnode.isBlocked()
        return False
    
    def getCurrentPathNode(self):
        return self.map.getPathNodeAt([self.rect.centerx, self.rect.centery])
    
    def setMovementsTowardNode(self, pathnode):
        if not self.isOnCenter(pathnode):
            
            if self.last_position == self.rect.center: # Supposed to move but got stuck
                self.movement(random.choice([Bomberman.Direction.LEFT,
                                             Bomberman.Direction.RIGHT,
                                             Bomberman.Direction.UP,
                                             Bomberman.Direction.DOWN]))
                self.last_position = self.rect.center
            else:
                if math.fabs(self.rect.x - pathnode.rect.x) > math.fabs(self.rect.y - pathnode.rect.y):
                    if self.rect.x - pathnode.rect.x > 0:
                        self.movement(Bomberman.Direction.LEFT)
                    else:
                        self.movement(Bomberman.Direction.RIGHT)
                else:
                    if self.rect.y - pathnode.rect.y > 0:
                        self.movement(Bomberman.Direction.UP)
                    else:
                        self.movement(Bomberman.Direction.DOWN)
                self.last_position = self.rect.center
        else:
            self.last_position = None
            
            
        